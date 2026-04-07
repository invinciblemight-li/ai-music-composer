#!/usr/bin/env python3
"""
音乐分析工具
分析旋律、和弦进行、曲式结构等
"""

import argparse
import re
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from collections import Counter
import json


@dataclass
class Note:
    """音符"""
    pitch: int  # MIDI 音高
    duration: float  # 时值
    time: float  # 开始时间


@dataclass
class Chord:
    """和弦"""
    root: str
    quality: str
    duration: float
    time: float


class MelodyAnalyzer:
    """旋律分析器"""
    
    def __init__(self):
        self.scale_degrees = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    
    def analyze_range(self, notes: List[Note]) -> Dict:
        """分析音域"""
        if not notes:
            return {}
        
        pitches = [n.pitch for n in notes]
        return {
            'lowest': min(pitches),
            'highest': max(pitches),
            'range_semitones': max(pitches) - min(pitches),
            'range_octaves': (max(pitches) - min(pitches)) / 12
        }
    
    def analyze_contour(self, notes: List[Note]) -> List[str]:
        """分析旋律轮廓"""
        if len(notes) < 2:
            return []
        
        contour = []
        for i in range(1, len(notes)):
            diff = notes[i].pitch - notes[i-1].pitch
            if diff > 0:
                contour.append('up')
            elif diff < 0:
                contour.append('down')
            else:
                contour.append('same')
        
        return contour
    
    def analyze_intervals(self, notes: List[Note]) -> Dict:
        """分析音程使用"""
        if len(notes) < 2:
            return {}
        
        intervals = []
        for i in range(1, len(notes)):
            interval = abs(notes[i].pitch - notes[i-1].pitch)
            intervals.append(interval)
        
        interval_names = {
            0: 'Unison', 1: 'Minor 2nd', 2: 'Major 2nd',
            3: 'Minor 3rd', 4: 'Major 3rd', 5: 'Perfect 4th',
            6: 'Tritone', 7: 'Perfect 5th', 8: 'Minor 6th',
            9: 'Major 6th', 10: 'Minor 7th', 11: 'Major 7th',
            12: 'Octave'
        }
        
        counter = Counter(intervals)
        return {
            'total_intervals': len(intervals),
            'interval_distribution': {
                interval_names.get(k, f'{k} semitones'): v 
                for k, v in counter.most_common()
            },
            'most_common': interval_names.get(counter.most_common(1)[0][0], 'Unknown') if counter else None,
            'average_interval': sum(intervals) / len(intervals) if intervals else 0,
            'largest_leap': max(intervals) if intervals else 0
        }
    
    def analyze_rhythm(self, notes: List[Note]) -> Dict:
        """分析节奏"""
        durations = [n.duration for n in notes]
        counter = Counter(durations)
        
        return {
            'total_notes': len(notes),
            'duration_distribution': dict(counter),
            'most_common_duration': counter.most_common(1)[0] if counter else None,
            'average_duration': sum(durations) / len(durations) if durations else 0,
            'rhythmic_variety': len(counter)  # 不同节奏型的数量
        }
    
    def detect_repetition(self, notes: List[Note], min_length: int = 4) -> List[Tuple[int, int]]:
        """检测重复动机"""
        repetitions = []
        pitch_sequence = [n.pitch for n in notes]
        
        for length in range(min_length, len(pitch_sequence) // 2 + 1):
            for i in range(len(pitch_sequence) - length * 2 + 1):
                pattern = pitch_sequence[i:i+length]
                for j in range(i + length, len(pitch_sequence) - length + 1):
                    if pitch_sequence[j:j+length] == pattern:
                        repetitions.append((i, j, length))
        
        return repetitions
    
    def analyze_key(self, notes: List[Note]) -> Dict:
        """分析调性（简化版）"""
        pitch_classes = [n.pitch % 12 for n in notes]
        counter = Counter(pitch_classes)
        
        # 常见大调的特征音
        major_profiles = {
            'C': [6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88],
            'G': [2.88, 6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29],
            'D': [2.29, 2.88, 6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66],
            'A': [3.66, 2.29, 2.88, 6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39],
            'E': [2.39, 3.66, 2.29, 2.88, 6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19],
        }
        
        # 计算与各个调的相似度
        pitch_distribution = [counter.get(i, 0) for i in range(12)]
        total = sum(pitch_distribution)
        if total > 0:
            pitch_distribution = [p/total for p in pitch_distribution]
        
        best_key = 'C'
        best_score = -1
        
        for key, profile in major_profiles.items():
            score = sum(p * profile[i] for i, p in enumerate(pitch_distribution))
            if score > best_score:
                best_score = score
                best_key = key
        
        return {
            'suggested_key': best_key,
            'confidence': best_score,
            'pitch_class_distribution': dict(counter)
        }


class ChordProgressionAnalyzer:
    """和弦进行分析器"""
    
    # 常见和弦进行模式
    COMMON_PROGRESSIONS = {
        'I-V-vi-IV': ['I', 'V', 'vi', 'IV'],
        'vi-IV-I-V': ['vi', 'IV', 'I', 'V'],
        'I-vi-IV-V': ['I', 'vi', 'IV', 'V'],
        'I-IV-V': ['I', 'IV', 'V'],
        'ii-V-I': ['ii', 'V', 'I'],
        'I-V-vi-iii-IV': ['I', 'V', 'vi', 'iii', 'IV'],
        'I-♭VII-IV': ['I', '♭VII', 'IV'],
        'vi-♭VI-♭III-♭VII': ['vi', '♭VI', '♭III', '♭VII'],
    }
    
    def analyze(self, chords: List[Chord]) -> Dict:
        """分析和弦进行"""
        chord_symbols = [f"{c.root}{c.quality}" for c in chords]
        roman_symbols = self._to_roman_numerals(chords)
        
        return {
            'chord_sequence': chord_symbols,
            'roman_numerals': roman_symbols,
            'unique_chords': list(set(chord_symbols)),
            'progression_length': len(chords),
            'detected_patterns': self._detect_patterns(roman_symbols),
            'harmonic_rhythm': self._analyze_harmonic_rhythm(chords)
        }
    
    def _to_roman_numerals(self, chords: List[Chord]) -> List[str]:
        """转换为罗马数字（简化版）"""
        # 假设 C 大调
        degree_map = {
            'C': 'I', 'D': 'ii', 'E': 'iii', 'F': 'IV',
            'G': 'V', 'A': 'vi', 'B': 'vii°'
        }
        
        result = []
        for chord in chords:
            roman = degree_map.get(chord.root, chord.root)
            if chord.quality == 'm':
                roman = roman.lower()
            result.append(roman)
        
        return result
    
    def _detect_patterns(self, roman_symbols: List[str]) -> List[str]:
        """检测常见进行模式"""
        detected = []
        
        for name, pattern in self.COMMON_PROGRESSIONS.items():
            pattern_str = '-'.join(pattern)
            roman_str = '-'.join(roman_symbols)
            if pattern_str in roman_str:
                detected.append(name)
        
        return detected
    
    def _analyze_harmonic_rhythm(self, chords: List[Chord]) -> Dict:
        """分析和声节奏"""
        durations = [c.duration for c in chords]
        
        return {
            'average_chord_duration': sum(durations) / len(durations) if durations else 0,
            'chord_changes_per_bar': len(chords) / sum(durations) * 4 if sum(durations) > 0 else 0,
            'longest_chord': max(durations) if durations else 0,
            'shortest_chord': min(durations) if durations else 0
        }


class SongStructureAnalyzer:
    """歌曲结构分析器"""
    
    def analyze_sections(self, sections: List[Dict]) -> Dict:
        """分析歌曲段落结构"""
        total_bars = sum(s.get('bars', 0) for s in sections)
        section_types = Counter(s.get('section', 'unknown') for s in sections)
        
        return {
            'total_sections': len(sections),
            'total_bars': total_bars,
            'section_types': dict(section_types),
            'average_section_length': total_bars / len(sections) if sections else 0,
            'structure_sequence': [s.get('section', 'unknown') for s in sections]
        }
    
    def suggest_improvements(self, analysis: Dict) -> List[str]:
        """根据分析结果给出改进建议"""
        suggestions = []
        
        # 检查音域
        if 'range_octaves' in analysis:
            if analysis['range_octaves'] > 2:
                suggestions.append("音域较宽，考虑简化旋律或调整音区")
            elif analysis['range_octaves'] < 0.5:
                suggestions.append("音域较窄，可以尝试扩展旋律范围")
        
        # 检查重复
        if 'repetitions' in analysis and len(analysis['repetitions']) == 0:
            suggestions.append("旋律缺乏重复元素，考虑添加动机重复以增强记忆点")
        
        # 检查节奏
        if 'rhythmic_variety' in analysis:
            if analysis['rhythmic_variety'] < 3:
                suggestions.append("节奏型较单一，可以尝试更多节奏变化")
        
        # 检查音程
        if 'largest_leap' in analysis:
            if analysis['largest_leap'] > 12:
                suggestions.append("存在大跳音程，确保演唱者能够胜任")
        
        return suggestions


class MusicAnalyzer:
    """综合音乐分析器"""
    
    def __init__(self):
        self.melody_analyzer = MelodyAnalyzer()
        self.chord_analyzer = ChordProgressionAnalyzer()
        self.structure_analyzer = SongStructureAnalyzer()
    
    def analyze_abc(self, abc_content: str) -> Dict:
        """分析 ABC 记谱法内容"""
        # 这里简化处理，实际应该完整解析 ABC
        # 返回基础分析结果
        return {
            'format': 'ABC',
            'content_length': len(abc_content),
            'lines': len(abc_content.split('\n')),
            'note': '完整解析需要实现 ABC 解析器'
        }
    
    def analyze_melody(self, notes: List[Note]) -> Dict:
        """综合分析旋律"""
        return {
            'range': self.melody_analyzer.analyze_range(notes),
            'contour': self.melody_analyzer.analyze_contour(notes),
            'intervals': self.melody_analyzer.analyze_intervals(notes),
            'rhythm': self.melody_analyzer.analyze_rhythm(notes),
            'repetitions': self.melody_analyzer.detect_repetition(notes),
            'key_analysis': self.melody_analyzer.analyze_key(notes)
        }
    
    def generate_report(self, analysis: Dict) -> str:
        """生成分析报告"""
        report = []
        report.append("=" * 50)
        report.append("音乐分析报告")
        report.append("=" * 50)
        
        for section, data in analysis.items():
            report.append(f"\n【{section}】")
            if isinstance(data, dict):
                for key, value in data.items():
                    report.append(f"  {key}: {value}")
            elif isinstance(data, list):
                for item in data[:10]:  # 只显示前10个
                    report.append(f"  - {item}")
            else:
                report.append(f"  {data}")
        
        return '\n'.join(report)


def main():
    parser = argparse.ArgumentParser(description='音乐分析工具')
    parser.add_argument('-f', '--file', help='分析 ABC 文件')
    parser.add_argument('-m', '--melody', help='旋律数据（JSON格式）')
    parser.add_argument('-c', '--chords', help='和弦进行（JSON格式）')
    parser.add_argument('-o', '--output', help='输出报告文件')
    
    args = parser.parse_args()
    
    analyzer = MusicAnalyzer()
    analysis = {}
    
    if args.file:
        with open(args.file, 'r', encoding='utf-8') as f:
            abc_content = f.read()
        analysis['abc_analysis'] = analyzer.analyze_abc(abc_content)
    
    if args.melody:
        melody_data = json.loads(args.melody)
        notes = [Note(**n) for n in melody_data]
        analysis['melody_analysis'] = analyzer.analyze_melody(notes)
    
    if args.chords:
        chord_data = json.loads(args.chords)
        chords = [Chord(**c) for c in chord_data]
        analysis['chord_analysis'] = analyzer.chord_analyzer.analyze(chords)
    
    report = analyzer.generate_report(analysis)
    
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"报告已保存到: {args.output}")
    else:
        print(report)


if __name__ == '__main__':
    main()
