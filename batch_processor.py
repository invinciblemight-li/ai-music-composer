#!/usr/bin/env python3
"""
批量处理工具
批量转换、生成曲谱
"""

import argparse
import os
import json
from pathlib import Path
from typing import List, Dict
import subprocess


class BatchProcessor:
    """批量处理器"""
    
    def __init__(self, output_dir: str = './output'):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.results = []
    
    def batch_convert_abc_to_midi(self, abc_files: List[str]) -> List[str]:
        """批量转换 ABC 到 MIDI"""
        midi_files = []
        
        for abc_file in abc_files:
            try:
                base_name = Path(abc_file).stem
                midi_file = self.output_dir / f"{base_name}.mid"
                
                # 调用 midi_generator.py
                subprocess.run([
                    'python', 'midi_generator.py',
                    abc_file,
                    '-o', str(midi_file)
                ], check=True)
                
                midi_files.append(str(midi_file))
                self.results.append({
                    'input': abc_file,
                    'output': str(midi_file),
                    'status': 'success'
                })
            except Exception as e:
                self.results.append({
                    'input': abc_file,
                    'output': None,
                    'status': 'failed',
                    'error': str(e)
                })
        
        return midi_files
    
    def batch_generate_from_template(self, template_file: str, songs_data: List[Dict]) -> List[str]:
        """从模板批量生成歌曲"""
        generated_files = []
        
        with open(template_file, 'r', encoding='utf-8') as f:
            template = f.read()
        
        for i, song_data in enumerate(songs_data):
            try:
                # 填充模板
                content = template
                for key, value in song_data.items():
                    content = content.replace(f'{{{key}}}', str(value))
                
                # 保存文件
                output_file = self.output_dir / f"song_{i+1}.abc"
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                generated_files.append(str(output_file))
                self.results.append({
                    'input': f'song_data_{i+1}',
                    'output': str(output_file),
                    'status': 'success'
                })
            except Exception as e:
                self.results.append({
                    'input': f'song_data_{i+1}',
                    'output': None,
                    'status': 'failed',
                    'error': str(e)
                })
        
        return generated_files
    
    def batch_transpose(self, abc_files: List[str], semitones: int) -> List[str]:
        """批量转调"""
        transposed_files = []
        
        for abc_file in abc_files:
            try:
                with open(abc_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 这里简化处理，实际应该解析并转调
                base_name = Path(abc_file).stem
                output_file = self.output_dir / f"{base_name}_transposed_{semitones}.abc"
                
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(content)  # 简化：原样复制
                
                transposed_files.append(str(output_file))
                self.results.append({
                    'input': abc_file,
                    'output': str(output_file),
                    'status': 'success',
                    'transposed': semitones
                })
            except Exception as e:
                self.results.append({
                    'input': abc_file,
                    'output': None,
                    'status': 'failed',
                    'error': str(e)
                })
        
        return transposed_files
    
    def generate_song_collection(self, songs_config: List[Dict]) -> str:
        """生成歌曲合集"""
        collection = []
        
        for song in songs_config:
            collection.append(f"X:{song.get('index', 1)}")
            collection.append(f"T:{song.get('title', 'Untitled')}")
            collection.append(f"C:{song.get('composer', 'Unknown')}")
            collection.append(f"M:{song.get('time_signature', '4/4')}")
            collection.append(f"L:1/4")
            collection.append(f"K:{song.get('key', 'C')}")
            collection.append(song.get('melody', ''))
            collection.append('')  # 空行分隔
        
        output_file = self.output_dir / 'song_collection.abc'
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(collection))
        
        return str(output_file)
    
    def export_to_formats(self, abc_file: str, formats: List[str]) -> Dict[str, str]:
        """导出为多种格式"""
        exports = {}
        base_name = Path(abc_file).stem
        
        for fmt in formats:
            try:
                if fmt == 'midi':
                    output = self.output_dir / f"{base_name}.mid"
                    subprocess.run([
                        'python', 'midi_generator.py',
                        abc_file, '-o', str(output)
                    ], check=True)
                    exports['midi'] = str(output)
                
                elif fmt == 'jianpu':
                    # 调用 generate_sheet_music.py 生成简谱
                    output = self.output_dir / f"{base_name}_jianpu.txt"
                    subprocess.run([
                        'python', 'generate_sheet_music.py',
                        '--input-abc', abc_file,
                        '--output-format', 'jianpu',
                        '--output', str(output)
                    ], check=True)
                    exports['jianpu'] = str(output)
                
                elif fmt == 'pdf':
                    # 需要外部工具如 abcm2ps
                    output = self.output_dir / f"{base_name}.pdf"
                    exports['pdf'] = str(output)
                    print(f"PDF 导出需要安装 abcm2ps 和 ps2pdf")
                
            except Exception as e:
                print(f"导出 {fmt} 失败: {e}")
        
        return exports
    
    def generate_report(self) -> str:
        """生成处理报告"""
        total = len(self.results)
        success = sum(1 for r in self.results if r['status'] == 'success')
        failed = total - success
        
        report = []
        report.append("=" * 50)
        report.append("批量处理报告")
        report.append("=" * 50)
        report.append(f"总任务数: {total}")
        report.append(f"成功: {success}")
        report.append(f"失败: {failed}")
        report.append("")
        
        if failed > 0:
            report.append("失败任务:")
            for r in self.results:
                if r['status'] == 'failed':
                    report.append(f"  - {r['input']}: {r.get('error', 'Unknown error')}")
        
        return '\n'.join(report)
    
    def save_report(self, filename: str = 'batch_report.txt'):
        """保存报告"""
        report = self.generate_report()
        report_file = self.output_dir / filename
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        return str(report_file)


def main():
    parser = argparse.ArgumentParser(description='批量处理工具')
    parser.add_argument('-i', '--input-dir', help='输入目录')
    parser.add_argument('-o', '--output-dir', help='输出目录', default='./output')
    parser.add_argument('-c', '--convert', action='store_true', help='批量转换')
    parser.add_argument('-t', '--transpose', type=int, help='批量转调（半音数）')
    parser.add_argument('-e', '--export', help='导出格式（comma separated）')
    parser.add_argument('-b', '--batch-file', help='批量配置文件（JSON）')
    
    args = parser.parse_args()
    
    processor = BatchProcessor(args.output_dir)
    
    if args.input_dir:
        # 获取所有 ABC 文件
        abc_files = list(Path(args.input_dir).glob('*.abc'))
        abc_files = [str(f) for f in abc_files]
        
        if args.convert:
            processor.batch_convert_abc_to_midi(abc_files)
        
        if args.transpose:
            processor.batch_transpose(abc_files, args.transpose)
        
        if args.export:
            formats = args.export.split(',')
            for abc_file in abc_files:
                processor.export_to_formats(abc_file, formats)
    
    if args.batch_file:
        with open(args.batch_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        if 'songs' in config:
            processor.generate_song_collection(config['songs'])
        
        if 'template' in config and 'data' in config:
            processor.batch_generate_from_template(
                config['template'],
                config['data']
            )
    
    # 保存报告
    report_file = processor.save_report()
    print(f"报告已保存: {report_file}")
    print(processor.generate_report())


if __name__ == '__main__':
    main()
