#!/usr/bin/env python3
"""
AI 音乐曲谱生成器
支持 ABC 记谱法和简谱生成
"""

import argparse
import json
import re
import sys
from dataclasses import dataclass
from typing import List, Optional, Tuple
from pathlib import Path


@dataclass
class Note:
    """音乐音符"""
    pitch: str  # 音高，如 "C", "D", "E"
    octave: int  # 八度，0=中央C所在八度
    duration: float  # 时值（以四分音符为1）
    is_rest: bool = False  # 是否为休止符
    
    def to_abc(self) -> str:
        """转换为 ABC 记谱法"""
        if self.is_rest:
            duration_str = self._get_abc_duration()
            return f"z{duration_str}"
        
        # 处理八度
        if self.octave < 0:
            pitch = self.pitch.lower() + "," * abs(self.octave)
        elif self.octave > 0:
            pitch = self.pitch.lower() + "'" * self.octave
        else:
            pitch = self.pitch.upper()
        
        duration_str = self._get_abc_duration()
        return f"{pitch}{duration_str}"
    
    def to_jianpu(self) -> str:
        """转换为简谱"""
        if self.is_rest:
            return "0"
        
        # 音名到唱名的映射
        pitch_map = {
            "C": "1", "D": "2", "E": "3", "F": "4",
            "G": "5", "A": "6", "B": "7"
        }
        
        base = pitch_map.get(self.pitch.upper(), "1")
        
        # 处理八度
        if self.octave < 0:
            # 低音 - 下方加点
            base = base + "̣" * abs(self.octave)
        elif self.octave > 0:
            # 高音 - 上方加点
            base = base + "̇" * self.octave
        
        # 处理时值
        if self.duration == 0.5:
            base = base + "̲"  # 八分音符
        elif self.duration == 0.25:
            base = base + "̲̲"  # 十六分音符
        elif self.duration == 2:
            base = base + "-"  # 二分音符
        elif self.duration == 4:
            base = base + " - - -"  # 全音符
        elif self.duration == 1.5:
            base = base + "."  # 附点四分音符
        
        return base
    
    def _get_abc_duration(self) -> str:
        """获取 ABC 记谱法的时值表示"""
        if self.duration == 1:
            return ""
        elif self.duration == 0.5:
            return "/2"
        elif self.duration == 0.25:
            return "/4"
        elif self.duration == 2:
            return "2"
        elif self.duration == 4:
            return "4"
        elif self.duration == 1.5:
            return "3/2"
        else:
            return f"{int(self.duration * 2)}/2"


@dataclass
class Chord:
    """和弦"""
    root: str  # 根音
    quality: str  # 性质（如 "", "m", "7", "maj7"）
    duration: float = 1.0  # 时值
    
    def to_abc(self) -> str:
        """转换为 ABC 记谱法（和弦标记）"""
        chord_name = f'"{self.root}{self.quality}"'
        return chord_name
    
    def to_jianpu(self) -> str:
        """转换为简谱和弦标记"""
        return f"[{self.root}{self.quality}]"


@dataclass
class Measure:
    """小节"""
    notes: List[Note]
    chords: List[Optional[Chord]] = None
    
    def __post_init__(self):
        if self.chords is None:
            self.chords = []
    
    def to_abc(self) -> str:
        """转换为 ABC 记谱法"""
        result = []
        for i, note in enumerate(self.notes):
            # 添加和弦标记（如果有）
            if i < len(self.chords) and self.chords[i]:
                result.append(self.chords[i].to_abc())
            result.append(note.to_abc())
        return " ".join(result)
    
    def to_jianpu(self) -> str:
        """转换为简谱"""
        notes_str = " ".join([n.to_jianpu() for n in self.notes])
        if self.chords:
            chords_str = " ".join([c.to_jianpu() if c else "" for c in self.chords])
            return f"{chords_str}\n{notes_str}"
        return notes_str


@dataclass
class Song:
    """歌曲"""
    title: str
    composer: str
    key: str
    time_signature: str
    tempo: int
    measures: List[Measure]
    lyrics: Optional[List[str]] = None
    
    def to_abc(self) -> str:
        """生成完整的 ABC 记谱法文本"""
        lines = [
            f"X:1",
            f"T:{self.title}",
            f"C:{self.composer}",
            f"M:{self.time_signature}",
            f"L:1/4",
            f"Q:1/4={self.tempo}",
            f"K:{self.key}",
            ""
        ]
        
        # 添加旋律
        melody_line = ""
        for i, measure in enumerate(self.measures):
            melody_line += measure.to_abc()
            melody_line += " |"
            if (i + 1) % 4 == 0:  # 每4小节换行
                lines.append(melody_line)
                melody_line = ""
        
        if melody_line:
            lines.append(melody_line)
        
        # 添加歌词（如果有）
        if self.lyrics:
            lines.append("")
            for lyric_line in self.lyrics:
                lines.append(f"w: {lyric_line}")
        
        return "\n".join(lines)
    
    def to_jianpu(self) -> str:
        """生成简谱文本"""
        lines = [
            f"# {self.title}",
            f"作曲：{self.composer}",
            f"调性：{self.key}",
            f"拍号：{self.time_signature}",
            f"速度：{self.tempo} BPM",
            ""
        ]
        
        # 添加简谱
        jianpu_line = ""
        for i, measure in enumerate(self.measures):
            jianpu_line += measure.to_jianpu() + " | "
            if (i + 1) % 4 == 0:
                lines.append(jianpu_line)
                jianpu_line = ""
        
        if jianpu_line:
            lines.append(jianpu_line)
        
        # 添加歌词
        if self.lyrics:
            lines.append("")
            lines.append("## 歌词")
            for lyric_line in self.lyrics:
                lines.append(lyric_line)
        
        return "\n".join(lines)


