import os
import pickle
from configparser import ConfigParser

# Load
parser = ConfigParser()
parser.read('dev.ini')
dir_ = parser.get('Parsing', 'dir_', fallback='maildir')
rank = parser.getint('Decomposition', 'rank', fallback=14)
email_path = os.path.join(os.getcwd(), dir_)

conv_token = pickle.load(open(email_path \
                              + f"/Data_Pickle/conv_tokens{rank}.p", 'rb')
                        )
author = pickle.load(open(email_path \
                          + f"/Data_Pickle/author{rank}.p", 'rb')+
                    )

for conv in conv_token:
    print(conv)

print('\n')

for a in author:
    print(a)
