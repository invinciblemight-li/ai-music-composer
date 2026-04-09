# 🎵 AI Music Composer

> 一个强大的 AI 音乐创作工具，支持歌词创作、旋律生成、曲谱转换，以及 AI 人声歌曲合成。

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Instruments](https://img.shields.io/badge/Instruments-17,750+-orange.svg)](references/instruments_17000_plus.md)
[![Genres](https://img.shields.io/badge/Genres-300+-purple.svg)](references/music_genres_complete.md)

---

## ✨ 核心功能

### 1. 📝 AI 歌词创作
- 根据主题、风格、情感自动生成歌词
- 支持多种语言（中文、英文、日文等）
- 自动分段：主歌、副歌、桥段、Rap

### 2. 🎼 旋律与曲谱生成
- 自动生成旋律（ABC 记谱法）
- 导出 MIDI 文件
- 导出音频文件（WAV）
- 简谱输出

### 3. 🎤 AI 人声歌曲合成 ⭐ **新功能**
- 支持 Suno AI 生成带人声的完整歌曲
- 支持 Udio 高音质歌曲生成
- 本地 TTS 朗读（非歌声）
- 自动生成平台操作指南

### 4. 🎸 超大数据库
- **17,750+ 种乐器** - 全球最大的乐器数据库
- **300+ 音乐风格** - 覆盖全球各类音乐
- 包含中国传统乐器、世界民族乐器、电子乐器等

---

## 🚀 快速开始

### 安装

```bash
git clone https://github.com/invinciblemight-li/ai-music-composer.git
cd ai-music-composer
pip install -r requirements.txt
```

### 创作一首歌

```bash
# 启动创作工具
python scripts/compose_song.py

# 输入你的创作需求
# 例如："帮我创作一首 R&B 风格的聚会歌曲"
```

### 生成 AI 人声歌曲

```bash
# 使用 Suno 生成人声歌曲
python scripts/voice_generator.py song.txt -p suno -t "歌曲名" -s "r&b"

# 使用 Udio 生成
python scripts/voice_generator.py song.txt -p udio

# 本地 TTS 朗读
python scripts/voice_generator.py song.txt -p tts
```

---

## 📁 项目结构

```
ai-music-composer/
├── scripts/
│   ├── compose_song.py          # 歌曲创作主程序
│   ├── voice_generator.py       # AI 人声生成器 ⭐
│   ├── abc_converter.py         # ABC 记谱法转换
│   ├── midi_generator.py        # MIDI 文件生成
│   └── audio_exporter.py        # 音频导出
├── references/
│   ├── instruments_17000_plus.md    # 17,750+ 乐器数据库 ⭐
│   ├── instruments_3000_plus.md     # 3,800+ 精简版
│   ├── music_genres_complete.md     # 300+ 音乐风格
│   └── music_theory_guide.md        # 音乐理论指南
├── SKILL.md                     # 完整使用文档
├── README.md                    # 本文件
└── requirements.txt             # 依赖包
```

---

## 🎤 AI 人声功能详解

由于 Suno/Udio API 需要申请访问权限，目前采用**半自动化方案**：

### 方案一：Suno AI（推荐）

1. 访问 https://suno.com
2. 注册并登录账号
3. 使用本工具生成操作指南：
   ```bash
   python scripts/voice_generator.py your_song.txt -p suno
   ```
4. 按照指南在 Suno 上输入歌词和风格
5. 生成并下载 MP3

### 方案二：网易天音（国内可用）

1. 访问 https://tianyin.163.com
2. 使用网易云音乐账号登录
3. 点击 "AI 创作" → "一键写歌"
4. 输入歌词和风格

### 方案三：ACE Studio（专业级）

1. 下载 ACE Studio 软件
2. 导入 MIDI 文件
3. 选择 AI 歌手
4. 精细调整每个音符
5. 导出音频

---

## 🎸 乐器数据库

本项目包含全球最大的乐器数据库：

| 分类 | 数量 | 示例 |
|------|------|------|
| 弦乐器 | 800+ | 小提琴、吉他、二胡、古琴、西塔尔 |
| 管乐器 | 600+ | 长笛、萨克斯、唢呐、尺八、奈伊笛 |
| 打击乐器 | 700+ | 架子鼓、非洲鼓、编钟、塔布拉 |
| 键盘乐器 | 200+ | 钢琴、电子琴、手风琴、管风琴 |
| 电子乐器 | 400+ | 合成器、鼓机、采样器、MIDI 控制器 |
| 民族乐器 | 2,500+ | 全球各民族传统乐器 |
| 古代乐器 | 400+ | 古希腊、中世纪、中国古代乐器 |
| **总计** | **17,750+** | |

---

## 🎼 音乐风格

支持 300+ 种音乐风格：

- **西方流行**：Pop, Rock, Electronic, Hip-Hop, R&B, Jazz, Blues, Country, Folk, Reggae, Latin, Classical
- **世界音乐**：非洲、凯尔特、中东、印度、亚洲、加勒比
- **中国音乐**：传统民乐、现代流行、少数民族音乐
- **实验音乐**：先锋、噪音、氛围、极简主义

---

## 🌟 实战案例

### 《今晚不回家》- R&B 派对歌曲

**提示词**：
```
帮我创作一首聚会时的 R&B 风格歌曲
```

**生成内容**：
- ✅ 完整歌词（主歌、副歌、桥段、Rap）
- ✅ ABC 记谱法
- ✅ MIDI 文件
- ✅ WAV 音频
- ✅ Suno 人声生成指南

**歌词节选**：
```
今晚不回家 一起跳舞吧
让节奏带着我们飞呀飞呀
今晚不回家 忘掉那牵挂
在这舞池中央绽放最耀眼光华
```

---

## 🤝 参与开发

我们欢迎所有对 AI 音乐创作感兴趣的开发者加入！

### 🎯 当前开发重点

#### 1. AI 人声唱歌功能 ⭐ **急需帮助**

**目标**：实现真正的 AI 人声歌曲合成，而不仅仅是朗读

**待解决问题**：
- [ ] Suno API 自动化调用（需要 API Key）
- [ ] 本地 AI 歌声合成模型集成
- [ ] 支持更多中文 AI 歌声平台
- [ ] 歌声情感控制（欢快、悲伤、激昂等）
- [ ] 多声部合唱生成

**技术方向**：
- 研究 DiffSinger、VITS 等开源歌声合成模型
- 探索 ACE Studio、X Studio 等工具的自动化
- 集成网易天音、腾讯音乐等国内平台 API

#### 2. 乐器数据库扩展

- [ ] 添加乐器音频样本
- [ ] 添加乐器图片和详细介绍
- [ ] 按地区/文化分类浏览

#### 3. 曲谱功能增强

- [ ] 五线谱生成
- [ ] 吉他谱/尤克里里谱
- [ ] 和弦谱自动生成
- [ ] 乐谱 PDF 导出

#### 4. 其他功能

- [ ] Web 界面（Gradio/Streamlit）
- [ ] 批量歌曲生成
- [ ] 歌曲风格迁移
- [ ] 歌词翻译功能

### 💡 如何贡献

1. **Fork** 本仓库
2. 创建你的功能分支：`git checkout -b feature/amazing-feature`
3. 提交更改：`git commit -m 'Add amazing feature'`
4. 推送分支：`git push origin feature/amazing-feature`
5. 创建 **Pull Request**

### 📞 联系我们

- 提交 Issue：https://github.com/invinciblemight-li/ai-music-composer/issues
- 讨论区：https://github.com/invinciblemight-li/ai-music-composer/discussions

---

## 📄 许可证

本项目采用 [MIT](LICENSE) 许可证。

---

## 🙏 致谢

- 乐器数据来源：[DataSN.io](https://datasn.io)
- 音乐理论参考：[All the Musical Instruments of the World](https://www.allthemusicalinstrumentsoftheworld.com/)
- AI 歌声合成：Suno, Udio, 网易天音, ACE Studio

---

## 🎵 让每个人都能创作音乐

> "不会音乐也能写歌" —— 这是我们的初心。

无论你是专业音乐人还是业余爱好者，AI Music Composer 都能帮助你实现音乐创作梦想。

**快来加入我们，一起打造最强大的 AI 音乐创作工具！** 🚀

---

<p align="center">
  ⭐ Star 本项目，支持我们继续开发！
</p>
