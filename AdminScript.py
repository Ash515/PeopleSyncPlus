#Flask Imports
from flask import *
from flask import flash
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
admincursor = get_cursor()

AdminApp=Blueprint('AdminApp', __name__, template_folder='templates')

@AdminApp.route('/AdminLanding')
def AdminLanding():
    return render_template('/Admin/AdminLanding.html')


@AdminApp.route('/ManageEmpdata')
def ManageEmpdata():
    return render_template('/Admin/ManageEmpdata.html')

@AdminApp.route('/add_employee', methods=['POST'])
def add_employee():
    empid = request.form.get('empid')
    name = request.form.get('name')
    phno = request.form.get('phno')
    seating = request.form.get('seating')
    destination = request.form.get('destination')
    team = request.form.get('team')
    manager = request.form.get('manager')
    org = request.form.get('org')
    doj = request.form.get('doj')
    officelocation = request.form.get('officelocation')
    shift = request.form.get('shift')
    employmentstatus = request.form.get('employmentstatus')
    profile_pic = request.files['profile_pic'].read()
    emppass = request.form.get('emppass')

    # if empid:
    #     admincursor.execute("""
    #         UPDATE empinfo SET name=%s, phno=%s, seating=%s, destination=%s, 
    #         team=%s, manager=%s, org=%s, doj=%s, officelocation=%s, shift=%s, 
    #         employmentstatus=%s, profile_pic=%s WHERE empid=%s
    #     """, (name, phno, seating, destination, team, manager, org, doj, officelocation, shift, employmentstatus, profile_pic, empid))
    # else:
    admincursor.execute("""
    INSERT INTO empinfo (empid,name, phno, seating, destination, team, manager, 
    org, doj, officelocation, shift, employmentstatus, profile_pic,emppass) 
            VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)
        """, (empid,name, phno, seating, destination, team, manager, org, doj, officelocation, shift, employmentstatus, profile_pic,emppass))

    con.commit()
    return redirect(url_for('index'))

@AdminApp.route('/delete_employee/<int:empid>')
def delete_employee(empid):
    admincursor.execute("DELETE FROM empinfo WHERE empid=%s", (empid,))
    con.commit()
    return redirect(url_for('index'))