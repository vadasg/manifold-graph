import pylab,numpy
from matplotlib.font_manager import fontManager, FontProperties


#set fonts here
font= FontProperties(size='small')
params = {'backend': 'ps',
          'axes.labelsize': 18,
          'xtick.labelsize': 16,
          'ytick.labelsize': 16,
          'legend.fontsize': 16,
          #'font.family': 'sans',
          'font.serif': ['Times','Palatino','serif'],
          'font.size': 16,
          'ps.usedistiller': 'xpdf',  
          }
pylab.rcParams.update(params)


#set figure size
csize=6 #inches = 2.95 used in chemosphere
fig_size=(csize,csize*1.618)
#adjust spacing


#yt = [0, 500, 1500, 2500, 3500]  #y axis ticks

fig = pylab.figure()

fig.subplots_adjust(top=0.95,bottom=0.1,left=0.10,right=0.93,hspace=0.35,wspace=0.2)

# this is plot 1 with Procut orange data


ax = fig.add_subplot(1,1,1)

diameters = [ 1, 1.63, 2, 2.43, 3, 3.26, 4, 4.87 ]
steps =[ '1', 'H', '2', 'J', '3', '2H', '4', '2J' ]
counts = [ 3, 184, 409, 2445, 1060, 582, 93, 11 ] 

diameters1= [ 1, 2, 3, 4, ]
counts1= [ 3, 409, 1060, 93 ] 

diameters2 = [ 1.63, 2.43, 3.26, 4.87 ]
steps2 =[ 'H', 'J', '2H', '2J' ]
counts2 = [ 184, 2445, 582, 11 ] 

#ax.plot(diameters,counts,'k--',alpha=0.5)
for d,c in zip(diameters1,counts1):
    ax.plot([d,d],[1,c],'k--')

for d,c,s in zip(diameters2,counts2,steps2):
    ax.plot([d,d],[2.3,c],'k--')
    ax.text(d,1.3,s,horizontalalignment='center')

ax.semilogy(diameters,counts,'ro')
#rects1 = ax.bar(ind+width, procutMeans, width, color='r', yerr=procutStd)
#rects1 = ax.bar(ind, procutMeans, width, color='r', yerr=procutStd)
# add some
ax.set_xlabel('Diameter')
#ax.xaxis.set_label_coords(0.5, -0.12)
ax.set_ylabel('Count (log scale)')
ax.set_title('Global statistics')
ax.set_xticks([0] + diameters + [5,6])
#ax.set_yticks(yt)
ax.set_xticklabels( ['0','1','','2','','3','','4','','5','6'], horizontalalignment='center')
a=ax.axis([0,6,1,numpy.max(counts)*5])



#ax.legend( ('Procut Orange',), loc=1 ) #add trailing comma to make it a tuple so full word is printed



pylab.savefig('./paper/figures/global_statistics.png', dpi=300)
pylab.show()
