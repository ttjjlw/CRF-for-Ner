# 环境配置：
crf_learn.exe

crf_test.exe

libcrfpp.dll

template.txt

必须含有以上文件，才可以运行本模型。

# 数据格式：

train_set 格式如下：
> 7212_17592_21182/c  8487_8217_14790_19215_4216_17186_6036_18097/o/n
> 4234_11634_7747/b  16108_13711_3445_14499_4688/o/n
...
test_set格式如下：
> 2240_7105_4246_21224_962_13514_2203_17735_16929_4531_5025/n
> 17624_9942_8428_16419_7040_6000_4250_3445/n
...
输入：
训练时，设置以下参数

train_set='data_set/trains.txt'  #训练数据

dg_train_set='dg_data_set/dg_trains.txt'

off_tag_train_set='offtag_set/offtag_trains.txt'

dg_off_tag_train_set='dg_data_set/dg_off_tag_trains.txt'

valid_set='data_set/train_v.txt' #验证集

off_tag_valid_set='offtag_set/offtag_valid.txt'

dg_valid_set='dg_data_set/dg_valid.txt'

预测输出结果时：
train_set='data_set/trains.txt'  #训练数据

dg_train_set='dg_data_set/dg_trains.txt'

off_tag_train_set='offtag_set/offtag_trains.txt'

dg_off_tag_train_set='dg_data_set/dg_off_tag_trains.txt'

`以上也可不需要，直接利用训练过程保存的模型`

test_set='data_set/test.txt' #测试集

dg_test_set='dg_data_set/dg_test.txt'

