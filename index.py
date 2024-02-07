from config import app, db, Pflanze, User, MsgCat
from flask import Flask, render_template, redirect, url_for, request, flash
from werkzeug.utils import secure_filename
import forms
import os
from flask_login import current_user, login_user, logout_user, login_required
from urllib import parse



@app.route("/user/<id>", methods=['GET','POST'])
def user_details(id):
    form = forms.UserForm()
    users = db.session.query(User).filter(User.id == id)

    if request.method == 'POST':
        #wenn im Ändern-Modus
        if 'aendern' in request.form:
            for user in users:
                user.username = form.username.data
                user.email = form.email.data
        
            db.session.commit()
    else:
        for user in users:
            form.username.data = user.username
            form.email.data = user.email
        
    return render_template('user.html',
                           form = form)


@app.route('/admin')
def administer():
    users = User.query.all()
    form = forms.UserForm()
    return render_template('administer.html', form=form, users=users)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('start_page'))
    form = forms.RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Sie haben sich erfolgreich registriert.', MsgCat.OK.value)
        return redirect(url_for('login'))
    return render_template('register.html', title='Registrieren', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('start_page'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('start_page'))
    form = forms.LoginForm()
    if form.is_submitted():
        print('submitted')
        if form.validate():
            print('valid')
            user = User.query.filter_by(username=form.username.data).first()
            if user is None or not user.check_password(form.password.data):
                flash('Benutzername oder Passwort inkorrekt.', MsgCat.ERR.value)
                return redirect(url_for('login'))
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or parse.urlparse(next_page).netloc != '':
                next_page = url_for('start_page')
            return redirect(next_page)
    return render_template('login.html', title='Anmelden', form=form)

@app.route("/pflanze/<id>", methods=['GET','POST'])
@login_required
def form_pflanze_details(id):

    pflanze_form = forms.PflanzeForm()
    pflanze = db.session.query(Pflanze).filter(Pflanze.id == id).first()

    if request.method == 'POST':

        #wenn im Ändern-Modus
        if 'aendern' in request.form:
            if current_user.is_admin != True and current_user.id != pflanze.created_by:
                flash('Keine Berechtigung zum Ändern dieses Eintrags.', MsgCat.ERR.value)
            elif pflanze_form.validate_on_submit():
                pflanze.name = pflanze_form.name.data
                pflanze.wissenschaft_name = pflanze_form.wissenschaft_name.data
                pflanze.familie = pflanze_form.familie.data
                pflanze.vegetationszone = pflanze_form.vegetationszone.data
                pflanze.will_sonne = pflanze_form.will_sonne.data
                pflanze.gefahr = pflanze_form.gefahr.data
        
                db.session.commit()

                #ggf. noch die Bild-Datei hochladen
                f = request.files['bild']
                if f.filename != '':
                    str = app.config['UPLOAD_FOLDER'] + '/Pflanze_' + id + '.jpg'
                    f.save(str)

                return redirect(url_for('pflanzen_page'))

        #wenn im Löschen-Modus
        elif 'loeschen' in request.form:
            if current_user.is_admin != True and current_user.id != pflanze.created_by:
                flash('Keine Berechtigung zum Löschen dieses Eintrags.', MsgCat.ERR.value)
            else:
                db.session.query(Pflanze).filter_by(id = id).delete()
                db.session.commit()
                return redirect(url_for('pflanzen_page'))
        elif 'abbrechen' in request.form:
            return redirect(url_for('pflanzen_page'))

    pflanze_bild_datei = '/static/uploads/Pflanze_' + id + '.jpg'
    pflanze_form.name.data = pflanze.name
    pflanze_form.wissenschaft_name.data = pflanze.wissenschaft_name
    pflanze_form.familie.data = pflanze.familie
    pflanze_form.vegetationszone.data = pflanze.vegetationszone
    pflanze_form.will_sonne.data = pflanze.will_sonne
    pflanze_form.gefahr.data = pflanze.gefahr
        
    return render_template('pflanze.html',
                           pflanze_form = pflanze_form,
                           pflanze_bild_datei = pflanze_bild_datei)


@app.route('/')
@app.route('/index')
def start_page():
    pflanzen = db.session.query(Pflanze).limit(3).all()
    return render_template('index.html',
                            pflanzen = pflanzen)



@app.route('/pflanzen', methods = ['GET', 'POST'])
@app.route("/pflanzen/<id>", methods=['GET','POST'])
def pflanzen_page(id=0):

    form = forms.PflanzeForm()
    pflanzen = Pflanze.query.all()

    detail_form = forms.PflanzeForm()
    modus = "change" #Default

    print(id)
    if (id == "new"):
        print("insert")
        showModal = True
        modus = "insert"
    elif (id != 0):
        detail_pflanzen = db.session.query(Pflanze).filter(Pflanze.id == id)
        print('Anzahl: ' + str(detail_pflanzen.count()))

        for pflanze in detail_pflanzen:
            #detail_form.bild.data = '/static/uploads/Pflanze_' + id + '.jpg'
            detail_form.name.data = pflanze.name
            detail_form.wissenschaft_name.data = pflanze.wissenschaft_name
            detail_form.familie.data = pflanze.familie
            detail_form.vegetationszone.data = pflanze.vegetationszone
            detail_form.will_sonne.data = pflanze.will_sonne
            detail_form.gefahr.data = pflanze.gefahr

        showModal = True
        modus = "update"
    else:
        showModal = False

    print(request.method)
    if request.method == 'POST':
        if 'anlegen' in request.form:
            if detail_form.validate_on_submit():
                pflanze = Pflanze(  name = detail_form.name.data,
                                    wissenschaft_name = detail_form.wissenschaft_name.data,
                                    familie = detail_form.familie.data,
                                    vegetationszone = detail_form.vegetationszone.data,
                                    will_sonne = detail_form.will_sonne.data,
                                    gefahr = detail_form.gefahr.data,
                                    created_by = current_user.id)

                db.session.add(pflanze)
                db.session.commit()

                #ggf. noch die Bild-Datei hochladen
                f = request.files['bild']
                if f.filename != '':
                    string = app.config['UPLOAD_FOLDER'] + '/Pflanze_' + str(pflanze.id) + '.jpg'
                    f.save(string)

                return redirect(url_for('pflanzen_page'))
            else:
                showModal = True #um die Fehler anzuzeigen
        elif 'aendern' in request.form:
            print("aendern")
            if detail_form.validate_on_submit():
                print("valid")
                print(detail_pflanzen)
                for pflanze in detail_pflanzen:
                    print(pflanze.name)
                    print(detail_form.name.data)
                    pflanze.name = detail_form.name.data
                    print(pflanze.name)
                    print(id)
                    print(pflanze.id)
                    print('Anzahl: ' + str(detail_pflanzen.count()))
                    pflanze.wissenschaft_name = detail_form.wissenschaft_name.data
                    pflanze.familie = detail_form.familie.data
                    pflanze.vegetationszone = detail_form.vegetationszone.data
                    pflanze.will_sonne = detail_form.will_sonne.data
                    pflanze.gefahr = detail_form.gefahr.data
        
                db.session.commit()
                return redirect(url_for('pflanzen_page'))
            else:
                showModal = True #um die Fehler anzuzeigen
        elif 'bild_hochladen' in request.form:
            for pflanze in detail_pflanzen: #TODO: read?!
                return redirect(url_for('upload_file',id=pflanze.id))

    return render_template('pflanzen.html',
                            pflanzen = pflanzen,
                            form = form,
                            detail_form = detail_form,
                            showModal = showModal,
                            modus = modus)


if __name__ == "__main__": # Ausführen
    app.run(debug=True) # Starten