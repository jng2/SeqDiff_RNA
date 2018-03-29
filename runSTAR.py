#in order to make this not hardcoded and capable of taking any type of files
# we can add in argparse functionality to have gtf file argument as well as fastq arguments


from subprocess import call
#input annotion
call('cd ~/star')
call('wget ftp://ftp.ensembl.org/pub/release-77/gtf/drosophila_melanogaster/Drosophila_melanogaster.BDGP5.77.gtf.gz')
call('gunzip Drosophila_melanogaster.BDGP5.77.gtf.gz')

#input our files
#add in calls to upload our files to the /star/ directory

  
#running
call('--cd ~/alt_cuff-unstr')
#this is probably not our path to star need to update that below
call('~/star/code/STAR-STAR_2.4.0k/bin/Linux_x86_64/STAR\')
call('--runThreadN 12 --genomeDir ~/star/genome/ \')
call('--sjdbGTFfile ~/star/Drosophila_melanogaster.BDGP5.77.gtf --sjdbOverhang 100 \')
#change these fastq files below to our files
call('--readFilesIn ~/star/ENCFF001RFH.fastq.gz ~/star/ENCFF001RFG.fastq.gz --readFilesCommand zcat \')
call('--outSAMtype BAM SortedByCoordinate Unsorted \')
call('--outSAMstrandField intronMotif')

#p is number of threads
call('~/star/code/cufflinks-2.2.1.Linux_x86_64/cufflinks -p 1 Aligned.sortedByCoord.out.bam')

     
## All of this under is the exact same thing as up top, but is just a little more pretty.  ALso only needs two calls, the first one makes the genome for star to use, the second is the alignment command     
#import os

#os.system("STAR --runThreadN 12 --runMode genomeGenerate --genomeDir /homes/jng2/UntitledFolder/STAR/holdme --genomeFastaFiles /homes/jng2/UntitledFolder/testgenome/dm6.fa ")

#--sjdbGTFfile /homes/jng2/UntitledFolder/testgenome/dmel-all-r6.20.gtf --sjdbOverhang 100 this doesn't like any of the .gtf files for some reason
#os.system("STAR --runMode alignReads --outSAMtype BAM SortedByCoordinate Unsorted -- readFilesCommand zcat --genomeDir /homes/jng2/UntitledFolder/STAR/holdme --readFilesIn /homes/jng2/UntitledFolder/testme.fastq.gz --runThreadN 12 --outFileNamePrefix testmeout")
