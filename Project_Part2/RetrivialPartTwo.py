import math
import re
from nltk.stem import PorterStemmer
import operator
class my_dictionary(dict):
    def __init__(self):
        self = dict()

    def add(self, key, value):
        self[key] = value


length_normal = my_dictionary()
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

file3 = open("revised_postings.txt","w")

file = open("dictionary.txt","r") # INSERTING DICTIONARY VALUES INTO HASH TABLE
for n, line in enumerate(file.readlines()):
    word = line.split();
    insert(hash_table,word[0],line);
file.close()
i=0
file2 = open("postings.txt","r")
for n, line in enumerate(file2.readlines()): # HERE WE WRITE TERM FREQUENCY WEIGHT VALUES INTO NEW REVISED POSTING LIST AS (docID , tfw)
    word = line.split()
    number = int(word[1])
    number = 1 + math.log(number,10)
    result = str(word[0]) + " " + str(number) + "\n"
    file3.write(result)
    i=i+1
file2.close()
file3.close()


file3 = open("revised_postings.txt","r")  # LENGTH NORMALIZATION FACTOR PART
for n, line in enumerate(file3.readlines()):
    word = line.split()
    number = float(word[1])
    number = number*number
    if word[0] in length_normal:
        length_normal[word[0]] += number
    else:
        length_normal.add(word[0],number)

for key in length_normal:
    length_normal[key] = 1 / (math.sqrt(length_normal[key]))
    #print(key + "--->" + str(length_normal[key]))
    #print(length_normal)

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
        tf_list.append(list(posting_list[int(v[2])-1].split()))
        count=count+1
        v[2]=int(v[2])+1
    post_list[i] = tf_list

j=0

for i in query_terms:
    count = 0
    while(count<int(df_list[j])):
        t=len(posting_list) / int(df_list[j])
        product=float((post_list[i][count][1]))*math.log10(float(t))
        post_list[i][count][1]=product
        count=count+1
    j=j+1

query_dict={}
for i in query_terms:
    query_dict[i]=query_terms.count(i)

j=0
for i in query_dict:
    t = len(posting_list) / int(df_list[j])
    product=(1+int(query_dict[i]))*math.log10(float(t))
    query_dict[i]=product
    j=j+1

result_dict={}
df_dict={}
count=0
for i in query_terms:
    df_dict[i]=df_list[count]
    count=count+1
j=0

for sub in df_dict:
    df_dict[sub] = int(df_dict[sub])

for i in range(0, len(df_list)):
    df_list[i] = int(df_list[i])

while(j<int(max(df_list))):  # IN THIS ITERATION, WE CALCULATE COSINE SIMILARITY SCORES BEFORE MULTIPLYING DOCUMENT LENGTH FACTOR
    if(min(df_dict.values()))<=j:
        for z in list(df_dict):
            if (df_dict[z] == min(df_dict.values())):
                del df_dict[z]
    for i in df_dict:
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
            result_dict[key]=(float(result_dict[key]))*(float(length_normal[key]))


sorted_d = sorted(result_dict.items(), key=operator.itemgetter(1),reverse=True)

if(int(len(sorted_d))>10): # HERE IS SHOWING 10 RESULTS IN TERMINAL
    count=0
    for i in sorted_d:

        if(count==10):
            break
        result="docID:"+str(i[0])+"      Similarity:"+str(i[1])+"\n"
        print(result)
        count=count+1
else:
    for i in sorted_d:
        result = "docID:" + str(i[0])+"      Similarity:" + str(i[1]) + "\n"
        print(result)


file6=open("query4result.txt","w") # HERE IS PRINTING 10 RESULTS INTO TXT FILES
if(int(len(sorted_d))>10):
    count=0
    for i in sorted_d:

        if(count==10):
            break
        result="docID:"+str(i[0])+"      Similarity:"+str(i[1])+"\n"
        file6.write(result)
        count=count+1
else:
    for i in sorted_d:
        result = "docID:" + str(i[0])+"      Similarity:" + str(i[1]) + "\n"
        file6.write(result)


