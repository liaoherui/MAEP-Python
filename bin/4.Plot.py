#coding=utf-8
from __future__ import unicode_literals
##### Author : Liao Herui ######
##### E-mail : liaoherui@mail.dlut.edu.cn #######
import os
import re
import getopt
import sys
import rpy2.robjects as robjects
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.switch_backend('agg')
from pyecharts import Scatter,Overlap,Grid,Page,Line,Bar
#############  User Info #############################
######################################################
## How to use this pipeline	            	    ##		
##					    	    ##	 
## python 4.AR.py -v [overall] -s [sample_name_list]##
#############  Get  Option ###########################
opts,args=getopt.getopt(sys.argv[1:],"v:s:")
#fa_list=''
now=os.getcwd()
output=now+'/overall'  #[default]
overall='Y'
sl=''

for opt,arg in opts:
	if opt=="-v":
		overall=arg
	elif opt=='-s':
		sl=arg

if sl=='':
	print 'Please give the conf file sample_name list! This parameter is required!'
	exit()
print 'Plot Start ... ... ...'
#### Sample Name  List ######
fsn=open(sl,'r')
snl=[]
while True:
	line=fsn.readline().strip()
	if not line:break
	snl.append(line)

#############	Make  the output dir and the shell dir#############
for s in snl:
	if not os.path.exists('Plot/'+s):
		os.makedirs('Plot/'+s,0755)
if not os.path.exists('Log'):
	os.makedirs('Log',0755)
###### Over All N50 Value ##############################
if overall=='Y':
	#n50_all=[]
	#contig_name=[]
	if len(os.listdir('overall/quast'))<1:
		print 'Something wrong in overall quast...Please check...'
		exit()
	for filename1 in os.listdir('overall/quast'):
		n50_all=[]
	        contig_name=[]
		for filename in os.listdir('overall/quast/'+filename1):
			contig_name.append(filename)
			fo=open('overall/quast/'+filename1+'/'+filename+'/'+'report.txt','r')
			while True:
				line=fo.readline()
				if not line:break
				if re.search('N50',line):
		                        line=line.split()
	        	                n50=float(line[1])/float(1000)
					n50_all.append(n50)
		x=range(1,len(contig_name)+1)
		plt.figure(figsize=(12,6))
		plt.bar(x,n50_all,width=0.35,align='center',color='c',alpha=0.8)
		plt.xticks(x,contig_name,size='small',rotation=20)
		for a,b in zip(x,n50_all):
			plt.text(a, b+0.05, '%.0f' % b, ha='center', va= 'bottom',fontsize=7)
		plt.savefig('Plot/'+filename1+'/0.n50_overall.png')

####### Major Hash Generate #######
##### Start... ##########
####for coverage, this hash requires input list#########
co=open('Log/coverage.hash','r')
a=co.read()
cov=eval(a)


bq={}   #means bin quality ,eg: bq['zxy_pacbio_HGA']['High']=10 /bq['zxy'][zxy_pacbio_HGA]['completeness']['zxy_pacbio_HGA.001']=90.2
for s in snl:
	bq[s]={}
for filename in os.listdir('Tabel'):
	fb=open('Tabel/'+filename,'r')
	line=fb.readline()
	pre=re.split('\.',filename)[0]
	for s in snl:
		if pre not in bq[s]:
			if re.search(s,pre):
				bq[s][pre]={}
				bq[s][pre]['completeness']={}
				bq[s][pre]['contamination']={}
				bq[s][pre]['quality']={}
				bq[s][pre]['species']={}
				bq[s][pre]['N50']={}
	while True:
		s=''
		line=fb.readline().strip()
		if not line:break
		bin_name=line.split('\t')[0]
		quality=line.split('\t')[-1]
		completeness=line.split('\t')[1]
		contamination=line.split('\t')[2]
		species=line.split('\t')[7]
		N50=line.split('\t')[-3]
		species=re.sub('\(.*','',species)
		for sn in snl:
			if re.search(sn,line):s=sn
		#bq[s][pre][bin_name]={}
		if cov[pre]=='Null':
			bq[s][pre]['coverage']='Null'
		else:
			if 'coverage' not in bq[s][pre]:
				bq[s][pre]['coverage']={}
				bq[s][pre]['coverage'][bin_name]=cov[pre][bin_name]
			else:
				bq[s][pre]['coverage'][bin_name]=cov[pre][bin_name]
		bq[s][pre]['completeness'][bin_name]=float(completeness)
		bq[s][pre]['contamination'][bin_name]=float(contamination)
		bq[s][pre]['N50'][bin_name]=float(N50)
		bq[s][pre]['quality'][bin_name]=quality
		bq[s][pre]['species'][bin_name]=species
		if quality not in bq[s][pre]:
			bq[s][pre][quality]=1
		else:
			bq[s][pre][quality]+=1
