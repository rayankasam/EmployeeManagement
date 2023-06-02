from flask import Flask, redirect, render_template, render_template_string,url_for, session, request
from checkPass import *
from addEmployee import *
app = Flask(__name__)
app.secret_key = b"2234JHG3[]opuhmiy757n7ijNT756654"
error = None
@app.route('/')
def index():
    return render_template_string("""
            {% if error %}
                <h2>{{ error }}</h2>
            {% endif %}
            {% if session['username'] %}
                <h1> Logged in as {{session['username']}}</h1>
                <a href="{{ url_for('addEmployee') }}" <button>Add an Employee</button></a>
            {% else %}
                <h1>Welcome! Please enter your email <a href="{{ url_for('login') }}">here.</a></h1>

            {% endif %}
                """)    
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        if checkPassword(request.form['email'],request.form['password']):
            session['username'] = request.form['email']
        return redirect(url_for('index'))
    return '''
        <form method="post">
            <h3>Email
            <p><input type=text name=email>
            <h3>Password
            <p><input type=text name=password>
            <p><input type=submit value=Login>
        </form>
    '''
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
    return '''
        <form method="post">
            <h2>Add an Employee to the system</h2>
            <h3>email*</h3>
            <p><input type=text name=email>
            <h3>password*</h3>
            <p><input type=text name=password>
            <h3>phoneNum*</h3>
            <p><input type=text name=phoneNum>
            <h3>First Name*</h3>
            <p><input type=text name=fName>
            <h3>Middle Name</h3>
            <p><input type=text name=mName>
            <h3>Last Name</h3>
            <p><input type=text name=lName>
            <h3>Sin number*</h3>
            <p><input type=text name=sinNum>
            <h3>Position</h3>
            <p><input type=text name=position>
            <p><input type=submit value=Submit>
        </form>
    '''
@app.route("/test")
def tester():
    error = "Error applied"
    return redirect(url_for("index"))
if __name__ == '__main__':
    add.debug = True
    app.run()
