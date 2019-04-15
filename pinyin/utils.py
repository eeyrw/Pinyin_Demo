# -*- coding=utf8 -*-
import os

dict_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'PhraseAndPinyin.txt')


def iter_dict():
    """
    遍历dict.txt文件
    """
    with open(dict_path, 'r', encoding='utf-8') as f:
        for i in range(40000000):
            phrase=f.readline()
            if not phrase:
                break
            phrase=phrase.rstrip(' \n')
            pinyinList=f.readline().rstrip(' \n').split(' ')
            yield phrase, 1, pinyinList
