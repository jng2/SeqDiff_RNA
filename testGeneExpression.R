library("Rsamtools")
bamfile <-BamFileList('/homes/jng2/UntitledFolder/AlignMe/C_2W_A_USR16088995L_HHFWCBBXX_L5_1_staroutAligned.out.bam',yieldSize = 2000000)
library("GenomicFeatures")
gtffile <- file.path('/homes/jng2/UntitledFolder/AlignMe/C_2W_A_USR16088995L_HHFWCBBXX_L5_1_staroutAligned.out.bam')
txdb <- makeTxDbFromGFF(gtffile, format = "gtf", circ_seqs = character())

ebg <- exonsBy(txdb, by="gene")

register(SerialParam())
se <- summarizeOverlaps(features=ebg, reads=bamfile,
                        mode="Union",
                        singleEnd=FALSE,
                        ignore.strand=TRUE,
                        fragments=TRUE )

colData(se)





