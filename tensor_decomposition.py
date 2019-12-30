import numpy as np
import tensorly as tl
from tensorly.decomposition import parafac
import pickle
from configparser import ConfigParser
import os

# Load
parser = ConfigParser()
parser.read('dev.ini')
dir_ = parser.get('Parsing', 'dir_', fallback='maildir')
email_path = os.path.join(os.getcwd(), dir_)
cwd = os.getcwd()

token_list = list(pickle.load(open(email_path + "/Data_Pickle/token_dict.p", 'rb')).keys())
tensor = np.load('tensor.npy')

rank = parser.getint('Decomposition', 'rank', fallback=25)
cluster_n = parser.getint('Decomposition', 'cluster_n', fallback=10)

weights, factors = parafac(tl.tensor(tensor), rank=rank, normalize_factors=True, non_negative=True)

# factors[0]: author
# factors[1]: months
# factors[2]: terms

# Column = Factor
token_factors = factors[2].T
time_factors = factors[1].T

tokens = []
intensity = []

for r in range(rank):

    loadings = token_factors[r][np.argsort(token_factors[r])[-cluster_n:]]

    intensity.append(time_factors[r])

    index = [np.where(token_factors[r] == l) for l in loadings]
    index = [item for sublist in index for item in sublist]
    index = set(item for sublist in index for item in sublist)

    tokens.append([token_list[i] for i in index])

pickle.dump(tokens, open(email_path + "/Data_Pickle/conv_tokens.p", "wb"))
pickle.dump(intensity, open(email_path + "/Data_Pickle/conv_intensity.p", "wb"))