from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, url_for, redirect, request, flash, send_from_directory, session
from flask_httpauth import HTTPBasicAuth
from app import app, db
from datetime import datetime, date, time, timedelta
import requests
from sqlalchemy import and_
from app.forms import sitsiForm
from app.models import sitsiModel
from flask_wtf.csrf import CSRFProtect, CSRFError
import os
from app import sqlite_to_csv
from werkzeug.datastructures import MultiDict
from urllib.parse import urlparse, urlunparse
import subprocess
import time
import json

auth = HTTPBasicAuth()

csrf = CSRFProtect()

try:
    file = open("auth.conf", "r")
    lines = file.readlines()
    
    users = {}
    roles = {}

    for line in lines:
        new_user = line.split(",", 6)
        users[new_user[0]] = new_user[1]
        roles[new_user[0]] = new_user[2:6]

except FileNotFoundError as e:
    print(e)

    password = str(os.urandom(64))
    print("auth.conf not found, created default user")
    print("For production, please create auth.conf with proper users and hashed passwords")
    print("username: admin")
    print("password: " + password)
    
    users = {
        "admin": generate_password_hash(password)
    }

    roles = {
        "admin": "admin"
    }

else:
    file.close()






@auth.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users.get(username), password):
        return username

@auth.get_user_roles
def get_user_roles(user):
    return roles.get(user)





@app.route('/')
def index():
    return render_template('index.html', title='OTiTin ilmot', page="index")


@app.route('/pitsakaljasitsit', methods=['GET', 'POST'])
def pitsakaljasitsit():
    form = sitsiForm()

    starttime = datetime(2021, 10, 26, 12, 00, 00)
    endtime = datetime(2021, 11, 2, 23, 59, 59)
    nowtime = datetime.now()

    limit = 60
    maxlimit = 90
    
    entrys = sitsiModel.query.all()
    totalcount = sitsiModel.query.count()
    for entry in entrys:
        if(entry.etunimi == form.etunimi.data and entry.sukunimi == form.sukunimi.data):
            flash('Olet jo ilmoittautunut')

            return render_template('pitsakaljasitsit.html', title='pitsakaljasitsit ilmoittautuminen',
                                    entrys=entrys,
                                    totalcount=totalcount,
                                    starttime=starttime,
                                    endtime=endtime,
                                    nowtime=nowtime,
                                    limit=limit,
                                    form=form,
                                    page="pitsakaljasitsit")


    if request.method == 'POST':
        validate = form.validate_on_submit()
        submitted = form.is_submitted()
    else:
        validate = False
        submitted = False

    if validate and submitted and totalcount <= maxlimit:
        if totalcount >= limit:
            flash('Ilmoittautuminen onnistui, olet varasijalla')
        else:
            flash('Ilmoittautuminen onnistui')

        sub = sitsiModel(
            etunimi = form.etunimi.data,
            sukunimi = form.sukunimi.data,
            email = form.email.data,
            alkoholi = form.alkoholi.data,
            mieto = form.mieto.data,
            pitsa = form.pitsa.data,
            allergiat = form.allergiat.data,
            consent0 = form.consent0.data,
            consent1 = form.consent1.data,
            datetime = nowtime
        )
        db.session.add(sub)
        db.session.commit()

        if totalcount >= limit:
            msg = [
                "echo \"Hei", str(form.etunimi.data), " ", str(form.sukunimi.data), 
                "\n\nOlet ilmoittautunut OTiTin Pitsakalja sitseille. Olet varasijalla. ", 
                "Jos sitseille jää syystä tai toisesta vapaita paikkoja, niin sinuun voidaan olla yhteydessä. ", 
                "\n\nJos tulee kysyttävää, niin voit olla sähköpostitse yhteydessä pepeministeri@otit.fi",
                "\n\nÄlä vastaa tähän sähköpostiin, vastaus ei mene silloin mihinkään.\"",
                "|mail -aFrom:no-reply@otitkakspistenolla.oulu.fi -s 'OTiT Pitsakaljasitsit ilmoittautuminen'", str(form.email.data)
            ]
        else:
            msg = [
                "echo \"Hei", str(form.etunimi.data), " ", str(form.sukunimi.data), 
                "\n\nOlet ilmoittautunut OTiTin Pitsakalja sitseille. Tässä vielä maksuohjeet: ", 
                "\n\n", "Hinta alkoholillisen juoman kanssa on 20€ ja alkoholittoman juoman ", 
                "kanssa 17€. Maksu tapahtuu tilisiirrolla Oulun Tietoteekkarit ry:n tilille ", 
                "FI03 4744 3020 0116 87. Kirjoita viestikenttään nimesi, ", 
                "Pitsakalja-sitsit sekä alkoholiton tai alkoholillinen valintasi mukaan.",
                "\n\nJos tulee kysyttävää, niin voit olla sähköpostitse yhteydessä pepeministeri@otit.fi",
                "\n\nÄlä vastaa tähän sähköpostiin, vastaus ei mene silloin mihinkään.\"",
                "|mail -aFrom:no-reply@otitkakspistenolla.oulu.fi -s 'OTiT Pitsakaljasitsit ilmoittautuminen'", str(form.email.data)
            ]

        cmd = ' '.join(msg)
        returnvalue = os.system(cmd)

        return redirect(url_for('pitsakaljasitsit'))

    elif submitted and totalcount > maxlimit:
        totalcount -= totalcount
        flash('Ilmoittautuminen on jo täynnä')

    elif (not validate) and submitted:
        flash('Ilmoittautuminen epäonnistui, tarkista syöttämäsi tiedot')


    return render_template('pitsakaljasitsit.html', title='pitsakaljasitsit ilmoittautuminen',
                            entrys=entrys,
                            totalcount=totalcount,
                            starttime=starttime,
                            endtime=endtime,
                            nowtime=nowtime,
                            limit=limit,
                            form=form,
                            page="pitsakaljasitsit")


