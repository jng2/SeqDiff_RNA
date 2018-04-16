import os
import argparse
import gzip



##WORK IN PROGRESS

#set up our argument parser
parser = argparse.ArgumentParser()
parser.add_argument("fq",help="fastq or directory(compressed or not) containig all fastq")
parser.add_argument("fs",help="genome fasta")
parser.add_argument("gtf",help="gtf annotation")
parser.add_argument("out",help="output directory")
#parser.add_arugment("meta",help="Enter in the metadata file path")
args = parser.parse_args()

##file identification

#identify fastq or directory(compressed or not) containing all fastq files
filelist=[]
if(os.path.isdir(args.fq)):
  filelist=os.listdir(args.fq)
elif(os.path.isfile(args.fq)):
  if ".gz" in args.fq:
    filelist=os.listdir(gzip.open(args.fq))
  elif ".fastq" in args.fq:
    filelist.append(args.fq)
else:
  print("fastq could not be found")
    
#identify gtf and fasta for STAR
gtf = args.gtf
fasta =  args.fs

#loop through fastq files and run them on star
#we can add an if statement here to check if we even need to run star. 
for i in filelist:
  #######  STAR
  print(i+'\n helloooooo')
  fastq = i

  os.system("STAR --runThreadN 1 --runMode genomeGenerate --genomeDir "+genDir+" --sjdbGTFfile "+gtf+' --sjdbOverhang 100 --genomeFastaFiles '+fasta)
  print('hi')
  os.system("STAR --runMode alignReads --outSAMtype BAM Unsorted -- readFilesCommand zcat --genomeDir "+genDir+" --readFilesIn "+fastq+" --runThreadN 1 --outFileNamePrefix genDir/StarOut/"+ i)

  #######  BIOCONDUCTOR
  #This will display output, however we may need to add a line of code to 
  # testGeneExpression.R that stores output of multiple runs into a directory.
  # Then we can view our data in a more organized manner. 
  os.system("Rscript testGeneExpression.R " +"genDir/StarOut/"+ i )
