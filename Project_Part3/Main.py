import math
import re
from nltk.stem import PorterStemmer
import operator
class generated_document:
    def __init__(self,term,docID,tf):
        self.term = term
        self.docID = docID
        self.tf = tf

terms_list = []
generated_list = []
ps = PorterStemmer()


with open("200_content.txt",encoding='utf-8') as f:
    lines = f.read()

content = lines.split("\n")
N = len(content)
i=0
for n, line in enumerate(content):
      list1 = line.split()
      i=i+1
      for e in list1:
          if not(e.isalnum()):
              counter = False
              if len(e) == 1:
                  if (bool(re.match('^(?=.[0-9]$)(?=.[a-zA-Z])', e))) == False:
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
              if e == '': continue
              elif e[len(e)-1] == '.': e = e[:-1]
              generated_obj = generated_document(e,str_e,1)
              generated_list.append(generated_obj)
              #terms_list.append(e)

          else:
              e = e.lower()
              e = ps.stem(e)
              str_e = str(n+1)
              generated_obj = generated_document(e, str_e,1)
              generated_list.append(generated_obj)
              #terms_list.append(e)


sorted_list = sorted(generated_list,key=lambda x:x.term)
#=======================================================================================================================
i=0
pos_index={}
count=0
for i in sorted_list:

    if i.term in pos_index:
        if i.docID in pos_index[i.term][1]:
            pos_index[i.term][1][i.docID]+=1
            #print(i.term,"=>",i.docID)
        else:

            pos_index[i.term][1][i.docID]=i.tf
        pos_index[i.term][0] = len(pos_index[i.term][1])
    else:
        pos_index[i.term]=[]
        pos_index[i.term].append(1)
        pos_index[i.term].append({})
        pos_index[i.term][1][i.docID]=i.tf

#print(pos_index["hsbc"])
#d=pos_index["hsbc"][1]
#print(list((pos_index["hsbc"][1]).keys()))
file = open("dictionary.txt","w")
f = open("posting.txt","w")
offset=0
for i in pos_index:
    result=i+" "+str(pos_index[i][0])+" "+str(offset)+"\n"
    offset=offset+int(pos_index[i][0])
    j = 0
    file.write(str(result))
    while(j<int(pos_index[i][0])):
        key=list((pos_index[i][1]).keys())
        value = list((pos_index[i][1]).values())
        res=str(key[j])+","+str(value[j])+"\n"
        f.write(str(res))
        j=j+1
#===============================================================================================================

file.close()
f.close()
class my_dictionary(dict):
    def __init__(self):
        self = dict()

    def add(self, key, value):
        self[key] = value


length_normal = my_dictionary()#
length_normal2 = my_dictionary()
query_terms = [] # Stores the tokenized query terms
ps = PorterStemmer()
posting_list=[]
def insert(hash_table, key, value):  # HASH TABLE INSERT PART OF THE DICTIONARY ELEMENTS
    hash_key = (ord(key[0])) % len(hash_table)
    bucket = hash_table[hash_key]
    bucket.append((key,value))


def search(hash_table, key): # SEARCH IN HASH TABLE FOR FINDING ELEMENTS OF HASH TABLE
    hash_key = ord(key[0]) % len(hash_table)
    bucket = hash_table[hash_key]
    for i, kv in enumerate(bucket):
        k, v = kv
        if key == k:
            return v

hash_table = [[] for _ in range(40)]

file = open("dictionary.txt","r") # INSERTING DICTIONARY VALUES INTO HASH TABLE
for n, line in enumerate(file.readlines()):
    word = line.split();
    insert(hash_table,word[0],line);


file.close()

#file3 = open("revised_postings.txt","w")
i=0
file2 = open("posting.txt","r")
docid_tf_tfw_list=[]
temp_post_list = []
for n, line in enumerate(file2.readlines()): # HERE WE WRITE TERM FREQUENCY WEIGHT VALUES INTO NEW REVISED POSTING LIST AS (docID , tfw)
    word = line.split(",")
    temp_post_list.append(word)
    number = int(word[1])
    number = 1 + math.log(number,10)
    tmp=word[1].split("\n")
    result = str(word[0]) + ","+str(tmp[0])+","+ str(number)
    #file3.write(result)
    docid_tf_tfw_list.append(result)
    i = i + 1
file2.close()
#file3.close()

for line in docid_tf_tfw_list:#found document length same as project 2
    word = line.split(",")
    number = float(word[2])
    number = number * number
    if word[0] in length_normal:
        length_normal[word[0]] += number
    else:
        length_normal.add(word[0], number)

for line in docid_tf_tfw_list:#found document length sum of tfs
    word = line.split(",")
    number = float(word[1])
    number = number+number
    if word[0] in length_normal2:
        length_normal2[word[0]] += number
    else:
        length_normal2.add(word[0],number)


