import os
import pandas as pd
from nvidia_plot_roofline_multiple_kernels import roofline

datadir = '/Users/matthewleinhauser/AMD-Instruction-Roofline-using-rocProf-Metrics/'
files = [x for x in os.listdir(datadir) if x.endswith('.csv') and x.startswith('lbm')]
files.sort()
files = [os.path.join(datadir, file) for file in files]
dfs = {}
for file in files:
    tag, ext = os.path.splitext(os.path.basename(file))
    dfs[tag] = pd.DataFrame()
    with open(file, 'r') as f:
        cnt = 0
        while True:
            ln = f.readline()
            if not ln:
                break
            cnt += 1
            if 'Host Name' in ln:
                break
        df = pd.read_csv(file, skiprows=cnt - 1)
        dft = df.groupby(['Kernel Name', 'Metric Name']).sum()
        dfmetric = pd.pivot_table(dft, index='Kernel Name', columns='Metric Name', values='Metric Value')
        dfmetric['Count'] = df.groupby(['Kernel Name']).count()['ID'].div(dfmetric.shape[1])

        dfmetric['Rank'] = dfmetric['Ranks']

        dfmetric['Programming Model'] = dfmetric['API']

        dfmetric['FLOP/s'] = dfmetric['FLOPS']

        dfmetric['Arithmetic Intensity'] = dfmetric['AI']

        dfs[tag] = dfmetric

tags = dfs.keys()
flag = 'HBM'  # 'HBM','L2','L1' or 'all'

all_AI_HBM = []
all_FLOPS = []
all_RANKS = []
all_API = []
LABELS = []

for tag in tags:
    dfm = dfs[tag]
    LABELS.append(dfm.index[0])
    all_AI_HBM.append(float(dfm['Arithmetic Intensity']))
    all_FLOPS.append(float(dfm['FLOP/s']))
    all_RANKS.append(int(dfm['Rank']))
    all_API.append(int(dfm['Programming Model']))

roofline(all_FLOPS, all_AI_HBM, all_RANKS, all_API, LABELS, flag)