##### Bin Figure ########
#### 1 . Bar Figure and Level Bar Figure ####
sp={}
for key1 in bq:
	if key1 not in sp:
		sp[key1]={}
	for key2 in bq[key1]:
		if key2 not in sp[key1]:
			sp[key1][key2]=[]
		for key3 in bq[key1][key2]['species']:
			#if bq[key1][key2]['quality'][key3]=='Low' or bq[key1][key2]['quality'][key3]=='Other':continue
			if bq[key1][key2]['species'][key3] not in sp[key1][key2]:
				sp[key1][key2].append(bq[key1][key2]['species'][key3])
			else:continue
osp=open('Log/sp.hash','w+')
osp.write(str(sp))
osp.close()

def bar(bq,outdir):
	bar=Bar("Bin质量分布柱形图","可点击分别查看other/low/medium/high Bin数量")
	tp=[]	
	num_other=[]
	num_low=[]
	num_medium=[]
	num_high=[]
	for key1 in bq:
		if 'Other' not in bq[key1]:
			bq[key1]['Other']=0
		if 'Low' not in bq[key1]:
	                bq[key1]['Low']=0
		if 'Medium' not in bq[key1]:
	                bq[key1]['Medium']=0	
		if 'High' not in bq[key1]:
	        	bq[key1]['High']=0
		tp.append(key1)		
		num_other.append(bq[key1]['Other'])
		num_low.append(bq[key1]['Low'])
		num_medium.append(bq[key1]['Medium'])
		num_high.append(bq[key1]['High'])
	bar.add('Other',tp,num_other)
	bar.add('Low',tp,num_low)
	bar.add('Medium',tp,num_medium)
	bar.add('High',tp,num_high,is_label_show=True,xaxis_rotate=20)
	bar.width=1200
	bar.height=600
	bar.render(outdir+'/1_bar.html')
	#bar.render('Pyechart/bin_bar.html')

	###Level Bar plot ######
	bar2=Bar("Bin数据堆叠柱状图","显示不同质量Bin占比组成\n\n")
	attr=[]
	other=[]
	low=[]
	medium=[]
	high=[]
	for key1 in bq:
		attr.append(key1)
		if 'Other' not in bq[key1]:
                        bq[key1]['Other']=0
                if 'Low' not in bq[key1]:
                        bq[key1]['Low']=0
                if 'Medium' not in bq[key1]:
                        bq[key1]['Medium']=0
                if 'High' not in bq[key1]:
                        bq[key1]['High']=0			
		total=bq[key1]['Other']+bq[key1]['Low']+bq[key1]['Medium']+bq[key1]['High']
		other.append(float(float(bq[key1]['Other'])/float(total)))	
		low.append(float(float(bq[key1]['Low'])/float(total)))
		medium.append(float(float(bq[key1]['Medium'])/float(total)))
		high.append(float(float(bq[key1]['High'])/float(total)))
	bar2.add('Other',attr,other,is_stack=True)	
	bar2.add('Low',attr,low,is_stack=True)
	bar2.add('Medium',attr,medium,is_stack=True)
	bar2.add('High',attr,high,is_stack=True,xaxis_rotate=20)
	bar2.width=1200
	bar2.height=600
	bar2.render(outdir+'/2_lb.html')

