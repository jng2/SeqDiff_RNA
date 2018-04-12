import os

#starting to compile the wrapper

#1 input for /path/to/folder/ which contains all necessary files
print("Enter the path to the SeqDiff directory.\nDirectory should contain\nA folder titled 'FASTQ' containing 1-10 fastq files,\nOne gtf annotation file,\nOne genome .fasta file\n")
genDir = input(">")

#identify directory containing all fastq files
filelist=os.listdir(genDir + "/FASTQ/")

#identify gtf and fasta for STAR
gtf = str(name for name in os.listdir(genDir) if ".gtf" in name)
fasta =  str(name for name in os.listdir(genDir) if ".fasta" in name)

#loop through fastq files and run them on star
#we can add an if statement here to check if we even need to run star. 
for i in filelist:
  #######  STAR
  print(i+'\n helloooooo')
  fastq = genDir+"/FASTQ/" + i

  os.system("STAR --runThreadN 1 --runMode genomeGenerate --genomeDir "+genDir+" --sjdbGTFfile "+gtf+' --sjdbOverhang 100 --genomeFastaFiles '+fasta)
  os.system("STAR --runMode alignReads --outSAMtype BAM Unsorted -- readFilesCommand zcat --genomeDir "+genDir+" --readFilesIn "+fastq+" --runThreadN 1 --outFileNamePrefix genDir/StarOut/"+ i)

  #######  BIOCONDUCTOR
  #This will display output, however we may need to add a line of code to 
  # testGeneExpression.R that stores output of multiple runs into a directory.
  # Then we can view our data in a more organized manner. 
  os.system("Rscript testGeneExpression.R " +"genDir/StarOut/"+ i )
