#@Author: Rohin Singh

from flask import Flask
from flask import render_template, abort, url_for, json, jsonify, Flask, Response, send_from_directory, send_file, Flask, make_response, request
import pandas as pd
import json
import os
import requests
import pyodbc

app = Flask(__name__)

#initialising s1
# filename = os.path.join(app.root_path,'data/data.json')
# with open(filename) as outfile:
# data = "https://segmentcode.blob.core.windows.net/segmentcodecontainer/data.json?sp=r&st=2021-06-07T13:01:31Z&se=2021-06-07T21:01:31Z&spr=https&sv=2020-02-10&sr=b&sig=e2MX6C%2F3%2Fu2vy99YYZdnynteNWKsu68QHn%2BvU8kBTfA%3D"

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
        import pyodbc 
        cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                      'SERVER=tcp:segmentcodedbserver.database.windows.net,1433;'
                      'DATABASE=segmentcodedb;UID=segmentcode;PWD=Mahesh143;')

        cursor = cnxn.cursor()
        cursor.execute("SELECT Partno,Name,Demarcation,Functiongroup,PartType,SegmentCode,SegmentDescription FROM segmentjune03 WHERE Partno="+pno) 
        res = cursor.fetchone()
        if res==None:
            ex="Caution: The results are blank because the number you've entered might not exist. Please try again!"
        else:
            ex="We found the following details:"
        return render_template("public/form_result.html",r=res,ex=ex)

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
        sch=""
        for i in s_list:
            if i!="":
                sch+=i+" "
        #postman code to hit azure api
        url = "https://cognitivesearchtest.search.windows.net/indexes/segetcode-column-wise-azuresql-index/docs/search?api-version=2020-06-30-Preview&query_type=semantic&searchFields=Partno,Name,Demarcation,Characteristics,Functiongroup,PartType,Weight,Material,Length,Width,Height&queryLanguage=en-us"

        payload = json.dumps({
            "search": sch
        })
        headers = {
        'api-key': 'A328C26CC0F9AF89AC6ABF68E0A809E2',
        'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        res=response.json()
        r_list=[]
        if res['value']==[]:
            ex="Caution: The results are blank because the part details you've entered might not exist. Please try again!"
        else:
            ex="We found the following details:"
            r=res['value']
	    unique={elem["Functiongroup"]: elem for elem in r}.values() 
            unique=list(unique)
        return render_template("public/form_result1.html",data=unique,ex=ex)

@app.route('/dummy',methods=['GET','POST'])
def blank():
    return render_template("public/dummy.html")


if __name__ == "__main__":
    app.run(debug=True,
		threaded=True, use_reloader=False)
