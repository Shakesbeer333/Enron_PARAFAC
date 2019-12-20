import numpy as np
import tensorly as tl
from tensorly.decomposition import parafac
import pickle
from configparser import ConfigParser
import os
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm

# Load
parser = ConfigParser()
parser.read('dev.ini')
dir_ = parser.get('Parsing', 'dir_', fallback='maildir')
email_path = os.path.join(os.getcwd(), dir_)
cwd = os.getcwd()

token_list = list(pickle.load(open(email_path + "/Data_Pickle/token_dict.p", 'rb')).keys())
dates = pickle.load(open(email_path + "/Data_Pickle/dates.p", 'rb'))
tensor = np.load('tensor.npy')

rank = 12
cluster_n = 5

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

######
# Plot
######

timeline = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

fig_per_plot = 7

plt.figure(1)

intensity_index = 0
subplot_index = 0

colors = cm.rainbow(np.linspace(0, 1, rank + 1))

for i in range(1, rank + 1):

    if subplot_index % fig_per_plot == 0 and i != 1:
        sub_pos = 1
        plt.rcParams["figure.figsize"] = (18, 12)
        plt.savefig(cwd + f'/Gantt/Gantt{i - 1}.png')
        plt.close()
        subplot_index = 1

    else:
        subplot_index += 1

    print(intensity_index, '-', subplot_index)
    pos = int(str(fig_per_plot) + str(1) + str(subplot_index))
    plt.subplot(pos)
    plt.subplots_adjust(hspace=0.4)
    plt.plot(timeline, intensity[intensity_index], color=colors[i])
    plt.ylabel('Conversation\nLevel')
    plt.ylim(0, 1.1)
    plt.text(-0.45, 0.75, f'Topic {i}', bbox=dict(facecolor='white', edgecolor='white', alpha=0.5))
    # plt.text(0.5, 0.5, f'California',bbox=dict(facecolor=colors[i], edgecolor = 'white', alpha=0.5))
    plt.yticks(np.arange(0, 1.1, 0.2))

    plt.grid(True)
    # plt.title(tokens[intensity_index][0])
    plt.rcParams["figure.figsize"] = (18, 12)

    intensity_index += 1

plt.savefig(cwd + '/Gantt/Gantt_last.png')
plt.close()
