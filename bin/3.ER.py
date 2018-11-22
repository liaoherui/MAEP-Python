#### Author : Liao Herui ######
#### E-mail : liaoherui@mail.dlut.edu.cn ########
import os
import re
import gzip
import random
import getopt
import time
import sys
#######sub function###############
def motify(line,which):
	level3=''
        ele=re.split('/',line)
	if which=='checkm':
		name=ele[-5]
	        return name
	elif which=='coverage':
		if re.search('barcode',ele[6]):
			 level2='b'
		else:level2='r'
		ele2=re.split('_',ele[7])
		if len(ele2)>2:
			level3+=str(ele2[1])+str(ele2[2])
		if len(ele2)==2:
			level3+=str(ele2[1])
		name='a'+level2+'_'+level3
		if re.search('idba',line):
                        name='idba'
		if re.search('megahit',line):
                        name='megahit'
                if re.search('spades',line):
                        name='spades'
                return name	
	else:
		name=ele[-4]
		return name

def suiji(s,d):
        strs=[]
        strs.append(s)
        strs.append(d)
        n=random.randint(0,len(strs)-1)
        return strs[n]
##################################
##### Get Option #################
opts,args=getopt.getopt(sys.argv[1:],"o:g:")
pwd=os.getcwd()
output=pwd+'/Result'  #[default]
crun='N'   #[default without coverage]
gl='Y'   #[defalut]
for opt,arg in opts:
        if opt=="-o":
                output=arg
	elif opt=='-g':
		gl=arg
#### List Generate #############
'''
if not gl=='N':
        #### Checkm list ####
        os.system('find '+output+' -name \'checkm\' >checkm.list')
        fc=open('checkm.list','r')
        oc=open('list/checkm.list','w+')
        while True:
                line=fc.readline().strip()
                if not line:break
                oc.write(line+'/result'+'\n')
        fc.close()
        os.system('rm checkm.list')
        #### Aragorn list ####
        a=os.popen('find '+output+' -name \'aragorn\' > list/aragorn.list | echo \'aragorn_list done\'').read().strip()
	print a
        #### Barrnap list ####
        b=os.popen('find '+output+' -name \'barrnap\' > list/barrnap.list| echo \'barrnap_list done\'').read().strip()
	print b
        #### Quast list ####
        q=os.popen('find '+output+' -name \'quast\' > list/quast.list| echo \'quast_list done\'').read().strip()
	print q
        #### Kraken list ####
        k=os.popen('find '+output+' -name \'kraken\' > list/kraken.list| echo \'kraken_list done\'').read().strip()
	print k
'''
##### Main ######################
result={}
class1=[]

for filename1 in os.listdir(output):
	if re.search('_',filename1):
		class1.append(filename1)
		result[filename1]={}
for c in class1:
	for filename2 in os.listdir(output+'/'+c):
		result[c][filename2]={}
###	checkm	########
f1=open('list/checkm.list','r')
while True:
	line=f1.readline()
	if not line:break
	line=line.strip()
	c=motify(line,'checkm')
	f1_s=open(line,'r')
	while True:
		line=f1_s.readline()
		if not line:break
		line=line.strip()	
		if re.search('-',line) or re.search('Marker',line):
			#print line
			continue
		#if re.search(post,line.lower()) or re.search(post,line):
		else:
			ele=line.split()
			result[c][ele[0]]['completeness']=ele[12]	
			result[c][ele[0]]['contamination']=ele[13]
#print result
###	aragorn	#########
f2=open('list/aragorn.list','r')
while True:
	line=f2.readline()
	if not line:break
	line=line.strip()
	ele=line.split('/')
	b=ele[-3]
	c=motify(line,'aragorn')	
	f2s=open(line+'/result.txt','r')
	while True:
		line2=f2s.readline()
		if not line2:break
		if re.search('Total',line2) and re.search('tRNA',line2):
			nums=re.split('=',line2)
			num=nums[1].strip()
			result[c][b]['tRNA_Num']=num
		elif re.search('Number of tRNA genes',line2):
			nums=re.split('=',line2)
                        num=nums[1].strip()
                        result[c][b]['tRNA_Num']=num
		else:
			continue
	if 'tRNA_Num' not in result[c][b]:
		print c+' '+b
###	barrnap	#########
f3=open('list/barrnap.list','r')
while True:
	line=f3.readline()
	if not line:break
	line=line.strip()
	ele=line.split('/')
	b=ele[-3]
	c=motify(line,'barrnap')
	f3_s=open(line+'/result.txt','r')
	s5=[]
	s23=[]
	s16=[]
	while True:
		line=f3_s.readline()
		if not line:break
		line=line.strip()
		if re.search('23S_rRNA',line):
			s23.append(line)
		elif re.search('16S_rRNA',line):
			s16.append(line)
		elif re.search('5S_rRNA',line):
			s5.append(line)
	if len(s5)>1 or len(s5)==1:
		result[c][b]['5S_RNA']='yes'
	else:
		result[c][b]['5S_RNA']='no'
	if len(s23)>1 or len(s23)==1:
                result[c][b]['23S_RNA']='yes'
        else:
                result[c][b]['23S_RNA']='no'
	if len(s16)>1 or len(s16)==1:
                result[c][b]['16S_RNA']='yes'
        else:
                result[c][b]['16S_RNA']='no'
