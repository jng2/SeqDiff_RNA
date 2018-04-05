import os

#starting to compile the wrapper

#1 input for /path/to/folder/ which contains all necessary files
print("Enter the path to the SeqDiff directory.\nDirectory should contain\nA folder titled 'FASTQ' containing 1-10 fastq files,\nOne gtf annotation file,\nOne genome .fasta file")
genDir = input("SeqDiff Directory path: ")

filelist=os.listdir(genDir + "/FASTQ/")
filecount = len(filelist)
gtf = (name for name in os.listdir(genDir) if ".gtf" in name)
fasta =  (name for name in os.listdir(genDir) if ".fasta" in name)
type(gtf)
type(fasta)

for i in filelist:
  #######  STAR
  fastq = genDir+"/FASTQ/" + i
  

  os.system("nohup STAR --runThreadN 1 --runMode genomeGenerate --genomeDir "+genDir+" --sjdbGTFfile "+gtf+' --sjdbOverhang 100 --genomeFastaFiles '+fasta)
  os.system("STAR --runMode alignReads --outSAMtype BAM Unsorted -- readFilesCommand zcat --genomeDir "+genDir+" --readFilesIn "+fastq+" --runThreadN 1 --outFileNamePrefix"+ fastq +".out")

  #######  BIOCONDUCTOR
  
  #os.system("Rscript testGeneExpression.R " + )
