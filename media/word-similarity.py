import numpy as np
import os
import  io
import  re

from numpy import  dot
from numpy.linalg import  norm

#chcp.com 65001
#export PYTHONIOENCODING=utf-8

def load_embedding_model(path):
    word_with_Feature = {}

    model = open(path, encoding="utf-8", errors = "ignore" )

    for lines in model:
        line  = lines.split()
        if len(line)<=1:
            continue
        word  = line[0]
        vector = np.asarray(line[1:],dtype="float")
        word_with_Feature[ word ] = vector
        #print (word)

    return  word_with_Feature

def word_similarity( wv1, wv2 ):

    cos_sim = dot( wv1, wv2 )/ ( norm(wv1) * norm (wv2) )

    cos_sim = cos_sim * 100

    return  cos_sim

def readinput(path, features):

    text = ''
    with open(path, 'r', encoding="utf-8") as f:
        text = f.read()


    text = text.split()

    l = len(text)
    idx = 0
    while (True):

        w1 = text[idx]
        w2 = text[idx+1]

        idx +=2

        if idx>=l:
            break

        if w1 in features and w2 in features:

            v1 = features[w1]
            v2 = features[w2]

            cos_sim = word_similarity(v1,v2)

            print ('Similarity of ', w1,':',w2," = ",cos_sim)
        else:

            print(w1, " or ", w2, "not found\ n")



def next_simantically_syntactically_similar(path, features):
    text = ''
    with open(path, 'r', encoding="utf-8") as f:
        text = f.read()
    text = text.split()
    l = len(text)
    idx = 0
    while (idx < l):
        w1 = text[idx]
        if w1 in features:
            mx = -100
            res = ''
            for w in features:

                if w==w1:
                    continue

                v1 = features[w1]
                v2 = features[w]
                cos_sim = word_similarity(v1, v2)
                if cos_sim > mx :
                    res = w
                    mx = cos_sim
            print ('Max Match with: ', w1, ' = ', res)
        else:

            print (w1,"Not Found")

        idx = idx +1

if __name__ == "__main__":
    word_with_feature_Value =load_embedding_model('E:\\fiu-student\\vectors.txt')
    path2 = 'E:\\fiu-student\\input.txt'
    readinput(path2,word_with_feature_Value)
    #next_simantically_syntactically_similar(path2,word_with_feature_Value)
   #word_with_feature_Value = load_embedding_model('E:\\fiu-student\\glove-w15-D-100-I-30.txt')
    #
    # w1 = 'রেলকর্মীরা'
    # w2 =  'রেলপুলিশ'
    #
    #
    #
    # if w1 in word_with_feature_Value and w2 in word_with_feature_Value:
    #
    #     wv1 = word_with_feature_Value[w1]
    #     wv2 = word_with_feature_Value[w2]
    #
    #     sim_core = word_similarity(wv1,wv2)
    #     print (sim_core)