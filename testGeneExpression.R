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

tab = data.frame(logFC = hi$log2FoldChange, negLogPval = -log10(hi$pvalue))
head(tab)
par(mar = c(5, 4, 4, 4))
plot(tab, pch = 16, cex = 0.6, xlab = expression(log[2]~fold~change), ylab = expression(-log[10]~pvalue))
lfc = 2
pval = 0.01
signGenes = (abs(tab$logFC) > lfc & tab$negLogPval > -log10(pval))
points(tab[signGenes, ], pch = 16, cex = 0.8, col = "red") 
abline(h = -log10(pval), col = "green3", lty = 2) 
abline(v = c(-lfc, lfc), col = "blue", lty = 2) 
mtext(paste("pval =", pval), side = 4, at = -log10(pval), cex = 0.8, line = 0.5, las = 1) 
mtext(c(paste("-", lfc, "fold"), paste("+", lfc, "fold")), side = 3, at = c(-lfc, lfc), cex = 0.8, line = 0.5)

