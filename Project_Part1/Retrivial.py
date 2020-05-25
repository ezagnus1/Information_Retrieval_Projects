import re
from nltk.stem import PorterStemmer
import string
class generated_document:
    def __init__(self,term,docID,tf):
        self.term = term
        self.docID = docID
        self.tf=tf

terms_list = []
generated_list = []
ps = PorterStemmer()
file = open("200_title.txt","r")
for n, line in enumerate(file.readlines()):
      list1 = line.split()

      for e in list1:
          if not(e.isalnum()):
              counter = False
              if len(e) == 1:
                  if (bool(re.match('^(?=.*[0-9]$)(?=.*[a-zA-Z])', e))) == False:
                      continue
              for e_sub in e:
                  if e_sub.isnumeric():
                    counter = True
                    continue
                  elif (bool(re.match('^(?=.*[a-zA-Z])', e_sub))):
                    continue
                  elif counter == True:
                      if(e_sub == '.'):
                          continue
                      else:
                          e = e.replace(e_sub, '')
                          continue

                  else:
                      e = e.replace(e_sub, '')
              e = e.lower()
              e = ps.stem(e)
              str_e = str(n+1)
              generated_obj = generated_document(e,str_e,1)
              generated_list.append(generated_obj)


          else:
              e = e.lower()
              e = ps.stem(e)
              str_e = str(n+1)
              generated_obj = generated_document(e, str_e,1)
              generated_list.append(generated_obj)


sorted_list = sorted(generated_list,key=lambda x:x.term)

i=0

while(i<len(sorted_list)-1):
    if((sorted_list[i].term==sorted_list[i+1].term) and (sorted_list[i].docID==sorted_list[i+1].docID)):
        sorted_list[i].tf = sorted_list[i].tf + 1
        sorted_list.pop(i+1)
        i=i+2
        continue


    else:

        sorted_list[i].tf = 1

    i = i + 1

pos_index={}
file_no=1
for i in sorted_list:
    if i.term in pos_index:
        pos_index[i.term][0]=pos_index[i.term][0]+1

        if file_no in pos_index[i.term][1]:
            pos_index[i.term][1][file_no].append(i.docID+","+str(i.tf))

        else:
            pos_index[i.term][1][file_no] = [i.docID+","+str(i.tf)]
    else:

        pos_index[i.term] = []
        pos_index[i.term].append(1)
        pos_index[i.term].append({})
        pos_index[i.term][1][file_no] = [i.docID+","+str(i.tf)]
    if (i.tf == 2):
        pos_index[i.term][0]=pos_index[i.term][0]+1

termsList=[]
for i in sorted_list:
    if (i.term in termsList):
        continue
    else:
        termsList.append(i.term)

d=[]#dictinory list
offset=0
df=0
file = open("dictionary.txt","w")
f = open("posting.txt","w")

for i in termsList:
    offset = offset + df
    d=pos_index[i]
    df=d[0]#document frequency
    docid_list=d[1][1]#hold doc id and term frequncy list
    result=i+" "+str(df)+" "+str(offset)+"\n"
    file.write(str(result))
    j = 0
    while(j<len(docid_list)):
        f.write(docid_list[j])
        f.write("\n")
        j=j+1


file.close()
f.close()