##### 2.Black(completeness) and Red(contamination) Scatter Plot ######
sc={}
#name=[]
def scatter(bq,output):
	page=Page()
	page.height=900
	c=0
	for key1 in bq:
		cp=[] #completeness
		ct=[] #contamination
		a=sorted(bq[key1]['completeness'].items(),key=lambda x:x[1],reverse=True)
		#c=0
		for e in a:
			cp.append(bq[key1]['completeness'][e[0]])
			ct.append(bq[key1]['contamination'][e[0]])
		c+=1
		x=range(1,len(cp)+1)
		#grid=Grid()
		#overlap = Overlap()
		#scatter = Scatter()
		#scatter2 = Scatter(key1)
		if c%2==0:
			#2
			if c%4!=0:
				overlap2 = Overlap()
		                scatter3 = Scatter()
				scatter3.add("Completeness",x,cp,yaxis_label_textcolor='red',yaxis_line_color='red',xaxis_type='category',xaxis_max=max(x),legend_pos="40%",legend_orient="vertical")
				scatter4 = Scatter(key1,title_pos="25%")
				scatter4.add('Contamination',x,ct,xaxis_type='category',xaxis_max=max(x),legend_pos="40%",legend_orient="vertical")
				overlap2.add(scatter4)
		                overlap2.add(scatter3)
			#4
			else:
				overlap4 = Overlap()
                                scatter7 = Scatter()
                                scatter7.add("Completeness",x,cp,yaxis_label_textcolor='red',yaxis_line_color='red',xaxis_type='category',xaxis_max=max(x),legend_pos="90%",legend_orient="vertical")
                                scatter8 = Scatter(key1,title_pos="75%")
                                scatter8.add('Contamination',x,ct,xaxis_type='category',xaxis_max=max(x),legend_pos="90%",legend_orient="vertical")
                                overlap4.add(scatter8)
                                overlap4.add(scatter7)
			#overlap2.render(output+'/3.scatter_o2.html')
		else:
			#1
			if (c+1)%4!=0:
				overlap = Overlap()
		                scatter = Scatter()
				scatter.add("Completeness",x,cp,yaxis_label_textcolor='red',yaxis_line_color='red',xaxis_type='category',xaxis_max=max(x),legend_pos="15%",legend_orient="vertical")
	                        scatter2 = Scatter(key1)
                        	scatter2.add('Contamination',x,ct,xaxis_type='category',xaxis_max=max(x),legend_pos="15%",legend_orient="vertical")
				overlap.add(scatter2)
				overlap.add(scatter)
			#3
			else:
				overlap3 = Overlap()
                                scatter5= Scatter()
                                scatter5.add("Completeness",x,cp,yaxis_label_textcolor='red',yaxis_line_color='red',xaxis_type='category',xaxis_max=max(x),legend_pos="65%",legend_orient="vertical")
                                scatter6= Scatter(key1,title_pos="50%")
                                scatter6.add('Contamination',x,ct,xaxis_type='category',xaxis_max=max(x),legend_pos="65%",legend_orient="vertical")
                                overlap3.add(scatter6)
                                overlap3.add(scatter5)
			#overlap.render(output+'/3.scatter_o1.html')
		'''
		if c==len(bq.keys()) and c%2!=0:
			grid=Grid()
                        grid.add(overlap,grid_left="60%")
			page.add(grid)
			continue
		'''
		if c%2==0:
			if c%4!=0:
				grid.add(overlap2,grid_left="55%",grid_width=250)
			else:
				grid.add(overlap4,grid_left="80%",grid_width=200)
                                page.add(grid)
			#grid.render(output+'/3.scatter.html')
			#page.render(output+'/3.scatter.html')
		else:
			if (c+1)%4==0:
				grid.add(overlap3, grid_left="30%",grid_width=250)
			else:
				grid=Grid()
				grid.width=1500
				grid.height=300
				grid.add(overlap,grid_left="5%",grid_width=250)
			#grid.render(output+'/3.scatter.html')
                        #page.render(output+'/3.scatter.html')
                        #exit()
	page.render(output+'/3_scatter.html')

###### 3.Upset Plot ########################################
def upset(sam,output): #sam -> sample_name
	pwd=os.getcwd()
	fu=open('Log/sp.hash','r')
	fr=open('Log/upset.R','w+')
	a=fu.read()
	d=eval(a)
	tem={}
	all_species={}
	m=0
	for key1 in d:
		at=[]
		tem=d[key1]
		for key2 in d[key1]:
                	for e in d[key1][key2]:
	                        if e not in at:
        	                        at.append(e)
	        all_species[key1]=at
	for key in d:
		inhash={}
		inhash['name']=[]
		al=all_species[key]
		for a in al:
			inhash['name'].append(a)
		for key2 in d[key]:
			inhash[key2]=[]
			for a in al:
				if a in d[key][key2]:
					inhash[key2].append(1)
				else:
					inhash[key2].append(0)
		frame=pd.DataFrame(inhash)
	        frame.to_csv('Log/'+key+'.csv', index=False, header=True)
	fr.write('library(UpSetR)\npng("'+pwd+'/'+output+'/4_upset.png",width=1200,height=800,res=72*2)\n')
	fr.write('frame<-read.csv("'+pwd+'/Log/'+sam+'.csv",header = TRUE, sep=",")\n')
	fr.write('upset(frame, nsets = 12, nintersects = 30,order.by = c("freq", "degree"), decreasing = c(TRUE,FALSE))\n')
	fr.write('dev.off()')
	fr.close()
	robjects.r.source('Log/upset.R')	
