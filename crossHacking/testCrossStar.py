import os

import argparse as ap
parser = ap.ArgumentParser()
parser.add_argument('genDir',help="Please enter in the path for where you wish the genome to be stored")
parser.add_argument('genomme',help='Please enter in the path for the genome .fasta file.')
parser.add_argument('gtf',help='Please enter in the path for the .gtf file that pairs with the .fasta file')
parser.add_argument('inp',help='Please enter in the path for the fastq file'
#parser.add_argument('output',help='Please enter in the name and path of the output file you wished to be written.')
args= parser.parse_args()

                    
                    
print("STAR --runThreadN 1 --runMode genomeGenerate --genomeDir "+genDir+" --sjdbGTFfile "+gtf+' --sjdbOverhang 100 --genomeFastaFiles '+genome)
print("STAR --runMode alignReads --outSAMtype BAM Unsorted -- readFilesCommand zcat --genomeDir "+genDir+" --readFilesIn "+line+" --runThreadN 1 --outFileNamePrefix hiout")
                    
                    
                    
                    
                    
                    
                    
