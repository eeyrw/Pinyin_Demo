# -*- coding=utf8 -*-
"""
    viterbi算法实现
"""
import sys
sys.path.append(r'./')    #要用绝对路径
from pinyin.model import Emission, Transition
from pinyin.utils import iter_dataset
import difflib
import pickle

def viterbi(pinyin_list):
    """
    viterbi算法实现输入法

    Args:
        pinyin_list (list): 拼音列表
    """
    start_char = Emission.join_starting(pinyin_list[0])
    V = {char: prob for char, prob in start_char}

    for i in range(1, len(pinyin_list)):
        pinyin = pinyin_list[i]

        prob_map = {}
        for phrase, prob in V.items():
            character = phrase[-1]
            result = Transition.join_emission(pinyin, character)
            if not result:
                continue

            state, new_prob = result
            prob_map[phrase + state] = new_prob + prob

        if prob_map:
            V = prob_map
        else:
            return V
    return V

def calculatePhraseDiff(strA,strB):
    phraseLen=len(strA)
    diffStr=''.join(difflib.ndiff(strA,strB))
    diffCount=0
    for diffItem in difflib.ndiff(strA,strB):
        if '-' in diffItem:
            diffCount+=1
    error=diffCount*100/phraseLen
    #return '%4f%%:%s'%(error,diffStr)
    return (phraseLen,error,diffStr)


def test_viterbi():
    count=0
    resultList=[]
    print('Testing...')
    with open('testResult.txt','wb+') as f:
        for phrase,pinyinList in iter_dataset('./pinyin/test.txt'):
            #if count>100:
            #    break
            #count+=1
            V = sorted(list(viterbi(pinyinList).items()), key=lambda d: d[1], reverse=True)
            predictPhrase=V[0][0]
            resultList.append(calculatePhraseDiff(phrase,predictPhrase))
            #f.write(calculatePhraseDiff(phrase,predictPhrase)+'\n')
        
        pickle.dump(resultList, f) # 序列化到文件




if __name__ == '__main__':
    test_viterbi()
    # while 1:
    #     string = input('input:')
    #     pinyin_list = string.split()
    #     V = viterbi(pinyin_list)

    #     for phrase, prob in sorted(list(V.items()), key=lambda d: d[1], reverse=True):
    #         print(phrase, prob)
