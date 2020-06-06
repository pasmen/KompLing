from nltk.corpus import wordnet
import re

def WordModel(text):
    text = ' '.join(text.split('\n'))
    set_word = set(list(filter(None, re.split('\W', text.lower()))))
    dct_synonyms = dict()
    for i in set_word:
       synonyms = set()
       for x in wordnet.synsets(i):
           synonyms.add(x.lemmas()[0].name())
       dct_synonyms[i] = synonyms if len(synonyms) > 0 else {i}
    lst = []
    for word, synonym in dct_synonyms.items():
       lst.append("{:<10} {}".format(word, synonym))
    file = open('Synonim\\file.txt', 'w')
    file.write('\n'.join(lst))
    file.close()

