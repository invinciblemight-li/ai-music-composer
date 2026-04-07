---
name: ai-music-composer
description: |
  AI音乐创作与曲谱生成工具。当用户需要：
  1. 创作原创歌曲（歌词+旋律）
  2. 将音乐转换为曲谱（五线谱/简谱/ABC记谱法）
  3. 提取或生成音乐符号表示
  4. 将歌词配上旋律
  时使用此 Skill。
  
  触发词：创作歌曲、生成曲谱、提取乐谱、谱写音乐、音乐转谱、作曲
---

# AI 音乐创作与曲谱生成

此 Skill 提供完整的 AI 音乐创作工作流，从创意生成到可演奏的曲谱输出。

## 核心功能

### 1. 歌曲创作
- 根据主题、情感、风格生成原创歌词
- 为歌词配上旋律（音高+节奏）
- 支持多种音乐风格：流行、民谣、古典、摇滚、电子等

### 2. 曲谱格式支持
- **ABC 记谱法**：文本格式，易于分享和编辑
- **简谱**：数字记谱，适合中文用户
- **MIDI**：可播放的数字音乐文件
- **MusicXML**：专业音乐软件兼容格式

### 3. 曲谱提取与转换
- 将音乐描述转换为标准记谱
- 支持旋律提取和和弦标注
- 生成多声部乐谱

## 使用流程

### 场景 A：从零创作歌曲

1. **收集需求**
   - 歌曲主题/情感
   - 目标风格（流行/民谣/古典等）
   - 时长/结构（verse-chorus-bridge 等）
   - 调性偏好（C大调、A小调等）

2. **生成歌词**
   - 根据主题创作歌词
   - 设计韵律结构
   - 分段标注（主歌/副歌/桥段）

3. **谱写旋律**
   - 为每段歌词配上旋律
   - 标注音高（如 C4, E4, G4）
   - 标注节奏（四分音符、八分音符等）
   - 添加和弦进行

4. **生成曲谱**
   - 使用 `scripts/generate_sheet_music.py` 生成标准曲谱
   - 输出 ABC 记谱法文本
   - 可选：生成简谱表示

5. **输出交付**
   - 提供完整歌词
   - 提供 ABC 记谱法文本
   - 提供简谱表示
   - 提供音乐结构说明

### 场景 B：将现有歌词谱曲

1. **分析歌词结构**
   - 识别段落（主歌/副歌）
   - 确定每行音节数
   - 标记韵脚位置

2. **设计旋律**
   - 根据情感选择调性
   - 为每行设计旋律线
   - 确保旋律与歌词重音匹配

3. **生成曲谱**（同上）

### 场景 C：提取/转换曲谱

1. **解析输入**
   - 如果是音乐描述，提取音高和节奏信息
   - 如果是现有记谱，识别格式

2. **转换格式**
   - 使用脚本转换为 ABC 记谱法
   - 生成简谱表示

3. **验证输出**
   - 检查记谱法语法
   - 确保可播放性

## ABC 记谱法规范

ABC 记谱法是文本格式的音乐记谱标准，格式如下：

```abc
X:1
T:歌曲标题
C:作曲者
M:4/4
L:1/4
K:C

% 旋律部分
C D E F | G A B c | c B A G | F E D C |
```

### 头部字段说明
- `X:` - 参考编号
- `T:` - 标题
- `C:` - 作曲者
- `M:` - 拍号（如 4/4, 3/4, 6/8）
- `L:` - 默认音符长度（如 1/4 = 四分音符）
- `K:` - 调号（如 C, G, Dm, Am）
- `Q:` - 速度（如 1/4=120）

### 音符表示
- 音高：`C, D, E, F, G, A, B`（低音），`C D E F G A B`（中音），`c d e f g a b`（高音）
- 升号：`^C`，降号：`_C`，还原：`=C`
- 音符长度：`C`（默认），`C2`（双倍），`C/2`（一半），`C3/2`（附点）
- 休止符：`z`

### 常用节奏
- 四分音符：`C`
- 八分音符：`C/2` 或 `C`（当 L:1/8 时）
- 十六分音符：`C/4`
- 附点音符：`C3/2`

### 小节与小节线
- `|` - 小节线
- `||` - 双小节线（段落结束）
- `|:` 和 `:|` - 重复记号

## 简谱规范

简谱使用数字 1-7 表示音阶：

```
1 2 3 4 5 6 7
Do Re Mi Fa Sol La Si
```

### 音高表示
- 低音：数字下加点（如 ̣1 ̣2 ̣3）
- 中音：纯数字（1 2 3）
- 高音：数字上加点（如 1̇ 2̇ 3̇）

### 节奏表示
- 全音符：5 - - -
- 二分音符：5 -
- 四分音符：5
- 八分音符：5̲（下划线）
- 十六分音符：5̲̲（双下划线）
- 附点音符：5.

### 示例
```
1 2 3 4 | 5 5 6 5 | 4 3 2 1 |
```

## 参考资料

### 核心参考资料
- **和弦进行**: `references/chord_progressions.md` - 15+ 种常用和弦进行
- **音乐风格**: `references/music_styles.md` - 流行、民谣、摇滚等风格指南
- **音乐理论**: `references/music_theory.md` - 音阶、和弦、曲式等理论基础

