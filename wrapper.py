import os

#starting to compile the wrapper

#1 input for /path/to/folder/ which contains all necessary files
print("Enter the path to the SeqDiff directory.\nDirectory should contain\nA folder titled 'FASTQ' containing 1-10 fastq files,\nOne gtf annotation file,\nOne genome .fasta file")
#genDir = input("SeqDiff Directory path: ")
genDir = "/homes/jng2/SeqDiff"
filelist=os.listdir(genDir + "/FASTQ/")
filecount = len(filelist)
gtf = str(name for name in os.listdir(genDir) if ".gtf" in name)
fasta =  str(name for name in os.listdir(genDir) if ".fasta" in name)
print(type(gtf))
print(type(fasta))

for i in filelist:
  #######  STAR
  print(i+'\n helloooooo')
  fastq = genDir+"/FASTQ/" + i
  

  os.system("STAR --runThreadN 1 --runMode genomeGenerate --genomeDir "+genDir+" --sjdbGTFfile "+gtf+' --sjdbOverhang 100 --genomeFastaFiles '+fasta)
 # os.system("STAR --runMode alignReads --outSAMtype BAM Unsorted -- readFilesCommand zcat --genomeDir "+genDir+" --readFilesIn "+fastq+" --runThreadN 1 --outFileNamePrefix genDir/StarOut/"+ i)

  #######  BIOCONDUCTOR
  
  #os.system("Rscript testGeneExpression.R " + )
