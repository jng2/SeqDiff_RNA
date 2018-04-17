import os
import argparse
import gzip



##WORK IN PROGRESS

#Shouldn't run nohup in wrapper, probably running on windows machine.  Maybe find something else?
#Any other arguments?
#Ways we can make sure that the code will stop if user does something wrong?
#We need a function call to fastqc, how should we approach it?


#set up our argument parser
parser = argparse.ArgumentParser()
parser.add_argument("fq",help="fastq or directory(compressed or not) containig all fastq")
parser.add_argument("fs",help="genome fasta")
parser.add_argument("gtf",help="gtf annotation")
parser.add_argument("out",help="output directory")
parser.add_argument("meta",help="Enter in the metadata file path")
parser.add_argument('--NoStarGenome',help="If you don't need to do set up a STAR genome, please use this option.",default='no',action='store_const', const='yes')
parser.add_argument('--NoStarAlignment',help="If you don't need to do any alignment of fastq files, please use this option.", default='no',action='store_const', const='yes')

args = parser.parse_args()

##file identification

#identify fastq or directory(compressed or not) containing all fastq files
filelist=[]
if(os.path.isdir(args.fq)):
    filelist=os.listdir(args.fq)
elif(os.path.isfile(args.fq)):
    if ".gz" in args.fq:
        filelist=os.listdir(gzip.open(args.fq))
    elif ".fastq" in args.fq or ".fq" in args.fq:
        filelist.append(args.fq)
else:
    print("fastq could not be found") #kill the program here!
filelist.sort() #sort should allow for it.  Check by odd/even amount for left right? Check for duplicates?
star=args.NoStarGenome
alignMe=args.NoStarAlignment
print(star)
#identify gtf and fasta for STAR
gtf = args.gtf
fasta =  args.fs

#loop through fastq files and run them on star
#we can add an if statement here to check if we even need to run star. 
#this now works!

#need a checker to make sure there are matching pairs of the repeats

if star=='no':
    os.system("STAR --runThreadN 1 --runMode genomeGenerate --genomeDir "+args.out+" --sjdbGTFfile "+gtf+' --sjdbOverhang 100 --genomeFastaFiles '+fasta)
if alignMe =='no':
    x=0
    line1=''
    line2=''
    for i in filelist:
      #######  STAR
        if x==0:
            line1=args.fq+i
            name=i
            x+=1
        elif x==1:
            line2=args.fq+i

            x=0
            oname=name+"_starout"
            os.system("STAR --runMode alignReads --outSAMtype BAM Unsorted -- readFilesCommand zcat --genomeDir "+args.out+" --readFilesIn "+line1 +' '+ line2+" --runThreadN 1 --outFileNamePrefix "+args.out+ oname)



    
  #######  BIOCONDUCTOR
  #This will display output, however we may need to add a line of code to 
  # testGeneExpression.R that stores output of multiple runs into a directory.
  # Then we can view our data in a more organized manner.
hi=args.out
hi=hi[:-1]
group=args.group.strip()
os.system("Rscript testGeneExpression.R "+args.meta+' ' +hi + ' ' + gtf + ' ' + group) 
