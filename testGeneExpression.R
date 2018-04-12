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

sampleTable <-read.csv("/homes/jng2/UntitledFolder/testInfoTable.csv",row.names=1)
filenames <- file.path("/homes/jng2/UntitledFolder/AlignMeActual",paste0(sampleTable$Run,"_staroutAligned.out.bam"))
bamfile <-BamFileList(filenames,yieldSize = 2000000)

gtffile <- file.path('/homes/jng2/UntitledFolder/testgenome/dmel-all-r6.20.gtf')
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

dds<-DESeqDataSet(se,design = ~Group)
nrow(dds)
dds <- dds[ rowSums(counts(dds)) > 1, ]
nrow(dds)

dds <- DESeq(dds)
res <- results(dds)
res
res <- results(dds, contrast=c("Group","Control","JetLagged"))
res.05 <- results(dds, alpha = 0.05)
res.05sub <- subset(res.05,padj<.05)
mcols(res.05,use.names = TRUE)
mcols(res, use.names = TRUE)
summary(res)
summary(res.05)
write.csv(res.05sub,file="2W_ControlJetlag.csv")
#queryMany(res.05,fields="")

resSig <- subset(res, padj < 0.1)
head(resSig[ order(resSig$log2FoldChange), ])
head(resSig[ order(resSig$log2FoldChange, decreasing = TRUE), ])
summary(resSig[ order(resSig$log2FoldChange), ])
summary(resSig[ order(resSig$log2FoldChange, decreasing = TRUE), ])
hi<-proc.time() - ptm
hi
#count<-assay(se)
#head(count,5)

