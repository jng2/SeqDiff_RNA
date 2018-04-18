# Pipeline for differential gene expression analysis of RNA-Seq data. 
![](https://github.com/jng2/SeqDiff_RNA/blob/master/DiffExpressionPipeline.jpg)

Based on experimental results from the Cavanaugh Lab at Loyola University Chicago.
Cavanaugh Lab Website: https://cavanaughlab.weebly.com

## FastQC for quality control
Download FastQC from https://www.bioinformatics.babraham.ac.uk/projects/download.html#fastqc
Drag and Drop files into FastQC to determine quality of data
If per base sequence content is uneven at the beginning this is due to primers and is okay.  You can cut this area out of the sequence, for this analysis we removed the first 10 bases.
If per sequence GC content is uneven, this is okay because the _Drosophila melanogaster_ genome has a GC bias
The sequence duplication levels may be high.  This is because RNA-Seq libraries contain transcripts of exons that occur at various frequencies. 


## How to use STAR

https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4631051/

Alternate Protocol 9: Mapping RNA-seq reads and running Cufflinks to assemble and quantify transcripts for un-stranded RNA-seq data Cufflinks (Trapnell et al 2010) is a popular software package for assembly and quantification of transcript using RNA-seq data. In this protocol STAR outputs BAM file with coordinate-sorted alignments, which is then used by Cufflinks to assemble and quantify novel transcript structures. This Protocol works with un-stranded RNA-seq data. For stranded RNA-seq data see the Alternate Protocol 7.

Necessary Resources Hardware Same as in the Basic Protocol.

Software Same as in the Alternate Protocol 7.

Input files Same as in the Basic Protocol.

Generating the coordinate-sorted BAM file and running Cufflinks transcript assembly and quantification



Make a run directory and switch to it:
mkdir ~/star/alt_cuff-unstr cd ~/star/alt_cuff-unstr 2. Map the FASTQ files located in the ~/star/directory (see Input Files) outputting coordinate-sorted BAM:

~/star/code/STAR-STAR_2.4.0k/bin/Linux_x86_64/STAR
--runThreadN 12 --genomeDir ~/star/genome/ 
--sjdbGTFfile ~/star/Homo_sapiens.GRCh38.79.gtf --sjdbOverhang 100 
--readFilesIn ~/star/ENCFF001RFH.fastq.gz ~/star/ENCFF001RFG.fastq.gz --readFilesCommand zcat 
--outSAMtype BAM SortedByCoordinate Unsorted 
--outSAMstrandField intronMotif --outSAMstrandField intronMotif option adds an XS attribute to the spliced alignments in the BAM file, which is required by Cufflinks for unstranded RNA-seq data.

In the same directory run the basic Cufflinks command:
~/star/code/cufflinks-2.2.1.Linux_x86_64/cufflinks -p 12 Aligned.sortedByCoord.out.bam -p 12 defines the number of threads used by Cufflinks.

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

It is important that the Metadata is formatted properly in order for Bioconductor to run properly. Here is an [example of the proper format.](https://github.com/jng2/SeqDiff_RNA/blob/master/metadata.txt):
````
File,Time,Group,Run
C_3W_A_USR16088998L_HHFWCBBXX_L5_1,3W,Control,C_3W_A_USR16088998L_HHFWCBBXX_L5_1
````
In this example, the file name is C_3W_A_USR16088998L_HHFWCBBXX_L5_1, it is from the 3 week time point, in the control group, and run is the file name repeated.

## Bioconductor Alignment

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
