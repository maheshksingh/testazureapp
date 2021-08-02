#@Author: Rohin Singh

# #This is segment search mark3 and the improvements are as follows 
# -Improved accuracy of search 2
# -Suggestion engine added to search 2

from flask import Flask
from flask import render_template, abort, url_for, json, jsonify, Flask, Response, send_from_directory, send_file, Flask, make_response, request
import pandas as pd
import json
import os
import requests
import itertools
from operator import itemgetter
import pyodbc
from rank_bm25 import BM25Okapi

app = Flask(__name__)

# retrieve datasettry:
cnxn = pyodbc.connect('ODBC Driver 17 for SQL Server};'
'SERVER=tcp:segmentcodedbserver.database.windows.net,1433;'
'DATABASE=segmentcodedb;UID=segmentcode;PWD=Mahesh143;')

#reading input
@app.route('/',methods=['GET','POST'])
def anal():
        return render_template("public/form.html")

@app.route('/form1',methods=['GET','POST'])
def s1():
    if request.method=='GET':
        return render_template("public/s1.html")
    elif request.method=='POST':
        pno=request.form.get("pno")
        cursor = cnxn.cursor()
        cursor.execute("SELECT Partno,Name, Demarcation,Characteristics, Functiongroup,PartType,Weight,Material,Length,Width,Height,ReferencePart,PrecedingPart,SuccedingPart,SegmentCode,SegmentDescription FROM segmentjune03 WHERE Partno="+pno) 
        res = cursor.fetchone()
        nos={}

        #reference part
        if res[11]!=None:
            ref_no=res[11]
            cursor.execute("SELECT Partno,Name, SegmentCode,SegmentDescription FROM segmentjune03 WHERE Partno="+ref_no)
            ref=cursor.fetchone()
            nos['Reference Part']=ref
        #preceding part
        if res[12]!=None:
            pre_no=res[12]
            cursor.execute("SELECT Partno,Name, SegmentCode,SegmentDescription FROM segmentjune03 WHERE Partno="+pre_no)
            pre=cursor.fetchone()
            nos['Preceeding Part']=pre
        #succeeding part
        if res[13]!=None:
            suc_no=res[13]
            cursor.execute("SELECT Partno,Name, SegmentCode,SegmentDescription FROM segmentjune03 WHERE Partno="+suc_no)
            suc=cursor.fetchone()
            nos['Suceeding Part']=suc
        if res==None:
            ex="Caution: The results are blank because the number you've entered might not exist. Please try again!"
        else:
            ex="We found the following details:"
        return render_template("public/form_result.html",r=res,ex=ex,nos=nos)

@app.route('/form2',methods=['GET','POST'])
def s2(): 
    if request.method=='GET':
        return render_template("public/s2.html")
    elif request.method=='POST':
        name=request.form.get("pname")
        des=request.form.get("pdes")
        char=request.form.get("pchar")
        func=request.form.get("pfunc")
        funcd=request.form.get("pfuncd")
        dem=request.form.get("pdem")
        pty=request.form.get("pty")
        wgt=request.form.get("wgt")
        mat=request.form.get("mat")
        lgt=request.form.get("lgt")
        hgt=request.form.get("hgt")
        wdt=request.form.get("wdt")
        #search string by user
        s_list=[]
        s_list.append(name)
        s_list.append(des)
        s_list.append(char)
        s_list.append(func)
        s_list.append(funcd)
        s_list.append(dem)
        s_list.append(pty)
        s_list.append(wgt)
        s_list.append(mat)
        s_list.append(lgt)
        s_list.append(hgt)
        s_list.append(wdt)
        query=""
        for i in s_list:
            if i!="":
                query+=i+" "
        SQL_Query = pd.read_sql_query("select Name, Demarcation,Characteristics, Functiongroup,PartType,Weight,Material,Length,Width,Height,SegmentCode,SegmentDescription from segmentjune03 WHERE Name LIKE '%"+name+"%'", cnxn)
        df = pd.DataFrame(SQL_Query, columns=['Name','Demarcation','Charactersistics','Functiongroup','PartType','Weight','Material','Length','Width','Height','SegmentCode','SegmentDescription'])
        df.reset_index(level=0, inplace=True)
        df2 = df[df.columns[0:]].apply(lambda x: ' '.join(x.dropna().astype(str)),axis=1)
        list1 = df2.tolist()

        #parse list into corpus
        corpus = list1
        tokenized_corpus = [doc.split(" ") for doc in corpus]
        bm25 = BM25Okapi(tokenized_corpus)

        #result
        tokenized_query = query.split(" ")
        doc_scores = bm25.get_scores(tokenized_query)
        res=bm25.get_top_n(tokenized_query, corpus, n=3)
        #Extracting index numbers of results to fetch from db
        index=[]
        result_df=pd.DataFrame()
        for i in res:
            first=i.split(" ")[0]
            index.append(first)
        #extracting result rows from dataframe
        for i in index:
            i=int(i)
            result_df = result_df.append(df[df['index'] == i])
        result = result_df.to_dict(
                orient='records', 
                )        
        if result==None:
            ex="Caution: The results are blank because the number you've entered might not exist. Please try again!"
        else:
            ex="We found the following details:"
        return render_template("public/form_result1.html",data=result,ex=ex)

@app.route('/dummy',methods=['GET','POST'])
def blank():
    return render_template("public/dummy.html")

@app.route('/loading',methods=['GET','POST'])
def load():
    return render_template("public/loading.html")

if __name__ == "__main__":
    app.run(debug=True,
		threaded=True, use_reloader=False)
