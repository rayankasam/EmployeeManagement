from flask import Flask, redirect, render_template, url_for, session, request
from dbInteraction.addEmployee import addToDB
from dbInteraction.checkPass import checkPassword
from dbInteraction.time import punchIN
from dbInteraction.time import punchOut
from dbInteraction.getData import getData
from applySpecs import allowedAddEmployee
app = Flask(__name__)
app.secret_key = b"2234JHG3[]opuhmiy757n7ijNT756654"
error = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        data = request.form.to_dict()
        if 'email' not in data or 'password' not in data:
            return redirect(url_for('index'))
        if checkPassword(request.form['email'],request.form['password']):
            session['username'] = request.form['email']
            session['permissions'] = getData(session['username'])['permissionType']
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
    if session.get('username') is not None and allowedAddEmployee(getData(session['username'])['permissionType']):
        return render_template("addEmployee.html")
    else:
        return redirect(url_for('index'))


@app.route('/shiftPunches', methods=['GET', 'POST'])
def shiftPunches():
    ID = getData(session['username'])['employeeID']
    if request.method == 'POST':
        data = request.form.get('punch')
        print(data)
        print(ID)
        if (data == 'IN'):
            punchIN(ID)
        elif (data == 'OUT'):
            punchOut(ID)
        return redirect(url_for('index'))
    return render_template("shiftPunches.html")
        
    
        
    
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route("/test")
def tester():
    error = "Error applied"
    return redirect(url_for("index"))

if __name__ == '__main__':
    app.debug = True
    app.run()
