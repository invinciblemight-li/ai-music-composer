#!/usr/bin/env python3
"""
AI 人声歌曲生成器
将歌词发送到 Suno/Udio 等 AI 音乐平台生成带人声的完整歌曲
"""

import os
import sys
import json
import time
import argparse
from typing import Optional, List, Dict


class VoiceGenerator:
    """AI 人声歌曲生成器"""
    
    def __init__(self, platform: str = "suno"):
        self.platform = platform.lower()
        self.api_key = self._get_api_key()
        
    def _get_api_key(self) -> Optional[str]:
        """获取 API Key"""
        env_var = f"{self.platform.upper()}_API_KEY"
        return os.getenv(env_var)
    
    def generate_suno(self, lyrics: str, style: str = "pop", title: str = "Untitled") -> Dict:
        """
        使用 Suno API 生成带人声的歌曲
        
        注意：Suno API 需要申请访问权限
        官方文档：https://suno.ai
        """
        print(f"[*] 正在使用 Suno 生成歌曲: {title}")
        print(f"[*] 风格: {style}")
        print(f"[*] 歌词长度: {len(lyrics)} 字符")
        
        if not self.api_key:
            print("[!] 未设置 SUNO_API_KEY 环境变量")
            print("[i] 请前往 https://suno.ai 申请 API 访问权限")
            return self._generate_manual_instructions("Suno", lyrics, style, title)
        
        # 这里集成实际的 Suno API 调用
        # 由于 Suno API 目前处于封闭状态，这里提供伪代码
        
        print("\n" + "="*60)
        print("[AI] AI 人声生成")
        print("="*60)
        print(f"平台: Suno AI")
        print(f"歌曲: {title}")
        print(f"风格: {style}")
        print("\n[*] 歌词预览:")
        print(lyrics[:200] + "..." if len(lyrics) > 200 else lyrics)
        print("\n[OK] 如果使用 API，将生成:")
        print("   - 带人声的完整 MP3 音频")
        print("   - 伴奏版本 (Instrumental)")
        print("   - 歌词时间轴 (LRC 格式)")
        print("="*60)
        
        return {
            "platform": "suno",
            "title": title,
            "style": style,
            "status": "manual_required",
            "lyrics": lyrics
        }
    
    def generate_udio(self, lyrics: str, style: str = "pop", title: str = "Untitled") -> Dict:
        """
        使用 Udio API 生成带人声的歌曲
        
        官网：https://udio.com
        """
        print(f"[*] 正在使用 Udio 生成歌曲: {title}")
        
        if not self.api_key:
            print("[!]  未设置 UDIO_API_KEY 环境变量")
            return self._generate_manual_instructions("Udio", lyrics, style, title)
        
        print("\n" + "="*60)
        print("[AI] AI 人声生成")
        print("="*60)
        print(f"平台: Udio")
        print(f"歌曲: {title}")
        print(f"风格: {style}")
        print("\n[OK] 如果使用 API，将生成高质量人声歌曲")
        print("="*60)
        
        return {
            "platform": "udio",
            "title": title,
            "style": style,
            "status": "manual_required"
        }
    
    def generate_local_tts(self, lyrics: str, voice: str = "zh-CN-XiaoxiaoNeural") -> str:
        """
        使用本地 TTS 生成朗读版（非歌声）
        
        需要安装: pip install edge-tts
        """
        try:
            import edge_tts
            import asyncio
            
            output_file = f"tts_output_{int(time.time())}.mp3"
            
            async def generate():
                communicate = edge_tts.Communicate(lyrics, voice)
                await communicate.save(output_file)
            
            asyncio.run(generate())
            print(f"[OK] TTS 生成完成: {output_file}")
            return output_file
            
        except ImportError:
            print("[X] 请先安装 edge-tts: pip install edge-tts")
            return None
    
    def _generate_manual_instructions(self, platform: str, lyrics: str, style: str, title: str) -> Dict:
        """生成手动操作指南"""
        
        instructions = f"""
+==============================================================+
|           {platform} AI 人声生成 - 手动操作指南           |
+==============================================================+

由于 {platform} API 需要申请访问权限，请按以下步骤操作：

[*] 步骤 1: 访问官网
   网址: {"https://suno.com" if platform == "Suno" else "https://udio.com"}

[*] 步骤 2: 注册/登录账号
   - 使用邮箱或 Google 账号注册
   - 免费用户每天有额度限制

[*] 步骤 3: 创建新歌曲
   - 点击 "Create" 或 "Generate"
   - 选择 "Custom Mode" (自定义模式)

[*] 步骤 4: 输入以下信息

【歌曲标题】
{title}

【音乐风格】
{style}

【歌词】
{lyrics}

[*] 步骤 5: 生成并下载
   - 点击 Generate 等待生成
   - 下载 MP3 或 WAV 格式

[i] 提示:
- 免费版有每日生成次数限制
- 可以多次生成选择最佳版本
- 生成的歌曲版权归用户所有

===============================================================
"""
        print(instructions)
        
        # 保存到文件
        instruction_file = f"{title.replace(' ', '_')}_{platform.lower()}_instructions.txt"
        with open(instruction_file, 'w', encoding='utf-8') as f:
            f.write(instructions)
        print(f"[*] 操作指南已保存到: {instruction_file}")
        
        return {
            "platform": platform.lower(),
            "title": title,
            "style": style,
            "status": "manual_instructions",
            "instruction_file": instruction_file
        }


