import codecs
import os

# 0 install crf++ https://taku910.github.io/crfpp/
# 1 train data in
# 2 test data in
# 3 crf train
# 4 crf test
# 5 submit test
'''train_set->get_dg_train->model  offtag_train_set->dgofftag_train_set->model->result_file->get_f1score->训练集的f1score'''
'''offtag_valid_set->dg_offtag_valid_set->model->get_fiscore->验证集上的f1score'''
data_set_path='data_set/'
dg_data_set_path='dg_data_set/'
offtag_set_path='offtag_set/'
for path in [data_set_path,dg_data_set_path,offtag_set_path]:
    if not os.path.exists(path):
        os.makedirs(path)

train_set='data_set/train_t_8.txt'  #训练数据
dg_train_set='dg_data_set/train_t_8.txt'
off_tag_train_set='offtag_set/offtag_train_t_8.txt'
dg_off_tag_train_set='dg_data_set/dg_off_tag_train_t_8.txt'


valid_set='data_set/train_v_8.txt' #验证集
off_tag_valid_set='offtag_set/offtag_valid.txt'
dg_valid_set='dg_data_set/dg_valid.txt'

test_set='data_set/test.txt' #测试集
dg_test_set='dg_data_set/dg_test.txt'
valid_flag=1 #01表示训练，输出验证集f1score，0则直接生成预测文件
def get_f1score(result_file, target_file):
    result = open(result_file, 'r', encoding='utf-8')
    target = open(target_file, 'r', encoding='utf-8')
    r_lines = result.readlines()
    t_lines = target.readlines()
    total_tags = 0  # target样本的字段数
    correct_tags = 0  # result中抽取出的正确字段数
    total_tab_tags = 0  # result中抽取出的字段数
    for r_line, t_line in zip(r_lines, t_lines):
        r_lis = r_line.split('  ')
        t_lis = t_line.split('  ')
        for r_tag, t_tag in zip(r_lis, t_lis):
            if t_tag[-1] in ['a', 'b', 'c']:
                total_tags += 1
            if r_tag[-1] in ['a', 'b', 'c']:
                total_tab_tags += 1
                if r_tag[-1] == t_tag[-1] and len(r_tag) == len(t_tag):
                    correct_tags += 1
    recall = round(correct_tags / total_tags, 4)
    precise = round(correct_tags / total_tab_tags, 4)
    f1score = round(2 * recall * precise / (recall + precise), 4)
    result.close()
    target.close()
    return f1score



