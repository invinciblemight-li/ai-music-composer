#!/usr/bin/env python3
"""
MIDI 文件生成器
支持从 ABC 记谱法或旋律数据生成 MIDI 文件
"""

import argparse
import re
from typing import List, Tuple, Optional
from dataclasses import dataclass

try:
    from midiutil import MIDIFile
except ImportError:
    print("请先安装 midiutil: pip install midiutil")
    raise


@dataclass
class MidiNote:
    """MIDI 音符"""
    pitch: int  # MIDI 音高 (0-127)
    time: float  # 开始时间（拍）
    duration: float  # 时值（拍）
    velocity: int = 100  # 力度 (0-127)


@dataclass
class MidiTrack:
    """MIDI 音轨"""
    name: str
    instrument: int  # MIDI 乐器编号
    notes: List[MidiNote]


class ABCtoMidiConverter:
    """ABC 记谱法转 MIDI 转换器"""
    
    # 音名到 MIDI 音高的映射（C4 = 60）
    PITCH_TO_MIDI = {
        'C,': 48, 'D,': 50, 'E,': 52, 'F,': 53, 'G,': 55, 'A,': 57, 'B,': 59,
        'C': 60, 'D': 62, 'E': 64, 'F': 65, 'G': 67, 'A': 69, 'B': 71,
        'c': 72, 'd': 74, 'e': 76, 'f': 77, 'g': 79, 'a': 81, 'b': 83,
        "c'": 84, "d'": 86, "e'": 88, "f'": 89, "g'": 91, "a'": 93, "b'": 95,
        "c''": 96, "d''": 98, "e''": 100, "f''": 101, "g''": 103,
    }
    
    # 调号到升降号的映射
    KEY_SIGNATURES = {
        'C': 0, 'G': 1, 'D': 2, 'A': 3, 'E': 4, 'B': 5, 'F#': 6, 'C#': 7,
        'F': -1, 'Bb': -2, 'Eb': -3, 'Ab': -4, 'Db': -5, 'Gb': -6, 'Cb': -7,
        'Am': 0, 'Em': 1, 'Bm': 2, 'F#m': 3, 'C#m': 4, 'G#m': 5, 'D#m': 6, 'A#m': 7,
        'Dm': -1, 'Gm': -2, 'Cm': -3, 'Fm': -4, 'Bbm': -5, 'Ebm': -6, 'Abm': -7,
    }
    
    def __init__(self):
        self.default_note_length = 1/4  # 默认四分音符
        self.tempo = 120
        self.key = 'C'
        self.time_signature = (4, 4)
    
    def parse_abc(self, abc_content: str) -> List[MidiTrack]:
        """解析 ABC 记谱法内容"""
        lines = abc_content.strip().split('\n')
        
        # 解析头部信息
        melody_notes = []
        lyrics = []
        in_header = True
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # 解析头部字段
            if in_header and line[1:2] == ':':
                field = line[0]
                value = line[2:].strip()
                
                if field == 'L':  # 默认音符长度
                    self._parse_length(value)
                elif field == 'Q':  # 速度
                    self._parse_tempo(value)
                elif field == 'K':  # 调号
                    self.key = value.split()[0]
                elif field == 'M':  # 拍号
                    self._parse_time_signature(value)
                elif field == 'w':  # 歌词
                    lyrics.append(value)
                continue
            
            # 旋律开始
            if line and not line.startswith('%'):
                in_header = False
                notes = self._parse_melody_line(line)
                melody_notes.extend(notes)
        
        # 创建音轨
        tracks = []
        
        # 旋律音轨
        melody_track = MidiTrack(
            name="Melody",
            instrument=0,  # 钢琴
            notes=melody_notes
        )
        tracks.append(melody_track)
        
        return tracks
    
    def _parse_length(self, value: str):
        """解析音符长度"""
        match = re.match(r'(\d+)/(\d+)', value)
        if match:
            self.default_note_length = int(match.group(1)) / int(match.group(2))
    
    def _parse_tempo(self, value: str):
        """解析速度"""
        match = re.search(r'(\d+)', value)
        if match:
            self.tempo = int(match.group(1))
    
    def _parse_time_signature(self, value: str):
        """解析拍号"""
        match = re.match(r'(\d+)/(\d+)', value)
        if match:
            self.time_signature = (int(match.group(1)), int(match.group(2)))
    
    def _parse_melody_line(self, line: str) -> List[MidiNote]:
        """解析旋律行"""
        notes = []
        current_time = 0.0
        
        # 移除和弦标记（引号内的内容）
        line = re.sub(r'"[^"]*"', '', line)
        
        # 解析音符
        tokens = self._tokenize(line)
        
        for token in tokens:
            if token in ['|', '||', '|:', ':|', '::']:
                continue
            
            note = self._parse_note(token, current_time)
            if note:
                notes.append(note)
                current_time += note.duration
        
        return notes
    
    def _tokenize(self, line: str) -> List[str]:
        """将旋律行分解为 token"""
        # 简单的分词
        tokens = []
        i = 0
        while i < len(line):
            if line[i] in ' |:\n':
                if line[i:i+2] in ['||', '|:', ':|', '::']:
                    tokens.append(line[i:i+2])
                    i += 2
                else:
                    tokens.append(line[i])
                    i += 1
            elif line[i] in 'ABCDEFGabcdefg':
                # 读取完整的音符
                note = line[i]
                i += 1
                # 读取八度标记
                while i < len(line) and line[i] in "',":
                    note += line[i]
                    i += 1
                # 读取升降号
                if i < len(line) and line[i] in '^_=':
                    note = line[i] + note
                    i += 1
                # 读取时值
                duration = ''
                while i < len(line) and (line[i].isdigit() or line[i] == '/'):
                    duration += line[i]
                    i += 1
                if duration:
                    note += duration
                tokens.append(note)
            elif line[i] == 'z':  # 休止符
                rest = 'z'
                i += 1
                duration = ''
                while i < len(line) and (line[i].isdigit() or line[i] == '/'):
                    duration += line[i]
                    i += 1
                if duration:
                    rest += duration
                tokens.append(rest)
            else:
                i += 1
        
        return tokens
    
    def _parse_note(self, token: str, time: float) -> Optional[MidiNote]:
        """解析单个音符"""
        if token.startswith('z'):  # 休止符
            duration = self._parse_duration(token[1:])
            return MidiNote(pitch=0, time=time, duration=duration, velocity=0)
        
        # 解析音高
        match = re.match(r'^([\^_=]?)([A-Ga-g])([,\']*)(\d*)(/(\d+))?$', token)
        if not match:
            return None
        
        accidental = match.group(1) or ''
        pitch_name = match.group(2)
        octave_markers = match.group(3) or ''
        duration_num = match.group(4) or ''
        duration_denom = match.group(6) or ''
        
        # 构建音名
        if pitch_name.isupper():
            base_pitch = pitch_name
        else:
            base_pitch = pitch_name.upper()
        
        # 应用升降号
        if accidental == '^':
            base_pitch = '#' + base_pitch
        elif accidental == '_':
            base_pitch = 'b' + base_pitch
        
        # 应用八度
        if "'" in octave_markers:
            base_pitch = base_pitch.lower() + "'" * octave_markers.count("'")
        elif ',' in octave_markers:
            base_pitch = base_pitch.lower() + ',' * octave_markers.count(',')
        
        # 获取 MIDI 音高
        midi_pitch = self.PITCH_TO_MIDI.get(base_pitch, 60)
        
        # 应用调号升降
        midi_pitch = self._apply_key_signature(midi_pitch, pitch_name.upper())
        
        # 解析时值
        duration = self._parse_duration(duration_num, duration_denom)
        
        return MidiNote(pitch=midi_pitch, time=time, duration=duration)
    
    def _parse_duration(self, num_str: str = '', denom_str: str = '') -> float:
        """解析时值"""
        if not num_str and not denom_str:
            return self.default_note_length * 4  # 转换为四分音符为单位
        
        if '/' in num_str:
            parts = num_str.split('/')
            num = int(parts[0]) if parts[0] else 1
            denom = int(parts[1]) if len(parts) > 1 and parts[1] else 2
            return (num / denom) * 4
        
        if num_str:
            num = int(num_str)
            if denom_str:
                denom = int(denom_str)
                return (num / denom) * 4
            else:
                return num * self.default_note_length * 4
        
        return self.default_note_length * 4
    
    def _apply_key_signature(self, pitch: int, note_name: str) -> int:
        """应用调号升降"""
        sharps_flats = self.KEY_SIGNATURES.get(self.key, 0)
        
        # 简化的调号处理
        sharp_order = ['F', 'C', 'G', 'D', 'A', 'E', 'B']
        flat_order = ['B', 'E', 'A', 'D', 'G', 'C', 'F']
        
        if sharps_flats > 0:
            for i in range(sharps_flats):
                if note_name == sharp_order[i]:
                    pitch += 1
        elif sharps_flats < 0:
            for i in range(abs(sharps_flats)):
                if note_name == flat_order[i]:
                    pitch -= 1
        
        return pitch


