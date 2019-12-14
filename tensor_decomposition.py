import numpy as np
from utils import *
import tensorly as tl
from tensorly import unfold as tl_unfold
from tensorly.decomposition import parafac
import logging
from sktensor import dtensor, ktensor
from sktensor import dtensor, cp_als
import pickle
from configparser import ConfigParser
import os
import matplotlib.pyplot as plt
import string

# Load
parser = ConfigParser()
parser.read('dev.ini')
dir_ = parser.get('Parsing', 'dir_', fallback = 'maildir')
email_path = os.path.join(os.getcwd(), dir_)

token_list = list(pickle.load(open(email_path + "/Data_Pickle/token_dict.p", 'rb')).keys())
dates = pickle.load(open(email_path + "/Data_Pickle/dates.p", 'rb'))
tensor = np.load('tensor.npy')

rank = 2
cluster_n = 5



weights, factors = parafac(tl.tensor(tensor), rank = rank, normalize_factors = 1, non_negative = True)

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



plt.subplot(211)
plt.plot(dates, intensity[0], 'r')
plt.subplot(212)
plt.plot(dates, intensity[1], 'b')
plt.close()


np.linspace(0,11,12)




factors = parafac(tl.tensor(tensor), rank = 1)


from scipy.io.matlab import loadmat
from sktensor import dtensor, cp_als

# Load Matlab data and convert it to dense tensor format
mat = loadmat('/home/julian/Downloads/brod.mat')
T = dtensor(mat['X'])

# Decompose tensor using CP-ALS
P,x, c = cp_als(T, 3, init='random')

from sktensor import dtensor, ktensor
U = [np.random.rand(i, 3) for i in (2, 2, 2)]
print(U)

T = dtensor(ktensor(U).toarray())

P, fit, itr = cp_als(T, 3, init = 'random')

np.allclose(T, P.totensor(), atol = 0.001)



T = np.arange(0,60).reshape((3,4,5))

# Mode 0 unfolding
T.reshape(3,8)

# Mode 1 unfolding
T.reshape(4, 6)

# Mode 2 unfolding
T.reshape(2, 12)


####
# Example Data
#
# 3 Authors
# 5 Terms: Air | Water | Soil | Car | Truck
# 4 Time Periods


####

data = np.array([

        # Author 1
        [[ 0,  0,  0,  1,  2],
        [ 0,  0,  0,  3,  4],
        [0, 0, 0, 9, 14],
        [0, 0, 0, 10, 10]],

        # Author 2
       [[10, 14, 15, 0, 0],
        [8, 8, 12, 0, 0],
        [5, 0, 5, 0, 0],
        [0, 0, 4, 0, 0]],

        # Author 3
       [[5, 5, 5, 0, 0],
        [6, 6, 6, 6, 6],
        [33, 23, 15, 10, 12],
        [0, 0, 0, 12, 15]]
    ])




T = dtensor(ktensor(data).toarray())

P, fit, itr = cp_als(dtensor(data), 2, init = 'random')

np.allclose(T, P.totensor(), atol = 0.001)

import plotly.figure_factory as ff

df = [dict(Task="Job A", Start='2009-01-01', Finish='2009-02-28', Complete=0),
      #dict(Task="Job B", Start='2008-12-05', Finish='2009-04-15', Complete=0.5),
      dict(Task="Job C", Start='2009-02-20', Finish='2009-05-30', Complete=0.86),
      dict(Task="Job C", Start='2009-06-20', Finish='2009-10-30', Complete=1),
      ]

colorscale=[
       [(-0.25, 0), 'blue'],
       [(0,0.25), 'white'],
       [(0.25, 1), 'red'],
            ]

fig = ff.create_gantt(df, colors='Blackbody', index_col='Complete', show_colorbar=True, group_tasks=True)
fig.show()



import plotly.plotly as py
df = [dict(Task="Job-1", Start='2017-01-01', Finish='2017-02-02', Resource='Complete'),
  dict(Task="Job-1", Start='2017-01-15', Finish='2017-03-15', Resource='Incomplete'),
  dict(Task="Job-2", Start='2017-01-17', Finish='2017-02-17', Resource='Not Started'),
  dict(Task="Job-2", Start='2017-01-17', Finish='2017-02-17', Resource='Complete'),
  dict(Task="Job-3", Start='2017-03-10', Finish='2017-03-20', Resource='Not Started'),
  dict(Task="Job-3", Start='2017-04-01', Finish='2017-04-20', Resource='Not Started'),
  dict(Task="Job-3", Start='2017-05-18', Finish='2017-06-18', Resource='Not Started'),
  dict(Task="Job-4", Start='2017-01-14', Finish='2017-03-14', Resource='Complete')]

colors = {'Not Started': 'rgb(220, 0, 0)',
      'Incomplete': (1, 0.9, 0.16),
      'Complete': 'rgb(0, 255, 100)'}

fig = ff.create_gantt(df, colors=colors, index_col='Resource', show_colorbar=True, group_tasks=True)

#py.iplot(fig, filename='gantt-group-tasks-together', world_readable=True)