def avdl(length_norm):
    sum=0
    for i in length_norm.values():
        sum=sum+float(i)
    return float(sum)/float(len(length_norm))

#score_dict={}
#score_dict2={}

def document_length(docid):
    counter=0
    for i in docid_tf_tfw_list:
        line=i.split(",")
        if line[0]==docid:
            counter=counter+1

    return counter

'''for i in length_normal:
    dl=document_length(length_normal[i])
    score=okapi(len(length_normal),length_normal[i],dl,avdl1,len(docid_tf_tfw_list))
    if i in score_dict:
        score_dict[i]=float(score_dict[i])+float(score)
    else:
        score_dict[i]=score

for i in length_normal2:
    dl=document_length(length_normal2[i])
    score=okapi(len(length_normal2),length_normal2[i],dl,avdl2,len(docid_tf_tfw_list))
    if i in score_dict2:
        score_dict2[i]=float(score_dict2[i])+float(score)
    else:
        score_dict2[i]=score
'''


#======================================================================================================================== QUERY AND COSINE SIMILARITY
query_token = input("Please enter a query\n")  #  Requesting the query term from User
list1 = query_token.split()
for e in list1:
    if not (e.isalnum()):
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
                if (e_sub == '.'):
                    continue
                else:
                    e = e.replace(e_sub, '')
                    continue

            else:
                e = e.replace(e_sub, '')
        e = e.lower()
        e = ps.stem(e)
        query_terms.append(e)

    else:
        e = e.lower()
        e = ps.stem(e)
        query_terms.append(e)

posting_list=[]
post_list={}

j=0
df_list=[]

file3 = open("revised_postings.txt","w")
i=0
file2 = open("posting.txt","r")
for n, line in enumerate(file2.readlines()): # HERE WE WRITE TERM FREQUENCY WEIGHT VALUES INTO NEW REVISED POSTING LIST AS (docID , tfw)
    word = line.split(',')
    number = int(word[1])
    number = 1 + math.log(number,10)
    result = str(word[0]) + " " + str(number) + "\n"
    file3.write(result)
    i=i+1
file2.close()
file3.close()


file4=open("revised_postings.txt","r")
for l in file4.readlines():
    posting_list.append(l)
file4.close()
#dictionary de tut
for i in query_terms:
    count = 0
    v=search(hash_table,i)
    v=v.split(" ")
    df_list.append(v[1])
    tf_list=[]
    while(count<int(v[1])):
        tf_list.append(list(posting_list[int(v[2])].split()))
        count=count+1
        v[2]=int(v[2])+1
    post_list[i] = tf_list

#print(df_list)
j=0

for i in query_terms:
    count = 0
    while(count<int(df_list[j])):
        t = N / int(df_list[j])   # N / idf
        product=float((post_list[i][count][1]))*math.log10(float(t))
        post_list[i][count][1]=product
        count=count+1
    j=j+1

query_dict={}
temp_query_dict = {}
for i in query_terms:
    query_dict[i]=query_terms.count(i)
    temp_query_dict[i] = query_terms.count(i)

j=0
#print(query_dict)
for i in query_dict:
    t = N / int(df_list[j])
    product=(1+int(query_dict[i]))*math.log10(float(t))
    query_dict[i]=product
    j=j+1



result_dict={}
result_dict2 = {}
df_dict={}
df_dict2={}
count=0
for i in query_terms:
    df_dict[i]=df_list[count]
    count=count+1

count=0
for i in query_terms:
    df_dict2[i]=df_list[count]
    count=count+1

j=0

for sub in df_dict:
    df_dict[sub] = int(df_dict[sub])

for sub in df_dict2:
    df_dict2[sub] = int(df_dict2[sub])

for i in range(0, len(df_list)):
    df_list[i] = int(df_list[i])

#================================================= STARTING OKAPI FUNCTION

k1=1.2
k2=1.2
b=0.75
#avdl1=avdl(length_normal)
avdl2=avdl(length_normal2)

t=0
tfi = 0
result_arr = []
result_final = []
while(j<int(max(df_list))):
    if(min(df_dict.values())) <=j:
        for z in list(df_dict):
            if (df_dict[z] == min(df_dict.values())):
                del df_dict[z]
    for i in df_dict:
       dci = (post_list[i][j][0]) #string type
       dfi = df_dict[i] # int type
       v = search(hash_table,i)
       v = v.split(" ")
       for t in range(0,dfi-1):
           if (temp_post_list[int(v[2])+t][0]) == dci:
               tfi = int((temp_post_list[int(v[2])+t][1]))
               break

       qtfi = int(temp_query_dict[i])
       dl = document_length(length_normal2[dci])
       K = k1 * ((1 - b) + b * (float(dl) / float(avdl2)))
       wi = math.log(((N - dfi + 0.5) / (dfi + 0.5)), 10)
       dti = ((k1 + 1) * tfi) / (K + tfi)
       qti = ((k2 + 1) * qtfi) / (k2 + qtfi)
       res = wi * dti * qti
       result_arr.append(i)
       result_arr.append(wi)
       result_arr.append(dti)
       result_arr.append(qti)
       result_arr.append(res)
       if(dci in result_dict2.keys()):
            result_dict2[dci] = result_dict2[dci] + result_arr
            result_arr = []
            result_dict2[dci][4] += res
       else:
            result_dict2[dci] = result_arr
            result_arr = []
    j=j+1