def parse_song_file(file_path: str) -> Dict:
    """解析歌曲文件，提取歌词和元数据"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 简单解析：查找歌词部分
    lines = content.split('\n')
    lyrics_lines = []
    title = "Untitled"
    style = "pop"
    
    in_lyrics = False
    for line in lines:
        line = line.strip()
        
        # 提取标题
        if line.startswith('# 《') and line.endswith('》'):
            title = line[3:-1]
        elif line.startswith('**歌名**') or line.startswith('**标题**'):
            title = line.split('**')[-2] if '**' in line else line.split(':')[-1].strip()
        
        # 提取风格
        elif '风格' in line and ':' in line:
            style = line.split(':')[-1].strip().lower()
        
        # 收集歌词（排除标记行和空行）
        elif line and not line.startswith('#') and not line.startswith('**') and not line.startswith('['):
            if not line.startswith('```') and not line.startswith('>'):
                lyrics_lines.append(line)
    
    return {
        "title": title,
        "style": style,
        "lyrics": '\n'.join(lyrics_lines)
    }


def main():
    parser = argparse.ArgumentParser(description='AI 人声歌曲生成器')
    parser.add_argument('input', help='输入文件路径（歌曲文本文件）或歌词文本')
    parser.add_argument('-p', '--platform', default='suno', 
                       choices=['suno', 'udio', 'tts'],
                       help='AI 人声平台 (默认: suno)')
    parser.add_argument('-t', '--title', help='歌曲标题')
    parser.add_argument('-s', '--style', default='pop',
                       help='音乐风格 (默认: pop)')
    parser.add_argument('-o', '--output', help='输出文件名')
    
    args = parser.parse_args()
    
    print("="*60)
    print("AI Music Composer - 人声歌曲生成器")
    print("="*60)
    
    # 解析输入
    if os.path.isfile(args.input):
        song_data = parse_song_file(args.input)
        lyrics = song_data['lyrics']
        title = args.title or song_data['title']
        style = args.style or song_data['style']
    else:
        lyrics = args.input
        title = args.title or "AI Generated Song"
        style = args.style
    
    # 生成人声
    generator = VoiceGenerator(platform=args.platform)
    
    if args.platform == 'suno':
        result = generator.generate_suno(lyrics, style, title)
    elif args.platform == 'udio':
        result = generator.generate_udio(lyrics, style, title)
    elif args.platform == 'tts':
        output = generator.generate_local_tts(lyrics)
        if output:
            print(f"[OK] 已生成朗读版: {output}")
            print("[!] 注意: TTS 是朗读，不是歌声")
    
    print("\n[*] 完成!")


if __name__ == '__main__':
    main()
