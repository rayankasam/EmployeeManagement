from flask import Flask, redirect, render_template, url_for, session, request,  json
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
from dbInteraction.getAmountDue import getAmountDue
from dbInteraction.shifts import getPeople
from dbInteraction.shifts import getShifts
from dbInteraction.shifts import lastPunch
from dbInteraction.shifts import shifts
from dbInteraction.time import punchOut
from dbInteraction.getData import getData
from applySpecs import allowedAddEmployee
from datetime import datetime

app = Flask(__name__)
app.secret_key = b"2234JHG3[]opuhmiy757n7ijNT756654"
error = None


@app.route('/')
def index():
    if 'EMPID' in session:
        currentPunch = lastPunch(session['EMPID'])
        # Formatting duration of current shift
        currentDuration, _, _ = str(
            currentShift(session['EMPID'])).partition('.')
        currentDuration = currentDuration[:-3]
    else:
        currentDuration = False
        currentPunch = False
    print(currentPunch)
    return render_template('index.html', currentDuration=currentDuration, currentPunch=currentPunch)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form.to_dict()
        if 'email' not in data or 'password' not in data:
            return redirect(url_for('index'))
        if checkPassword(request.form['email'], request.form['password']):
            session['username'] = request.form['email']
            session['permissions'] = getData(session['username'])[
                'permissionType']
            session['firstName'] = getData(session['username'])['firstName']
            session['EMPID'] = getData(session['username'])['employeeID']
            session['lastPunch'] = lastPunch(session['EMPID'])
        return redirect(url_for('index'))
    return render_template("login.html")


@app.route('/addEmployee', methods=['GET', 'POST'])
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
    session['lastPunch'] = lastPunch(ID)
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


@app.route('/amountDue', methods=['GET', 'POST'])
def amountDue():
    if session['permissions'] == 0:
        employees = getPeople()
        if request.method == 'POST':
            employee = request.form.to_dict()['employee']
            amountDue = getAmountDue(employee)
            return render_template('amountDue.html', employees=employees, amount=amountDue)
        return render_template('amountDue.html', employees=employees, amount=False)
    else:
        return redirect(url_for('index'))


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

        shifts(data['employee'], data['startTime'],
               data['endTime'], data['shiftType'])
        return redirect(url_for('index'))
    return render_template("addShifts.html", employees=employees)


@app.route('/shifts', methods=['GET', 'POST'])
def shifts():
    empID = getData(session['username'])['employeeID']
    allShifts = getShifts(empID)
    shiftList = []
    for shift in allShifts:
        work = {'title': 'Shift',
                'start': datetime.strptime(
                    shift[0], '%Y-%m-%d %H:%M').strftime('%Y-%m-%dT%H:%M:%S'),

                'end': datetime.strptime(
                    shift[1], '%Y-%m-%d %H:%M').strftime('%Y-%m-%dT%H:%M:%S')}
        shiftList.append(work)
    return render_template("shifts.html", allShifts=shiftList)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.debug = True
    app.run()
