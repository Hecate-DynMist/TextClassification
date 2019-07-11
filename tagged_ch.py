
# coding: utf-8

# In[31]:


import pandas as pd
article = pd.read_excel('Articles56.xlsx')
daily = pd.read_excel('Dailies56.xlsx')
label = pd.read_excel('label.xlsx')

article = article[['id','title','description','content']]
daily = daily[['id','title','content']]
article.name='article'
daily.name='daily'

import re
def clean(raw):
    r1 = u'[a-zA-Z0-9’!"#$%&\'()*+,-./:;<=>?@，。?★、…【】《》？“”‘’！[\\]^_`{|}~\s（）：△ ©]+'
    r2 = "[\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）]+"
    r3 =  "[.!//_,$&%^*()<>+\"'?@#-|:~{}]+|[——！\\\\，。=？、：“”‘’《》【】￥……（）△:]+" 
    r4 =  "\\【.*?】+|\\《.*?》+|\\#.*?#+|[.!/_,$&%^*()<>+""'?@|:~{}#]+|[——！\\\，。=？、：“”‘’￥……（）《》【】]"

    text1 = re.sub(r1,'',raw)
    text2 = re.sub(r2,'',text1)
    text3 = re.sub(r3,'',text2)
    text4 = re.sub(r4,'',text3)
    return text4


def septext(text):
    Lword = []
    for x in text: 
        Lword.append(''.join(x))
    with open('/home/lene/Documents/chinese_stop_words.txt') as f:
        stopWords = [line.strip() for line in f.readlines()]
    stopWords.extend(['跟', '后', '在','再次','多个','的','另','被','年','月','而','与','所以','这些',                       '近年来','我','文曾','至','以','去年','为','已','人'])
    words = [w for w in Lword if w not in stopWords]
    return words

import jieba
import warnings
warnings.filterwarnings('ignore')

def token(df):
    df['ccontent'] = ''
    df['ctitle'] = ''
    df.content = df.content.astype(str)
    df.title = df.title.astype(str)

    for i in range(len(df)):
        df.ccontent[i] = septext(jieba.cut(clean(df.content[i])))
        df.ctitle[i] = septext(jieba.cut(clean(df.title[i])))
    return df

from ast import literal_eval
taga = pd.read_excel('article_tag_hecate.xlsx')
taga =tag[['title','name']]
tagd = pd.read_excel('daily_tag_hecate.xlsx')
tagd =tagd[['title','name']]

def merge(df,tag):
    df1 = pd.merge(df,tag,on='title',how='left')
    return df1

def transfername(df):
    df['tag_title'] = ''
    df['tag_name'] = ''
    df['tag_content'] = ''
    df.ctitle = df.ctitle.apply(set)
    df.ccontent = df.ccontent.apply(set)
    for i in range(len(df)):
        if str(df['name'][i])!='nan':
            df['name'][i] = set(literal_eval(df['name'][i]))
    return df

def match(words):
    tag=set()
    for column in label.columns:
        for word in words:
            if word in label[column].tolist():
                tag.add(str(column))
    return tag

def taged(df,base,tag):
    for i in range(len(df)):
        if str(df[base][i])!='nan':
            df[tag][i] = match(df[base][i])
    return df

def generate(df,tag):
    df1 = df.dropna(subset=['title'])
    df1 = merge(token(df1),tag)
    df1 = transfername(df1)
    taged(df1,'ctitle','tag_title')
    taged(df1,'name','tag_name')
    taged(df1,'ccontent','tag_content')
    df1.to_excel(df.name+'_tagged.xlsx')

generate(daily,tagd)
generate(article,tagd)

