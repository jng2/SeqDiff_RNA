import os
import sys
import argparse
import gzip






#set up our argument parser
parser = argparse.ArgumentParser()
parser.add_argument("fq",help="fastq or directory(compressed or not) containing all fastq")
parser.add_argument("fa",help="genome fasta")
parser.add_argument("gtf",help="gtf annotation")
parser.add_argument("out",help="output directory")
parser.add_argument("meta",help="Enter in the metadata file path")
parser.add_argument('--NoStarGenome',help="If you don't need to do set up a STAR genome, please use this option.",default='no',action='store_const', const='yes')
parser.add_argument('--NoStarAlignment',help="If you don't need to do any alignment of fastq files, please use this option.", default='no',action='store_const', const='yes')
parser.add_argument('--UseParser',help="If MyGene is no longer working with FlyBase, please use this option to use a python parser instead.  It will not be able to output all of the variables, however.",default='no',action='store_const', const='yes')
parser.add_argument('--RInstall',help="If you need to install R stuff, use this option.",default='no',action='store_const', const='yes')
args = parser.parse_args()

##file identification

#identify fastq or directory containing all fastq files
filelist=[] #stores all fastq
if(os.path.isdir(args.fq)): # check if argument given is directory
    filelist=os.listdir(args.fq)
    for file in filelist:
        if((".fastq" not in file) and (".fq" not in file)): #check that the files given within the directory are fastq files, else end program
            print("fastq directory contains inelligible files")
            sys.exit(0)
elif(os.path.isfile(args.fq)): # check if argument given is file
    if(".fastq" in args.fq or ".fq" in args.fq):
        filelist.append(args.fq)
else:#we can't find any 
    print("fastq could not be found") 
    sys.exit(0)
filelist.sort() #sort should allow for it.  Check by odd/even amount for left right? Check for duplicates?
star=args.NoStarGenome
alignMe=args.NoStarAlignment
print(star)


#identify gtf
if ".gtf" in args.gtf:
    gtf = args.gtf
else:
    print("gtf could not be found")
    sys.exit(0)
    
#identify fasta 
if ".fasta" in args.fa:
    fasta =  args.fa
else: 
    print("fasta could not be found")
    sys.exit(0)

#loop through fastq files and run them on star
if star=='no': #forgo alignment if user dictates such
    os.system("STAR --runThreadN 1 --runMode genomeGenerate --genomeDir "+args.out+" --sjdbGTFfile "+gtf+' --sjdbOverhang 100 --genomeFastaFiles '+fasta)
if alignMe =='no':
    x=0
    line1=''
    line2=''
    for i in filelist:
      #######  STAR
        if x==0:
            line1=args.fq+i
            name=i.replace(".fq.gz", ".sd").replace(".fastq.gz",".sd")
            x+=1
        elif x==1:
            line2=args.fq+i

            x=0
            oname=name+"_starout"
            os.system("STAR --runMode alignReads --outSAMtype BAM Unsorted -- readFilesCommand zcat --genomeDir "+args.out+" --readFilesIn "+line1 +' '+ line2+" --runThreadN 1 --outFileNamePrefix "+args.out+ oname)



    
  #######  BIOCONDUCTOR
#By default bioconductor's mygene is used to pull info from flybase
if args.UseParser=='no':
    hi=args.out
    hi=hi[:-1]
   # group=args.group.strip()
    os.system("Rscript testGeneExpression.R "+args.meta+' ' +hi + ' ' + gtf + ' ' + args.RInstall) 
#in the event user doesn't want to use bioconductor's mygene to pull info from flybase, they can use this parser to pull info from annotation
else:
    import csv
    holdme={}
    with open('dmel-all-r6.20.gtf') as gtf:
    #Make dictionary of the gtf file
        for line in gtf:
            hi=line.split('\t')
            hey=hi[8].split('"')
            if hey[1] not in holdme.keys():
                holdme[hey[1]]=hey[3]
    ans=[]
    with open('2W_ControlJetlag.csv') as csvfile:
        yo = csv.reader(csvfile, delimiter=",") #yo is a csv.reader object that plays like a list
        i=0
        for line in yo:
            if i>=1:
                print(line[0])
                if line[0] in holdme.keys(): #searches if flybase id is found within dictionary and then takes the name from the dictionary.  The only information that i could find within the .gtf file
                    line.append(holdme[line[0]])
                    ans.append(line)
            else:
                strign="Name"
                line.append(strign)
                ans.append(line)
            i+=1
    with open('2W_ControlJetlagTest_pythonparser.csv','w',newline='') as csvout: #writes it out
        writer=csv.writer(csvout,delimiter=',')
        for line in ans:
            writer.writerow(line)
