# -*- coding: utf-8 -*-

"""
Report 10: Statistical Language Models

A statistical language model assigns some probability, P(s), to a sentance of
N words. Using probability theory, the probability of each word, w, given the
words that precede it is

    P(s) = P(w1)P(w2|w1)P(w3|w1w2)...P(wn|w1w2...wn-1)
    
An n-gram language model is constructed using the assumption that the probability
of a word depends solely on the n-1 number of words before the current word.

The performance of the n-gram model is determine using perplexity, which measures
how well the model predicts a body of text of length N. It can be thought of as
the average number of possible words that can follow any word
"""


import numpy as np
import matplotlib.pyplot as plt
from numpy.random import choice


# Plot the top 10 words of The Phantom of the Opera
file = open('PhantomOpera.txt', encoding = 'utf8')
play = file.read()
file.close()

play = play.lower()
punctuation = '#:;,.!?-[]*'
for char in punctuation:
    play = play.replace(char, '')
    
words = play.split()
words[0] = 'the' # get rid of garbage characters

wordCount = {}
for word in words:
    if word in wordCount:
        wordCount[word] += 1
    else:
        wordCount[word] = 1

sortWords = sorted(wordCount.items(), key = lambda x: x[1], reverse = True)

counts = [pair[1] for pair in sortWords]
count10 = counts[:10]
labels = [pair[0] for pair in sortWords]
label10 = labels[:10]

colorlist = ['fuchsia', 'deeppink', 'red', 'orange', 'yellow', 'green', 'blue',
             'indigo', 'purple', 'darkviolet']
plt.figure(figsize = (6, 6))
plt.pie(count10, labels = label10, autopct = '%.0f%%', colors = colorlist)

plt.title('Top 10 Words in $\it{The\ Phantom\ of\ the\ Opera}$', fontsize = 14)


# Create n-gram models using "Pride and Prejudice"
file = open('PridePrejudice.txt', encoding = 'utf8')
book = file.read().split()
file.close()


def calc_probs(wordList):
    
    """
    Creates a dictionary of all the words and their associated word count.
    
    Parameters:
        wordlist (list[str]): list containing all of the words of the 
        chosen text
    
    Returns:
        list[str]: a list of all the words
        
        probs (list[float]): a list of corresponding probabilites of all the words
    """
    
    totalWords = len(wordList)
    wordCount = {word:0 for word in wordList}
    
    for word in wordList:
        wordCount[word] += 1
    
    probs = [freq/totalWords for freq in wordCount.values()]
    
    return list(wordCount.keys()), probs


# Unigram Model
unigram = calc_probs(book)
W, P = unigram
print('\nThe number of distinct words in Pride and Prejudice is', len(W), '\n')

nWords = 350
for word in choice(W, p = P, size = nWords):
    print(word, end = ' ')
    
unigramDict = {w:p for w, p in zip(*unigram)}

total = 0 
for word in book:
    prob = unigramDict[word]
    total += np.log2(prob)

perplexity = 2**(-total/len(book))
print('\n\nUnigram Perplexity = {}'.format(perplexity))


# Bigram Model
firstWords = book[:-1] # ignore first word
secondWords = book[1:] # ignore last word

wordDictBi = {word:[] for word in firstWords}
for w1, w2 in zip(firstWords, secondWords):
    wordDictBi[w1].append(w2)

bigram = {key:calc_probs(value) for key, value in wordDictBi.items()}
print('\nThe number of bigrams in Pride and Prejudice is', len(bigram), '\n')

nWords = 350
W, P = unigram
word1 = choice(W, p = P)

for i in range(nWords):
    print(word1, end = ' ')
    W2, P2 = bigram[word1]
    word2 = choice(W2, p = P2)
    word1 = word2

bigramDict = {key:{w:p for w, p in zip(*value)} for key, value in bigram.items()}

total = 0
first = book[0] # get first word probability
prob = unigramDict[first] 
total += np.log2(prob)

for second in book[1:]:
    prob = bigramDict[first][second]
    total += np.log2(prob)
    first = second

perplexity = 2**(-total/len(book))
print('\n\nBigram Perplexity = {}'.format(perplexity))


# Trigram Model
firstWords = book[:-1]
secondWords = book[1:]
thirdWords = book[2:]

wordDictTri = {(w1, w2):[] for w1, w2 in zip(firstWords, secondWords)}
for w1, w2, w3 in zip(firstWords, secondWords, thirdWords):
    wordDictTri[w1, w2].append(w3)

trigram = {key:calc_probs(value) for key, value in wordDictTri.items()}

print('\nThe number of trigrams in Pride and Prejudice is', len(trigram), '\n')

nWords = 350
W, P = unigram
word1 = choice(W, p = P)
W2, P2 = bigram[word1]
word2 = choice(W2, p = P2)

for i in range(nWords):
    print(word1, end = ' ')
    W3, P3 = trigram[(word1, word2)]
    word3 = choice(W3, p = P3)
    word1 = word2
    word2 = word3

trigramDict = {key:{w:p for w, p in zip(*value)} for key, value in trigram.items()}

total = 0
first = book[0] # get first word probability
prob = unigramDict[first] 
total += np.log2(prob)

second = book[1] # get second word probability
prob = bigramDict[first][second]
total += np.log2(prob)

for third in book[2:]:
    prob = trigramDict[(first, second)][third]
    total += np.log2(prob)
    first = second
    second = third

perplexity = 2**(-total/len(book))
print('\n\nTrigram Perplexity = {}'.format(perplexity))


# Quadrigram Model
firstWords = book[:-1]
secondWords = book[1:]
thirdWords = book[2:]
fourthWords = book[3:]

wordDictQuad = {(w1, w2, w3):[] for w1, w2, w3 in zip(firstWords, secondWords, thirdWords)}
for w1, w2, w3, w4 in zip(firstWords, secondWords, thirdWords, fourthWords):
    wordDictQuad[w1, w2, w3].append(w4)

quadrigram = {key:calc_probs(value) for key, value in wordDictQuad.items()}

print('\nThe number of quadrigrams in Pride and Prejudice is', len(quadrigram), '\n')

nWords = 350
W, P = unigram
word1 = choice(W, p = P)
W2, P2 = bigram[word1]
word2 = choice(W2, p = P2)
W3, P3 = trigram[(word1, word2)]
word3 = choice(W3, p = P3)

for i in range(nWords):
    print(word1, end = ' ')
    W4, P4 = quadrigram[(word1, word2, word3)]
    word4 = choice(W4, p = P4)
    word1 = word2
    word2 = word3
    word3 = word4

quadrigramDict = {key:{w:p for w, p in zip(*value)} for key, value in quadrigram.items()}

total = 0
first = book[0] # get first word probability
prob = unigramDict[first] 
total += np.log2(prob)

second = book[1] # get second word probability
prob = bigramDict[first][second]
total += np.log2(prob)

third = book[2] # get third word probability
prob = trigramDict[(first, second)][third]
total += np.log2(prob)

for fourth in book[3:]:
    prob = quadrigramDict[(first, second, third)][fourth]
    total += np.log2(prob)
    first = second
    second = third
    third = fourth

perplexity = 2**(-total/len(book))
print('\n\nQuadrigram Perplexity = {}'.format(perplexity))