### 完整数据库（新增）
- **全球音乐风格大全**: `references/music_genres_complete.md` - 300+ 种音乐风格
  - 西方流行音乐（Pop, Rock, Electronic, Hip-Hop, R&B, Jazz, Blues, Country, Folk, Reggae, Latin, Classical等）
  - 世界音乐（非洲、凯尔特、中东、印度、亚洲、加勒比等）
  - 中国音乐（传统、现代流行、少数民族）
  - 日本/韩国音乐
  - 实验/先锋音乐

- **全球乐器大全**: `references/instruments_complete.md` - 500+ 种乐器
  - 弦乐器（弓弦、拨弦、击弦）
  - 管乐器（木管、铜管）
  - 打击乐器（体鸣、膜鸣）
  - 键盘乐器
  - 电子乐器
  - 声乐
  - 古代/历史乐器

### 特色风格指南（新增）
- **中国国风音乐创作指南**: `references/guofeng_guide.md` - 国风音乐完整创作手册
  - 古风流行、仙侠风、戏曲流行、宫廷风、新国风等8大子类型
  - 五声音阶运用、传统乐器编配
  - 歌词创作技巧、常用意象
  - 代表曲目分析、制作流程

- **粤语流行音乐创作指南**: `references/cantopop_guide.md` - 粤语歌完整创作手册
  - 粤语九声六调与旋律匹配
  - 经典粤语流行、情歌、摇滚、说唱等8大风格
  - 著名词人风格（黄霑、林夕、黄伟文等）
  - 押韵技巧、倒音避免
  - 粤语国风音乐创作

## 高级功能

### MIDI 生成

将 ABC 记谱法转换为可播放的 MIDI 文件：

```bash
python scripts/midi_generator.py song.abc -o output.mid -t 120
```

### 歌词创作辅助

检查韵律、音节数、押韵词推荐：

```bash
# 计算音节数
python scripts/lyrics_helper.py -c "歌词文本"

# 查找押韵词
python scripts/lyrics_helper.py -r "爱"

# 分析歌词结构
python scripts/lyrics_helper.py -a lyrics.txt
```

### 音乐分析

分析旋律、和弦进行、曲式结构：

```bash
python scripts/music_analyzer.py -f song.abc
```

### 批量处理

批量转换、转调、导出：

```bash
# 批量转换 ABC 到 MIDI
python scripts/batch_processor.py -i ./songs -o ./output --convert

# 批量转调（升调 2 个半音）
python scripts/batch_processor.py -i ./songs --transpose 2

# 批量导出多种格式
python scripts/batch_processor.py -i ./songs --export midi,jianpu
```

### 歌曲模板

使用预定义的歌曲结构模板：`assets/song_templates.json`

包含 8 种模板：
- 标准流行歌曲
- 民谣叙事
- 摇滚劲歌
- 抒情 ballad
- 十二小节蓝调
- ABABCB 现代流行
- 中国风
- 舞曲电子

## 脚本使用

### 生成曲谱

```bash
python scripts/generate_sheet_music.py \
  --title "歌曲名" \
  --composer "作曲者" \
  --key "C" \
  --time-signature "4/4" \
  --tempo "120" \
  --melody "C D E F G A B c" \
  --chords "C G Am F" \
  --output-format abc
```

### 转换为简谱

```bash
python scripts/generate_sheet_music.py \
  --input-abc "song.abc" \
  --output-format jianpu
```

### 生成 MIDI

```bash
python scripts/midi_generator.py song.abc -o output.mid -t 120
```

### 歌词辅助

```bash
python scripts/lyrics_helper.py -c "歌词文本"        # 计算音节
python scripts/lyrics_helper.py -r "爱"              # 查找押韵词
python scripts/lyrics_helper.py -a lyrics.txt        # 分析结构
```

### 音乐分析

```bash
python scripts/music_analyzer.py -f song.abc         # 分析 ABC 文件
```

### 批量处理

```bash
python scripts/batch_processor.py -i ./songs --convert
python scripts/batch_processor.py -i ./songs --transpose 2
```

## 输出示例

### 完整歌曲交付物

```markdown
# 《示例歌曲》

**作曲**：AI Composer
**调性**：C大调
**拍号**：4/4
**速度**：100 BPM

## 歌词

**[主歌 1]**
示例歌词第一行
示例歌词第二行

**[副歌]**
示例副歌第一行
示例副歌第二行

## ABC 记谱法

```abc
X:1
T:示例歌曲
C:AI Composer
M:4/4
L:1/4
Q:1/4=100
K:C
"C" C E G E | "G" D G B G | "Am" A c e c | "F" F A c A |
```

## 简谱

```
1 3 5 3 | 2 5 7̇ 5 | 6 1̇ 3̇ 1̇ | 4 6 1̇ 6 |
```

## 和弦进行

- 主歌：C - G - Am - F
- 副歌：F - G - C - Am
```

## 注意事项

1. **音域考虑**：确保旋律在人声舒适音域内（通常 C3-C5）
2. **节奏匹配**：旋律节奏应与歌词自然重音匹配
3. **和弦简化**：初学者歌曲使用简单三和弦
4. **可演奏性**：生成的曲谱应能在常见工具中播放（如 EasyABC, MuseScore）
5. **版权说明**：AI 生成的音乐可能涉及版权问题，建议用于学习和个人创作参考

## 相关工具推荐

- **ABC 播放器**：EasyABC, ABCjs
- **乐谱软件**：MuseScore, LilyPond
- **在线转换**：abcnotation.com
- **简谱软件**：JP-Word, 谱谱风
