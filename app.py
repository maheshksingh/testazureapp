from flask import Flask
from flask import render_template


app = Flask(__name__)

@app.route("/")
def hello():
    #return "Hello, World!"
    return render_template("public/form.html")

if __name__ == "__main__":
    app.run(debug=True,
		threaded=True, use_reloader=False)
