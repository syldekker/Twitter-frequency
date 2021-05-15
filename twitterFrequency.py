# coding: utf-8

import random
import re
import sys
from collections import defaultdict
import math


## EXTRA CREDIT ##
def rand(hist):
    rnum = random.uniform(0, 1)
    for x in hist:
        rnum -= hist[x]
        if rnum < 0: return x
    return x


## PART 1 ##
def clean(line):
    # use the following syntax for all your replacements so that unicode is properly treated
    # line = re.sub(u'replace_regexp','with_regexp',line)
    line = re.sub(u'@(\w+):?', '@@@', line)  # works
    line = re.sub(u'((http)|(www))\S+', 'www', line)  # works
    line = re.sub(u'#\w+', '###', line)  # works
    line = re.sub(u'\B(\s*)[^0-9a-zA-Z_@#]*(\w+)([^0-9a-zA-Z_@#]*)(\s+)|[^0-9a-zA-Z_@#]*$', '\\1\\2\\4', line)
    line = re.sub(u'\s+([^0-9a-zA-Z_@#]+)\s+', '\\1', line)
    line = line.lower()
    # print(line+"\n")
    return line


## PART 2 ##
def normalize(hist):
    # this is a void function that normalizes the counts in hist
    # given a dictionary of word-frequency pairs, this function modifies the frequencies so that they sum to 1
    sum_val = 0.0
    for value in hist.values():
        sum_val += value
    for word in hist:
        hist[word] = hist.get(word, value) / sum_val
    # remove the following print statement once you complete this function
    # print("Normalize doesn't do anything yet")


def get_freqs(f):
    wordfreqs = defaultdict(lambda: 0)
    lenfreqs = defaultdict(lambda: 0)

    for line in f.readlines():
        # print(line)
        line = clean(line)
        words = re.split(u'\s+|\s+[-]+\s+', line)
        lenfreqs[len(words)] += 1
        for word in words:
            wordfreqs[word.encode('utf-8')] += 1
    normalize(wordfreqs)
    normalize(lenfreqs)
    return (wordfreqs, lenfreqs)


## PART 3 ##
def save_histogram(hist, filename):
    outfilename = re.sub("\.txt$", "_out.txt", filename)
    outfile = open(outfilename, 'w', encoding='utf-8')
    print("Printing Histogram for", filename, "to", outfilename)
    counter = 1
    for word, count in sorted(hist.items(), key=lambda pair: pair[1], reverse=True):
        str1 = word.decode('utf-8')
        output = "%-13.6f\t%s\t\t\t%f\t\t\t%f\n" % (count, str1, math.log(count), math.log(counter))
        counter += 1
        outfile.write(output)


## PART 4 ##
def get_top(hist, N):
    # return a list of the N most frequent words in hist
    N = 128
    stopwords = []
    for word, count in sorted(hist.items(), key=lambda pair: pair[1], reverse=True):
        if len(stopwords) < N:
            stopwords.append(word)
    return stopwords


def filter(hist, stop):
    for key in stop:
        if key in hist: hist.pop(key)
    normalize(hist)


def main():
    file1 = open(sys.argv[1], encoding="utf-8")
    (wordf1, lenf1) = get_freqs(file1)
    stopwords = get_top(wordf1, 0)
    save_histogram(wordf1, sys.argv[1])

    for fn in sys.argv[2:]:
        file = open(fn, encoding="utf-8")
        (wordfreqs, lenfreqs) = get_freqs(file)
        filter(wordfreqs, stopwords)
        save_histogram(wordfreqs, fn)
        ## EXTRA CREDIT ##
        print("Printing random tweets from", fn)
        for x in range(5):
            n = rand(lenfreqs)
            print(n, "random words:")
            for i in range(n):
                print(' ', rand(wordfreqs).decode('utf-8'), end='')
            print()


## This is special syntax that tells python what to do (call main(), in this case) if this  script is called directly
## this gives us the flexibility so that we could also import this python code in another script and use the functions
## we defined here
if __name__ == "__main__":
    main()
