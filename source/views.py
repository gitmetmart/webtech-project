from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    """
        Deze functie handelt het verzoek af voor de homepagina van de applicatie.
        Als het verzoek een POST-verzoek is, wordt er een nieuwe notitie toegevoegd aan de database.
        Als het verzoek een GET-verzoek is, wordt de homepagina gerenderd met de ingelogde gebruiker.
    """
    if request.method == 'POST': 
        note = request.form.get('note') #Vraagt de notes op

        if len(note) < 1:
            flash('Note is too short!', category='error')   #Staat lege notes niet toe 
        else:
            new_note = Note(data=note, user_id=current_user.id) #providing the schema for the note 
            db.session.add(new_note)    #Laat de gebruiker nieuwe notes toevoegen aan de database
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)  #Returnt de home pagine + ingeloggede user

@views.route('/update-note', methods=['POST'])
def update_note(note_id, new_data):
    """
        Deze functie handelt het verzoek af om een notitie bij te werken.
        Het verzoek bevat de ID van de notitie die moet worden bijgewerkt en de nieuwe gegevens voor de notitie.
        Als de notitie bestaat en de gebruiker is de eigenaar van de notitie, wordt de notitie bijgewerkt in de database.
    """
    note = json.loads(request.data) #Vraag het Index.html java script bestand op (Index.js)
    noteId = note['noteId']
    new_data = note['newData']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id: #checkt of de user id's gelijkt staat aan het user note id voor dat er een update mag worden uitgevoerd
            note.data = new_data
            db.session.commit()
    return True

@views.route('/delete-note', methods=['POST'])
def delete_note():  
    """
    Deze functie handelt het verzoek af om een notitie te verwijderen.
    Het verzoek bevat de ID van de notitie die moet worden verwijderd.
    Als de notitie bestaat en de gebruiker is de eigenaar van de notitie, wordt de notitie verwijderd uit de database.
    """
    note = json.loads(request.data) #Vraag het Index.html java script bestand op (Index.js)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id: #checkt of de user id's gelijkt staat aan het user note id voor dat er een delete mag worden uitgevoerd
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

@views.route('/about')
def about():
    """
    Deze functie handelt het verzoek af voor de about-pagina van de applicatie.
    De about-pagina wordt gerenderd.
    """
    return render_template("about.html", user=current_user)