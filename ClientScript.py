#Flask Imports
from flask import *
from flask import flash,Blueprint
import bcrypt
import os
import requests
from flask_login import LoginManager
from functools import wraps
from wtforms import *

#Common Imports
import urllib.request
from utils import format_checkin
import time
from datetime import date

#Pgsql Imports
import psycopg2

#MySQl Imports
# from flask_mysqldb import MySQL
# import MySQLdb.cursors


#Native DB Imports
from dbparams import con
from dbparams import get_cursor

#Native Files
import AdminScript

# login_manager = LoginManager()


ClientApp=Blueprint('ClientApp', __name__, template_folder='templates')

"""
MySQL configuration
app.secret_key = "super secret key"
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='professionals'
mysql=MySQL(app)
login_manager.init_app(app)
"""
# con = psycopg2.connect(dbname="professionals", user='postgres', host='localhost', password='Post@515',port=5433)


@ClientApp.route('/')
def index():
    return render_template('/Index.html')

@ClientApp.errorhandler(404) 
def invalid_route(e): 
    return "Invalid route."

@ClientApp.route('/signin')
def signin():
    return render_template('/Auth/Signin.html')

def login_required(f):
    @wraps(f)
    def wrap(*args,**kwargs):
        if 'logged_in' in session:
            return f(*args,**kwargs)
        else:
            flash("You need to login first.")
            return redirect(url_for('empsigin'))
    return wrap



@ClientApp.route('/empsignin',methods=['GET','POST'])
def empsigin():
    message = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'empid' in request.form and 'emppass' in request.form:
        # Create variables for easy access
        empid = request.form['empid']
        emppassword = request.form['emppass']
        # Check if account exists using MySQL
       # cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur1 = get_cursor()
        cur1.execute('SELECT * FROM empinfo WHERE empid = %s AND emppass = %s', (empid, emppassword))
        # Fetch one record and return result
        
        empvalidation= cur1.fetchone()
               
        if empvalidation:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['empid'] = empvalidation[0]  #'empid'
            session['emppassword'] = empvalidation[1]  #'emppass'
            
            # Redirect to Dashboard page
           # return render_template('/service/Dashboard.html')
            return redirect(url_for('ClientApp.main'))
        
        else:
            # Account doesnt exist or username/password incorrect
            message = 'Incorrect username/password!'
            flash(message)
    return render_template('/index.html', message='')

# @login_manager.user_loader
# def load_user(user_id):
#     return User.get(user_id)

@ClientApp.route('/backtomain')
def backtomain():
    return render_template('/service/Dashboard.html')


# instatuscheck=checkedin
# print(instatuscheck)
checkedin=False
global n
n="text"


@ClientApp.route('/main')
#@login_required
def main():
    eid = session['empid']
    cur = get_cursor()
    cur.execute('SELECT * FROM empinfo WHERE empid= %s', (eid,))
    ename = cur.fetchall()
    con.commit()

    cur.execute('SELECT * FROM empinfo')
    newhires = cur.fetchall()

    cur.execute('SELECT * FROM holidays')
    holidays = cur.fetchall()

    cur.execute('SELECT * FROM goalset WHERE empid=%s', (eid,))
    goals = cur.fetchall()

    global checkedin

    cur.execute('SELECT checkin FROM empinfo WHERE empid=%s', (eid,))
    checkintime = cur.fetchone()
    checkintime = checkintime[0] if checkintime else None

    cur.execute('SELECT checkout FROM empinfo WHERE empid=%s', (eid,))
    checkouttime = cur.fetchone()
    checkouttime = checkouttime[0] if checkouttime else None

    cur.execute('SELECT checkindate FROM empinfo WHERE empid=%s', (eid,))
    checkindate = cur.fetchone()
    checkindate = checkindate[0] if checkindate else None

    cur.execute('SELECT checkoutdate FROM empinfo WHERE empid=%s', (eid,))
    checkoutdate = cur.fetchone()
    checkoutdate = checkoutdate[0] if checkoutdate else None

    try:
        t = time.localtime()
        current_checkin_time = time.strftime("%H:%M:%S", t)
        current_checkin_date = date.today()

        if checkintime is None or checkouttime is None:
            raise ValueError("Check-in time or check-out time is missing.")
        if checkindate is None or checkoutdate is None:
            raise ValueError("Check-in date or check-out date is missing.")

        if checkintime < checkouttime and checkindate == checkoutdate:
            checkedin = False
        elif checkintime < checkouttime and checkindate < checkoutdate:
            checkedin = False
        elif checkintime > checkouttime and checkindate < checkoutdate:
            checkedin = False
        else:
            checkedin = True

    except Exception as e:
        print(f"Error occurred: {e}")
        checkedin = False  # Default to not checked in if error happens

    cur.execute('SELECT * FROM quicklinks')
    quicklinks = cur.fetchall()

    cur.execute('SELECT shift FROM empinfo WHERE empid=%s', (eid,))
    shift = cur.fetchone()
    formatted_shift = shift[0] if shift else "Shift details not available"

    return render_template(
        '/service/Dashboard.html',
        n=n,
        shift=formatted_shift,
        checkedin=checkedin,
        name=ename,
        id=session['empid'],
        newhires=newhires,
        holidays=holidays,
        goals=goals,
        quicklinks=quicklinks
    )

