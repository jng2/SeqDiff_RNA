# Pipeline for Differential Gene Expression Analysis of RNA-Seq Data. 
![](https://github.com/jng2/SeqDiff_RNA/blob/master/DiffExpressionPipeline.jpg)

Based on experimental results from the [Cavanaugh Lab](https://cavanaughlab.weebly.com) at Loyola University Chicago.

## Important Notes
Will only work on a machine running LINUX or MacOS.  [Python3.6](https://www.python.org/downloads/release/python-365/)
 and [R](https://cran.r-project.org/mirrors.html) are needed.

STAR, Python and R must be added to your system's global environment PATH.

Links to help you add these programs for [MacOS](https://www.architectryan.com/2012/10/02/add-to-the-path-on-mac-os-x-mountain-lion/#.Uydjga1dXDg) and [LINUX](https://www.youtube.com/watch?v=lhDiQZdUQRI)

## FastQC for quality control
Download FastQC from https://www.bioinformatics.babraham.ac.uk/projects/download.html#fastqc
Drag and Drop files into FastQC to determine quality of data
If per base sequence content is uneven at the beginning this is due to primers and is okay.  You can cut this area out of the sequence, but leaving it in will not alter the results of the differential expression analysis. 
If per sequence GC content is uneven, this is okay because the _Drosophila melanogaster_ genome has a GC bias
The sequence duplication levels may be high.  This is because RNA-Seq libraries contain transcripts of exons that occur at various frequencies. This step is done manually because it is more user-friendly and useful to visualize the data to determine the quality of the sequences to be used in the pipeline. 


## Bioconductor Metadata Input File Format

It is important that the Metadata is formatted properly in order for Bioconductor to run properly. Here is an [example of the proper format](https://github.com/jng2/SeqDiff_RNA/blob/master/metadata.txt):
````
File,Time,Group,Run
C_3W_A_USR16088998L_HHFWCBBXX_L5_1,3W,Control,C_3W_A_USR16088998L_HHFWCBBXX_L5_1
````
In this example, the file name is C_3W_A_USR16088998L_HHFWCBBXX_L5_1, it is from the 3 week time point, in the control group, and run is the file name repeated.


## Cloning or Downloading Repository from Github

To clone or download this repository, click clone or download on the main page of this github repository. 

## Additional tips for running from command line
To run a program from the command line, you must navigate to the folder where the program is located or enter the full path to said program. When you open the command line, you will be located within your user directory/folder. You can get a list of the files and other directories within the current directory by typing 'ls' in to the command line. You can also find out what the path to your current directory by typing 'pwd'. To enter into any of the directories listed by 'ls', you can type 'cd x', replacing 'x' with an actual directory name, such as "Documents'. It is recommended you place your files somewhere easy to find, within a folder close to your home(~) directory. For the first example below, the full path to our encompassing would be ~/Documents/ExampleRun/.  In some operating systems it is possible to drag and drop files onto the command line and it will automatically write the full path to that file. 

For each argument, if you aren't currently located within the directory containing your file, you must provide the full path to said file. For example: ~/Documents/myfile.gtf

It is recommended that you:
- Create a folder for each unique species differential expression project 
- Designate folders for output and metadata within project folder
- Put all of the fastq files you wish to run within a single folder. 
- Add the optional arguments --NoStarGenome if you have generated a STAR genome and --NoStarAlignment if you have aligned your fastq files to your reference genome. This will significantly reduce the time for a run. 

## Python Wrapper
After completing quality control locally. Data files can be input into the python wrapper, [zorya.py](https://github.com/jng2/SeqDiff_RNA/blob/master/zorya.py) that will run through every other step of the differential expression pipeline. In order to run the pipeline, in terminal on a mac or command prompt on a windows computer, type the following command:
```
python3 zorya.py fq fa gtf out meta --NoStarGenome --NoStarAlignment --UseParser
```

The following arguments for the python wrapper are for the following pieces of information:
* **fq**: the fastq file or directory(compressed or not) containing all fastq files
* **fa**: the fasta file containing the reference genome
* **gtf**: the gtf file containing the gtf gene annotation for the reference genome (note: the fasta and gtf files for the reference genome should be obtained from the same source to avoid difficulties with STAR alignment)
* **out**: the output directory
* **meta**: metadata csv file path (file construction process shown below)
* **--NoStarGenome**: add this argument if you have previously set up a STAR genome (this step takes a long time, so adding this argument allows you to skip it if it has already been completed)
* **--NoStarAligmnent**: add this argument if you have previously aligned the fastq files to the reference genome (this step takes a long time, so adding this argument allows you to skip it if it has already been completed)
* **--UseParser**: if MyGene no longer can retrieve information from FlyBase (due to FlyBase transitioning to a paid database) 

Example: Run named "ExampleRun" w/ Folder of fastq files 
```
python3 zorya.py ~/Documents/Zorya/ExampleRun/Fastqs/ ~/Documents/Zorya/ExampleRun/my_organism.fasta ~/Documents/Zorya/ExampleRun/annotation.gtf ~/Documents/Zorya/ExampleRun/Output/ ~/Documents/Zorya/metadata.csv
```

Example: Run named "ExampleRun2" w/ single fastq
```
python3 zorya.py ~/Documents/Zorya/ExampleRun2/my_organism.fastq ~/Documents/Zorya/ExampleRun2/my_organism.fasta ~/Documents/Zorya/ExampleRun2/annotation.gtf ~/Documents/Zorya/ExampleRun2/Output/ ~/Documents/Zorya/ExampleRun2/metadata.csv
```

## Final Bioconductor Output

The final Bioconductor output is a csv file containing the following information: 
* **X**: gene name
* **baseMean**: average of the normalized count values divided by the size of factors, taken over all samples in the _DESeqDataSet_
* **log2FoldChange**: effect size estimate, how much a gene's expression has changed between groups 
* **lfcSE(logfoldchangeStandardError)**: estimate of uncertainty of the effect size estimate
* **stat**: Wald statistic
* **p-value**: Wald test p-value, the probability that the fold change is as strong as the observed one or stronger given the null hypotheses
* **padj**: Benjamini-Hochberg adjusted p-value, lowered false discovery rate
* **symbol**: gene symbol obtained from MyGene database
* **type**: gene type obtained from MyGene database

**Example:**

| X | baseMean | log2FoldChange | lfcSE | stat | p-value | padj | symbol | type |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| FBgn0024897 | 122.142693644405 | -1.40124063594649 | 0.272652681194509 | -5.1392879388076 | 2.75781528244776e-07 | 0.00105893212307788 | b6 | protein-coding |

More details on the output can be found [here](http://www.bioconductor.org/help/workflows/rnaseqGene/#building-the-results-table) in section 6.2, building the results table.

The Bioconductor output will also include a volcano plot like the one shown below.  A volcano plot is a scatterplot that combines magnitude of change and a measure of statistical significance in order to identify data points with large magnitude changes that are statistically significant. In the plot below, the red dots indicate the statistically significant differentially expressed genes between the week 3 control and jet lagged groups. The blue lines indicate the threshold of fold change of differential expression a gene must reach and the green line indicates the threshold of the p-value related this gene must be under for the differential expression to be significant. 
![](https://github.com/jng2/SeqDiff_RNA/blob/master/Week3Volanco.PNG)
