# D:\localE\python
# -*-coding:utf-8-*-
# Author ycx
# Date
file=open('data_set/trains.txt','r',encoding='utf-8')
train=open('data_set/train_t_3.txt','w')
valid=open('data_set/train_v_3.txt','w')
lines=file.readlines()
print(len(lines))
i=1
lis_t=[]
lis_v=[]
for line in lines:
    if i%8!=0 and i%7!=0 and i%3==0and len(lis_v)<2000:
        lis_v.append(line)
    else:
        lis_t.append(line)
    i+=1
print(i)
print(len(lis_v))
print(len(lis_t))
train.writelines(lis_t)
valid.writelines(lis_v)

# file=open('data_set/corpus.txt','r',encoding='utf-8')
# train=open('offtag_set/offtag_trains.txt','r',encoding='utf-8')
# test=open('data_set/test.txt','r',encoding='utf-8')
# file_all=open('data_set/corpus_all.txt','w')
# for line in file.readlines():
#     file_all.write(line)
# for line in train.readlines():
#     file_all.write(line)
# for line in test.readlines():
#     file_all.write(line)
#
# file.close()
# train.close()
# file_all.close()

# file_all=open('data_set/corpus_all.txt','r',encoding='utf-8')
# lines=file_all.readlines()
# print(len(lines))
# file=open('data_set/corpus.txt','r',encoding='utf-8')
# lines=file.readlines()
# print(len(lines))