def off_tags(train_file,offtag_file,n=10**10):
    write_str_lis = []
    with open(train_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            str_lis=[]
            for tag in line.strip().split('  '):
                str_lis.append(tag[:-2])
            write_str_lis.append('_'.join(str_lis)+'\n')
            if len(write_str_lis)>=n:  #取到设置的行数就退出
                break
    with open(offtag_file,'w',encoding='utf-8') as f:
        f.writelines(write_str_lis)

#off_tags(train_file,offtag_file,2000)

def get_dg_train(train_dir,dg_train_dir):
    '''
    :param train_dir:
    :param dg_train_dir:
    :return:
    '''
    with codecs.open(train_dir, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        results = []
        for line in lines:
            features = []
            tags = []
            samples = line.strip().split('  ')
            for sample in samples:
                sample_list = sample[:-2].split('_')
                tag = sample[-1]
                features.extend(sample_list)
                tags.extend(['O'] * len(sample_list)) if tag == 'o' else tags.extend(
                    ['B-' + tag] + ['I-' + tag] * (len(sample_list) - 1))
            results.append(dict({'features': features, 'tags': tags}))
        # [{'features': ['7212', '17592', '21182', '8487', '8217', '14790', '19215', '4216', '17186', '6036',
        # '18097', '8197', '11743', '18102', '5797', '6102', '15111', '2819', '10925', '15274'],
        # 'tags': ['B-c', 'I-c', 'I-c', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O',
        # 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O']}]
        train_write_list = []
        with codecs.open(dg_train_dir, 'w', encoding='utf-8') as f_out:
            for result in results:
                for i in range(len(result['tags'])):
                    train_write_list.append(result['features'][i] + '\t' + result['tags'][i] + '\n')
                train_write_list.append('\n')
            f_out.writelines(train_write_list)


def get_dg_test(test_dir,dg_test_dir):
    '''

    :param test_dir:
    :param dg_test_dir:
    :return: 获得dg_test与通过get_dg_train获得dg_train不同，每个句子之间隔两行，而且没有标签
    '''
    with codecs.open(test_dir, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        results = []
        for line in lines:
            features = []
            sample_list = line.split('_')
            features.extend(sample_list)
            results.append(dict({'features': features}))
        test_write_list = []
        with codecs.open(dg_test_dir, 'w', encoding='utf-8') as f_out:
            for result in results:
                for i in range(len(result['features'])):
                    test_write_list.append(result['features'][i] + '\n')
                test_write_list.append('\n')
            f_out.writelines(test_write_list)


def Gettime(p=''):
    import time
    t = time.asctime(time.localtime(time.time()))  # t=Thu Jul 25 09:53:23 2019
    t = t.split()[2:4]  # t=['25', '09:54:56']
    d = [t[0]] + t[1].split(':')[:-1]
    d = '_'.join(d)+" "+p
    return d  # d=25_09_54
def get_result_file(dg_file,result_file):
    f_write = open(result_file, 'w', encoding='utf-8')
    with open(dg_file, 'r', encoding='utf-8') as f:
        lines = f.read().split('\n\n')
        for line in lines:
            if line == '':
                continue
            tokens = line.split('\n')
            features = []
            tags = []
            for token in tokens:
                feature_tag = token.split()
                if len(feature_tag) < 2:
                    print(feature_tag)
                    continue
                features.append(feature_tag[0])
                tags.append(feature_tag[-1])
            samples = []
            i = 0
            while i < len(features):
                sample = []
                if tags[i] == 'O':
                    sample.append(features[i])
                    j = i + 1
                    while j < len(features) and tags[j] == 'O':
                        sample.append(features[j])
                        j += 1
                    samples.append('_'.join(sample) + '/o')

                else:
                    if tags[i][0] != 'B':
                        print(tags[i][0] + ' error start')
                    sample.append(features[i])
                    j = i + 1
                    while j < len(features) and tags[j][0] == 'I' and tags[j][-1] == tags[i][-1]:
                        sample.append(features[j])
                        j += 1
                    samples.append('_'.join(sample) + '/' + tags[i][-1])
                i = j
            f_write.write('  '.join(samples) + '\n')
    f_write.close()
if not os.path.isfile(off_tag_train_set):
    print('训练集offtags....')
    off_tags(train_set,off_tag_train_set)  #给训练集脱tags
if not os.path.isfile(off_tag_valid_set):
    off_tags(valid_set,off_tag_valid_set)  #给验证集脱tags
    print('验证集offtags....')
# step 1 train offtag_train in
if not os.path.isfile(dg_train_set):
    get_dg_train(train_dir=train_set,dg_train_dir=dg_train_set)
    print(train_set[-9:]+' dg中...')
if not os.path.isfile(dg_off_tag_train_set):
    get_dg_test(test_dir=off_tag_train_set,dg_test_dir=dg_off_tag_train_set)
    print('dg_off_tag_train dg中...')
# step 2 test data in
if valid_flag:
    test=off_tag_valid_set
    dg_test=dg_valid_set
else:
    test = test_set
    dg_test = dg_test_set
if not os.path.isfile(dg_test):
    get_dg_test(test_dir=test,dg_test_dir=dg_test)
    print(test+' dg中...')

para_lis=['-f 2 -c 12 -m 500']
f1_score=[]
if not os.path.exists('dg_result/'):os.makedirs('dg_result/')
for para in para_lis:
    # 3 crf train
    crf_train = "crf_learn " + para + " template.txt " + dg_train_set + " dg_model"
    print(crf_train)
    os.system(crf_train)

    # 4 crf test
    ###############  注意：此处的 dg_test 文件是每句话隔两行
    crf_test = "crf_test -m dg_model"+" " + dg_test + " -o dg_result/dg_result.txt"
    os.system(crf_test)

    #5 crf train
    crf_train_test="crf_test -m dg_model"+" "+ dg_off_tag_train_set+" -o dg_result/dg_result_train.txt"
    os.system(crf_train_test)
    T = Gettime('')
    valid_submit_dir='valid_submit_dir/'
    if not os.path.exists(valid_submit_dir):os.makedirs(valid_submit_dir)
    submit_dir='submit_dir/'
    if not os.path.exists(valid_submit_dir): os.makedirs(submit_dir)
    if valid_flag:
        result_file = valid_submit_dir + 'dg_val_resullt' + T+ '.txt'
    else:
        result_file=submit_dir + 'dg_submit' + T+'_'.join(para) + '.txt'
    result_file_t=valid_submit_dir+'train_result'+T+'.txt'
    # 5 submit data
    get_result_file(dg_file="dg_result/dg_result.txt",result_file=result_file)
    get_result_file(dg_file="dg_result/dg_result_train.txt",result_file=result_file_t)
    # calcuate f1score
    train_f1score=get_f1score(result_file=result_file_t,target_file=train_set)
    print('训练集f1score:',train_f1score)

    if valid_flag:
        val_f1score=get_f1score(result_file=result_file,target_file=valid_set)
        print('验证集f1score:',val_f1score)
        if not os.path.exists('logs/'):os.makedirs('logs/')
        with open ('logs/logs.txt','a',encoding='utf-8') as f:
            f.write('训练集f1score: '+str(train_f1score)+'验证集f1score: '
                    +str(val_f1score)+' '+T+crf_train[:-33]+"\n")
        f1_score.append(val_f1score)
        if len(f1_score)>=4:
            if f1_score[-1]<f1_score[-2] and f1_score[-2]<=f1_score[-3] and f1_score[-3]<=f1_score[-4]:
                exit()