user_status = {"status": "Available", "color": "green"}

@ClientApp.route("/update_status", methods=["POST"])
def update_status():
    data = request.json
    user_status["status"] = data.get("status")
    user_status["color"] = data.get("color")
    return jsonify({"message": "Status updated successfully"}), 200

@ClientApp.route("/get_status", methods=["GET"])
def get_status():
    return jsonify(user_status), 200



@ClientApp.route('/viewprofile')
# @login_required
def viewprofile():
    profileid=session['empid']
    #cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur = get_cursor()
    cur.execute('SELECT * from empinfo where empid= %s',(profileid,))
    profile=cur.fetchall()
    return render_template('/service/Profile.html',profile=profile,profileid=profileid)


@ClientApp.route('/updateprofile/<int:id>',methods=['POST','GET'])
def updateprofile(id):
    id=session['empid']
    if request.method == 'POST':
        
        empphno = request.form['phone-number']
        empseating = request.form['seating']
        cur = get_cursor()
        cur.execute("UPDATE empinfo SET phno = %s, seating= %s WHERE empid = %s", 
               (empphno,empseating, session['empid'],))
        
        con.commit()
        return redirect(url_for('viewprofile'))
    return render_template('/service/Updatefield.html',id=id)

@ClientApp.route('/teamdirectory')
def teamdirectory():
    return render_template('/service/Directory.html')

@ClientApp.route('/humanresource')
def humanresource():
    teamname='Human Resource'
    head='Guru Moorthi K'
    cur = get_cursor()
    cur.execute('SELECT * from  hr')
    team_profile=cur.fetchall()
    return render_template('/service/Directory-profiles.html',head=head,team_profile=team_profile,team_name=teamname)

@ClientApp.route('/employeeinfo/<int:eid>',methods=['POST','GET'])
def employeeinfo(eid):
    s_id=session['empid']
    cur = get_cursor()
    cur.execute('SELECT * from  hr where id=%s',(eid,))
    team_p=cur.fetchall()
    con.commit()
    cur = get_cursor()
    cur.execute('SELECT * from  empinfo where empid=%s',(eid,))
    emp_p=cur.fetchall()
    cur.execute('SELECT * from  skillset where empid=%s',(eid,))
    empSkills=cur.fetchall()
    cur.execute('SELECT * from  managers')
    manager=cur.fetchall()
    return render_template('/service/Employeeinfo.html',manager=manager,emp_p=emp_p,team_p=team_p,s_id=s_id,empSkills=empSkills)


@ClientApp.route('/employeeskills/<int:seid>',methods=['POST','GET'])
def employeeskills(seid):
    seid=session['empid']
    if request.method=='POST':
        skill = request.form['skills']
        skillrate=request.form['skillrate']
        cur = get_cursor()   
        cur.execute("insert into skillset(empid,skill,rating) values(%s,%s,%s)",(seid,skill,skillrate,))
        con.commit()
    return render_template('/service/Employeeskills.html',id=seid)

