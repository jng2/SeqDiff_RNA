import os
import sys
import argparse
import gzip



##WORK IN PROGRESS

#Shouldn't run nohup in wrapper, probably running on windows machine.  Maybe find something else?
#Any other arguments?
#Ways we can make sure that the code will stop if user does something wrong?
#We need a function call to fastqc, how should we approach it?


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

#identify fastq or directory(compressed or not) containing all fastq files
filelist=[]
if(os.path.isdir(args.fq)):
    filelist=os.listdir(args.fq)
elif(os.path.isfile(args.fq)):
    #if ".gz" in args.fq:
     #   filelist=os.listdir(gzip.open(args.fq))
    if(".fastq" in args.fq or ".fq" in args.fq):
        filelist.append(args.fq)
else:
    print("fastq could not be found") #kill the program here!
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
            name=i.replace(".fq.gz", "").replace(".fastq.gz","")
            x+=1
        elif x==1:
            line2=args.fq+i

            x=0
            oname=name+"_starout"
            os.system("STAR --runMode alignReads --outSAMtype BAM Unsorted -- readFilesCommand zcat --genomeDir "+args.out+" --readFilesIn "+line1 +' '+ line2+" --runThreadN 1 --outFileNamePrefix "+args.out+ oname)



    
  #######  BIOCONDUCTOR
  #This will display output
  # testGeneExpression.R that stores output of multiple runs into a directory. I->It doesn't.  I can try to do that?
  # Then we can view our data in a more organized manner.
if args.UseParser=='no':
    hi=args.out
    hi=hi[:-1]
   # group=args.group.strip()
    os.system("Rscript testGeneExpression.R "+args.meta+' ' +hi + ' ' + gtf + ' ' + args.RInstall) 

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
