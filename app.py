from flask import Flask
from flask import render_template
import requests
from flask import request, json
import os

app = Flask(__name__)

@app.route("/")
def hello():
    #return "Hello, World!"
    return render_template("public/form.html")

@app.route('/form1',methods=['GET','POST'])
def s1():
    if request.method=='GET':
        return render_template("public/s1.html")
    elif request.method=='POST':
        pno=request.form.get("pno")
        pno=int(pno)
        return render_template("public/s2.html")

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
        #search string by user
        s_list=[]
        s_list.append(name)
        s_list.append(des)
        s_list.append(char)
        s_list.append(func)
        s_list.append(funcd)
        s_list.append(dem)
        sch=""
        for i in s_list:
            if i!="":
                sch+=i+" "
        #postman code to hit azure api
        url = "https://qnaversion3-asvagkygeipvz44.search.windows.net/indexes/latest-azuresql-index/docs/search?api-version=2020-06-30"

        payload = '{\r\n    \"search\":\"'+sch+'\"\r\n}'
        headers = {'api-key': '4A50EEE8690AC6E0407E1C7969CACE5A',
                    'Content-Type': 'application/json'
                    }

        response = requests.request("POST", url, headers=headers, data = payload)
        res=response.json()
        r_list=[]
        if res['value']==[]:
            ex="Caution: The results are blank because the part details you've entered might not exist. Please try again!"
        else:
            ex="We found the following details:"
            for i in range(0,3):
                r_list.append(res['value'][i])
        return render_template("public/form_result1.html",data=r_list,ex=ex)


if __name__ == "__main__":
    app.run(debug=True,
		threaded=True, use_reloader=False)
