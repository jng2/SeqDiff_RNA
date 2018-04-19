if(args[4]='yes'){
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


ptm <- proc.time()
args=commandArgs(trailingOnly = TRUE)
sampleTable <-read.csv(args[1],row.names=1)
filenames <- file.path(args[2],paste0(sampleTable$Run,"_staroutAligned.out.bam")) #naming might fuck up ><
bamfile <-BamFileList(filenames,yieldSize = 2000000)

gtffile <- file.path(args[3])
txdb <- makeTxDbFromGFF(gtffile, format = "gtf", circ_seqs = character())


ebg <- exonsBy(txdb, by="gene")

register(SerialParam())


se <- summarizeOverlaps(features=ebg, reads=bamfile,
                        mode="Union",
                        singleEnd=FALSE,
                        ignore.strand=TRUE,
                        fragments=TRUE )


colData(se) <- DataFrame(sampleTable)
colData(se)
#i <- args[4]
dds<-DESeqDataSet(se,design = ~ Group)
nrow(dds)
dds <- dds[ rowSums(counts(dds)) > 1, ]
nrow(dds)

dds <- DESeq(dds)
res <- results(dds)
res
#res <- results(dds, contrast=c("Group","Control","JetLagged"))
res.05 <- results(dds, alpha = 0.05)
res.05sub <- subset(res.05,padj<.05)
mcols(res.05,use.names = TRUE)
#mcols(res, use.names = TRUE)
summary(res.05)
print('why')
write.csv(res,file="2W_ControlJetLaggedp_1.csv")
write.csv(res.05sub,file="testmeOut.csv")
print('please')
hi=read.csv("2W_ControlJetLaggedp_1.csv",header=TRUE)
print('fuck')
hey<-getGenes(hi[,1],fields = "symbol type_of_gene")
print('fucccccdsasd')

hey<-hey[!duplicated(hey[1]),]


hi$symbol<-hey$symbol

hi$type<-hey$type_of_gene

write.csv(hi,file="2W_ControlJetLaggedp_1NoContstast.csv")

