from flask import Flask, redirect, render_template, url_for, session, request
from dbInteraction.addEmployee import addToDB
from dbInteraction.checkPass import checkPassword
from dbInteraction.time import punchIN
from dbInteraction.time import lastPunch
from dbInteraction.time import currentShift
from dbInteraction.timeWorked import today
from dbInteraction.timeWorked import weekToDay
from dbInteraction.timeWorked import monthToDay
from dbInteraction.timeWorked import custom
from dbInteraction.timeWorked import certainDate
from dbInteraction.timeWorked import beforeDate
from dbInteraction.timeWorked import afterDate
from dbInteraction.timeWorked import certainMonth
from dbInteraction.timeWorked import certainYear
from dbInteraction.shifts import getPeople
from dbInteraction.shifts import addShifts
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
            session['firstName'] = getData(session['username'])['firstName']
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
        if (data == 'IN'):
            punchIN(ID)
        elif (data == 'OUT'):
            punchOut(ID)
        session['lastPunch'] = lastPunch(ID)
        return redirect(url_for('index'))
    return render_template("shiftPunches.html")
        
@app.route('/timeWorked', methods=['GET', 'POST'])
def timeWorked():
    ID = getData(session['username'])['employeeID']
    if request.method == 'POST':
        data = request.form.to_dict()
        print(data)   
        if data['dates'] == 'TODAY':
            print("today")
            output = today(ID)
            return render_template('timeWorked.html', output=output)

        elif data['dates'] == 'WTD':
            output = weekToDay(ID)
            return render_template('timeWorked.html', output=output)
        
        elif data['dates'] == 'MTD':
            output = monthToDay(ID)
            return render_template('timeWorked.html', output=output)
            
        elif data['dates'] == 'CD':
            output = certainDate(ID, data['certainDate'])
            return render_template('timeWorked.html', output=output)
            
        elif data['dates'] == 'CY':
            output = certainYear(ID, data['certainYear'])
            return render_template('timeWorked.html', output=output)
            
        elif data['dates'] == 'CM':
            output = certainMonth(ID, data['certainMonth'])
            return render_template('timeWorked.html', output=output)
            
        elif data['dates'] == 'BEFORE':
            output = beforeDate(ID, data["beforeDate"])
            return render_template('timeWorked.html', output=output)

            
        elif data['dates'] == 'AFTER':
            output = afterDate(ID, data["afterDate"])
            return render_template('timeWorked.html', output=output)
            
        elif data['dates'] == 'CUS':
            output = custom(ID, data["startDate"], data["endDate"])
            return render_template('timeWorked.html', output=output)

        else:
            return render_template("timeWorked.html")
    return render_template("timeWorked.html")


@app.route('/addShifts', methods=['GET', 'POST'])
def addShifts():
    employees = getPeople()
    if request.method == 'POST':
        data = request.form.to_dict()
        print(data)
        print(data['employee'])
        print(data['startTime'])
        print(data['endTime'])
        print(data['shiftType'])
        
        addShifts(data['employee'], data['startTime'], data['endTime'], data['shiftType'])
        return redirect(url_for('index'))
    return render_template("addShifts.html", employees=employees)     
       
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
