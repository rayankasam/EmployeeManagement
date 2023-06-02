from flask import Flask, redirect, render_template, render_template_string,url_for, session, request
app = Flask(__name__)
app.secret_key = b"2234JHG3[]opuhmiy757n7ijNT756654"

@app.route('/')
def index():
    return render_template_string("""
            {% if session['username'] %}
                <h1> Logged in as {{session['username']}}</h1>
            {% else %}
                <h1>Welcome! Please enter your email <a href="{{ url_for('login') }}">here.</a></h1>

            {% endif %}
                """)    
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        if request.form['password']
            session['username'] = request.form['username']
        return redirect(url_for('index'))
    return '''
        <form method="post">
            <h3>Username<\h3>
            <p><input type=text name=username>
            <h3>Password<\h3>
            <p><input type=text name=password>
            <p><input type=submit value=Login>
        </form>
    '''
@app.route('/addEmployee',methods=['GET','POST'])
def addEmployee():
    if request.method == 'POST':
        ...
    return '''
        <>
    '''
if __name__ == '__main__':
    app.run()
