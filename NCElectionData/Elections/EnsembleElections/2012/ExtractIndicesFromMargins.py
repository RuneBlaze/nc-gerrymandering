import numpy as np 

#Get the number of elections in the Margin file
#filename = "3Dists.txt"
f=open('M.txt','r')
j=0
for line in f:
	j+=1;
f.close()
j=j/13

#Second loop: in this loop:
#(i) get the average for each sorted district to prep for the gerrymandering index
#(ii) get the interpolated zero for the fine histogram and output to a file for each election
#(iii) get the mean value for the above index

precs = np.zeros(13);
means = np.zeros(13);
fin=open('margins.txt','r')
foutFH1=open('fineHist1.txt','w')
foutWst=open('wastedVote.txt','w')
foutEg=open('egapinlit.txt','w')
meanContinuousNoRepubElected  = 0;

for i in range(j):
	for k in range(13):
		prec = float(fin.readline().split()[1]);
		means[k]+=prec;
		precs[k] =prec;
	#find the continuous value for dems elected
	l = 0;
	while precs[l]<0.5:
		l+=1;
	contNoRepubElected  = l + (0.5-precs[l-1])/(precs[l]-precs[l-1]);
	meanContinuousNoRepubElected += contNoRepubElected
	foutFH1.write(str(contNoRepubElected));
	foutFH1.write("\n");
	#calculate the wasted vote index
	totD=0; totR=0
	wstD=0; wstR=0
	for k in range(13):
		totD+=precs[k]; totR+=1-precs[k]
		if precs[k]<0.5:
			wstR+=(1-precs[k])-0.5;
			wstD+=precs[k]
		else:
			wstD+=precs[k]-0.5;
			wstR+=(1-precs[k])
	effgap = wstD/totD-wstR/totR
	effgap2= (wstD-wstR)/13.0
	foutWst.write(str(effgap))
	foutWst.write("\n")
	foutEg.write(str(effgap2))
	foutEg.write("\n")

for k in range(13):
	means[k]*=1.0/float(j);
print means

meanContinuousNoRepubElected*=1.0/float(j);
print meanContinuousNoRepubElected

fin.close()
foutFH1.close()
foutWst.close()
foutEg.close()

#thrid time through
fin=open('M.txt','r')
foutG=open('gInd.txt','w')
foutR=open('rInd.txt','w')
for i in range(j):
	gind = 0
	for k in range(13):
		prec = float(fin.readline().split()[1]);
		gind+= (means[k]-prec)**2
		precs[k]=prec
	foutG.write(str(np.sqrt(gind)))
	foutG.write("\n")
	#get rep ind
	l=0
	while precs[l]<0.5:
		l+=1;
	contNoRepubElected  = l + (0.5-precs[l-1])/(precs[l]-precs[l-1]);
	repind = contNoRepubElected-meanContinuousNoRepubElected
	#print contNoRepubElected, meanContinuousNoRepubElected, contNoRepubElected-meanContinuousNoRepubElected
	foutR.write(str(repind))
	foutR.write("\n")
fin.close()
foutG.close()
foutR.close()