@ClientApp.route('/skilldetails/<int:uid>',methods=['post','get'])
def skilldetails(uid):
    seid=session['empid']
    cur = get_cursor()   
    cur.execute("select skill from skillset where uid=%s",(uid,))
    skillrecord=cur.fetchone()
    cur = get_cursor() 
    cur.execute("select uid from skillset where uid=%s",(uid,)) 
    del_id=cur.fetchone()
    cur.execute("select * from skillset where uid=%s",(uid,))
    skill_data=cur.fetchall()
    cur.execute('SELECT * from  empinfo where empid=%s',(seid,))
    emp_ids=cur.fetchall()
    cur.execute("select empid from skillset where uid=%s",(uid,))
    empid_matcher=cur.fetchall()
    cur.execute("select uid from skillset where uid=%s",(uid,)) 
    record_uid=cur.fetchone()
    return render_template('/service/SkillDetails.html',emp_ids=emp_ids,empid_matcher=empid_matcher,skillrecord=skillrecord,del_id=del_id,seid=seid,skill_data=skill_data,record_uid=record_uid)

@ClientApp.route("/delete_data/<int:uid>", methods=["GET","POST"])
def delete_data(uid):
    seid=session['empid']
    cur= get_cursor() 
    cur.execute("delete from skillset where uid=%s and empid=%s",(uid,seid,))
    cur.connection.commit()
    cur.close() 
    return redirect(url_for('ClientApp.employeeinfo',eid=seid))

@ClientApp.route("/personaldetail-update/<int:id>",methods=["GET","POST"])
def personaldetailsupdate(id):
    id=session["empid"]
    return render_template("/service/PersonalDetails.html")


@ClientApp.route("/goals",methods=['GET','POST'])
def goals():
    emp_id=session['empid']
    cur=get_cursor()
    cur.execute('SELECT * FROM empinfo WHERE empid= %s ',(emp_id,))
    empdetail=cur.fetchall()
    if request.method == 'POST':
        taskname = request.form['tname']
        taskdescription = request.form['description']
        startdate = request.form['startdate']
        duedate = request.form['duedate']
        priority = request.form['priority']
        status = request.form['status']
        
        
        cur1= get_cursor()
        cur1.execute("INSERT INTO goalset(empid,taskname,description,startdate,duedate,priority,status) VALUES (%s,%s,%s,%s,%s,%s,%s)",(emp_id,taskname,taskdescription,startdate,duedate,priority,status,))
        
        con.commit()
        flash("Record Added Successfully !")
    return render_template("/service/Goals.html",empdetails=empdetail)
   
@ClientApp.route("/goaldetails/<int:gid>",methods=['GET','POST'])
def goalDetails(gid):
    emp_id=session['empid']
    cur=get_cursor()
    cur.execute('SELECT * FROM goalset WHERE gid= %s ',(gid,))
    goals=cur.fetchall()
    cur=get_cursor()
    cur.execute("select * from empinfo where empid=%s",(emp_id,))
    empdata_goal=cur.fetchall()
    # flash("Not found")
    return render_template('/service/Goaldetails.html',goals=goals,empdata_goal=empdata_goal,emp_id=emp_id,gid=gid)

@ClientApp.route('/closetaskstatus/<int:gid>',methods=['POST','GET'])
def closetaskstatus(gid):
    g_id=gid
    name="Closed"
    cur = get_cursor()
    cur.execute("UPDATE goalset SET status = %s where gid=%s",(name,g_id,))
    con.commit()
    return redirect(url_for('main'))
    
@ClientApp.route('/opentaskstatus/<int:gid>',methods=['POST','GET'])
def opentaskstatus(gid):
    g_id=gid
    name="Open"
    cur = get_cursor()
    cur.execute("UPDATE goalset SET status = %s where gid=%s",(name,g_id,))
    con.commit()
    return redirect(url_for('main'))



@ClientApp.route("/taskdeletion/<int:gid>", methods=["GET","POST"])
def taskdeletion(gid):
    g_id=gid
    cur= get_cursor() 
    cur.execute("delete from goalset where gid=%s",(gid,))
    cur.connection.commit()
    cur.close() 
    return redirect(url_for('main'))

