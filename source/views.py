from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
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

@views.route('/delete-note', methods=['POST'])
def delete_note():  
    note = json.loads(request.data) #Vraag het Index.html java script bestand op (Index.js)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id: #checkt of de user id's gelijkt staat aan het user note id voor dat er een delete mag worden uitgevoerd
            db.session.delete(note)
            db.session.commit()

    return jsonify({})