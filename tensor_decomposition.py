import numpy as np
import tensorly.contrib.sparse as stl
from tensorly.contrib.sparse.decomposition import parafac as sparse_parafac
import pickle
from configparser import ConfigParser
import os

# Load
parser = ConfigParser()
parser.read('dev.ini')
dir_ = parser.get('Parsing', 'dir_', fallback='maildir')
email_path = os.path.join(os.getcwd(), dir_)
cwd = os.getcwd()

token_list = list(pickle.load(open(email_path \
                                   + "/Data_Pickle/token_dict.p", 'rb')).keys()
                 )
employee_list = pickle.load(open(email_path \
                                 + "/Data_Pickle/employee_list.p", 'rb')
                           )
dense_tensor = np.load('tensor.npy')
dense_tensor = dense_tensor.astype('float32')
sparse_tensor = stl.tensor(dense_tensor)

rank = parser.getint('Decomposition', 'rank', fallback=25)
cluster_n = parser.getint('Decomposition', 'cluster_n', fallback=10)

weights, factors = sparse_parafac(sparse_tensor, 
                                  rank=rank, 
                                  init='random', 
                                  normalize_factors=True, 
                                  non_negative=True
                                 )

# factors[0]: author
# factors[1]: months
# factors[2]: terms

# Column = Factor
token_factors = factors[2].todense().T
time_factors = factors[1].todense().T
author_factors = factors[0].todense().T

tokens = []
intensity = []
author = []

for r in range(rank):
    loadings = token_factors[r][np.argsort(token_factors[r])[-cluster_n:]]
    index = [np.where(token_factors[r] == l) for l in loadings]
    index = [item for sublist in index for item in sublist]
    index = set(item for sublist in index for item in sublist)
    tokens.append([token_list[i] for i in index])

    loadings = author_factors[r][np.argsort(author_factors[r])[-cluster_n:]]
    index = [np.where(author_factors[r] == l) for l in loadings]
    index = [item for sublist in index for item in sublist]
    index = set(item for sublist in index for item in sublist)
    author.append([employee_list[i] for i in index])

    intensity.append(time_factors[r])

pickle.dump(tokens, 
            open(email_path + f"/Data_Pickle/conv_tokens{rank}.p", "wb")
           )
pickle.dump(intensity,
            open(email_path + f"/Data_Pickle/conv_intensity{rank}.p", "wb")
           )
pickle.dump(author, 
            open(email_path + f"/Data_Pickle/author{rank}.p", "wb")
           )
