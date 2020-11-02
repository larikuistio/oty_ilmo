from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, url_for, redirect, request, flash, send_from_directory, session
from flask_httpauth import HTTPBasicAuth
from app import app, db
from datetime import datetime, date, time, timedelta
import requests
from sqlalchemy import and_
from app.forms import pubivisaForm, korttijalautapeliiltaForm, fuksilauluiltaForm, slumberpartyForm, pakohuoneForm
from app.models import pubivisaModel, korttijalautapeliiltaModel, fuksilauluiltaModel, slumberpartyModel, pakohuoneModel
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

    password = os.urandom(64)
    print("created default user")
    print("username: admin")
    print("password: " + str(password))
    
    users = {
        "admin": generate_password_hash(password)
    }

    roles = {
        "admin": "admin"
    }

    for line in lines:
        new_user = line.split(",", 6)
        users[new_user[0]] = generate_password_hash(new_user[1])
        roles[new_user[0]] = new_user[2:6]

except FileNotFoundError as e:
    print(e)

    password = os.urandom(64)
    print("auth.conf not found, created default user")
    print("username: admin")
    print("password: " + str(password))
    
    users = {
        "admin": generate_password_hash(password)
    }

    roles = {
        "admin": "admin"
    }

else:
    file.close()


KAPSI = False

try:
    file = open("routes.conf", "r")
    lines = file.readlines()

    for line in lines:
        conf_line = line.split(":", 2)
        
        if "kapsi" in conf_line[0]:
            if "true" in conf_line[1]:
                KAPSI = True
            else:
                KAPSI = False

except FileNotFoundError as e:
    print(e)
    print("routes.conf not found")

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
    return render_template('index.html', title='OTY:n ilmot', page="index")

