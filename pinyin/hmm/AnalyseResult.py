import sys
sys.path.append(r'./')    #要用绝对路径
from pinyin.model import Emission, Transition
from pinyin.utils import iter_dataset
import difflib
import pickle
import pprint
import numpy as np
from functools import reduce
import random

def getRawString(diffString):
    diffList=[]
    for i in range(0,len(diffString),3):
        diffList.append(diffString[i:i+3])
    strA=''.join(difflib.restore(diffList,1))
    strB=''.join(difflib.restore(diffList,2))
    return (strA,strB)

if __name__ == '__main__':
    fp = open("testResult.txt","rb")
    resultList=pickle.load(fp)
    fp.close()
    resultList.sort(key=lambda x: x[0])
    # with open('testResultVisual.txt','w',encoding='utf-8') as f:
    #     for i in resultList:
    #         pprint.pprint(i,f)
    resultList_le5=[]
    resultList_gt5le10=[]
    resultList_gt10le20=[]
    resultList_gt20=[]    
    for result in resultList:
        if result[0]<=5:
            resultList_le5.append(result)
        elif result[0]>5 and result[0]<=10:
            resultList_gt5le10.append(result)
        elif result[0]>10 and result[0]<=20:
            resultList_gt10le20.append(result)
        elif result[0]>20:
            resultList_gt20.append(result)
    with open('AnalysisResult.txt','w',encoding='utf-8') as f:
        f.write('Mean error totaly: %s\n'%np.mean(np.array([result[1] for result in resultList])))   
        f.write('Mean error with 0~5: %s\n'%np.mean(np.array([result[1] for result in resultList_le5])))    
        f.write('Mean error with 6~10: %s\n'%np.mean(np.array([result[1] for result in resultList_gt5le10])))    
        f.write('Mean error with 11~20: %s\n'%np.mean(np.array([result[1] for result in resultList_gt10le20]))) 
        f.write('Mean error with >20: %s\n'%np.mean(np.array([result[1] for result in resultList_gt20]))) 

        secure_random = random.SystemRandom()

        f.write('Example within 0~5:\n')
        for i in range(5):
            randomItem=secure_random.choice(resultList_le5)
            f.write('真值：%s\n预测：%s\n\n'%getRawString(randomItem[2]))
        f.write('Example within 6~10:\n')
        for i in range(5):
            randomItem=secure_random.choice(resultList_gt5le10)
            f.write('真值：%s\n预测：%s\n\n'%getRawString(randomItem[2]))
        f.write('Example within 11~20:\n')
        for i in range(5):
            randomItem=secure_random.choice(resultList_gt10le20)
            f.write('真值：%s\n预测：%s\n\n'%getRawString(randomItem[2]))
        f.write('Example within >20:\n')
        for i in range(7):
            randomItem=secure_random.choice(resultList_gt20)
            f.write('%s\n'%randomItem[2])
            f.write('真值：%s\n预测：%s\n\n'%getRawString(randomItem[2]))
