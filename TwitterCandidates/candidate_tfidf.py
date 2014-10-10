import math
import string
from collections import Counter
import os
import time


def words(d):
    wordlist = []
    #remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)
    #words = d.translate(string.maketrans(string.punctuation, ' '*len(string.punctuation)))
    #words = d.translate(string.maketrans("",""), string.punctuation)
    punc = u'!"#%\'()*+,-./:;<=>?@[\]^_`{|}~'
    #translate_table = dict((ord(char), u' ') for char in punc)
    replace = ' '*(len(punc))
    translate_table = string.maketrans(punc, replace)
    translate_table = translate_table.decode("latin-1")
    words = d.translate(translate_table)


    words = words.split()
    #words = words.strip()
    for word in words:
        if len(word) > 2 and not word.isdigit():
            wordlist.append(word.lower())
    return wordlist

def create_indexes(fileList, searching=False):
    tf_map = {}
    df = {}
    for f in fileList:
        d = open(f, "r").read()
        wordlist = words(d)
        n = float(len(wordlist))
        tf = Counter(wordlist)
        for t in tf.keys():
            tf[t] = tf[t]/n
            #if being used in a search engine, returns list of docs with word rather than count
            if searching == True:
                if t not in df:
                    df[t] = []
                else:
                    df[t].append(f)
            else:
                if t not in df:
                    df[t] = 1
                else:
                    df[t] += 1
        tf_map[f] = tf
    return tf_map, df

def doc_tfidf(tf, df, N, searching=False):
    #takes input from tf_map[f] for a SINGLE document
    tfidf = {}
    for t in tf:
        if searching == False:
            dft = df[t]/float(N)
        else:
            dft = (len(df[t]) + 1)/(float(N + 1))

        idft = 1/float(dft)
        tfidf[t] = tf[t]*math.log(idft)
    return tfidf

def create_tfidf_map(fileList, searching=False, paramList = None):
    N = len(fileList)
    tfidf_map = {}

    if searching == False:
        tf_map, df = create_indexes(fileList)
        for f in fileList:
            tfidf_map[f] = doc_tfidf(tf_map[f], df, N)

    #if in searching mode, calls this function with parameters that were already generated
    #in main, because they need to be used for the search mechanism to work. This avoids
    #having to perform these operations twice
    else:
        tf_map = paramList[0]
        df = paramList[1]
        for f in fileList:
            tfidf_map[f] = doc_tfidf(tf_map[f], df, N, searching=True)

    return tfidf_map

if __name__ == '__main__':
    files = []
    start = time.time()

    candidateList = {"Gary Peters":"MI", "Terri Lynn Land":"MI","Al Franken":"MN","Mike McFadden":"MN",
                         "Mark Begich":"AK","Dan Sullivan":"AK","Mark Pryor":"AR","Tom Cotton":"AR","Mark Udall":"CO",
                         "Cory Gardner":"CO","David Perdue":"GA","Michelle Nunn":"GA","Bruce Braley":"IA",
                         "Joni Ernst":"IA","Pat Roberts":"KS","Greg Orman":"KS","Jeanne Shaheen":"NH",
                        "Scott Brown":"NH","Kay Hagan":"NC","Thom Tillis":"NC","Mitch McConnell":"KY",
                        "Alison Grimes":"KY","Mary Landrieu":"LA","Bill Cassidy":"LA","Rob Maness": "LA"}
    for candidateName in candidateList:
        fileNameStem = "".join(candidateName.split())
        candTextName = fileNameStem + "Text.txt"
        files.append(candTextName)
    N = len(files)
    (file_to_histo, word_to_numdocs) = create_indexes(files)
    for f in files:
        tfmap = doc_tfidf(file_to_histo[f], word_to_numdocs, N)
        # convert map to a Counter object so we can use most_common()
        print os.path.basename(f)
        for i in range(0,20):
            term_pair = Counter(tfmap).most_common(20)[i]
            term_pair = Counter(tfmap).most_common(20)[i]
            print "Result %d: (%s, %1.4f)" % (i, term_pair[0], term_pair[1])
    end = time.time()
    print "Implementation took %f seconds" % (end - start)
