
# coding: utf-8

# In[ ]:


import os
with open('untitled.txt') as inputfile:
    for line in inputfile:
        line=line.rstrip()
        os.system("cutadapt -u 10 -o "+line+"_snipped_.fq.gz " +line)