class MidiGenerator:
    """MIDI 文件生成器"""
    
    def __init__(self, tempo: int = 120):
        self.tempo = tempo
        self.tracks = []
    
    def add_track(self, track: MidiTrack):
        """添加音轨"""
        self.tracks.append(track)
    
    def generate(self, filename: str):
        """生成 MIDI 文件"""
        midi = MIDIFile(len(self.tracks))
        
        for i, track in enumerate(self.tracks):
            # 设置音轨名称
            midi.addTrackName(i, 0, track.name)
            
            # 设置乐器
            midi.addProgramChange(i, 0, 0, track.instrument)
            
            # 添加音符
            for note in track.notes:
                if note.velocity > 0:  # 不是休止符
                    midi.addNote(
                        i, 0, note.pitch,
                        note.time, note.duration,
                        note.velocity
                    )
        
        # 设置速度
        midi.addTempo(0, 0, self.tempo)
        
        # 写入文件
        with open(filename, 'wb') as f:
            midi.writeFile(f)
        
        print(f"MIDI 文件已生成: {filename}")


def main():
    parser = argparse.ArgumentParser(description='ABC 记谱法转 MIDI')
    parser.add_argument('input', help='输入 ABC 文件')
    parser.add_argument('-o', '--output', help='输出 MIDI 文件', default='output.mid')
    parser.add_argument('-t', '--tempo', type=int, help='速度 (BPM)', default=120)
    
    args = parser.parse_args()
    
    # 读取 ABC 文件
    with open(args.input, 'r', encoding='utf-8') as f:
        abc_content = f.read()
    
    # 转换
    converter = ABCtoMidiConverter()
    tracks = converter.parse_abc(abc_content)
    
    # 生成 MIDI
    generator = MidiGenerator(tempo=args.tempo)
    for track in tracks:
        generator.add_track(track)
    
    generator.generate(args.output)


if __name__ == '__main__':
    main()
