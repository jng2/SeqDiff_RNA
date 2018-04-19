# Pipeline for Differential Gene Expression Analysis of RNA-Seq Data. 
![](https://github.com/jng2/SeqDiff_RNA/blob/master/DiffExpressionPipeline.jpg)

Based on experimental results from the [Cavanaugh Lab](https://cavanaughlab.weebly.com) at Loyola University Chicago.

## FastQC for quality control
Download FastQC from https://www.bioinformatics.babraham.ac.uk/projects/download.html#fastqc
Drag and Drop files into FastQC to determine quality of data
If per base sequence content is uneven at the beginning this is due to primers and is okay.  You can cut this area out of the sequence, but leaving it in will not alter the results of the differential expression analysis. 
If per sequence GC content is uneven, this is okay because the _Drosophila melanogaster_ genome has a GC bias
The sequence duplication levels may be high.  This is because RNA-Seq libraries contain transcripts of exons that occur at various frequencies. This step is done manually because it is more user-friendly and useful to visualize the data to determine the quality of the sequences to be used in the pipeline. 

## Organizing Files For Pipeline
* **Make metadata file**
* **how to clone repo or download from github**

## Pyhton Wrapper
After completing quality control locally. Data files can be input into the python wrapper, [SeqDiff.py](https://github.com/jng2/SeqDiff_RNA/blob/master/SeqDiff.py) that will run through every other stepp of the differential expression pipeline. In order to run the pipeline, in terminal on a mac or command prompt on a windows computer, type the following comand:
```
python3 SeqDiff.py fq fa gtf out meta --NoStarGenome --NoStarAlignment --UseParser
```
The following arguements for the python wraper are for the following pieces of information:
* **fq**: the fastq file or directory(compressed or not) containing all fastq files
* **fa**: the fasta file containing the reference genome
* **gtf**: the gtf file containing the gtf gene annoation for the reference genome (note: the fasta and gtf files for the reference genome should be obtained from the same source to avoid difficulties with STAR alignment)
* **out**: the output directory
* **meta**: metadata file path 
* **--NoStarGenome**: add this argument if you have previously set up a STAR genome (this step takes a long time, so adding this agrument allows you to skip it if it has already been competed)
* **--NoStarAligmnent**: add this argument if you have previously aligned the fastq files to the reference genome (this step takes a long time, so adding this agrument allows you to skip it if it has already been competed)
* **--UseParser**: if MyGene no longer can retrieve information from FlyBase (due to FlyBase transitioning to a paid database) 


## How to use STAR

https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4631051/

Alternate Protocol 9: Mapping RNA-seq reads and running Cufflinks to assemble and quantify transcripts for un-stranded RNA-seq data Cufflinks (Trapnell et al 2010) is a popular software package for assembly and quantification of transcript using RNA-seq data. In this protocol STAR outputs BAM file with coordinate-sorted alignments, which is then used by Cufflinks to assemble and quantify novel transcript structures. This Protocol works with un-stranded RNA-seq data. For stranded RNA-seq data see the Alternate Protocol 7.

Necessary Resources Hardware Same as in the Basic Protocol.

Software Same as in the Alternate Protocol 7.

Input files Same as in the Basic Protocol.

Generating the coordinate-sorted BAM file and running Cufflinks transcript assembly and quantification



Make a run directory and switch to it:
```
mkdir ~/star/alt_cuff-unstr cd ~/star/alt_cuff-unstr 2. Map the FASTQ files located in the ~/star/directory (see Input Files) outputting coordinate-sorted BAM:
```

~/star/code/STAR-STAR_2.4.0k/bin/Linux_x86_64/STAR
--runThreadN 12 --genomeDir ~/star/genome/ 
--sjdbGTFfile ~/star/Homo_sapiens.GRCh38.79.gtf --sjdbOverhang 100 
--readFilesIn ~/star/ENCFF001RFH.fastq.gz ~/star/ENCFF001RFG.fastq.gz --readFilesCommand zcat 
--outSAMtype BAM SortedByCoordinate Unsorted 
--outSAMstrandField intronMotif --outSAMstrandField intronMotif option adds an XS attribute to the spliced alignments in the BAM file, which is required by Cufflinks for unstranded RNA-seq data.

In the same directory run the basic Cufflinks command:
```
~/star/code/cufflinks-2.2.1.Linux_x86_64/cufflinks -p 12 Aligned.sortedByCoord.out.bam -p 12 defines the number of threads used by Cufflinks.
```

Cufflinks output files are described in Alternative Protocol 7.


## Bioconductor Installation 
Bioconductor: Run these lines in R
```
source("http://bioconductor.org/workflows.R")
workflowInstall("rnaseqGene")
```
## R Packages Necessary for Bioconductor Alignment

[dplyr](https://cran.r-project.org/web/packages/dplyr/index.html)
tool for working with data frame like objects, both in and out of memory

[ggplot2](https://cran.r-project.org/web/packages/ggplot2/index.html)
tool for creating data visualizations using the grammar of graphics

## Bioconductor Necessary Software Packages
source(“https://bioconductor.org/biocLite.R”)
````
biocLite(c(“Rsamtools”, “DESeq2”, “GenomicFeatures”,"BiocParallel","GenomicRanges","GenomicAlignments"))
````
[Rsamtools](https://bioconductor.org/packages/3.6/bioc/html/Rsamtools.html)
provides facilities for parsing samtools BAM (binary) files representing aligned sequences

[DESeq2](https://bioconductor.org/packages/3.6/bioc/html/DESeq2.html)
performs differential gene expression analysis based on the negative binomial distribution

[GenomicFeatures](https://bioconductor.org/packages/3.6/bioc/html/GenomicFeatures.html)
provides tools for making and manipulating transcript centric annotations

[BiocParallel](https://www.bioconductor.org/packages/release/bioc/html/BiocParallel.html)
provides modified versions and novel implementations of functions for parallel evaluation of Bioconductor objects

[GenomicRanges](https://www.bioconductor.org/packages/release/bioc/html/GenomicRanges.html)
representation and manipulation of genomic intervals defined along a genome

[GenomicAlignments](https://www.bioconductor.org/packages/release/bioc/html/GenomicAlignments.html)
representation and manipulation of short genomic alignments

## Bioconductor Metadata Input File Format

It is important that the Metadata is formatted properly in order for Bioconductor to run properly. Here is an [example of the proper format](https://github.com/jng2/SeqDiff_RNA/blob/master/metadata.txt):
````
File,Time,Group,Run
C_3W_A_USR16088998L_HHFWCBBXX_L5_1,3W,Control,C_3W_A_USR16088998L_HHFWCBBXX_L5_1
````
In this example, the file name is C_3W_A_USR16088998L_HHFWCBBXX_L5_1, it is from the 3 week time point, in the control group, and run is the file name repeated.

## Bioconductor Alignment
[DESeq2](https://bioconductor.org/packages/3.6/bioc/html/DESeq2.html) is a Bioconductor package that performs differential gene expression analysis based on the negaitve binomial distribution. In this pipeline, the DESeq2 is used to determine which genes are differenitally expressed between pipelines using [_SummarizedExperiment_](http://bioconductor.org/packages/devel/bioc/vignettes/DESeq2/inst/doc/DESeq2.html#summarizedexperiment-input) input.

## Obtaining FlyBase data with Bioconductor MyGene

[MyGene](https://bioconductor.org/packages/release/bioc/html/mygene.html) is a Bioconductor package that allows users to query and retrieve gene annotation data from a variety of online databases. This pipeline uses it to obtain the gene symbol and gene type of a the differentially expressed genes determined by DeSeq2. This information is then added to the Bioconductor final csv output. 

## Final Bioconductor Output

The final Bioconductor output is a csv file containing the following information: 
* **X**: gene name
* **baseMean**: average of the normalized count values divided by the size of factors, taken over all samples in the _DESeqDataSet_
* **log2FoldChange**: effect size estimate, how much a gene's expression has changed between groups 
* **lfcSE(logfoldchangeStandardError)**: estimate of uncertainty of the effect size estimate
* **stat**: Wald statistic
* **p-value**: Wald test p-value, the probability thta the fold change is as strong as the observed one or stronger given the null hypotheses
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
