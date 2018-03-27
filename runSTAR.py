from subprocess import call
#input annotion
call('cd ~/star')
call('wget ftp://ftp.ensembl.org/pub/release-77/gtf/drosophila_melanogaster/Drosophila_melanogaster.BDGP5.77.gtf.gz')
call('gunzip Drosophila_melanogaster.BDGP5.77.gtf.gz')

#input our files
#add in calls to select our files

  
#running
call('--cd ~/alt_cuff-unstr')
call('~/star/code/STAR-STAR_2.4.0k/bin/Linux_x86_64/STAR\')
call('--runThreadN 12 --genomeDir ~/star/genome/ \')
call('--sjdbGTFfile ~/star/Homo_sapiens.GRCh38.79.gtf --sjdbOverhang 100 \')
call('--readFilesIn ~/star/ENCFF001RFH.fastq.gz ~/star/ENCFF001RFG.fastq.gz --readFilesCommand zcat \')
call('--outSAMtype BAM SortedByCoordinate Unsorted \')
call('--outSAMstrandField intronMotif')

call('~/star/code/cufflinks-2.2.1.Linux_x86_64/cufflinks -p 12 Aligned.sortedByCoord.out.bam')
