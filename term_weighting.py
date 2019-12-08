import nltk
nltk.download('stopwords')
nltk.download('wordnet')
from nltk.tokenize.regexp import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import string
from nltk.stem.porter import PorterStemmer
from configparser import ConfigParser
import os
import pandas as pd
pd.set_option('display.max_columns', 10)
import re
import numpy as np
from collections import Counter

parser = ConfigParser()
parser.read('dev.ini')
dir_ = parser.get('Parsing', 'dir_', fallback = 'maildir')

e_mails = os.path.join(os.getcwd(), os.path.join(dir_, 'Data_Pickle/e_mails.p',))

df = pd.read_pickle(e_mails)

#############################################################################
# Setting for Cleaning
#
lemma = WordNetLemmatizer()
porter = PorterStemmer()

stop = stopwords.words('english')
#todo write additional stopwors in txt file
add_regular = [r'To:',"cc:",r'Subject:', r'http\S*',r'From:',r'Sent:', "ect", "u", "fwd", "www", "com"]
add_dotall = ['-+ Forwarded.*\n.*-+\n',
              '-+Original Message-+.*\nFrom:.*\nSent:.*\nTo:.*\nSubject:.*\n',
              'http\S+',
              'www\S+',
              '.*on \d\d/\d\d/\d\d\d\d \d\d:\d\d:\d\d (AM|PM)?',
              '\S+@\S+',
              'To:.*(\n.*)+Subject:',
              ]

pattern = r'|'.join(add_dotall)




exclude = set(string.punctuation)

str_ = '['
for i in exclude:
    str_ += '\\' + i
str_ += ']'
#
#
#############################################################################

def token(text):

    text = re.sub(pattern = pattern, repl = '', string = text, count = 100, flags = re.IGNORECASE)

    #print(text)
    #print('-------------NEW MAIL---------------------------------------')

    text = text.rstrip().lower().split()

    # 1 - remove punctuation
    punc_free = [i for i in text if i not in exclude]

    # 2 - Remove all digits and stopwords
    stop_free = [i for i in punc_free if (not i.isdigit()) and (i not in stop)]

    # 3 - Lemmatize words
    normalized = [lemma.lemmatize(i) for i in stop_free]

    # 4 - Stem words
    stemmed = [porter.stem(token) for token in normalized]

    # 5 - Final cleaning

    # wow! --> wow     or       "include --> include
    cleaned_text = [re.sub(str_, '', i) for i in stemmed]

    # remove stopwords after lemmatizing and stemming
    #cleaned_text = [i for i in cleaned_text if ((i not in stop))]

    # remove digits after lemmatizing and stemming
    cleaned_text = [i for i in cleaned_text if not i.isdigit()]

    return cleaned_text

df['Token'] = df.apply(lambda x: token(x['Content']), axis = 1)

# Plausibility Check okay
def loc_local_weight(tokens):

    l = dict(nltk.FreqDist(tokens))
    l.update((x,np.log(1 + y)) for x,y in l.items())

    return Counter(l)


token_list = [item for sublist in df.agg({'Token': 'sum'}).values for item in sublist]
token_dict = dict(nltk.FreqDist(token_list))

# Plausibility check okay
def h_i_j(tokens):

    h = dict(nltk.FreqDist(tokens))
    h.update((x, y/token_dict[x]) for x,y in h.items())

    return Counter(h)


author_list = df['From'].values
author_dict = dict(zip(author_list, [0]*len(author_list)))

entropy_dict = dict(zip(token_list, [0]*len(token_list)))

# Plausibility check okay
def entropy_global_weight(h_i_j):

    entropy_copy = entropy_dict.copy()
    entropy_dict.update((x, (h_i_j[x]*np.log(h_i_j[x]))/len(author_dict) + entropy_copy[x]) for x in h_i_j)

# Plausibility check okay
def author_normalization(loc_log_weight, author):

    author_dict[author] = sum(loc_log_weight[x]*entropy_dict[x] for x in loc_log_weight)

# Plausibility check okay
def final_weight(l_i_j, author):

    x_i_j = dict(l_i_j.copy())

    x_i_j.update((x, y*entropy_dict[x]*author_dict[author]) for x, y in x_i_j.items())

    return x_i_j


# Local loc weight
#

df['Group_Key_l'] = df.apply(lambda x: str(x['From']) + '-' + str(x['Date'].year) + '-' + str(x['Date'].month), axis = 1)

df_grouped_l = df.groupby('Group_Key_l').agg({'Token': 'sum'})

df_grouped_l['Loc_local_weight'] = df_grouped_l.apply(lambda x: loc_local_weight(x['Token']), axis = 1)


# Entropy global weight
#

df_grouped_h = df.groupby('From').agg({'Token': 'sum'})

df_grouped_h['h_i_j'] = df_grouped_h.apply(lambda x: h_i_j(x['Token']), axis = 1)

del token_dict

df_grouped_h.apply(lambda x: entropy_global_weight(x['h_i_j']), axis = 1)

entropy_dict.update((x, 1 + y) for x,y in entropy_dict.items())

# Author normalization
#

df_grouped_l.reset_index(inplace = True)
df_grouped_l['Author'] = df_grouped_l.apply(lambda x: x['Group_Key_l'][ : re.search(r'-\d\d\d\d-', x['Group_Key_l']).start()], axis = 1)

df_grouped_a = df_grouped_l.groupby('Author').agg({'Loc_local_weight': 'sum'})

df_grouped_a.reset_index(inplace = True)

df_grouped_a.apply(lambda x: author_normalization(x['Loc_local_weight'], x['Author']), axis = 1)

author_dict.update((x,(np.sqrt(y))**-1) for x,y in author_dict.items())

# Final weighting
#

df_grouped_l['Final_Weight'] = df_grouped_l.apply(lambda x: final_weight(x['Loc_local_weight'].copy(), x['Author']), axis = 1)