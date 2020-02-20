import matplotlib.pyplot as plt
import numpy as np
from kenpompy.utils import login
from kenpompy.summary import get_pointdist
import pandas as pd
import math
import datetime
import pickle as pl
from Login.vars import kpUser, kpPass

gameDate = datetime.date.today()

byDate = gameDate.strftime("%b %d, %Y")

browser = login(kpUser, kpPass)
pd = get_pointdist(browser, season = None)

Off_FT = []
Off_2P = []
Off_3P = []
Off_FTstr = []
Team = []


#Get point distribution data from KenPom
for i in range(len(pd['Off-FT'])):
    try:
        Off_FT.append(float(pd['Off-FT'][i]))
        Off_2P.append(float(pd['Off-2P'][i]))
        Off_3P.append(float(pd['Off-3P'][i]))
        Off_FTstr.append(pd['Off-FT'][i])
        Team.append(pd['Team'][i])
    except KeyError:
        continue
 

# create variables
x = Off_2P 
y = Off_3P
names = Team
z = [.00001*Off_FT[i]**5.3 for i in range(len(x))]

cmap = plt.cm.RdYlGn

fig,ax = plt.subplots()
plt.xlabel('Percentage of Team Points from Two Pointers')
plt.ylabel('Percentage of Team Points from Three Pointers')
# plt.legend(loc="upper left")
# plt.legend(
#            labels  = ['Line', 'Sine', 'Arcsine'])
plt.title(f'2020 NCAA Offensive Team Point Distribution as of {byDate}')
sc = plt.scatter(x, y, s=z, alpha=.8, cmap='Reds', c=z, edgecolors="grey", linewidth=2)

annot = ax.annotate("", xy=(0,0), xytext=(20,20),textcoords="offset points",
                    bbox=dict(boxstyle="round", fc="w"),
                    arrowprops=dict(arrowstyle="->"))
annot.set_visible(False)


#Set hover values
def update_annot(ind):

    pos = sc.get_offsets()[ind["ind"][0]]
    annot.xy = pos
    text = "Percentage from Free Throws: {}, {}".format(" ".join([Off_FTstr[n] for n in ind["ind"]]), 
                           " ".join([names[n] for n in ind["ind"]]))
    annot.set_text(text)
    annot.get_bbox_patch().set_facecolor(cmap(z[ind["ind"][0]]))
    annot.get_bbox_patch().set_alpha(0.8)

#Set hover functionality
def hover(event):
    vis = annot.get_visible()
    if event.inaxes == ax:
        cont, ind = sc.contains(event)
        if cont:
            update_annot(ind)
            annot.set_visible(True)
            fig.canvas.draw_idle()
        else:
            if vis:
                annot.set_visible(False)
                fig.canvas.draw_idle()

fig.canvas.mpl_connect("motion_notify_event", hover)

plt.show()



