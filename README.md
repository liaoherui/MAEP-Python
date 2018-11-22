MAEP(Metagenomics Assebly Evaluation Pipeline)
==============

### Author: Liao Herui
### E-mail: liaoherui@mail.dlut.edu.cn

--------------

### Abstract
MAEP is a new version of LAEP and can be used to evaluate the assembly quality of metagenomics 
data(especially from the different sequencing platforms and different assembly strategies).By the
way ,this pipeline can support multiple samples parallel evaluation.<BR/><BR/>
**However,MAEP can only run on KMBGI's server.It will be updated to run on other servers soon after.**

### Manuals
* Step 1: Finish the MAEP.conf profile
* Step 2: Python go.1.py.Then,sh overall/qsub.sh and sh Submit/qsub.sh.Wait until jobs finish.
* Step 3: Python go.2.py

### Output(part)
* 1.Overall contig N50 value
* 2.Bin quality bar plot.(Build with pyechart)
* 3.Bin quality stack bar plot.(Build with pyechart)
* 4.Bin completeness/contamination scatter plot.(Build with pyechart)
* 5.Species upset plot.(Build with R)
**You can download the output_example dir to have a look at the output report.**