####	kraken	############################		
f4=open('list/kraken.list','r')
while True:
	line=f4.readline()
	line=line.strip()
	test=line
	line=re.sub('\n','',line)
	if not line:break
	ele=line.split('/')
	b=ele[-3]
	c=motify(line,'kraken')
	f4_s=open(line+'/result.report','r')
	#species variable
	percent=[]
	ps={}
	species=[]
	cv={}
	th={}
	#genus variable
	percent2=[]
	ps2={}
	species2=[]
        cv2={}
        th2={}
	#phylum variable
	percent3=[]
        ps3={}
        species3=[]
        cv3={}
        th3={}
	while True:
		line=f4_s.readline()
		if not line:break
		ele=line.split('\t')	
		if ele[3]=='S':
			cv[float(ele[0])]=ele[0]
			if ele[5].strip() not in th:
                                th[ele[5].strip()]=int(ele[2])
                        else:
                                print ele[5]+' appears more than one time!!!'
			if ele[0] not in percent:
				percent.append(float(ele[0]))
			if ele[5] not in species:
				species.append(ele[5].strip())
			if ele[0] not in ps:
				ps[ele[0]]=ele[5].strip()
			else:
				if int(ele[2])>th[ps[ele[0]]]:
					ps[ele[0]]=ele[5].strip()
					continue
				elif int(ele[2])<th[ps[ele[0]]]:
					continue
				else:
					ps[ele[0]]=suiji(ele[5].strip(),ps[ele[0]])
		elif ele[3]=='G':
			cv2[float(ele[0])]=ele[0]
                        if ele[5].strip() not in th2:
                                th2[ele[5].strip()]=int(ele[2])
                        else:
                                print ele[5]+' appears more than one time!!!'
                        if ele[0] not in percent2:
                                percent2.append(float(ele[0]))
                        if ele[5] not in species2:
                                species2.append(ele[5].strip())
                        if ele[0] not in ps2:
                                ps2[ele[0]]=ele[5].strip()
                        else:
                                if int(ele[2])>th2[ps2[ele[0]]]:
                                        ps2[ele[0]]=ele[5].strip()
                                        continue
                                elif int(ele[2])<th2[ps2[ele[0]]]:
                                        continue
                                else:
                                        ps2[ele[0]]=suiji(ele[5].strip(),ps2[ele[0]])
		elif ele[3]=='P':
			cv3[float(ele[0])]=ele[0]
                        if ele[5].strip() not in th3:
                                th3[ele[5].strip()]=int(ele[2])
                        else:
                                print ele[5]+' appears more than one time!!!'
                        if ele[0] not in percent3:
                                percent3.append(float(ele[0]))
                        if ele[5] not in species3:
                                species3.append(ele[5].strip())
                        if ele[0] not in ps3:
                                ps3[ele[0]]=ele[5].strip()
                        else:
                                if int(ele[2])>th3[ps3[ele[0]]]:
                                        ps3[ele[0]]=ele[5].strip()
                                        continue
                                elif int(ele[2])<th3[ps3[ele[0]]]:
                                        continue
                                else:
                                        ps3[ele[0]]=suiji(ele[5].strip(),ps3[ele[0]])
		else:continue
	p=sorted(percent)
	p2=sorted(percent2)
	p3=sorted(percent3)
	if not any(p):
		result[c][b]['largest_species']='Null'
	        result[c][b]['species_num']='0'
	else:
		result[c][b]['largest_species']=ps[cv[p[-1]]]+'('+cv[p[-1]].strip()+')'
	        result[c][b]['species_num']=str(len(species))
	if not any(p2):
		result[c][b]['largest_genus']='Null'
	        result[c][b]['genus_num']='0'
	else:
		result[c][b]['largest_genus']=ps2[cv2[p2[-1]]]+'('+cv2[p2[-1]].strip()+')'
	        result[c][b]['genus_num']=str(len(species2))
	if not any(p3):
		result[c][b]['largest_phylum']='Null'
	        result[c][b]['phylum_num']='0'
	else:
		result[c][b]['largest_phylum']=ps3[cv3[p3[-1]]]+'('+cv3[p3[-1]].strip()+')'
	        result[c][b]['phylum_num']=str(len(species3))

####	quast	#############################	
f5=open('list/quast.list','r')
while True:
	line=f5.readline()
	if not line:break
	line=line.strip()
	ele=line.split('/')
	b=ele[-3]
	c=motify(line,'quast')
	f5_s=open(line+'/report.txt','r')	
	while True:
		line=f5_s.readline()
		line2=line
		#line=line.strip()
		if not line:break	
		if re.search('N50',line):
			line=line.split()
			n50=line[1]
			result[c][b]['N50']=n50
		if re.search('Total',line2) and not re.search('\(',line2):
			line4=line2.split()
			tl=line4[2]
			result[c][b]['total_length']=tl