@ClientApp.route("/leaveform",methods=['GET','POST'])
def leaveform():
    emp_id=session['empid']
    cur=get_cursor()
    cur.execute('SELECT * FROM empinfo WHERE empid= %s ',(emp_id,))
    empdetail=cur.fetchall()
    if request.method == 'POST':
        leavetype = request.form['leavetype']
        fromdate = request.form['fromdate']
        todate = request.form['todate']
        leavedescription = request.form['description']
        cur1= get_cursor()
        cur1.execute("INSERT INTO leaverequest(empid,leavetype,fdate,tdate,description) VALUES (%s,%s,%s,%s,%s)",(emp_id,leavetype,fromdate,todate,leavedescription,))
        con.commit()
        flash("Record sent to Approval !")
    
    return render_template("/service/Leaveform.html",empdetails=empdetail)



   

@ClientApp.route("/checkin")
def checkin():
    session_id=session['empid']
    In_status="Office In"
    global checkedin
    checkedin=True
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    current_date=date.today()
    checkintime=current_time
    cur = get_cursor()
    cur.execute("UPDATE empinfo SET inoutstatus = %s, checkin=%s where empid=%s",(In_status,checkintime,session_id,))
    con.commit()
    cur = get_cursor()
    cur.execute("INSERT INTO attendancelog(empid,datestamp,checkinlog) VALUES (%s,%s,%s)",(session_id,current_date,checkintime,))
    con.commit()
    cur.execute("UPDATE empinfo SET checkindate = %s where empid=%s",(current_date,session_id,))
    con.commit()
    return redirect(url_for('main'))
  

@ClientApp.route("/checkout")
def checkout():
    session_id=session['empid']
    In_status="Out"
    global checkedin
    checkedin=False 
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    current_date=date.today()
    checkouttime=current_time
    cur=get_cursor()
    cur.execute("UPDATE empinfo SET inoutstatus = %s, checkout=%s where empid=%s",(In_status,checkouttime,session_id,))
    con.commit()
    cur = get_cursor()
    cur.execute("INSERT INTO attendancelog(empid,datestamp,checkoutlog) VALUES (%s,%s,%s)",(session_id,current_date,checkouttime,))
    con.commit()
    cur.execute("UPDATE empinfo SET checkoutdate = %s where empid=%s",(current_date,session_id,))
    con.commit()
    return redirect(url_for('ClientApp.main'))

@ClientApp.route('/attendancelog',methods=['GET','POST'])
def attendancelog():
    session_id=session['empid']
    global timerecords
    # timerecords=None
    if request.method=='POST':
        
        Qdate=request.form['givendate']
        cur = get_cursor() 
        cur.execute('SELECT * FROM attendancelog WHERE empid= %s and datestamp=%s ',(session_id,Qdate,)) 
        # global timerecords
        timerecords=cur.fetchall()
        return render_template('/service/AttendanceLog.html',session_id=session_id,timerecords=timerecords,Qdate=Qdate)
    return render_template('/service/AttendanceLog.html',session_id=session_id)
@ClientApp.route('/userlogout')
def userlogout():
    session.pop('empid')
    return redirect(url_for('index'))


@ClientApp.route('/directory')
def directory():
    #try:
        cur=get_cursor()
        
        # Fetch departments from your `directory` table
        cur.execute("SELECT DISTINCT department_name FROM directory ORDER BY department_name ASC;")
        result = cur.fetchall()
        
        # Extract department names into a simple list
        teams = [row[0] for row in result]
        
        cur.close()
        
        return render_template('/service/Directory.html', teams=teams)
    
    # except Exception as e:
    #        print(f"Error fetching directory data: {e}")
    #        return "An error occurred while loading the directory."

@ClientApp.route('/weatherreport', methods =['POST', 'GET'])
def weather():
     city = "Mumbai"
     api_key = "0f671a46ce00201b5cfa17ff2e13cbb9"
     url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
     response = requests.get(url)
     if response.status_code == 200:
         data = response.json()
         weather = data["weather"][0]["description"]
         temperature = data["main"]["temp"]
     else:
         weather = "Unknown"
         temperature = "0"
     return f"The weather in {city} is {weather}. The temperature is {temperature} degrees Celsius."

	


    









if __name__=='__main__':
    app.secret_key='super secret key'
    app.run(debug=True)
