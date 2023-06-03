from flask import Flask, redirect, render_template, render_template_string,url_for, session, request
from checkPass import *
from addEmployee import *
app = Flask(__name__)
app.secret_key = b"2234JHG3[]opuhmiy757n7ijNT756654"
error = None
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        if checkPassword(request.form['email'],request.form['password']):
            session['username'] = request.form['email']
        return redirect(url_for('index'))
    return render_template("login.html")

@app.route('/addEmployee',methods=['GET','POST'])
def addEmployee():
    if request.method == 'POST':
        data = request.form.to_dict()
        print(data)
        if data['mName'] == "":
            data['mName'] = None
        if data['lName'] == "":
            data['lName'] = None
        if data['position'] == "":
            data['position'] = None
        try:
            addToDB(data)
        except:
            print("Failed to add data")
        return redirect(url_for('index'))
    return render_template("addEmployee.html")

@app.route("/test")
def tester():
    error = "Error applied"
    return redirect(url_for("index"))

if __name__ == '__main__':
    app.debug = True
    app.run()