####	coverage	####################
if crun=='Y':
	f6=open('list/coverage.list','r')
	while True:
		line=f6.readline()
		if not line:break
		line=line.strip()
		c=motify(line,'coverage')
		find_fa=re.split('/',line)
		fa=re.split('_',find_fa[7])
		fa=fa[:-1]
		fa='_'.join(fa)
		fa_s=re.split('_',c)
		fa=fa_s[0]+'_'+fa
		f6_s=open(line,'r')	
		n={}
		cc={}
		coverage={}
		while True:
			line=f6_s.readline()
			line=line.strip()
			if not line:break
			ele=line.split()
			if ele[0] not in cc:
				cc[ele[0]]=float(ele[1])
				n[ele[0]]=1
			else:
				cc[ele[0]]+=float(ele[1])
				n[ele[0]]+=1
		#for key in cc:
			#coverage[key]='%.2f'%(cc[key]/n[key])
		if c=='ar_1':fa_dir='/home/zhanglu/assmebly_result/10X/athena/read_sub/maxbin_1'
		if c=='ar_12':fa_dir='/home/zhanglu/assmebly_result/10X/athena/read_sub/maxbin_1_2'
		if c=='ar_14':fa_dir='/home/zhanglu/assmebly_result/10X/athena/read_sub/maxbin_1_4'
		if c=='ar_18':fa_dir='/home/zhanglu/assmebly_result/10X/athena/read_sub/maxbin_1_8'
		if c=='ab_12':fa_dir='/home/zhanglu/assmebly_result/10X/athena/barcode_sub/maxbin_1_2'
		if c=='ab_14':fa_dir='/home/zhanglu/assmebly_result/10X/athena/barcode_sub/maxbin_1_4'
		if c=='ab_18':fa_dir='/home/zhanglu/assmebly_result/10X/athena/barcode_sub/maxbin_1_8'
		for filename_fa in os.listdir(fa_dir):
			if re.search('fasta',filename_fa):
				f6_ss=open(fa_dir+'/'+filename_fa,'r')
				cont=[]
				cov=0
				cov=float(cov)
				a=0
				while True:
					line=f6_ss.readline()
					if not line:break
					line=line.strip()
					if re.search('>',line):
						co=re.sub('>','',line)
						cont.append(co)
				for g in cont:
					cov+=float(cc[g])
					a+=n[g]
				cov='%.2f'%(cov/a)
				b=re.split('\.',filename_fa)
				b=b[:-1]
				b='.'.join(b)
				result[c][b]['coverage']=cov
####	quality #########
for key1 in result:
	for key2 in result[key1]:
		if float(result[key1][key2]['completeness'])>90.0 and float(result[key1][key2]['contamination'])<5.0 and (int(result[key1][key2]['tRNA_Num'])>18 or int(result[key1][key2]['tRNA_Num'])==18 ) and result[key1][key2]['5S_RNA']=='yes' and result[key1][key2]['16S_RNA']=='yes' and result[key1][key2]['23S_RNA']=='yes':
			result[key1][key2]['quality']='High'
		elif (float(result[key1][key2]['completeness'])>50.0 or float(result[key1][key2]['completeness'])==50.0) and float(result[key1][key2]['contamination'])<10.0:
			result[key1][key2]['quality']='Medium'
		elif float(result[key1][key2]['completeness'])<50.0 and float(result[key1][key2]['contamination'])<10.0:
                        result[key1][key2]['quality']='Low'
		else:	result[key1][key2]['quality']='Other'

####	Make Output File	#########
if crun=='Y':
	feature=['completeness','contamination','tRNA_Num','5S_RNA','16S_RNA','23S_RNA','largest_species','species_num','largest_genus','genus_num','largest_phylum','phylum_num','N50','total_length','coverage','quality']
else:
	feature=['completeness','contamination','tRNA_Num','5S_RNA','16S_RNA','23S_RNA','largest_species','species_num','largest_genus','genus_num','largest_phylum','phylum_num','N50','total_length','quality']
if not os.path.exists('Tabel'):
                os.makedirs('Tabel',0755)
for key1 in result:
	#if not os.path.exists('Result/'+key1):
		#os.makedirs('Result/'+key1,0755)
	o=open('Tabel/'+key1+'.bins.result','w+')
	if crun=='Y':
		o.write('bins_name\tcompleteness\tcontamination\ttRNA_Num\t5S_RNA\t16S_RNA\t23S_RNA\tlargest_species\tspecies_num\tlargest_genus\tgenus_num\tlargest_phylum\tphylum_num\tN50\ttotal_length\tcoverage\tquality\n')
	else:
		o.write('bins_name\tcompleteness\tcontamination\ttRNA_Num\t5S_RNA\t16S_RNA\t23S_RNA\tlargest_species\tspecies_num\tlargest_genus\tgenus_num\tlargest_phylum\tphylum_num\tN50\ttotal_length\tquality\n')
	for key2 in result[key1]:
		o.write(key2)
		for fe in feature:
			o.write('\t'+result[key1][key2][fe])
		o.write('\n')
