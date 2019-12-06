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
import re

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

    print(text)
    print('-------------NEW MAIL---------------------------------------')

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


def weight(tokens):

    #l = dict(nltk.FreqDist(n)
    #loc_local_weight =
    #entropy_global_weight =
    #author_normalization =


df['Group_Key'] = df.apply(lambda x: str(x['From']) + '-' + str(x['Date'].year) + '-' + str(x['Date'].month), axis = 1)

df_grouped = df.groupby('Group_Key').agg({'Token': 'sum'})

print(df_grouped)

df_grouped['Count'] = df_grouped.apply(lambda x: weight(x['Token']), axis = 1)