@app.route('/pubivisa', methods=['GET', 'POST'])
def pubivisa():
    form = pubivisaForm()

    starttime = datetime(2020, 10, 7, 12, 00, 00)
    endtime = datetime(2020, 10, 10, 23, 59, 59)
    nowtime = datetime.now()

    limit = 50
    maxlimit = 50
    
    entrys = pubivisaModel.query.all()
    count = 0
    totalcount = 0
    for entry in entrys:
        totalcount += entry.personcount

    for entry in entrys:
        if(entry.teamname == form.teamname.data):
            flash('Olet jo ilmoittautunut')

            return render_template('pubivisa.html', title='pubivisa ilmoittautuminen',
                                    entrys=entrys,
                                    totalcount=totalcount,
                                    starttime=starttime,
                                    endtime=endtime,
                                    nowtime=nowtime,
                                    limit=limit,
                                    form=form,
                                    page="pubivisa")

    if form.etunimi0.data and form.sukunimi0.data:
        count += 1
    if form.etunimi1.data and form.sukunimi1.data:
        count += 1
    if form.etunimi2.data and form.sukunimi2.data:
        count += 1
    if form.etunimi3.data and form.sukunimi3.data:
        count += 1

    totalcount += count

    if request.method == 'POST':
        validate = form.validate_on_submit()
        submitted = form.is_submitted()
    else:
        validate = False
        submitted = False

    if validate and submitted and totalcount <= maxlimit:
        flash('Ilmoittautuminen onnistui')
        sub = pubivisaModel(
            teamname = form.teamname.data,
            etunimi0 = form.etunimi0.data,
            sukunimi0 = form.sukunimi0.data,
            phone0 = form.phone0.data,
            email0 = form.email0.data,
            kilta0 = form.kilta0.data,
            etunimi1 = form.etunimi1.data,
            sukunimi1 = form.sukunimi1.data,
            phone1 = form.phone1.data,
            email1 = form.email1.data,
            kilta1 = form.kilta1.data,
            etunimi2 = form.etunimi2.data,
            sukunimi2 = form.sukunimi2.data,
            phone2 = form.phone2.data,
            email2 = form.email2.data,
            kilta2 = form.kilta2.data,
            etunimi3 = form.etunimi3.data,
            sukunimi3 = form.sukunimi3.data,
            phone3 = form.phone3.data,
            email3 = form.email3.data,
            kilta3 = form.kilta3.data,
            consent0 = form.consent0.data,
            consent1 = form.consent1.data,
            consent2 = form.consent2.data,

            personcount = count,

            datetime = nowtime
        )
        db.session.add(sub)
        db.session.commit()

        if KAPSI:
            msg = ["echo \"Hei", str(form.etunimi0.data), str(form.sukunimi0.data),
            "\n\nOlet ilmoittautunut pubivisaan. Syötit muun muassa seuraavia tietoja: ",
            "\n'Joukkueen nimi: ", str(form.teamname.data),
            "\n'Osallistujien nimet:\n", str(form.etunimi0.data), str(form.sukunimi0.data), "\n",
            str(form.etunimi1.data), str(form.sukunimi1.data), "\n",
            str(form.etunimi2.data), str(form.sukunimi2.data), "\n",
            str(form.etunimi3.data), str(form.sukunimi3.data), "\n",
            "\n\nÄlä vastaa tähän sähköpostiin",
            "\n\nTerveisin: ropottilari\"",
            "|mail -aFrom:no-reply@oty.fi -s 'pubivisa ilmoittautuminen' ", str(form.email0.data)]

            cmd = ' '.join(msg)
            returned_value = os.system(cmd)

            msg = ["echo \"Hei", str(form.etunimi1.data), str(form.sukunimi1.data),
            "\n\nOlet ilmoittautunut pubivisaan. Syötit muun muassa seuraavia tietoja: ",
            "\n'Joukkueen nimi: ", str(form.teamname.data),
            "\n'Osallistujien nimet:\n", str(form.etunimi0.data), str(form.sukunimi0.data), "\n",
            str(form.etunimi1.data), str(form.sukunimi1.data), "\n",
            str(form.etunimi2.data), str(form.sukunimi2.data), "\n",
            str(form.etunimi3.data), str(form.sukunimi3.data), "\n",
            "\n\nÄlä vastaa tähän sähköpostiin",
            "\n\nTerveisin: ropottilari\"",
            "|mail -aFrom:no-reply@oty.fi -s 'pubivisa ilmoittautuminen' ", str(form.email1.data)]

            cmd = ' '.join(msg)
            returned_value = os.system(cmd)

            msg = ["echo \"Hei", str(form.etunimi2.data), str(form.sukunimi2.data),
            "\n\nOlet ilmoittautunut pubivisaan. Syötit muun muassa seuraavia tietoja: ",
            "\n'Joukkueen nimi: ", str(form.teamname.data),
            "\n'Osallistujien nimet:\n", str(form.etunimi0.data), str(form.sukunimi0.data), "\n",
            str(form.etunimi1.data), str(form.sukunimi1.data), "\n",
            str(form.etunimi2.data), str(form.sukunimi2.data), "\n",
            str(form.etunimi3.data), str(form.sukunimi3.data), "\n",
            "\n\nÄlä vastaa tähän sähköpostiin",
            "\n\nTerveisin: ropottilari\"",
            "|mail -aFrom:no-reply@oty.fi -s 'pubivisa ilmoittautuminen' ", str(form.email2.data)]

            cmd = ' '.join(msg)
            returned_value = os.system(cmd)

            msg = ["echo \"Hei", str(form.etunimi3.data), str(form.sukunimi3.data),
            "\n\nOlet ilmoittautunut pubivisaan. Syötit muun muassa seuraavia tietoja: ",
            "\n'Joukkueen nimi: ", str(form.teamname.data),
            "\n'Osallistujien nimet:\n", str(form.etunimi0.data), str(form.sukunimi0.data), "\n",
            str(form.etunimi1.data), str(form.sukunimi1.data), "\n",
            str(form.etunimi2.data), str(form.sukunimi2.data), "\n",
            str(form.etunimi3.data), str(form.sukunimi3.data), "\n",
            "\n\nÄlä vastaa tähän sähköpostiin",
            "\n\nTerveisin: ropottilari\"",
            "|mail -aFrom:no-reply@oty.fi -s 'pubivisa ilmoittautuminen' ", str(form.email3.data)]

            cmd = ' '.join(msg)
            returned_value = os.system(cmd)

        if KAPSI:
            return redirect('https://ilmo.oty.fi/pubivisa')
        else:
            return redirect(url_for('pubivisa'))

    elif submitted and totalcount > maxlimit:
        totalcount -= count
        flash('Ilmoittautuminen on jo täynnä')

    elif (not validate) and submitted:
        flash('Ilmoittautuminen epäonnistui, tarkista syöttämäsi tiedot')


    return render_template('pubivisa.html', title='pubivisa ilmoittautuminen',
                            entrys=entrys,
                            totalcount=totalcount,
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

    starttime = datetime(2020, 10, 7, 12, 00, 00)
    endtime = datetime(2020, 10, 13, 23, 59, 59)
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

    if request.method == 'POST':
        validate = form.validate_on_submit()
        submitted = form.is_submitted()
    else:
        validate = False
        submitted = False

    if validate and submitted and count <= maxlimit:
        flash('Ilmoittautuminen onnistui')
        sub = korttijalautapeliiltaModel(
            etunimi = form.etunimi.data,
            sukunimi = form.sukunimi.data,
            phone = form.phone.data,
            email = form.email.data,
            kilta = form.kilta.data,
            consent0 = form.consent0.data,
            consent1 = form.consent1.data,
            consent2 = form.consent2.data,

            datetime = nowtime
        )
        db.session.add(sub)
        db.session.commit()

        if KAPSI:
            msg = ["echo \"Hei", str(form.etunimi.data), str(form.sukunimi.data),
            "\n\nOlet ilmoittautunut kortti- ja lautapeli-iltaan. Syötit seuraavia tietoja: ",
            "\n'Nimi: ", str(form.etunimi.data), str(form.sukunimi.data),
            "\nSähköposti: ", str(form.email.data),
            "\nPuhelinnumero: ", str(form.phone.data),
            "\nKilta: ", str(form.kilta.data),
            "\n\nÄlä vastaa tähän sähköpostiin",
            "\n\nTerveisin: ropottilari\"",
            "|mail -aFrom:no-reply@oty.fi -s 'kortti- ja lautapeli-ilta ilmoittautuminen' ", str(form.email.data)]

            cmd = ' '.join(msg)
            returned_value = os.system(cmd)

        if KAPSI:
            return redirect('https://ilmo.oty.fi/korttijalautapeliilta')
        else:
            return redirect(url_for('korttijalautapeliilta'))

    elif submitted and count > maxlimit:
        flash('Ilmoittautuminen on jo täynnä')

    elif (not validate) and submitted:
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

    starttime = datetime(2020, 10, 7, 12, 00, 00)
    endtime = datetime(2020, 10, 13, 23, 59, 59)
    nowtime = datetime.now()

    limit = 70
    maxlimit = 70
    
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

    if request.method == 'POST':
        validate = form.validate_on_submit()
        submitted = form.is_submitted()
    else:
        validate = False
        submitted = False

    if validate and submitted and count <= maxlimit:
        flash('Ilmoittautuminen onnistui')
        sub = fuksilauluiltaModel(
            etunimi = form.etunimi.data,
            sukunimi = form.sukunimi.data,
            email = form.email.data,
            consent1 = form.consent1.data,

            datetime = nowtime,
        )
        db.session.add(sub)
        db.session.commit()

        if KAPSI:
            msg = ["echo \"Hei", str(form.etunimi.data), str(form.sukunimi.data),
            "\n\nOlet ilmoittautunut fuksilauluiltaan. Syötit seuraavia tietoja: ",
            "\n'Nimi: ", str(form.etunimi.data), str(form.sukunimi.data),
            "\nSähköposti: ", str(form.email.data),
            "\n\nÄlä vastaa tähän sähköpostiin",
            "\n\nTerveisin: ropottilari\"",
            "|mail -aFrom:no-reply@oty.fi -s 'fuksilauluilta ilmoittautuminen' ", str(form.email.data)]

            cmd = ' '.join(msg)
            returned_value = os.system(cmd)

        if KAPSI:
            return redirect('https://ilmo.oty.fi/fuksilauluilta')
        else:
            return redirect(url_for('fuksilauluilta'))

    elif submitted and count > maxlimit:
        flash('Ilmoittautuminen on jo täynnä')

    elif (not validate) and submitted:
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
    limit = 70

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




@app.route('/slumberparty', methods=['GET', 'POST'])
def slumberparty():
    form = slumberpartyForm()

    starttime = datetime(2020, 10, 21, 12, 00, 00)
    endtime = datetime(2020, 10, 27, 23, 59, 59)
    nowtime = datetime.now()

    limit = 50
    maxlimit = 50
    
    entrys = slumberpartyModel.query.all()
    count = slumberpartyModel.query.count()

    for entry in entrys:
        if(entry.etunimi == form.etunimi.data and entry.sukunimi == form.sukunimi.data):
            flash('Olet jo ilmoittautunut')

            return render_template('slumberparty.html', title='slumberparty ilmoittautuminen',
                                    entrys=entrys,
                                    count=count,
                                    starttime=starttime,
                                    endtime=endtime,
                                    nowtime=nowtime,
                                    limit=limit,
                                    form=form,
                                    page="slumberparty")

    if request.method == 'POST':
        validate = form.validate_on_submit()
        submitted = form.is_submitted()
    else:
        validate = False
        submitted = False

    if validate and submitted and count <= maxlimit:
        flash('Ilmoittautuminen onnistui')
        sub = slumberpartyModel(
            etunimi = form.etunimi.data,
            sukunimi = form.sukunimi.data,
            phone = form.phone.data,
            email = form.email.data,
            kilta = form.kilta.data,
            consent0 = form.consent0.data,
            consent1 = form.consent1.data,
            consent2 = form.consent2.data,

            datetime = nowtime
        )
        db.session.add(sub)
        db.session.commit()

        if KAPSI:
            msg = ["echo \"Hei", str(form.etunimi.data), str(form.sukunimi.data),
            "\n\nOlet ilmoittautunut slumberpartyyn. Syötit seuraavia tietoja: ",
            "\n'Nimi: ", str(form.etunimi.data), str(form.sukunimi.data),
            "\nSähköposti: ", str(form.email.data),
            "\nPuhelinnumero: ", str(form.phone.data),
            "\nKilta: ", str(form.kilta.data),
            "\n\nÄlä vastaa tähän sähköpostiin",
            "\n\nTerveisin: ropottilari\"",
            "|mail -aFrom:no-reply@oty.fi -s 'slumberparty ilmoittautuminen' ", str(form.email.data)]

            cmd = ' '.join(msg)
            returned_value = os.system(cmd)

        if KAPSI:
            return redirect('https://ilmo.oty.fi/slumberparty')
        else:
            return redirect(url_for('slumberparty'))

    elif submitted and count > maxlimit:
        flash('Ilmoittautuminen on jo täynnä')

    elif (not validate) and submitted:
        flash('Ilmoittautuminen epäonnistui, tarkista syöttämäsi tiedot')


    return render_template('slumberparty.html', title='slumberparty ilmoittautuminen',
                            entrys=entrys,
                            count=count,
                            starttime=starttime,
                            endtime=endtime,
                            nowtime=nowtime,
                            limit=limit,
                            form=form,
                            page="slumberparty")

@app.route('/slumberparty_data', methods=['GET'])
@auth.login_required(role=['admin', 'slumberparty'])
def slumberparty_data():
    limit = 50

    entries = slumberpartyModel.query.all()

    count = slumberpartyModel.query.count()

    return render_template('slumberparty_data.html', title='slumberparty data',
                           entries=entries,
                           count=count,
                           limit=limit)

@app.route('/slumberparty_data/slumberparty_model_data.csv')
@auth.login_required(role=['admin', 'slumberparty'])
def slumberparty_csv():

    os.system('mkdir csv')

    sqlite_to_csv.exportToCSV('slumberparty_model')

    dir = os.path.join(os.getcwd(), 'csv/')
    
    try:
        print(dir)
        return send_from_directory(directory=dir, filename='slumberparty_model_data.csv', as_attachment=True)
    except FileNotFoundError as e:
        print(e)
        abort(404)


@app.route('/pakohuone', methods=['GET', 'POST'])
def pakohuone():

    starttime = datetime(2020, 10, 21, 12, 00, 00)
    endtime = datetime(2020, 11, 27, 23, 59, 59)
    nowtime = datetime.now()

    limit = 20
    maxlimit = 20
    
    entrys = pakohuoneModel.query.all()
    count = pakohuoneModel.query.count()

    varatut = []
    varatut.append(('18:00', '', ''))
    varatut.append(('19:30', '', ''))
    for entry in entrys:
        varatut.append((entry.aika, entry.huone1800, entry.huone1930))

    form = pakohuoneForm()

    for entry in entrys:
        if((entry.etunimi0 == form.etunimi0.data and entry.sukunimi0 == form.sukunimi0.data) or entry.email0 == form.email0.data):
            flash('Olet jo ilmoittautunut')

            return render_template('pakohuone.html', title='pakohuone ilmoittautuminen',
                                    entrys=entrys,
                                    count=count,
                                    starttime=starttime,
                                    endtime=endtime,
                                    nowtime=nowtime,
                                    limit=limit,
                                    form=form,
                                    varatut=json.dumps(varatut),
                                    page="pakohuone")

    for entry in entrys:
        if(entry.aika == form.aika.data and (entry.huone1800 == form.huone1800.data or entry.huone1930 == form.huone1930.data)):
            flash('Valisemasi huone on jo varattu valitsemanasi aikana')

            return render_template('pakohuone.html', title='pakohuone ilmoittautuminen',
                                    entrys=entrys,
                                    count=count,
                                    starttime=starttime,
                                    endtime=endtime,
                                    nowtime=nowtime,
                                    limit=limit,
                                    form=form,
                                    varatut=json.dumps(varatut),
                                    page="pakohuone")


    if request.method == 'POST':
        validate = form.validate_on_submit()
        submitted = form.is_submitted()
    else:
        validate = False
        submitted = False

    if validate and submitted and count <= maxlimit:
        flash('Ilmoittautuminen onnistui')
        sub = pakohuoneModel(
            aika = form.aika.data,
            huone1800 = form.huone1800.data,
            huone1930 = form.huone1930.data,
            etunimi0 = form.etunimi0.data,
            sukunimi0 = form.sukunimi0.data,
            phone0 = form.phone0.data,
            email0 = form.email0.data,
            
            etunimi1 = form.etunimi1.data,
            sukunimi1 = form.sukunimi1.data,
            etunimi2 = form.etunimi2.data,
            sukunimi2 = form.sukunimi2.data,
            etunimi3 = form.etunimi3.data,
            sukunimi3 = form.sukunimi3.data,
            etunimi4 = form.etunimi4.data,
            sukunimi4 = form.sukunimi4.data,
            etunimi5 = form.etunimi5.data,
            sukunimi5 = form.sukunimi5.data,

            consent0 = form.consent0.data,

            datetime = nowtime
        )
        db.session.add(sub)
        db.session.commit()

        if KAPSI:
            msg = ["echo \"Hei", str(form.etunimi0.data), str(form.sukunimi0.data),
            "\n\nOlet ilmoittautunut OTYn Pakopelipäivä tapahtumaan. Syötit seuraavia tietoja: ",
            "\n'Nimi: ", str(form.etunimi0.data), str(form.sukunimi0.data),
            "\nSähköposti: ", str(form.email0.data),
            "\nPuhelinnumero: ", str(form.phone0.data),
            "\nMuiden joukkuelaisten nimet: ", str(form.etunimi1.data), str(form.sukunimi1.data),
            str(form.etunimi2.data), str(form.sukunimi2.data), 
            str(form.etunimi3.data), str(form.sukunimi3.data),
            str(form.etunimi4.data), str(form.sukunimi4.data),
            str(form.etunimi5.data), str(form.sukunimi5.data),
            "\n\nÄlä vastaa tähän sähköpostiin",
            "\n\nTerveisin: ropottilari\"",
            "|mail -aFrom:no-reply@oty.fi -s 'slumberparty ilmoittautuminen' ", str(form.email0.data)]

            cmd = ' '.join(msg)
            returned_value = os.system(cmd)

        if KAPSI:
            return redirect('https://ilmo.oty.fi/pakohuone')
        else:
            return redirect(url_for('pakohuone'))

    elif submitted and count > maxlimit:
        flash('Ilmoittautuminen on jo täynnä')

    elif (not validate) and submitted:
        flash('Ilmoittautuminen epäonnistui, tarkista syöttämäsi tiedot')


    return render_template('pakohuone.html', title='pakohuone ilmoittautuminen',
                            entrys=entrys,
                            count=count,
                            starttime=starttime,
                            endtime=endtime,
                            nowtime=nowtime,
                            limit=limit,
                            form=form,
                            varatut=json.dumps(varatut),
                            page="pakohuone")

@app.route('/pakohuone_data', methods=['GET'])
@auth.login_required(role=['admin', 'pakohuone'])
def pakohuone_data():
    limit = 20

    entries = pakohuoneModel.query.all()

    count = pakohuoneModel.query.count()

    return render_template('pakohuone_data.html', title='pakohuone data',
                           entries=entries,
                           count=count,
                           limit=limit)

@app.route('/pakohuone_data/pakohuone_model_data.csv')
@auth.login_required(role=['admin', 'pakohuone'])
def pakohuone_csv():

    os.system('mkdir csv')

    sqlite_to_csv.exportToCSV('pakohuone_model')

    dir = os.path.join(os.getcwd(), 'csv/')
    
    try:
        print(dir)
        return send_from_directory(directory=dir, filename='pakohuone_model_data.csv', as_attachment=True)
    except FileNotFoundError as e:
        print(e)
        abort(404)