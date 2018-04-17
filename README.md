# Pipeline for differential gene expression analysis of RNA-Seq data. 
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