@app.route('/pitsakaljasitsit_data', methods=['GET'])
@auth.login_required(role=['admin', 'pitsakaljasitsit'])
def pitsakaljasitsit_data():
    limit = 60

    entries = sitsiModel.query.all()

    count = sitsiModel.query.count()

    return render_template('pitsakaljasitsit_data.html', title='pitsakaljasitsit data',
                           entries=entries,
                           count=count,
                           limit=limit)

@app.route('/pitsakaljasitsit_data/sitsi_model_data.csv')
@auth.login_required(role=['admin', 'pitsakaljasitsit'])
def pitsakaljasitsit_csv():

    os.system('mkdir csv')

    sqlite_to_csv.exportToCSV('sitsi_model')

    dir = os.path.join(os.getcwd(), 'csv/')
    
    try:
        print(dir)
        return send_from_directory(directory=dir, path='.', filename='sitsi_model_data.csv', as_attachment=True)
    except FileNotFoundError as e:
        print(e)
        abort(404)




@app.route('/fucu', methods=['GET', 'POST'])
@auth.login_required(role=['admin', 'fucu'])
def fucu():
    form = fucuForm()

    starttime = datetime(2021, 10, 26, 12, 00, 00)
    endtime = datetime(2021, 11, 5, 23, 59, 59)
    nowtime = datetime.now()

    limit = 100
    maxlimit = 120
    
    entrys = fucuModel.query.all()
    totalcount = fucuModel.query.count()
    for entry in entrys:
        if(entry.etunimi == form.etunimi.data and entry.sukunimi == form.sukunimi.data):
            flash('Olet jo ilmoittautunut')

            return render_template('fucu.html', title='fucu ilmoittautuminen',
                                    entrys=entrys,
                                    totalcount=totalcount,
                                    starttime=starttime,
                                    endtime=endtime,
                                    nowtime=nowtime,
                                    limit=limit,
                                    form=form,
                                    page="fucu")


    if request.method == 'POST':
        validate = form.validate_on_submit()
        submitted = form.is_submitted()
    else:
        validate = False
        submitted = False

    if validate and submitted and totalcount <= maxlimit:
        if totalcount >= limit:
            flash('Ilmoittautuminen onnistui, olet varasijalla')
        else:
            flash('Ilmoittautuminen onnistui')

        sub = fucuModel(
            etunimi = form.etunimi.data,
            sukunimi = form.sukunimi.data,
            email = form.email.data,
            puh = form.puh.data,
            lahtopaikka = form.lahtopaikka.data,
            kiintio = form.kiintio.data,
            consent0 = form.consent0.data,
            consent1 = form.consent1.data,
            datetime = nowtime
        )
        db.session.add(sub)
        db.session.commit()

        if totalcount >= limit:
            msg = [
                "echo \"Hei", str(form.etunimi.data), " ", str(form.sukunimi.data), 
                "\n\nOlet ilmoittautunut OTiTin Fuksicursiolle. Olet varasijalla. ", 
                "Jos fuculle jää peruutuksien myötä vapaita paikkoja, niin sinuun voidaan olla yhteydessä. ",
                "\n\nÄlä vastaa tähän sähköpostiin, vastaus ei mene silloin mihinkään.\"",
                "|mail -aFrom:no-reply@otitkakspistenolla.oulu.fi -s 'OTiT Fuksicursio ilmoittautuminen'", str(form.email.data)
            ]
        else:
            msg = [
                "echo \"Hei", str(form.etunimi.data), " ", str(form.sukunimi.data), 
                "\n\nOlet ilmoittautunut OTiTin Fuksicursiolle. Tässä vielä syöttämäsi tiedot: ", 
                "\n\nNimi: ", str(form.etunimi.data), str(form.sukunimi.data), 
                "\nSähköposti: ", str(form.email.data), "\nPuhelinnumero: ", str(form.puh.data), 
                "\nLähtöpaikka: ", str(form.lahtopaikka.data), "\nKiintiö: ", str(form.kiintio.data), 
                "\n\nÄlä vastaa tähän sähköpostiin, vastaus ei mene silloin mihinkään.\"",
                "|mail -aFrom:no-reply@otitkakspistenolla.oulu.fi -s 'OTiT Fuksicursio ilmoittautuminen'", str(form.email.data)
            ]

        cmd = ' '.join(msg)
        returnvalue = os.system(cmd)

        return redirect(url_for('fucu'))

    elif submitted and totalcount > maxlimit:
        totalcount -= totalcount
        flash('Ilmoittautuminen on jo täynnä')

    elif (not validate) and submitted:
        flash('Ilmoittautuminen epäonnistui, tarkista syöttämäsi tiedot')


    return render_template('fucu.html', title='fucu ilmoittautuminen',
                            entrys=entrys,
                            totalcount=totalcount,
                            starttime=starttime,
                            endtime=endtime,
                            nowtime=nowtime,
                            limit=limit,
                            form=form,
                            page="fucu")


@app.route('/fucu_data', methods=['GET'])
@auth.login_required(role=['admin', 'fucu'])
def fucu_data():
    limit = 60

    entries = fucuModel.query.all()

    count = fucuModel.query.count()

    return render_template('fucu_data.html', title='fucu data',
                           entries=entries,
                           count=count,
                           limit=limit)

@app.route('/fucu_data/fucu_model_data.csv')
@auth.login_required(role=['admin', 'fucu'])
def fucu_csv():

    os.system('mkdir csv')

    sqlite_to_csv.exportToCSV('fucu_model')

    dir = os.path.join(os.getcwd(), 'csv/')
    
    try:
        print(dir)
        return send_from_directory(directory=dir, path='.', filename='fucu_model_data.csv', as_attachment=True)
    except FileNotFoundError as e:
        print(e)
        abort(404)
