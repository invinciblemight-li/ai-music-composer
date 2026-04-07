#!/usr/bin/env python3
"""
歌词创作辅助工具
提供韵律检查、音节计数、押韵词推荐等功能
"""

import argparse
import re
from typing import List, Tuple, Dict
from dataclasses import dataclass
from collections import defaultdict


@dataclass
class RhymeInfo:
    """押韵信息"""
    word: str
    rhyme_part: str
    tone: str  # 平仄


class LyricsHelper:
    """歌词创作助手"""
    
    # 汉语拼音韵母表（简化版）
    RHYME_TABLE = {
        # 单韵母
        'a': 'a', 'o': 'o', 'e': 'e', 'i': 'i', 'u': 'u', 'ü': 'ü',
        # 复韵母
        'ai': 'ai', 'ei': 'ei', 'ao': 'ao', 'ou': 'ou',
        'ia': 'ia', 'ie': 'ie', 'iao': 'iao', 'iu': 'iu',
        'ua': 'ua', 'uo': 'uo', 'uai': 'uai', 'ui': 'ui',
        'üe': 'üe',
        # 鼻韵母
        'an': 'an', 'en': 'en', 'in': 'in', 'un': 'un', 'ün': 'ün',
        'ang': 'ang', 'eng': 'eng', 'ing': 'ing', 'ong': 'ong',
        'ian': 'ian', 'uan': 'uan', 'üan': 'üan', 'uen': 'uen',
        'iang': 'iang', 'uang': 'uang', 'ueng': 'ueng', 'iong': 'iong',
    }
    
    # 常见押韵词库（简化示例）
    RHYME_WORDS = {
        'ang': ['光', '阳', '方', '长', '想', '唱', '望', '伤', '上', '让'],
        'an': ['天', '边', '年', '前', '见', '面', '言', '远', '愿', '念'],
        'ai': ['爱', '来', '在', '开', '海', '彩', '怀', '待', '改', '哀'],
        'ao': ['好', '笑', '道', '到', '老', '少', '早', '跑', '抱', '高'],
        'ou': ['有', '友', '走', '手', '头', '后', '由', '游', '忧', '柔'],
        'i': ['你', '我', '的', '里', '起', '去', '意', '离', '记', '期'],
        'o': ['多', '说', '过', '错', '落', '火', '果', '波', '歌', '和'],
        'e': ['的', '了', '着', '得', '歌', '河', '车', '色', '热', '乐'],
        'ing': ['情', '心', '听', '行', '明', '星', '影', '静', '境', '应'],
        'ong': ['中', '梦', '风', '空', '同', '动', '送', '痛', '懂', '红'],
    }
    
    def __init__(self):
        self.pinyin_dict = self._load_pinyin_dict()
    
    def _load_pinyin_dict(self) -> Dict[str, str]:
        """加载拼音字典（简化版）"""
        # 实际应用中应该加载完整的拼音字典
        return {
            '春': 'chun', '夏': 'xia', '秋': 'qiu', '冬': 'dong',
            '风': 'feng', '雨': 'yu', '雪': 'xue', '花': 'hua',
            '月': 'yue', '星': 'xing', '天': 'tian', '地': 'di',
            '山': 'shan', '水': 'shui', '云': 'yun', '梦': 'meng',
            '心': 'xin', '情': 'qing', '爱': 'ai', '想': 'xiang',
            '你': 'ni', '我': 'wo', '他': 'ta', '的': 'de',
            '了': 'le', '在': 'zai', '是': 'shi', '有': 'you',
            '大': 'da', '小': 'xiao', '好': 'hao', '来': 'lai',
            '去': 'qu', '上': 'shang', '下': 'xia', '前': 'qian',
            '后': 'hou', '左': 'zuo', '右': 'you', '中': 'zhong',
            '年': 'nian', '月': 'yue', '日': 'ri', '时': 'shi',
            '光': 'guang', '明': 'ming', '暗': 'an', '长': 'chang',
            '短': 'duan', '高': 'gao', '低': 'di', '远': 'yuan',
            '近': 'jin', '快': 'kuai', '慢': 'man', '新': 'xin',
            '旧': 'jiu', '美': 'mei', '丑': 'chou', '真': 'zhen',
            '假': 'jia', '对': 'dui', '错': 'cuo', '多': 'duo',
            '少': 'shao', '轻': 'qing', '重': 'zhong', '冷': 'leng',
            '热': 're', '深': 'shen', '浅': 'qian', '清': 'qing',
            '浊': 'zhuo', '静': 'jing', '动': 'dong', '开': 'kai',
            '关': 'guan', '生': 'sheng', '死': 'si', '老': 'lao',
            '少': 'shao', '男': 'nan', '女': 'nv', '父': 'fu',
            '母': 'mu', '子': 'zi', '女': 'nv', '兄': 'xiong',
            '弟': 'di', '姐': 'jie', '妹': 'mei', '友': 'you',
            '师': 'shi', '生': 'sheng', '人': 'ren', '民': 'min',
            '国': 'guo', '家': 'jia', '城': 'cheng', '乡': 'xiang',
            '路': 'lu', '街': 'jie', '门': 'men', '窗': 'chuang',
            '房': 'fang', '屋': 'wu', '楼': 'lou', '桥': 'qiao',
            '河': 'he', '江': 'jiang', '湖': 'hu', '海': 'hai',
            '洋': 'yang', '林': 'lin', '木': 'mu', '草': 'cao',
            '树': 'shu', '叶': 'ye', '根': 'gen', '枝': 'zhi',
            '果': 'guo', '实': 'shi', '种': 'zhong', '子': 'zi',
            '鸟': 'niao', '兽': 'shou', '鱼': 'yu', '虫': 'chong',
            '马': 'ma', '牛': 'niu', '羊': 'yang', '鸡': 'ji',
            '狗': 'gou', '猪': 'zhu', '猫': 'mao', '兔': 'tu',
            '龙': 'long', '凤': 'feng', '虎': 'hu', '狼': 'lang',
            '熊': 'xiong', '鹿': 'lu', '鹤': 'he', '燕': 'yan',
            '雀': 'que', '鸦': 'ya', '鸥': 'ou', '雁': 'yan',
            '琴': 'qin', '棋': 'qi', '书': 'shu', '画': 'hua',
            '诗': 'shi', '歌': 'ge', '舞': 'wu', '曲': 'qu',
            '戏': 'xi', '剧': 'ju', '影': 'ying', '视': 'shi',
            '音': 'yin', '乐': 'le', '声': 'sheng', '色': 'se',
            '香': 'xiang', '味': 'wei', '触': 'chu', '法': 'fa',
            '眼': 'yan', '耳': 'er', '鼻': 'bi', '舌': 'she',
            '身': 'shen', '意': 'yi', '喜': 'xi', '怒': 'nu',
            '哀': 'ai', '乐': 'le', '爱': 'ai', '恶': 'wu',
            '欲': 'yu', '贪': 'tan', '嗔': 'chen', '痴': 'chi',
            '慢': 'man', '疑': 'yi', '见': 'jian', '思': 'si',
            '念': 'nian', '想': 'xiang', '忆': 'yi', '忘': 'wang',
            '知': 'zhi', '觉': 'jue', '感': 'gan', '受': 'shou',
            '行': 'xing', '动': 'dong', '作': 'zuo', '为': 'wei',
            '成': 'cheng', '败': 'bai', '得': 'de', '失': 'shi',
            '利': 'li', '害': 'hai', '益': 'yi', '损': 'sun',
            '福': 'fu', '祸': 'huo', '吉': 'ji', '凶': 'xiong',
            '祥': 'xiang', '瑞': 'rui', '庆': 'qing', '贺': 'he',
            '祝': 'zhu', '愿': 'yuan', '祈': 'qi', '祷': 'dao',
            '求': 'qiu', '索': 'suo', '寻': 'xun', '觅': 'mi',
            '追': 'zhui', '赶': 'gan', '逃': 'tao', '避': 'bi',
            '躲': 'duo', '藏': 'cang', '匿': 'ni', '隐': 'yin',
            '现': 'xian', '露': 'lu', '显': 'xian', '示': 'shi',
            '表': 'biao', '达': 'da', '说': 'shuo', '话': 'hua',
            '讲': 'jiang', '谈': 'tan', '论': 'lun', '议': 'yi',
            '评': 'ping', '判': 'pan', '断': 'duan', '决': 'jue',
            '定': 'ding', '决': 'jue', '心': 'xin', '信': 'xin',
            '念': 'nian', '仰': 'yang', '望': 'wang', '期': 'qi',
            '待': 'dai', '等': 'deng', '候': 'hou', '望': 'wang',
        }
    
    def count_syllables(self, text: str) -> int:
        """计算音节数（汉字字数）"""
        # 移除标点符号
        text = re.sub(r'[^\u4e00-\u9fa5]', '', text)
        return len(text)
    
    def analyze_rhyme(self, text: str) -> List[RhymeInfo]:
        """分析文本的押韵情况"""
        lines = text.strip().split('\n')
        rhyme_infos = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # 获取每行最后一个字
            last_char = line[-1]
            if last_char in self.pinyin_dict:
                pinyin = self.pinyin_dict[last_char]
                rhyme_part = self._extract_rhyme(pinyin)
                tone = self._get_tone(pinyin)
                rhyme_infos.append(RhymeInfo(last_char, rhyme_part, tone))
        
        return rhyme_infos
    
    def _extract_rhyme(self, pinyin: str) -> str:
        """提取韵母"""
        # 简化的韵母提取
        for rhyme in sorted(self.RHYME_TABLE.keys(), key=len, reverse=True):
            if pinyin.endswith(rhyme):
                return self.RHYME_TABLE[rhyme]
        return pinyin[-1] if pinyin else ''
    
    def _get_tone(self, pinyin: str) -> str:
        """获取声调（简化版）"""
        # 实际应该根据拼音的声调标记判断
        # 这里简化为随机返回
        import random
        return random.choice(['平', '上', '去', '入'])
    
    def find_rhyme_words(self, char: str, max_results: int = 10) -> List[str]:
        """查找押韵词"""
        if char not in self.pinyin_dict:
            return []
        
        pinyin = self.pinyin_dict[char]
        rhyme = self._extract_rhyme(pinyin)
        
        return self.RHYME_WORDS.get(rhyme, [])[:max_results]
    
    def check_structure(self, lyrics: str) -> Dict:
        """检查歌词结构"""
        lines = [line.strip() for line in lyrics.strip().split('\n') if line.strip()]
        
        analysis = {
            'total_lines': len(lines),
            'syllables_per_line': [self.count_syllables(line) for line in lines],
            'rhyme_scheme': [],
            'suggestions': []
        }
        
        # 分析押韵
        rhyme_infos = self.analyze_rhyme(lyrics)
        if len(rhyme_infos) >= 2:
            # 检查是否押韵
            for i in range(len(rhyme_infos) - 1):
                if rhyme_infos[i].rhyme_part == rhyme_infos[i+1].rhyme_part:
                    analysis['rhyme_scheme'].append(f'行{i+1}和行{i+2}押韵')
        
        # 检查音节数一致性
        syllable_counts = analysis['syllables_per_line']
        if len(set(syllable_counts)) > 1:
            analysis['suggestions'].append('建议保持每行字数一致，增强节奏感')
        
        return analysis
    
    def suggest_lyrics(self, theme: str, style: str = '流行', lines: int = 4) -> str:
        """根据主题生成歌词建议"""
        # 主题词库
        theme_words = {
            '青春': ['梦想', '热血', '奋斗', '未来', '希望', '阳光', '汗水', '笑容'],
            '爱情': ['心动', '思念', '温柔', '甜蜜', '陪伴', '永远', '珍惜', '守候'],
            '友情': ['兄弟', '姐妹', '一起', '永远', '不离', '不弃', '陪伴', '同行'],
            '梦想': ['远方', '飞翔', '追逐', '坚持', '努力', '成功', '光芒', '辉煌'],
            '离别': ['再见', '珍重', '回忆', '思念', '远方', '祝福', '不舍', '眼泪'],
            '思念': ['远方', '夜空', '星光', '月亮', '风儿', '云儿', '心上', '梦里'],
        }
        
        words = theme_words.get(theme, ['美好', '幸福', '快乐', '希望'])
        
        # 简单的歌词模板
        templates = [
            f"{words[0]}在{words[1]}中{words[2]}",
            f"{words[3]}的{words[4]}永不{words[5]}",
            f"让{words[6]}带着{words[7]}飞翔",
            f"{words[0]}是我们最美的{words[1]}",
        ]
        
        return '\n'.join(templates[:lines])
    
    def format_lyrics(self, lyrics: str, section_type: str = 'verse') -> str:
        """格式化歌词，添加段落标记"""
        sections = {
            'verse': '[主歌]',
            'pre_chorus': '[导歌]',
            'chorus': '[副歌]',
            'bridge': '[桥段]',
            'outro': '[尾奏]',
        }
        
        header = sections.get(section_type, '')
        if header:
            return f"{header}\n{lyrics}"
        return lyrics