class SheetMusicGenerator:
    """曲谱生成器"""
    
    # 音名到数字的映射
    PITCH_TO_NUMBER = {
        "C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11
    }
    
    # 调号到升降号的映射
    KEY_SIGNATURES = {
        "C": [], "G": ["F#"], "D": ["F#", "C#"], "A": ["F#", "C#", "G#"],
        "E": ["F#", "C#", "G#", "D#"], "B": ["F#", "C#", "G#", "D#", "A#"],
        "F#": ["F#", "C#", "G#", "D#", "A#", "E#"],
        "C#": ["F#", "C#", "G#", "D#", "A#", "E#", "B#"],
        "F": ["Bb"], "Bb": ["Bb", "Eb"], "Eb": ["Bb", "Eb", "Ab"],
        "Ab": ["Bb", "Eb", "Ab", "Db"], "Db": ["Bb", "Eb", "Ab", "Db", "Gb"],
        "Gb": ["Bb", "Eb", "Ab", "Db", "Gb", "Cb"],
        "Cb": ["Bb", "Eb", "Ab", "Db", "Gb", "Cb", "Fb"],
        # 小调
        "Am": [], "Em": ["F#"], "Bm": ["F#", "C#"], "F#m": ["F#", "C#", "G#"],
        "C#m": ["F#", "C#", "G#", "D#"], "G#m": ["F#", "C#", "G#", "D#", "A#"],
        "D#m": ["F#", "C#", "G#", "D#", "A#", "E#"],
        "A#m": ["F#", "C#", "G#", "D#", "A#", "E#", "B#"],
        "Dm": ["Bb"], "Gm": ["Bb", "Eb"], "Cm": ["Bb", "Eb", "Ab"],
        "Fm": ["Bb", "Eb", "Ab", "Db"], "Bbm": ["Bb", "Eb", "Ab", "Db", "Gb"],
        "Ebm": ["Bb", "Eb", "Ab", "Db", "Gb", "Cb"],
        "Abm": ["Bb", "Eb", "Ab", "Db", "Gb", "Cb", "Fb"],
    }
    
    @staticmethod
    def parse_melody_string(melody_str: str) -> List[Note]:
        """
        解析旋律字符串
        格式："C4 D4 E4 F4" 或 "C D E F"
        """
        notes = []
        tokens = melody_str.split()
        
        for token in tokens:
            token = token.strip()
            if not token:
                continue
            
            # 解析休止符
            if token.upper() == "R" or token.upper() == "Z":
                notes.append(Note("", 0, 1.0, is_rest=True))
                continue
            
            # 解析音高和八度
            match = re.match(r'^([A-Ga-g])([,\']*)(\d*)$', token)
            if match:
                pitch = match.group(1).upper()
                octave_markers = match.group(2) or ""
                duration_str = match.group(3) or "4"
                
                # 计算八度
                octave = 0
                if octave_markers:
                    if "'" in octave_markers:
                        octave = octave_markers.count("'")
                    elif "," in octave_markers:
                        octave = -octave_markers.count(",")
                
                # 解析时值
                duration = int(duration_str) / 4 if duration_str else 1.0
                
                notes.append(Note(pitch, octave, duration))
            else:
                # 简单格式：只有音名，默认为四分音符
                if re.match(r'^[A-Ga-g]$', token):
                    pitch = token.upper()
                    octave = 0 if token.isupper() else 1
                    notes.append(Note(pitch, octave, 1.0))
        
        return notes
    
    @staticmethod
    def parse_chord_string(chord_str: str) -> List[Optional[Chord]]:
        """
        解析和弦字符串
        格式："C G Am F" 或 "C G Am F | C G C G"
        """
        chords = []
        tokens = chord_str.replace("|", " ").split()
        
        for token in tokens:
            token = token.strip()
            if not token:
                continue
            
            # 解析和弦
            match = re.match(r'^([A-G])([#b]?)(m?)(maj7|7|dim|aug|sus4|sus2|6|9)?$', token)
            if match:
                root = match.group(1)
                accidental = match.group(2) or ""
                minor = match.group(3) or ""
                extension = match.group(4) or ""
                
                quality = minor + extension
                chord = Chord(root + accidental, quality)
                chords.append(chord)
            else:
                chords.append(None)
        
        return chords
    
    @staticmethod
    def group_into_measures(
        notes: List[Note],
        chords: List[Optional[Chord]],
        time_signature: str
    ) -> List[Measure]:
        """
        将音符分组为小节
        """
        # 解析拍号
        match = re.match(r'(\d+)/(\d+)', time_signature)
        if match:
            beats_per_measure = int(match.group(1))
            beat_unit = int(match.group(2))
        else:
            beats_per_measure = 4
            beat_unit = 4
        
        # 计算每小节的总时值（以四分音符为单位）
        beat_duration = 4 / beat_unit  # 一个拍子的时值
        measure_duration = beats_per_measure * beat_duration
        
        measures = []
        current_notes = []
        current_chords = []
        current_duration = 0.0
        chord_idx = 0
        
        for note in notes:
            current_notes.append(note)
            
            # 分配和弦（如果有）
            if chords and chord_idx < len(chords):
                current_chords.append(chords[chord_idx])
                chord_idx += 1
            else:
                current_chords.append(None)
            
            current_duration += note.duration
            
            # 当小节满时，创建新小节
            if current_duration >= measure_duration:
                measures.append(Measure(current_notes, current_chords))
                current_notes = []
                current_chords = []
                current_duration = 0.0
        
        # 处理剩余音符
        if current_notes:
            measures.append(Measure(current_notes, current_chords))
        
        return measures
    
    @staticmethod
    def generate_song(
        title: str,
        composer: str,
        key: str,
        time_signature: str,
        tempo: int,
        melody_str: str,
        chord_str: Optional[str] = None,
        lyrics: Optional[List[str]] = None
    ) -> Song:
        """
        生成歌曲对象
        """
        notes = SheetMusicGenerator.parse_melody_string(melody_str)
        chords = SheetMusicGenerator.parse_chord_string(chord_str) if chord_str else []
        measures = SheetMusicGenerator.group_into_measures(notes, chords, time_signature)
        
        return Song(
            title=title,
            composer=composer,
            key=key,
            time_signature=time_signature,
            tempo=tempo,
            measures=measures,
            lyrics=lyrics
        )


