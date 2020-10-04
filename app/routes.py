from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, url_for, redirect, request, flash, send_from_directory, session
from app import app, db, basic_auth
from datetime import datetime, date, time, timedelta
import requests
from sqlalchemy import and_
from app.forms import pubivisaForm, korttijalautapeliiltaForm, fuksilauluiltaForm
from app.models import pubivisaModel, korttijalautapeliiltaModel, fuksilauluiltaModel
from flask_wtf.csrf import CSRFProtect, CSRFError
import os
from app import sqlite_to_csv
from werkzeug.datastructures import MultiDict
from urllib.parse import urlparse, urlunparse
import subprocess

app = Flask(__name__)
auth = HTTPBasicAuth()

try:
    password = os.urandom(64)
    print("created default user")
    print("username: admin")
    print("password: " + password)
    
    users = {
        "admin": generate_password_hash(password)
    }

    roles = {
        "admin": "admin"
    }

    file = open("auth.conf", "r")
    lines = file.readlines()

    for line in lines:
        new_user = line.split(",", 6)
        users[new_user[0]] = generate_password_hash(new_user[1])
        roles[new_user[0]] = new_user[2] + new_user[3] + new_user[4] + new_user[5]

except FileNotFoundError as e:
    print(e)

    password = os.urandom(64)
    print("auth.conf not found, created default user")
    print("username: admin")
    print("password: " + password)
    
    users = {
        "admin": generate_password_hash(password)
    }

    roles = {
        "admin": "admin"
    }

finally:
    file.close()


try:
    file = open("routes.conf", "r")
    lines = file.readlines()

    for line in lines:
        conf_line = line.split(":", 1)
        
        if conf_line[0] == "kapsi":
            if conf_line[1] = "true":
                KAPSI = True
            else:
                KAPSI = False

except FileNotFoundError as e:
    print(e)
    print("routes.conf not found")

finally:
    file.close()


@auth.verify_password
def verify_password(username, password):
    if username in users and username in allowed and \
            check_password_hash(users.get(username), password):
        return username

@auth.get_user_roles
def get_user_roles(user):
    return roles[user]


@app.route('/pubivisa', methods=['GET', 'POST'])
def pubivisa():
    form = pubivisaForm()

    starttime = datetime(2020, 8, 25, 12, 00, 00)
    endtime = datetime(2020, 8, 30, 18, 00, 00)
    nowtime = datetime.now()

    limit = 50
    maxlimit = 50
    
    entrys = pubivisaModel.query.all()
    count = pubivisaModel.query.count()

    for entry in entrys:
        if(entry.etunimi == form.etunimi.data and entry.sukunimi == form.sukunimi.data):
            flash('Olet jo ilmoittautunut')

            return render_template('pubivisa.html', title='pubivisa ilmoittautuminen',
                                    entrys=entrys,
                                    count=count,
                                    starttime=starttime,
                                    endtime=endtime,
                                    nowtime=nowtime,
                                    limit=limit,
                                    form=form,
                                    page="pubivisa")

    if form.validate_on_submit() and count <= maxlimit:
        flash('Ilmoittautuminen onnistui')
        sub = pubivisaModel(
            etunimi = form.etunimi.data,
            sukunimi = form.sukunimi.data,
            phone = form.phone.data,
            sapo = form.sapo.data,
            kilta = form.kilta.data,
            consent0 = form.consent0.data,
            consent1 = form.consent1.data,

            datetime = nowtime,
        )
        db.session.add(sub)
        db.session.commit()

        if KAPSI:
            msg = ["echo \"Hei" + form.etunimi.data + form.sukunimi.data + 
            "\n\nOlet ilmoittautunut pikniksitseille. Syötit seuraavia tietoja: " + 
            "\n'Nimi: " + form.etunimi.data + form.sukunimi.data + 
            "\nSähköposti: " + form.sapo.data + 
            "\nPuhelinnumero: " + form.phone.data + 
            "\nKilta: " + form.kilta.data + 
            "\n\nÄlä vastaa tähän sähköpostiin" + 
            "\n\nTerveisin: ropottilari\"" + 
            "|mail -aFrom:no-reply@oty.fi -s 'pubivisa ilmoittautuminen' ", form.sapo.data]

            cmd = msg
            returned_value = os.system(cmd)

        return redirect(url_for('pubivisa'))

    elif form.is_submitted() and count > maxlimit:
        flash('Ilmoittautuminen on jo täynnä')

    elif (not form.validate_on_submit() and form.is_submitted()):
        flash('Ilmoittautuminen epäonnistui, tarkista syöttämäsi tiedot')


    return render_template('pubivisa.html', title='pubivisa ilmoittautuminen',
                            entrys=entrys,
                            count=count,
                            starttime=starttime,
                            endtime=endtime,
                            nowtime=nowtime,
                            limit=limit,
                            form=form,
                            page="pubivisa")


