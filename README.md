Installation:

Bioconductor(run these lines in R):
source("http://bioconductor.org/workflows.R")
workflowInstall("rnaseqGene")

==============++++++////STAR\\\\++++++==============

Alternate Protocol 9: Mapping RNA-seq reads and running Cufflinks to assemble and quantify transcripts for un-stranded RNA-seq data
Cufflinks (Trapnell et al 2010) is a popular software package for assembly and quantification of transcript using RNA-seq data. In this protocol STAR outputs BAM file with coordinate-sorted alignments, which is then used by Cufflinks to assemble and quantify novel transcript structures. This Protocol works with un-stranded RNA-seq data. For stranded RNA-seq data see the Alternate Protocol 7.

Necessary Resources
Hardware
Same as in the Basic Protocol.

Software
Same as in the Alternate Protocol 7.

Input files
Same as in the Basic Protocol.

Generating the coordinate-sorted BAM file and running Cufflinks transcript assembly and quantification
1. Make a run directory and switch to it:

mkdir ~/star/alt_cuff-unstr
cd ~/star/alt_cuff-unstr
2. Map the FASTQ files located in the ~/star/directory (see Input Files) outputting coordinate-sorted BAM:

~/star/code/STAR-STAR_2.4.0k/bin/Linux_x86_64/STAR\
--runThreadN 12 --genomeDir ~/star/genome/ \
--sjdbGTFfile ~/star/Homo_sapiens.GRCh38.79.gtf --sjdbOverhang 100 \
--readFilesIn ~/star/ENCFF001RFH.fastq.gz ~/star/ENCFF001RFG.fastq.gz --readFilesCommand zcat \
--outSAMtype BAM SortedByCoordinate Unsorted \
--outSAMstrandField intronMotif
--outSAMstrandField intronMotif option adds an XS attribute to the spliced alignments in the BAM file, which is required by Cufflinks for unstranded RNA-seq data.

2. In the same directory run the basic Cufflinks command:

~/star/code/cufflinks-2.2.1.Linux_x86_64/cufflinks -p 12 Aligned.sortedByCoord.out.bam
-p 12 defines the number of threads used by Cufflinks.

3. Cufflinks output files are described in Alternative Protocol 7.
  
