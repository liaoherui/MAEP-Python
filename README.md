MAEP(Metagenomics Assebly Evaluation Pipeline)
==============


### E-mail: liaoherui@mail.dlut.edu.cn
### Version: V2.0

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

### Output
There are two parts of output.One is report(.html),another is literature figure.

Report Part:<BR/><BR/>
1.Overall contig N50 value
<p align="center">
  <img src="img/1.png" alt="Overall N50 example"/>
</p>

2.Bin quality bar plot.(Build with pyechart)
<p align="center">
  <img src="img/2.png" alt="Bin quality bar example"/>
</p>

3.Bin quality stack bar plot.(Build with pyechart)
<p align="center">
  <img src="img/3.png" alt="Bin quality bar stack example"/>
</p>

4.Bin completeness/contamination scatter plot.(Build with pyechart)
<p align="center">
  <img src="img/4.png" alt="Scatter example"/>
</p>

5.Genus/Species upset plot.(Build with R)
<p align="center">
  <img src="img/5.png" alt="Species upset example"/>
</p>

6.Bins N50 and coverage.(Overall and each bin)

<p align="center">
  <img src="img/6.1.png" alt="Overall Bins N50 and coverage"/>
</p>
<p align="center">
  <img src="img/6.2.png" alt="Bins N50 and coverage"/>
</p>

7.Genus/Species abundance stack bar.
<p align="center">
  <img src="img/7.1.png" alt="Genus abundance example"/>
</p>
<p align="center">
  <img src="img/7.2.png" alt="Species abundance example"/>
</p>

**For more details,you can download the  new_output_example dir to have a look at the output report and figure.**