@app.route('/pubivisa_data', methods=['GET'])
@auth.login_required(role=['admin', 'pubivisa'])
def pubivisa_data():
    limit = 50

    entries = pubivisaModel.query.all()

    count = pubivisaModel.query.count()

    return render_template('pubivisa_data.html', title='pubivisa data',
                           entries=entries,
                           count=count,
                           limit=limit)

@app.route('/pubivisa_data/pubivisa_model_data.csv')
@auth.login_required(role=['admin', 'pubivisa'])
def pubivisa_csv():

    os.system('mkdir csv')

    sqlite_to_csv.exportToCSV('pubivisa_model')

    dir = os.path.join(os.getcwd(), 'csv/')
    
    try:
        print(dir)
        return send_from_directory(directory=dir, filename='pubivisa_model_data.csv', as_attachment=True)
    except FileNotFoundError as e:
        print(e)
        abort(404)


@app.route('/korttijalautapeliilta', methods=['GET', 'POST'])
def korttijalautapeliilta():
    form = korttijalautapeliiltaForm()

    starttime = datetime(2020, 8, 25, 12, 00, 00)
    endtime = datetime(2020, 8, 30, 18, 00, 00)
    nowtime = datetime.now()

    limit = 50
    maxlimit = 50
    
    entrys = korttijalautapeliiltaModel.query.all()
    count = korttijalautapeliiltaModel.query.count()

    for entry in entrys:
        if(entry.etunimi == form.etunimi.data and entry.sukunimi == form.sukunimi.data):
            flash('Olet jo ilmoittautunut')

            return render_template('korttijalautapeliilta.html', title='korttijalautapeliilta ilmoittautuminen',
                                    entrys=entrys,
                                    count=count,
                                    starttime=starttime,
                                    endtime=endtime,
                                    nowtime=nowtime,
                                    limit=limit,
                                    form=form,
                                    page="korttijalautapeliilta")

    if form.validate_on_submit() and count <= maxlimit:
        flash('Ilmoittautuminen onnistui')
        sub = korttijalautapeliiltaModel(
            etunimi = form.etunimi.data,
            sukunimi = form.sukunimi.data,
            phone = form.phone.data,
            sapo = form.sapo.data,
            kilta = form.kilta.data,
            consent0 = form.consent0.data,
            consent1 = form.consent1.data,

            datetime = nowtime,
        )
        db.session.add(sub)
        db.session.commit()

        if KAPSI:
            msg = ["echo \"Hei" + form.etunimi.data + form.sukunimi.data + 
            "\n\nOlet ilmoittautunut kortti- ja lautapeli-iltaan. Syötit seuraavia tietoja: " + 
            "\n'Nimi: " + form.etunimi.data + form.sukunimi.data + 
            "\nSähköposti: " + form.sapo.data + 
            "\nPuhelinnumero: " + form.phone.data + 
            "\nKilta: " + form.kilta.data + 
            "\n\nÄlä vastaa tähän sähköpostiin" + 
            "\n\nTerveisin: ropottilari\"" + 
            "|mail -aFrom:no-reply@oty.fi -s 'kortti- ja lautapeli-ilta ilmoittautuminen' ", form.sapo.data]

            cmd = msg
            returned_value = os.system(cmd)

        return redirect(url_for('korttijalautapeliilta'))

    elif form.is_submitted() and count > maxlimit:
        flash('Ilmoittautuminen on jo täynnä')

    elif (not form.validate_on_submit() and form.is_submitted()):
        flash('Ilmoittautuminen epäonnistui, tarkista syöttämäsi tiedot')


    return render_template('korttijalautapeliilta.html', title='korttijalautapeliilta ilmoittautuminen',
                            entrys=entrys,
                            count=count,
                            starttime=starttime,
                            endtime=endtime,
                            nowtime=nowtime,
                            limit=limit,
                            form=form,
                            page="korttijalautapeliilta")

@app.route('/korttijalautapeliilta_data', methods=['GET'])
@auth.login_required(role=['admin', 'korttijalautapeliilta'])
def korttijalautapeliilta_data():
    limit = 50

    entries = korttijalautapeliiltaModel.query.all()

    count = korttijalautapeliiltaModel.query.count()

    return render_template('korttijalautapeliilta_data.html', title='korttijalautapeliilta data',
                           entries=entries,
                           count=count,
                           limit=limit)

