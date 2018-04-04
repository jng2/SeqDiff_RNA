library("Rsamtools")
library("GenomicFeatures")
library("BiocParallel")
library("GenomicRanges")
library("GenomicAlignments")
library("DESeq2")
library("dplyr")
library("ggplot2")

sampleTable <-read.csv("/homes/jng2/UntitledFolder/testInfoTableSmall.csv",row.names=1)
filenames <- file.path("/homes/jng2/UntitledFolder/AlignMe",paste0(sampleTable$Run,"_staroutAligned.out.bam"))
bamfile <-BamFileList(filenames,yieldSize = 2000000)

gtffile <- file.path('/homes/jng2/UntitledFolder/testgenome/dmel-all-r6.20.gtf')
txdb <- makeTxDbFromGFF(gtffile, format = "gtf", circ_seqs = character())

ebg <- exonsBy(txdb, by="gene")


se <- summarizeOverlaps(features=ebg, reads=bamfile,
                        mode="Union",
                        singleEnd=FALSE,
                        ignore.strand=TRUE,
                        fragments=TRUE )


colData(se) <- DataFrame(sampleTable)
colData(se)

dds<-DESeqDataSet(se,design = ~ Group + Time + Group:Time)
nrow(dds)
dds <- dds[ rowSums(counts(dds)) > 1, ]
nrow(dds)

dds <- DESeq(dds)
res <- results(dds)
res
res <- results(dds, contrast=c("Group","Control","JetLagged"))
mcols(res, use.names = TRUE)
summary(res)

#count<-assay(se)
#head(count,5)

