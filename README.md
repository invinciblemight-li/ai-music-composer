# 🎵 AI Music Composer Skill

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![WorkBuddy Skill](https://img.shields.io/badge/WorkBuddy-Skill-blue.svg)](https://github.com/invinciblemight-li/ai-music-composer)
[![Python](https://img.shields.io/badge/Python-3.8+-green.svg)](https://www.python.org/)

> **AI音乐创作与曲谱生成工具** - 由 invinciblemight-li  开发的 Skill，为了实现 AI 创作歌曲并提取完整曲谱。

[English](#english) | [中文](#中文)

---

## 🌟 核心功能

### 🎼 多格式曲谱支持
- **ABC 记谱法** - 文本格式，易于分享和编辑
- **简谱** - 数字记谱，适合中文用户
- **MIDI** - 可播放的数字音乐文件
- **MusicXML** - 专业音乐软件兼容格式

### 🎵 AI 歌曲创作
- 根据主题、情感、风格生成原创歌词和旋律
- 支持多种音乐风格：流行、民谣、古典、摇滚、电子等
- 自动配器和弦进行推荐

### 🎸 专业音乐数据库
- **300+ 音乐风格** - 全球音乐风格大全
- **500+ 乐器资料** - 全球乐器数据库
- **中国国风音乐** - 古风、仙侠、戏曲、宫廷等8大子类型
- **粤语流行音乐** - 经典粤语流行、情歌、摇滚等8大风格

###🛠️ 实用工具脚本
- **MIDI 生成器** - ABC 转 MIDI
- **歌词辅助工具** - 音节计算、押韵分析
- **音乐分析器** - 旋律、和弦、曲式分析
- **批量处理器** - 批量转换、转调、导出

---


## 📦 安装方法

### 方法 1：通过 ZIP 文件安装
1. 下载 `ai-music-composer.zip`
2. 解压到 WorkBuddy 的 skills 目录：
使用方法
触发方式
关键词触发：

帮我创作一首关于春天的歌
生成曲谱
"提取乐谱"
"谱写音乐"
显式调用：

@skill://ai-music-composer 帮我创作一首歌
示例 1：创作国风歌曲
输入：

@skill://ai-music-composer 创作一首仙侠风格的古风歌曲
输出：

完整歌词（主歌、导歌、副歌、桥段）
ABC 记谱法
简谱
和弦进行建议
编曲建议
示例 2：创作英文流行歌曲
输入：

@skill://ai-music-composer 创作一首关于爱情的英文流行歌曲
输出：

英文歌词
旋律曲谱
制作建议
📁 目录结构
ai-music-composer/
├── SKILL.md                    # Skill 核心说明文档
├── README.md                   # 本文件
├── LICENSE                     # MIT 许可证
├── .gitignore                  # Git 忽略配置
├── scripts/                    # 工具脚本（5个）
│   ├── generate_sheet_music.py # 曲谱生成
│   ├── midi_generator.py       # MIDI 生成器
│   ├── lyrics_helper.py        # 歌词辅助
│   ├── music_analyzer.py       # 音乐分析
│   └── batch_processor.py      # 批量处理
├── references/                 # 参考资料（7个）
│   ├── chord_progressions.md   # 常用和弦进行
│   ├── music_styles.md         # 音乐风格指南
│   ├── music_theory.md         # 音乐理论基础
│   ├── music_genres_complete.md    # 全球音乐风格大全（300+）
│   ├── instruments_complete.md     # 全球乐器大全（500+）
│   ├── guofeng_guide.md        # 中国国风音乐创作指南 ⭐
│   └── cantopop_guide.md       # 粤语流行音乐创作指南 ⭐
└── assets/                     # 资源文件
    ├── example_song.abc        # 示例歌曲
    ├── template.abc            # 曲谱模板
    └── song_templates.json     # 歌曲结构模板
🎨 支持的音乐风格
西方流行音乐
Pop, Rock, Electronic, Hip-Hop, R&B
Jazz, Blues, Country, Folk, Reggae
Latin, Classical, Metal, Punk, Indie
中国国风音乐（8大子类型）
风格	特点	代表元素
古风流行	古典诗词风格	五声音阶、古筝、琵琶
仙侠风	武侠仙侠题材	飘逸旋律、箫、古琴
戏曲流行	京剧/昆曲元素	戏腔、传统打击乐
宫廷风	雅乐音阶	编钟、庄重典雅
新国风	电子+传统融合	现代编曲、年轻化
国风摇滚	热血激昂	电吉他+传统乐器
国风电子	合成器民族旋律	EDM + 五声音阶
国风说唱	文言文+嘻哈	古韵歌词、现代节奏
粤语流行音乐（8大风格）
经典粤语流行（80-90年代）
粤语情歌（张学友、陈奕迅风格）
粤语摇滚（Beyond风格）
粤语说唱（粤语九声韵律）
港式民谣、TVB剧集歌等
🛠️ 脚本工具使用
生成曲谱
bash
复制
python scripts/generate_sheet_music.py \
  --title "歌曲名" \
  --composer "作曲者" \
  --key "C" \
  --time-signature "4/4" \
  --tempo "120" \
  --melody "C D E F G A B c" \
  --chords "C G Am F" \
  --output-format abc
MIDI 生成
bash
复制
python scripts/midi_generator.py song.abc -o output.mid -t 120
歌词辅助
bash
复制
python scripts/lyrics_helper.py -c "歌词文本"        # 计算音节
python scripts/lyrics_helper.py -r "爱"              # 查找押韵词
python scripts/lyrics_helper.py -a lyrics.txt        # 分析结构


复制
python scripts/music_analyzer.py -f song.abc         # 分析 ABC 文件
批量处理
bash
复制
python scripts/batch_processor.py -i ./songs --convert    # 批量转换
python scripts/batch_processor.py -i ./songs --transpose 2 # 批量转调
📝 ABC 记谱法示例
abc
复制
X:1
T:示例歌曲
C:AI Composer
M:4/4
L:1/4
Q:1/4=100
K:C

"C" C E G E | "G" D G B G | "Am" A c e c | "F" F A c A |
🎓 学习资源
国风音乐创作
五声音阶运用技巧
传统乐器编配指南
歌词创作与常用意象
代表曲目分析
粤语流行音乐
粤语九声六调与旋律匹配
著名词人风格分析（黄霑、林夕、黄伟文）
押韵技巧与倒音避免
粤语国风音乐创作
🤝 贡献
欢迎提交 Issue 和 Pull Request！

贡献内容
新增音乐风格
补充乐器资料
优化脚本工具
完善文档
📄 许可证
MIT License - 详见 LICENSE 文件

🙏 致谢
感谢 WorkBuddy 提供的 Skill 开发平台
感谢所有音乐理论参考资料的原创作者
感谢开源社区的支持
📮 联系我们
GitHub: @invinciblemight-li
仓库: ai-music-composer
享受音乐创作吧！ 🎵🎶   
