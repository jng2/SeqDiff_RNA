
# coding: utf-8

# In[17]:


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