sorted_o = sorted(result_dict2.items(), key=lambda e: e[1][4], reverse=True)
#================================================================
j=0
file7=open("okaquery4result.txt","w") # HERE IS WRITING OKAPI SIMILARITIES TO TXT FILE
if (int(len(sorted_o)) > 10):
    count = 0
    for i in sorted_o:
        #print((i[1][0]))
        if (count == 10):
            break
        num = len(i[1])
        j = 0
        while j < num:
            string = ""
            string = "("+ str(i[1][j]) +", " + str(i[1][j+1]) + ", "+  str(i[1][j+2]) + ", " + str(i[1][j+3]) + ")"+"\n"
            file7.write(string)
            j = j+5
        string = ""
        string = "docID:" + str(i[0]) + "      Similarity:" + str(i[1][4]) + "\n"
        file7.write(string)
        count = count+1
    file7.close()
else:
    for i in sorted_o:
        j = 0
        num = len(i[1])
        while j < num:
            string = ""
            string = "(" + str(i[1][j]) + ", " + str(i[1][j + 1]) + ", " + str(i[1][j + 2]) + ", " + str(i[1][j + 3]) + ")" + "\n"
            file7.write(string)
            j = j + 5
        string = ""
        string = "docID:" + str(i[0]) + "      Similarity:" + str(i[1][4]) + "\n"
        file7.write(string)
    file7.close()
#========================================================================================================
print(df_dict2)
j=0
while(j<int(max(df_list))):  # IN THIS ITERATION, WE CALCULATE COSINE SIMILARITY SCORES BEFORE MULTIPLYING DOCUMENT LENGTH FACTOR
    if(min(df_dict2.values()))<=j:
        for z in list(df_dict2):
            if (df_dict2[z] == min(df_dict2.values())):
                del df_dict2[z]
    for i in df_dict2:
        res=(float(post_list[i][j][1]))*(float(query_dict[i]))
        if(post_list[i][j][0] in result_dict.keys()):
            result_dict[post_list[i][j][0]] = float(result_dict[post_list[i][j][0]]) + float(res)

        else:
            result_dict[post_list[i][j][0]]=res
    j+=1
#print(result_dict)


for key in result_dict:  # DOCUMENT LENGTH NORMALIZATION ARE DONE HERE FOR EACH DOCUMENT
    for key2 in length_normal:
        if(key==key2):
            result_dict[key]=(float(result_dict[key]))*(1/(math.sqrt(length_normal[key])))


sorted_d = sorted(result_dict.items(), key=operator.itemgetter(1),reverse=True)

#============================================================================================ WRITING COSINE SIMILARITY TO TXT FILE
#print(pos_index)
file6=open("cosquery4result.txt","w") # HERE IS PRINTING 10 RESULTS INTO TXT FILES
if(int(len(sorted_d))>10):
    count=0
    for i in sorted_d:
        #print(i[0])
        if(count==10):
            break
        for j in query_terms:
            final_dft = int(pos_index[j][0])
            final_idf = math.log(N / final_dft,10)
            final_w_q = query_dict[j]
            final_l_normal = 1 / (length_normal[i[0]])
            for t in post_list[j]:
                if t[0] == i[0]:
                    final_tfw_d = float(t[1]) * final_idf
                    result = "(" + str(j)+", "+ str(final_w_q)+", "+ str(final_tfw_d) + ", "+ str(final_l_normal)+")"+"\n"
                    file6.write(result)
                    break

            
            
        result = ""
        result = "docID:"+str(i[0])+"      Similarity:"+str(i[1])+"\n"
        file6.write(result)
        result = ""
        count=count+1
else:
    for i in sorted_d:
        for j in query_terms:
            final_dft = int(pos_index[j][0])
            final_idf = math.log(N / final_dft, 10)
            final_w_q = query_dict[j]
            final_l_normal = 1 / (length_normal[i[0]])
            for t in post_list[j]:
                if t[0] == i[0]:
                    final_tfw_d = float(t[1]) * final_idf
                    result = "(" + str(j) + ", " + str(final_w_q) + ", " + str(final_tfw_d) + ", " + str(
                        final_l_normal) + ")" + "\n"
                    file6.write(result)
                    break
        result = ""
        result = "docID:" + str(i[0])+"      Similarity:" + str(i[1]) + "\n"
        file6.write(result)
        result = ""
