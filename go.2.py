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
#os.system('python bin/1.AR.py -l '+conf['bin_list']+' -o '+conf['output'])
#if conf['run']=='Y':
#os.system('python bin/2.Run.py -o '+conf['output']+' -r '+conf['run'])
os.popen('python bin/2.5.generate_list.py -o '+conf['output']+' -g '+conf['generate_list'])
if conf['step3']=='Y':
	os.system('python bin/3.ER.py -o '+conf['output']+' -g '+conf['generate_list'])
if conf['step4']=='Y':
	os.system('python bin/4.Plot.py -v '+conf['overall']+' -s '+conf['sample_name'])



	


