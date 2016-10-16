from scipy.stats import pearsonr
import csv
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns

sns.set_style("white")
sns.set_palette(sns.color_palette("deep"))

def read_data(f):
    data = []
    headers = []
    with open(f, "rb") as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        for row in reader:
            headers.append(row[:3])
            data.append(map(float, [r.split()[0] for r in row[3:]]))
    return np.array(data), headers


data, headers = read_data("/home/roger/Downloads/ende.csv")

data[:, 7] = data[:, 7] * 100

types = {"chain":[], "tree":[],"mixed":[]}

for i, row in enumerate(headers):
    types[row[1]].append(i)


data2, headers2 = read_data("/home/roger/Downloads/deen.csv")

data2[:, 7] = data2[:, 7] * 100

types2 = {"chain":[], "tree":[],"mixed":[]}

for i, row in enumerate(headers2):
    types2[row[1]].append(i)


# aer index = 7
# bleu index = 0
# meteor = 1

colors = {"chain": "r", "tree":"g", "mixed": "b"}
palette = sns.color_palette("deep")
colors = {c: palette[i] for i,c in enumerate(colors)}

#limits = [23.0,26,12.00,16.00]
limits = [14,16.5,30.00,41.00]

x, y = 0,7
#pearson_coff =  pearsonr(data[:,x],data[:,y])


for i, t in enumerate(types):
    indices = np.array(types[t])
    k = colors[t]
    plt.plot(data[indices,x],data[indices, y], "o", color=k, label=t)

bl = plt.plot((data[0,x], data[0,x]), (limits[2], limits[3]), 'k--', lw=1, label="baselines")[0]
plt.plot((limits[0], limits[1]), (data[0,y], data[0,y]), 'k--', lw=1)
plt.axis(limits)


x, y = 9,7
#pearson_coff =  pearsonr(data[:,x],data[:,y])


for t in types2:
    indices = np.array(types2[t])
    k = colors[t]
    plt.plot(data2[indices,x],data2[indices, y], ".", color=k)






aa = plt.plot([0],[0], "o", color=colors["chain"], label="DE$\\rightarrow$EN")[0]
bb = plt.plot([0],[0], ".", color=colors["chain"], label="EN$\\rightarrow$DE")[0]
chain = mpatches.Patch(color=colors["chain"], label='chain')
tree = mpatches.Patch(color=colors["tree"], label='tree')
mixed = mpatches.Patch(color=colors["mixed"], label='mixed')
plt.legend(handles=[chain, tree, mixed, aa, bb, bl])




#plt.legend(loc=3)
plt.xlabel("BLEU")
plt.ylabel("AER")
plt.show()

