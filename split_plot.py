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

fig.subplots_adjust(top=0.95,bottom=0.10,left=0.10,right=0.93,hspace=0.35,wspace=0.2)

# this is plot 1 with Procut orange data


ax = fig.add_subplot(1,1,1)

diameters = [ 1, 1.63, 2, 2.43, 3, 3.26, 4, 4.87 ]
steps =[ '1', 'H', '2', 'J', '3', '2H', '4', '2J' ]
counts = [ 3, 184, 409, 2445, 1060, 582, 93, 11 ] 
types = [ '$S^{3}/Q$',  '$L(4,1)$' ,'$L(3,1)$' ,'$RP^{3}$' ,'$S^{3}$' ]
markers = ['rs','ws','bx','ks','gs']

countd = {}
countd[ '$S^{3}/Q$'] = [ 0, 1, 0, 0, 0, 0, 0, 0 ]
countd[ '$L(4,1)$' ] = [ 0, 0, 0, 1, 0, 0, 0, 0 ]
countd[ '$L(3,1)$' ] = [ 0, 0, 1, 1, 0, 0, 0, 0 ]
countd[ '$RP^{3}$' ] = [ 0,10, 7, 5, 0, 0, 0, 0 ]
countd[ '$S^{3}$'  ]  = [ 3, 173, 401, 2438, 1060, 582, 93, 11 ]

#$1$ &  &  &  &   &3    & 3    \\
#$2$ & 1&  &1 &17 &574  & 593  \\
#$3$ &  &1 &1 &5  &3498 & 3505 \\
#$4$ &  &  &  &   &675  & 675   \\
#$5$ &  &  &  &   &11   & 11   \\
#Total&1 &1 &2 &22   &4761   &4787  \\




#ax.plot(diameters,counts,'k--',alpha=0.5)
for t,m in zip(types,markers):
    ax.semilogy(diameters,countd[t],m,ms=10,label=t,mew=1)
    for d,c,s in zip(diameters,counts,steps):
        ax.plot([d,d],[0.7,c],'k--')
    #    ax.text(d,c*1.5, s,horizontalalignment='center')

#rects1 = ax.bar(ind+width, procutMeans, width, color='r', yerr=procutStd)
#rects1 = ax.bar(ind, procutMeans, width, color='r', yerr=procutStd)
# add some
ax.set_xlabel('Diameter')
ax.set_ylabel('Count (log scale)')
ax.set_title('Global statistics')
ax.set_xticks(diameters)
#ax.set_yticks(yt)
ax.set_xticklabels( steps , horizontalalignment='center')
ax.axis([0,numpy.max(diameters)*1.1,0.7,numpy.max(counts)*5])
ax.legend(numpoints=1)


#ax.legend( ('Procut Orange',), loc=1 ) #add trailing comma to make it a tuple so full word is printed



pylab.savefig('./paper/figures/split_statistics.png', dpi=300)
pylab.show()
