# -*- coding=utf8 -*-
"""
    获取HMM模型
"""
import sys
sys.path.append(r'./')    #要用绝对路径
from math import log
import sqlite3
from pypinyin import pinyin, NORMAL
from pinyin.model import (
    Transition,
    Emission,
    Starting,
    init_hmm_tables,
    HMMSession
)
from pinyin.utils import iter_dict


def init_start():
    """
    初始化起始概率
    """
    print("Training start probablity matrix.")
    freq_map = {}
    total_count = 0
    for phrase, frequency,_ in iter_dict():
        total_count += frequency
        freq_map[phrase[0]] = freq_map.get(phrase[0], 0) + frequency

    # for character, frequency in freq_map.items():
    #     Starting.add(character, log(frequency / total_count))
    conn = sqlite3.connect('./pinyin/model/hmm.sqlite')
    cur = conn.cursor()
    sql = 'INSERT INTO starting (character, probability ) VALUES (?,?);'
    data = []
    for character, frequency in freq_map.items():
        data.append((character, log(frequency / total_count)))
    sql = sql[:-1] + ';'
    cur.executemany(sql, data)
    conn.commit()
    conn.close()
    # with open('start_p.txt', 'w', encoding='utf-8') as f:
    #     for character, frequency in freq_map.items():
    #         f.write("%s: %s\n"%(character, log(frequency / total_count)))

def init_emission():
    """
    初始化发射概率
    """
    print("Training emission probablity matrix.")
    character_pinyin_map = {}
    for phrase, frequency, pinyinList in iter_dict():
        pinyins = [[py] for py in pinyinList]#pinyin(phrase, style=NORMAL)
        for character, py in zip(phrase, pinyins):
            character_pinyin_count = len(py)
            if character not in character_pinyin_map:
                character_pinyin_map[character] = \
                    {x: frequency/character_pinyin_count for x in py}
            else:
                pinyin_freq_map = character_pinyin_map[character]
                for x in py:
                    pinyin_freq_map[x] = pinyin_freq_map.get(x, 0) + \
                                         frequency/character_pinyin_count

    # for character, pinyin_map in character_pinyin_map.items():
    #     sum_frequency = sum(pinyin_map.values())
    #     for py, frequency in pinyin_map.items():
    #         Emission.add(character, py, log(frequency/sum_frequency))
    conn = sqlite3.connect('./pinyin/model/hmm.sqlite')
    cur = conn.cursor()
    sql = 'INSERT INTO emission (character, pinyin,probability ) VALUES (?,?,?);'
    data = []
    for character, pinyin_map in character_pinyin_map.items():
        sum_frequency = sum(pinyin_map.values())
        for py, frequency in pinyin_map.items():
            data.append((character, py,log(frequency / sum_frequency)))
    sql = sql[:-1] + ';'
    cur.executemany(sql, data)
    conn.commit()
    conn.close()    
    # with open('emission_p.txt', 'w', encoding='utf-8') as f:
    #     for character, pinyin_map in character_pinyin_map.items():
    #         sum_frequency = sum(pinyin_map.values())
    #         for py, frequency in pinyin_map.items():
    #             f.write("%s, %s:%s\n"%(character, py,log(frequency / sum_frequency)))


def init_transition():
    """
    初始化转移概率
    """
    print("Training transition probablity matrix.")
    # todo 优化 太慢
    transition_map = {}
    for phrase, frequency,_ in iter_dict():
        for i in range(len(phrase) - 1):
            if phrase[i] in transition_map:
                transition_map[phrase[i]][phrase[i+1]] = \
                    transition_map[phrase[i]].get(phrase[i+1], 0) + frequency
            else:
                transition_map[phrase[i]] = {phrase[i+1]: frequency}

    # for previous, behind_map in transition_map.items():
    #     sum_frequency = sum(behind_map.values())
    #     for behind, freq in behind_map.items():
    #         Transition.add(previous, behind, log(freq / sum_frequency))
    conn = sqlite3.connect('./pinyin/model/hmm.sqlite')
    cur = conn.cursor()
    sql = 'INSERT INTO transition (previous, behind,probability ) VALUES (?,?,?);'
    data = []
    for previous, behind_map in transition_map.items():
        sum_frequency = sum(behind_map.values())
        for behind, freq in behind_map.items():
            data.append((previous, behind,log(freq / sum_frequency)))
    sql = sql[:-1] + ';'
    cur.executemany(sql, data)
    conn.commit()
    conn.close()      
    # with open('transition_p.txt', 'w', encoding='utf-8') as f:
    #     for previous, behind_map in transition_map.items():
    #         sum_frequency = sum(behind_map.values())
    #         for behind, freq in behind_map.items():
    #             f.write("%s->%s:%s\n"%(previous, behind,log(freq / sum_frequency)))

if __name__ == '__main__':
    init_hmm_tables()
    init_start()
    init_emission()
    init_transition()

    # 创建索引
    session = HMMSession()
    session.execute('create index ix_starting_character on starting(character);')
    session.execute('create index ix_emission_character on emission(character);')
    session.execute('create index ix_emission_pinyin on emission(pinyin);')
    session.execute('create index ix_transition_previous on transition(previous);')
    session.execute('create index ix_transition_behind on transition(behind);')
    session.commit()