###### 4. Bin N50 and Coverage ########
def bin_per(bq,output):		
	cpd={} #eg {'Low':'zxy_pacbio-HGA':'coverage':[12.3,12,3,1.5,102.5]}
	cpd['High']={}
	cpd['Medium']={}
	cpd['Low']={}
	for key1 in bq:
		cpd['High'][key1]={}
		cpd['Medium'][key1]={}
		cpd['Low'][key1]={}
		if not bq[key1]['coverage']=='Null':
			cpd['High'][key1]['coverage']=[]
			cpd['Medium'][key1]['coverage']=[]
			cpd['Low'][key1]['coverage']=[]
		cpd['High'][key1]['N50']=[]
                cpd['Medium'][key1]['N50']=[]
                cpd['Low'][key1]['N50']=[]
		for key2 in bq[key1]['quality']:
			if bq[key1]['quality'][key2] in cpd:
				if not bq[key1]['coverage']=='Null':
					cpd[bq[key1]['quality'][key2]][key1]['coverage'].append(bq[key1]['coverage'][key2])
				cpd[bq[key1]['quality'][key2]][key1]['N50'].append(bq[key1]['N50'][key2])
	arr=['High','Medium','Low']
	#pagez=Page()
	for a in arr:
		line_pdf_n50=Line("折线图测试")
		for pre in cpd[a]:
			hist_N50,te = np.histogram(cpd[a][pre]['N50'])
			tem,bin_edges_N50 = np.histogram(cpd[a][pre]['N50'],bins=9)
			#hist_coverage,bin_edges_coverage = np.histogram(cpd[a][pre]['coverage'])
			#cdf_N50=np.cumsum(hist_N50/sum(hist_N50))
			#cdf_coverage=np.cumsum(hist_coverage/sum(hist_coverage))
			#line = Line("折线图测试")
			line_pdf_n50.add(pre,bin_edges_N50,hist_N50)
		line_pdf_n50.render('Log/line_test.html')
		
	
	
	
	
	
tem={}
for key1 in bq:
        tem=bq[key1]
	bar(tem,'Plot/'+key1)
	scatter(tem,'Plot/'+key1)
	upset(key1,'Plot/'+key1)
	#bin_per(tem,'Plot/'+key1)		

ob1=open('Log/br.html','w+')
ob1.write('<br/>\n<br/>\n<br/>\n<br/>\n<br/>\n')
oe=open('Merge_Plot.sh','w+')
ob3=open('Log/scatter_p.html','w+')
ob3.write('<p><a style="font-weight:bold;font-size:18px;">Bin\'s Completeness and Contamination(Scatter)</a></p>\n<br\>\n')
for s in snl:
	if overall=='Y':
		ob2=open('Log/'+s+'_img.html','w+')
		ob2.write('<p><a style="font-weight:bold;font-size:18px;">Overall N50(kb) Bar</a></p>\n<br\>\n')
		ob2.write('<img src="'+s+'/0.n50_overall.png" alt="Overall N50 "/>\n')
		ob2.write('<br/>\n<br/>\n<br/>\n<br/>\n<br/>\n')
	ob5=open('Log/'+s+'_upset.html','w+')
	ob5.write('<p><a style="font-weight:bold;font-size:18px;">Species Upset Comparison</a></p>\n<br\>\n')
	ob5.write('<img src="'+s+'/4_upset.png" alt="Species Upset"/>\n')
	ob5.write('<br/>\n<br/>\n<br/>\n<br/>\n<br/>\n')
	if not os.path.exists('Report/'+s):
		os.makedirs('Report/'+s,0755)
	if overall=='Y':
		os.system('cp Plot/'+s+'/0.n50_overall.png Report/'+s+'/0.n50_overall.png')
	os.system('cp Plot/'+s+'/4_upset.png  Report/'+s+'/4_upset.png')
	if overall=='Y':
		oe.write('cat Log/'+s+'_img.html '+' Plot/'+s+'/1_bar.html Log/br.html '+' Plot/'+s+'/2_lb.html Log/br.html Log/scatter_p.html  Plot/'+s+'/3_scatter.html   Log/'+s+'_upset.html >Report/'+s+'.html\n')
	else:
		oe.write('cat  Plot/'+s+'/1_bar.html Log/br.html '+' Plot/'+s+'/2_lb.html Log/br.html Log/scatter_p.html  Plot/'+s+'/3_scatter.html   Log/'+s+'_upset.html >Report/'+s+'.html\n')
