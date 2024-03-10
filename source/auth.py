from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
import re

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    Functie voor het inloggen van gebruikers.

    Verwerkt het inloggen van gebruikers met behulp van het Flask-formulier.
    Controleert of de ingevoerde e-mail en wachtwoord overeenkomen met de gegevens in de database.
    Logt de gebruiker in en onthoudt de huidige gebruiker.
    Verwijst naar de homepagina na succesvol inloggen.

    Returns:
        rendered template: Het login.html-template met de huidige gebruiker.
    """
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')
    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    """
    Functie voor het uitloggen van gebruikers.

    Logt de huidige gebruiker uit en verwijst naar de loginpagina.

    Returns:
        redirect: Redirect naar de loginpagina.
    """
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    """
    Functie voor het aanmaken van nieuwe gebruikers.

    Verwerkt het aanmaken van nieuwe gebruikers met behulp van het Flask-formulier.
    Controleert of de ingevoerde e-mail geldig is en uniek is.
    Controleert de lengte van de e-mail, voornaam en wachtwoord.
    Hashes het wachtwoord en voegt de nieuwe gebruiker toe aan de database.
    Logt de nieuwe gebruiker in en verwijst naar de homepagina na succesvol aanmaken van het account.

    Returns:
        rendered template: Het sign_up.html-template met de huidige gebruiker.
    """
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        def is_valid_email(email):
            """
            Controleert of een e-mailadres geldig is.

            Args:
                email (str): Het e-mailadres dat gecontroleerd moet worden.

            Returns:
                bool: True als het e-mailadres geldig is, False anders.
            """
            pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
            return re.match(pattern, email) is not None
    
        def is_valid_first_name(first_name):
            """
            Controleert of een voornaam geldig is.

            Args:
                first_name (str): De voornaam die gecontroleerd moet worden.

            Returns:
                bool: True als de voornaam geldig is, False anders.
            """
            pattern = r'^[a-zA-Z]+$' # alleen letters
            return re.match(pattern, first_name) is not None
        
        def is_valid_password(password):
            """
            Controleert of een wachtwoord geldig is.

            Args:
                password (str): Het wachtwoord dat gecontroleerd moet worden.

            Returns:
                bool: True als het wachtwoord geldig is, False anders.
            """
            pattern = r'^[\w\.-]{7,}$' # minimaal 7 karakters
            return re.match(pattern, password) is not None

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif not is_valid_email(email):
            flash('Invalid email address.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif not is_valid_first_name(first_name):
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif not is_valid_password(password1):
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)


@auth.route('/about')
def about():
    """
    Deze functie handelt het verzoek af voor de about-pagina van de applicatie.
    De about-pagina wordt gerenderd.
    """
    return render_template("about.html", user=current_user)