import Table

fin = open('output.txt','r')
fout = open('./paper/bigtable.tex','w')

all = fin.readlines()
fin.close()
for i in range(len(all)):
    all[i] = all[i].replace(' ','$',1).replace(' ','$ $',1).replace('$',' $',1).replace('\n','$\n')
    all[i] = all[i].replace('E','')
    all[i] = all[i].replace('1H','H')
    all[i] = all[i].replace('1J','J')
    print all[i].split()
    print '\n'

max = len(all)
N = 5
extra = 1

chunks = [all[x:x+max/(N)+extra] for x in xrange(0,len(all),max/(N)+extra)]
chunks[-1] = chunks[-1] + ['']*(len(chunks[-2])-len(chunks[-1]))
for c in chunks:
    print len(c)

print len(chunks)


t = Table.Table(N, justs='l'*N, caption='Awesome results', label="tab:full")
t.add_header_row(['HEAD']*N)

t.add_data(chunks)
t.print_table(fout)
fout.close()
gin = open('./paper/bigtable.tex','r')
raw = gin.readlines()
gin.close()
out = ''
fout = open('./paper/bigtable.tex','w')

head = '$N$ & $t$ & $d$ &' * N
for i in raw:
    fout.write(i.replace(r'\begin{deluxetable}{'+'l'*N+'}',r'\begin{deluxetable}{'+'|llr|'*N+'}').replace('$ $','$ & $').replace(r'\tablecolumns{'+str(N)+'}',r'\tablecolumns{'+str(N*3)+'}').replace(' $',' & $',1).replace(r'\colhead{HEAD} & \colhead{HEAD} & \colhead{HEAD} & \colhead{HEAD} & \colhead{HEAD}',head[:-1] ))
fout.close()