def main():
    parser = argparse.ArgumentParser(
        description="AI 音乐曲谱生成器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 生成 ABC 记谱法
  python generate_sheet_music.py --title "示例歌曲" --key "C" --melody "C D E F G A B c"
  
  # 生成带和弦的简谱
  python generate_sheet_music.py --title "示例歌曲" --key "G" --melody "G A B c" \\
    --chords "G D Em C" --output-format jianpu
  
  # 从文件读取并转换格式
  python generate_sheet_music.py --input-abc song.abc --output-format jianpu
        """
    )
    
    parser.add_argument("--title", "-t", type=str, help="歌曲标题")
    parser.add_argument("--composer", "-c", type=str, default="AI Composer", help="作曲者")
    parser.add_argument("--key", "-k", type=str, default="C", help="调性（如 C, G, Am）")
    parser.add_argument("--time-signature", "-m", type=str, default="4/4", help="拍号（如 4/4, 3/4）")
    parser.add_argument("--tempo", type=int, default=100, help="速度（BPM）")
    parser.add_argument("--melody", type=str, help="旋律字符串（如 'C D E F G'）")
    parser.add_argument("--chords", type=str, help="和弦进行（如 'C G Am F'）")
    parser.add_argument("--lyrics", type=str, help="歌词文件路径")
    parser.add_argument("--input-abc", type=str, help="输入 ABC 文件路径")
    parser.add_argument("--output-format", "-f", type=str, choices=["abc", "jianpu", "both"], 
                        default="abc", help="输出格式")
    parser.add_argument("--output", "-o", type=str, help="输出文件路径")
    
    args = parser.parse_args()
    
    generator = SheetMusicGenerator()
    
    # 处理输入
    if args.input_abc:
        # 从 ABC 文件读取
        with open(args.input_abc, 'r', encoding='utf-8') as f:
            abc_content = f.read()
        print("从 ABC 文件读取功能待实现")
        return
    
    # 生成新歌曲
    if not args.title or not args.melody:
        print("错误：需要提供 --title 和 --melody 参数")
        parser.print_help()
        sys.exit(1)
    
    # 读取歌词
    lyrics = None
    if args.lyrics:
        with open(args.lyrics, 'r', encoding='utf-8') as f:
            lyrics = [line.strip() for line in f if line.strip()]
    
    # 生成歌曲
    song = generator.generate_song(
        title=args.title,
        composer=args.composer,
        key=args.key,
        time_signature=args.time_signature,
        tempo=args.tempo,
        melody_str=args.melody,
        chord_str=args.chords,
        lyrics=lyrics
    )
    
    # 输出结果
    output_content = []
    
    if args.output_format in ["abc", "both"]:
        abc_output = song.to_abc()
        output_content.append("=== ABC 记谱法 ===")
        output_content.append(abc_output)
        output_content.append("")
    
    if args.output_format in ["jianpu", "both"]:
        jianpu_output = song.to_jianpu()
        output_content.append("=== 简谱 ===")
        output_content.append(jianpu_output)
        output_content.append("")
    
    result = "\n".join(output_content)
    
    # 输出到文件或控制台
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(result)
        print(f"曲谱已保存到: {args.output}")
    else:
        print(result)


if __name__ == "__main__":
    main()
