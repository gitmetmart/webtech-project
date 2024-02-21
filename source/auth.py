from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():    #functie voor het inloggen van users
    if request.method == 'POST':    #maakt login velden bruikbaar voor email en password
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first() #Checkt het email 1 op 1
        if user:
            if check_password_hash(user.password, password):    #hashed het ingevoerde pass en checkt de overeenkomst met het database
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)     #Onthoudt current logged in user
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')  #logged de User uit 
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():  #functie voor het aanmaken van nieuwe gebruikers
    if request.method == 'POST':    #Maakt velden bruikbaar 
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first() #checkt of email al bestaat in de users database
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:    #checkt of email lengte groter is dan 4
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:   #checkt of naam lengte grote is dan 2
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:    #checkt of password en confirm password overeen komen
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:    #checkt of password een minimale lengte van 7 char heeft
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1)) #voegt nieuwe user toe met een gehashde versie van het wachtwoord
            db.session.add(new_user)                                                                        #Default hasing Algoritme is Sha256    
            db.session.commit()
            login_user(new_user, remember=True) #logged de nieuwe gebruiker in na aanmaak van account
            flash('Account created!', category='success')
            return redirect(url_for('views.home')) #load de home pagina

    return render_template("sign_up.html", user=current_user)