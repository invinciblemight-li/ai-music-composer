# AI Music Composer Skill

AI音乐创作与曲谱生成工具 - 为 WorkBuddy 开发的 Skill，实现 AI 创作歌曲并提取完整曲谱。

## 功能特性

- 🎵 **AI 歌曲创作** - 根据主题、情感、风格生成原创歌词和旋律
- 🎼 **多格式曲谱支持** - ABC 记谱法、简谱、MIDI、MusicXML
- 🎸 **和弦进行推荐** - 内置 15+ 种常用和弦进行
- 🎹 **音乐风格指南** - 300+ 种全球音乐风格
- 🏮 **国风音乐支持** - 古风、仙侠、戏曲、宫廷等中国风格
- 🎤 **粤语音乐支持** - 粤语流行、情歌、摇滚等完整指南
- 🎼 **乐器数据库** - 500+ 种全球乐器资料
- 📝 **完整工作流** - 从创意到可演奏曲谱的一站式解决方案
- 🔧 **高级工具** - MIDI生成、歌词辅助、音乐分析、批量处理

## 触发词

当用户说出以下关键词时，Skill 会被激活：
- "创作歌曲"
- "生成曲谱"
- "提取乐谱"
- "谱写音乐"
- "音乐转谱"
- "作曲"

## 安装方法

### 方法 1：通过 zip 文件安装
1. 下载 `ai-music-composer.zip`
2. 解压到 WorkBuddy 的 skills 目录：
   ```
   ~/.workbuddy/skills/ai-music-composer/
   ```

### 方法 2：直接使用
将本文件夹复制到：
```
~/.workbuddy/skills/ai-music-composer/
```

## 目录结构

```
ai-music-composer/
├── SKILL.md                    # Skill 核心说明文档
├── README.md                   # 本文件
├── LICENSE                     # MIT 许可证
├── .gitignore                  # Git 忽略配置
├── scripts/
│   ├── generate_sheet_music.py # 曲谱生成脚本
│   ├── midi_generator.py       # MIDI 生成器
│   ├── lyrics_helper.py        # 歌词创作辅助
│   ├── music_analyzer.py       # 音乐分析工具
│   └── batch_processor.py      # 批量处理工具
├── references/
│   ├── chord_progressions.md   # 常用和弦进行参考
│   ├── music_styles.md         # 音乐风格指南
│   ├── music_theory.md         # 音乐理论基础
│   ├── music_genres_complete.md    # 全球音乐风格大全（300+ 种）
│   ├── instruments_complete.md     # 全球乐器大全（500+ 种）
│   ├── guofeng_guide.md        # 中国国风音乐创作指南 ⭐
│   └── cantopop_guide.md       # 粤语流行音乐创作指南 ⭐
└── assets/
    ├── example_song.abc        # 示例歌曲
    ├── template.abc            # 曲谱模板
    └── song_templates.json     # 歌曲结构模板
```

## 使用示例

### 示例 1：创作一首关于青春的歌曲

**用户**: "帮我创作一首青春无悔的歌"

**AI 输出**:
- 完整歌词（主歌、导歌、副歌、桥段）
- ABC 记谱法
- 简谱
- 和弦进行建议

### 示例 2：生成曲谱

```bash
python scripts/generate_sheet_music.py \
  --title "示例歌曲" \
  --composer "AI Composer" \
  --key "G" \
  --time-signature "4/4" \
  --tempo 108 \
  --melody "G A B d d c B A" \
  --chords "G D Em C" \
  --output-format abc
```

## 支持的曲谱格式

### ABC 记谱法
文本格式的音乐记谱标准，易于分享和编辑。

```abc
X:1
T:示例歌曲
C:AI Composer
M:4/4
L:1/4
K:G
"G" G A B d | "D" d c B A |
```

### 简谱
数字记谱法，适合中文用户。

```
5 6 7̇ 2̇ | 2̇ 1̇ 7 6 |
```

## 音乐风格支持

### 全球风格（300+ 种）
- **流行 (Pop)** - 旋律流畅，节奏明快
- **民谣 (Folk)** - 叙事性强，易于传唱
- **摇滚 (Rock)** - 力量感强，强调反拍
- **古典 (Classical)** - 结构严谨，技巧丰富
- **爵士 (Jazz)** - 即兴演奏，切分音丰富
- **电子 (Electronic)** - 重复 Loop，极简主义
- **嘻哈 (Hip-Hop)** - 说唱、节奏驱动
- **R&B/Soul** - 灵魂乐、节奏布鲁斯
- **世界音乐** - 非洲、凯尔特、中东、印度等

### 中国国风音乐（8大子类型）
- **古风流行** - 古典诗词风格，五声音阶
- **仙侠风** - 武侠仙侠题材，飘逸旋律
- **戏曲流行** - 京剧/昆曲元素，戏腔唱法
- **宫廷风** - 雅乐音阶，庄重典雅
- **新国风** - 电子+传统，年轻化
- **国风摇滚** - 热血激昂，电吉他+传统乐器
- **国风电子** - 合成器演奏民族旋律
- **国风说唱** - 文言文+现代说唱

### 粤语流行音乐（8大风格）
- **经典粤语流行** - 80-90年代经典风格
- **粤语情歌** - 深情细腻，钢琴弦乐为主
- **粤语快歌/舞曲** - 节奏明快，电子元素
- **粤语摇滚** - Beyond风格，热血励志
- **粤语说唱** - 粤语九声韵律，独特 flow
- **粤语R&B** - 转音滑音，现代R&B
- **港式民谣** - 城市民谣，叙事性强
- **TVB剧集歌** - 电视剧主题曲风格

详见 `references/guofeng_guide.md` 和 `references/cantopop_guide.md`

## 常用和弦进行

### 万能进行
- **C大调**: C - G - Am - F
- **G大调**: G - D - Em - C

### 50年代进行
- **C大调**: C - Am - Dm - G

### 爵士标准
- **C大调**: Dm7 - G7 - Cmaj7

更多和弦进行请参考 `references/chord_progressions.md`

## 相关工具推荐

- **ABC 播放器**: [EasyABC](https://easyabc.sourceforge.net/), [ABCjs](https://abcjs.net/)
- **乐谱软件**: [MuseScore](https://musescore.org/), [LilyPond](https://lilypond.org/)
- **在线转换**: [abcnotation.com](https://abcnotation.com/)
- **简谱软件**: JP-Word, 谱谱风

## 技术说明

### 曲谱生成脚本

`scripts/generate_sheet_music.py` 支持以下功能：
- 解析旋律字符串
- 解析和弦进行
- 自动分组为小节
- 生成 ABC 记谱法
- 生成简谱

### 音符表示

**ABC 记谱法**:
- `C, D, E` - 低音
- `C D E` - 中音
- `c d e` - 高音
- `C2` - 二分音符
- `C/2` - 八分音符

**简谱**:
- `1 2 3 4 5 6 7` - 中音
- `̣1 ̣2 ̣3` - 低音（下方加点）
- `1̇ 2̇ 3̇` - 高音（上方加点）

## 注意事项

1. **音域考虑**: 确保旋律在人声舒适音域内（通常 C3-C5）
2. **节奏匹配**: 旋律节奏应与歌词自然重音匹配
3. **和弦简化**: 初学者歌曲使用简单三和弦
4. **可演奏性**: 生成的曲谱应能在常见工具中播放
5. **版权说明**: AI 生成的音乐可能涉及版权问题，建议用于学习和个人创作参考

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT License - 详见 LICENSE 文件

## 作者

AI Composer Team

---

**Enjoy making music!** 🎵
