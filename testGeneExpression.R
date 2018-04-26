args=commandArgs(trailingOnly = TRUE) 
if(args[4]=='yes'){  #If this argument is found, then will run the install for all of the packages
  source("https://bioconductor.org/biocLite.R")
  biocLite(c("Rsamtools", "DESeq2", "GenomicFeatures","BiocParallel","GenomicRanges","GenomicAlignments","Rsamtools","mygene"))
  
}

library("Rsamtools")
library("GenomicFeatures")
library("BiocParallel")
library("GenomicRanges")
library("GenomicAlignments")
library("DESeq2")
library("dplyr")
library("ggplot2")
library("mygene")


ptm <- proc.time() #sets up a timer

sampleTable <-read.csv(args[1],row.names=1) #creates a table that holds the in from the meta text file
filenames <- file.path(args[2],paste0(sampleTable$Run,".sd_staroutAligned.out.bam")) #grabs the .bam files from aligner
bamfile <-BamFileList(filenames,yieldSize = 2000000) #creates a large object that holds all of the bam files

gtffile <- file.path(args[3]) #grabs the gtf file
txdb <- makeTxDbFromGFF(gtffile, format = "gtf", circ_seqs = character()) #creates a gene model object necessary for analysis.  HOlds things like information about exons, transcripts and genes.


ebg <- exonsBy(txdb, by="gene") #Produces list of all exons grouped by gene

register(SerialParam()) #limits usage to one core

#creates a SummarizedExperiment object, which contains information about the experiment that will be fed into DESeq2

se <- summarizeOverlaps(features=ebg, reads=bamfile, 
                        mode="Union",
                        singleEnd=FALSE,
                        ignore.strand=TRUE,
                        fragments=TRUE )


colData(se) <- DataFrame(sampleTable) #grab the column names from the metadata 
colData(se)
#i <- args[4]
dds<-DESeqDataSet(se,design = ~ Group) #runs the analysis of the column "Group"
nrow(dds)
dds <- dds[ rowSums(counts(dds)) > 1, ] #gets rid of zero/1 value counts
nrow(dds)

dds <- DESeq(dds)
res <- results(dds)
mcols(res,use.names=TRUE)

write.csv(res,file='OutputAll.csv')
summary(res) #displays results of p-value .10

res.10sub <- subset(res,padj<.1) #saves subset of results with adjusted pvalue .10

#summary(res.05)
mcols(res.10sub, use.names = TRUE)
write.csv(res.10sub,file="Outputp.10.csv")
hi=read.csv("Outputp.10.csv",header=TRUE)
hey<-getGenes(hi[,1],fields = "symbol type_of_gene") #uses my gene function getGenes to talk with FlyBase to grab relevant information
hey<-hey[!duplicated(hey[1]),]
hi$symbol<-hey$symbol
hi$type<-hey$type_of_gene #places into hi object
write.csv(hi,file="Outputp.10.csv") #rewrites the file

