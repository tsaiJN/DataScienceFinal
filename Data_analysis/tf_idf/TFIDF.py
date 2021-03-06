import sys
import os
from operator import itemgetter
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer

def getFileList(path):
    file_list = []
    files = os.listdir(path)
    for f in files:
        if(f[0] == '.'):
            pass
        else:
            file_list.append(f)
    return file_list

def tfidf(filelist, path, outpath):
    corpus = []
    chatlist = []
    chatlen = []
    for ff in filelist:
        filename = path + ff
        file_in = open(filename, 'r')
        content = file_in.read()
        file_in.close()
        content_list = content.split('\n', 2)
        if len(content_list) > 2:
            chatlist.append(content_list[0])
            chatlen.append(content_list[1])
            corpus.append(content_list[2])

    vectorizer = CountVectorizer()
    transformer = TfidfTransformer()
    tfidf = transformer.fit_transform(vectorizer.fit_transform(corpus))

    word = vectorizer.get_feature_names()
    weight = tfidf.toarray()

    tfidfDict = {}
    tmpDict = {}
    for chat in range(len(file_list)):
        chatname = str(chatlist[chat])
        #print("File:" + chatname)
        tfidfDict[chatname] = {}
        tfidfDict[chatname]['len'] = []
        tfidfDict[chatname]['list'] = []
        tmpDict = {}
        for words in range(len(word)):
            if weight[chat][words] > 0:
                #print(word[words] + ":" + str(weight[chat][words]))
                tmpDict[word[words]] = weight[chat][words]
        sorted_list = sorted(tmpDict.items(), key=itemgetter(1), reverse=True)
        tfidfDict[chatname]['len'] = chatlen[chat]
        for item in sorted_list:
            tfidfDict[chatname]['list'].append(list(item))

    if not os.path.exists(outpath):
        os.mkdir(outpath)

    file_out = open(outpath + "tfidf_dict.txt", "w")
    file_out.write(str(tfidfDict))
    file_out.close()

    file_out = open(outpath + "tfidf_formatted.txt", "w")
    for item in tfidfDict:
        file_out.write(str(item) + " " + str(tfidfDict[item]['len']) + '\n')
        for i in range(len(tfidfDict[item]['list'])):
            file_out.write(str(tfidfDict[item]['list'][i]) + '\n')
    file_out.close()

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("usage: python TFIDF.py <file path> <output path>")
        print("example: python TFIDF.py ./CHL_text/ ./CHL_tfidf/")
    file_list = getFileList(sys.argv[1])
    tfidf(file_list, sys.argv[1], sys.argv[2])