@app.route('/korttijalautapeliilta_data/korttijalautapeliilta_model_data.csv')
@auth.login_required(role=['admin', 'korttijalautapeliilta'])
def korttijalautapeliilta_csv():

    os.system('mkdir csv')

    sqlite_to_csv.exportToCSV('korttijalautapeliilta_model')

    dir = os.path.join(os.getcwd(), 'csv/')
    
    try:
        print(dir)
        return send_from_directory(directory=dir, filename='korttijalautapeliilta_model_data.csv', as_attachment=True)
    except FileNotFoundError as e:
        print(e)
        abort(404)


@app.route('/fuksilauluilta', methods=['GET', 'POST'])
def fuksilauluilta():
    form = fuksilauluiltaForm()

    starttime = datetime(2020, 8, 25, 12, 00, 00)
    endtime = datetime(2020, 8, 30, 18, 00, 00)
    nowtime = datetime.now()

    limit = 50
    maxlimit = 50
    
    entrys = fuksilauluiltaModel.query.all()
    count = fuksilauluiltaModel.query.count()

    for entry in entrys:
        if(entry.etunimi == form.etunimi.data and entry.sukunimi == form.sukunimi.data):
            flash('Olet jo ilmoittautunut')

            return render_template('fuksilauluilta.html', title='fuksilauluilta ilmoittautuminen',
                                    entrys=entrys,
                                    count=count,
                                    starttime=starttime,
                                    endtime=endtime,
                                    nowtime=nowtime,
                                    limit=limit,
                                    form=form,
                                    page="fuksilauluilta")

    if form.validate_on_submit() and count <= maxlimit:
        flash('Ilmoittautuminen onnistui')
        sub = fuksilauluiltaModel(
            etunimi = form.etunimi.data,
            sukunimi = form.sukunimi.data,
            sapo = form.sapo.data,
            consent0 = form.consent0.data,
            consent1 = form.consent1.data,

            datetime = nowtime,
        )
        db.session.add(sub)
        db.session.commit()

        if KAPSI:
            msg = ["echo \"Hei" + form.etunimi.data + form.sukunimi.data + 
            "\n\nOlet ilmoittautunut fuksilauluiltaan. Syötit seuraavia tietoja: " + 
            "\n'Nimi: " + form.etunimi.data + form.sukunimi.data + 
            "\nSähköposti: " + form.sapo.data + 
            "\n\nÄlä vastaa tähän sähköpostiin" + 
            "\n\nTerveisin: ropottilari\"" + 
            "|mail -aFrom:no-reply@oty.fi -s 'fuksilauluilta ilmoittautuminen' ", form.sapo.data]

            cmd = msg
            returned_value = os.system(cmd)

        return redirect(url_for('fuksilauluilta'))

    elif form.is_submitted() and count > maxlimit:
        flash('Ilmoittautuminen on jo täynnä')

    elif (not form.validate_on_submit() and form.is_submitted()):
        flash('Ilmoittautuminen epäonnistui, tarkista syöttämäsi tiedot')


    return render_template('fuksilauluilta.html', title='fuksilauluilta ilmoittautuminen',
                            entrys=entrys,
                            count=count,
                            starttime=starttime,
                            endtime=endtime,
                            nowtime=nowtime,
                            limit=limit,
                            form=form,
                            page="fuksilauluilta")


@app.route('/fuksilauluilta_data', methods=['GET'])
@auth.login_required(role=['admin', 'fuksilauluilta'])
def fuksilauluilta_data():
    limit = 50

    entries = fuksilauluiltaModel.query.all()

    count = fuksilauluiltaModel.query.count()

    return render_template('fuksilauluilta_data.html', title='fuksilauluilta data',
                           entries=entries,
                           count=count,
                           limit=limit)

@app.route('/fuksilauluilta_data/fuksilauluilta_model_data.csv')
@auth.login_required(role=['admin', 'fuksilauluilta'])
def fuksilauluilta_csv():

    os.system('mkdir csv')

    sqlite_to_csv.exportToCSV('fuksilauluilta_model')

    dir = os.path.join(os.getcwd(), 'csv/')
    
    try:
        print(dir)
        return send_from_directory(directory=dir, filename='fuksilauluilta_model_data.csv', as_attachment=True)
    except FileNotFoundError as e:
        print(e)
        abort(404)