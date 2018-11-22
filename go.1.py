#### The begining of LAEP pipeline #############
#### Author : Liao Herui      ##################
#### E-mail : liaoherui@mail.dlut.edu.cn #######
import re
import os 
#### Go ! ####################################
pwd=os.getcwd()
f=open('MAEP.conf','r')
conf={}
while True:
	line=f.readline().strip()
	if not line:break
	if re.search('#',line):continue
	ele=line.split('=')
	ele[0]=ele[0].strip()
	ele[1]=ele[1].strip()
	if ele[0] not in conf:
		conf[ele[0]]=ele[1]
if not  re.search('/',conf['output']):
	conf['output']=pwd+'/'+conf['output']
if conf['overall']=='Y':
	os.system('python bin/0.overall.py -l '+conf['contig_list']+' -s '+conf['sample_name'])
if conf['step12']=='Y':
	os.system('python bin/1.AR.py -l '+conf['bin_list']+' -o '+conf['output'])
#if conf['run']=='Y':
if conf['step12']=='Y':
	os.system('python bin/2.Run.py -o '+conf['output']+' -a '+conf['all_big'])
#os.system('python bin/3.ER.py')


	


