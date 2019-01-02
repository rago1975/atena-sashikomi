#!/usr/bin/python
#-*- coding: utf-8 -*-
import sys
import datetime
import csv
import mojimoji
import subprocess

class Mkdata:
    jusho1 = []
    jusho2 = []
    bangou = []
    namae1 = []
    namae2 = []
    namae3 = []
    namae4 = []
    namae5 = []
    namae6 = []

    # .csvファイルを開く。辞書型で読み取り
    with open('juushoroku.csv', 'r') as f:
        datcsv = csv.DictReader(f)

        for row in datcsv:
            jusho1.append(row['住所１'])   
            jusho2.append(row['住所２'])
            bangou.append(row['郵便番号'])
            namae1.append(row['名前１'])
            namae2.append(row['名前２'])
            namae3.append(row['名前３'])
            namae4.append(row['名前４'])
            namae5.append(row['名前５'])
            namae6.append(row['名前６'])

    # 住所録の件数
    datasize = len(jusho1)

class Mktexfile:

    texbody = ''
    tab1 = '        '
    setlen = r'\setlength{\unitlength}{1truemm}'
    beginpic1 = r'\begin{picture}(20,96)(0,0)' # 郵便番号欄
    beginpic2 = r'\begin{picture}(122,96)(20,0)' # 宛名欄
    endpic = r'\end{picture}'
    
    # 郵便番号欄の各数字のポジション
    numposi = [[10,45.0],[10,52.0],[10,59.0],[10,66.6],[10,73.4],[10,80.2],[10,87.0]]
    numposi2 = []

    for i in range(7):
        numposi2.append(r'\put(' + str(numposi[i][0]) + ',' + str(numposi[i][1])+ r'){')

    # 宛名各要素のポジション
    ju1posi = r'\put(20,80){'
    ju2posi = r'\put(30,70){'
    na1posi = r'\put(30,50){'
    na2posi = r'\put(55,50){'
    na3posi = r'\put(30,40){'
    na4posi = r'\put(55,40){'
    na5posi = r'\put(55,30){'
    na6posi = r'\put(55,20){'
    samaposi = r'\put(83,50){'
    sama2posi = r'\put(83,40){'

    # texファイルのヘッダ
    with open('pretext.txt' , 'r') as f1:
        pretex = f1.read()

    # texファイルのフッタ
    with open('posttext.txt' , 'r') as f2:
        posttex = f2.read()

    texbody += pretex + '\n'

    for i in range(Mkdata.datasize):
        bangou_tmp = mojimoji.han_to_zen(Mkdata.bangou[i])
        texbody += setlen + '\n' + beginpic1 + '\n'
        
        for j in range(7):
            texbody = texbody + tab1 + numposi2[j] + r'\large ' + bangou_tmp[j] + r'}' + '\n'

        texbody += endpic + '\n'
        texbody += beginpic2 + '\n'

        jusho1_tmp = mojimoji.han_to_zen(Mkdata.jusho1[i])
        jusho2_tmp = mojimoji.han_to_zen(Mkdata.jusho2[i])

        if len(jusho1_tmp) > 17 or len(jusho2_tmp) > 15:
            ju1size = r'\large '
        else:
            ju1size = r'\Large '

        
        texbody += tab1 + ju1posi + ju1size + jusho1_tmp + r'}' + '\n'
        texbody += tab1 + ju2posi + ju1size + jusho2_tmp + r'}' + '\n'
        texbody += tab1 + na1posi + r'\huge ' + Mkdata.namae1[i] + r'}' + '\n'
        texbody += tab1 + na2posi + r'\huge ' + Mkdata.namae2[i] + r'}' + '\n'
        texbody += tab1 + samaposi + r'\huge ' + r'様}' + '\n'
        texbody += tab1 + na3posi + r'\huge ' + Mkdata.namae3[i] + r'}' + '\n'
        texbody += tab1 + na4posi + r'\huge ' + Mkdata.namae4[i] + r'}' + '\n'

        if len(Mkdata.namae4[i]) == 0 :
            pass
        else:
            texbody += tab1 + sama2posi + r'\huge ' + r'様}' + '\n'

        if len(Mkdata.namae5[i]) == 0 :
            pass
        else:
            texbody += tab1 + na5posi + r'\huge ' + Mkdata.namae5[i] + r'　様}' + '\n'

        if len(Mkdata.namae6[i]) == 0 :
            pass
        else:
            texbody += tab1 + na6posi + r'\huge ' + Mkdata.namae6[i] + r'　様}' + '\n'

        texbody +=  endpic + '\n'

        if i < (Mkdata.datasize - 1):
            texbody += r'\newpage' + '\n'
        else:
            texbody += posttex + '\n'

    with open('atena-sashikomi.tex', 'w') as f3:
        f3.write(texbody)

    try:
        subprocess.run('lualatex  atena-sashikomi.tex', shell=True, check=True)
    except subprocess.CalledProcessError:
        print('外部プログラムの実行に失敗しました')
    else:
        subprocess.run('qpdfview atena-sashikomi.pdf &' , shell=True)

def main():
    Mktexfile()

if __name__ == '__main__':
    main()