def main():
    parser = argparse.ArgumentParser(description='歌词创作辅助工具')
    parser.add_argument('-c', '--count', help='计算音节数', metavar='TEXT')
    parser.add_argument('-r', '--rhyme', help='查找押韵词', metavar='CHAR')
    parser.add_argument('-a', '--analyze', help='分析歌词文件', metavar='FILE')
    parser.add_argument('-s', '--suggest', help='生成歌词建议', metavar='THEME')
    parser.add_argument('-f', '--format', help='格式化歌词文件', metavar='FILE')
    
    args = parser.parse_args()
    
    helper = LyricsHelper()
    
    if args.count:
        count = helper.count_syllables(args.count)
        print(f"音节数: {count}")
    
    if args.rhyme:
        words = helper.find_rhyme_words(args.rhyme)
        print(f"与 '{args.rhyme}' 押韵的词: {', '.join(words)}")
    
    if args.analyze:
        with open(args.analyze, 'r', encoding='utf-8') as f:
            lyrics = f.read()
        analysis = helper.check_structure(lyrics)
        print(f"总行数: {analysis['total_lines']}")
        print(f"每行字数: {analysis['syllables_per_line']}")
        print(f"押韵情况: {analysis['rhyme_scheme']}")
        if analysis['suggestions']:
            print(f"建议: {analysis['suggestions']}")
    
    if args.suggest:
        suggestion = helper.suggest_lyrics(args.suggest)
        print(f"主题 '{args.suggest}' 的歌词建议:")
        print(suggestion)
    
    if args.format:
        with open(args.format, 'r', encoding='utf-8') as f:
            lyrics = f.read()
        formatted = helper.format_lyrics(lyrics, 'verse')
        print(formatted)


if __name__ == '__main__':
    main()
