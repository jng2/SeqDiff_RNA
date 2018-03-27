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
call('~/star/code/STAR-STAR_2.4.0k/bin/Linux_x86_64/STAR\')
call('--runThreadN 12 --genomeDir ~/star/genome/ \')
call('--sjdbGTFfile ~/star/Drosophila_melanogaster.BDGP5.77.gtf --sjdbOverhang 100 \')
#change these fastq files below to our files
call('--readFilesIn ~/star/ENCFF001RFH.fastq.gz ~/star/ENCFF001RFG.fastq.gz --readFilesCommand zcat \')
call('--outSAMtype BAM SortedByCoordinate Unsorted \')
call('--outSAMstrandField intronMotif')

call('~/star/code/cufflinks-2.2.1.Linux_x86_64/cufflinks -p 12 Aligned.sortedByCoord.out.bam')
