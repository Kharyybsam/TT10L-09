from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from .models import Lostitem
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():   #this function wil run whenever we go to "/"
    if request.method == 'POST': 
        note = request.form.get('note')#Gets the note from the HTML 

        if len(note) < 1:
            flash('Note is too short!', category='error') 
        else:
            new_note = Note(data=note, user_id=current_user.id)  #providing the schema for the note 
            db.session.add(new_note) #adding the note to the database 
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():  
    note = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})


@views.route('/delete-lostitem', methods=['POST'])
def delete_lostitem():  
    lostitem = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    lostitemid = lostitem['lostitemid']
    lostitem = Lostitem.query.get(lostitemid)
    if lostitem:
        if lostitem.user_id == current_user.id:
            db.session.delete(lostitem)
            db.session.commit()

    return jsonify({})
@views.route('/reportitem')
@login_required
def reportitempage():

    return render_template("reportitem.html",user=current_user)
  

@views.route('/reportfounditem',methods=['GET', 'POST'])
@login_required
def reportfounditempage():

    return render_template("reportfounditem.html",user=current_user)

@views.route('/reportlostitem',methods=['GET', 'POST'])
@login_required
def reportlostitempage():
    if request.method == 'POST': 
        itemname = request.form.get('name')#Gets the note from the HTML 
        itemdescription = request.form.get('description')
        if len(itemname) < 1:
            flash('Note is too short!', category='error') 
        else:
            new_lostitems = Lostitem(perru=itemname,description=itemdescription, user_id=current_user.id)  #providing the schema for the note 
            db.session.add(new_lostitems) #adding the note to the database 
            db.session.commit()
            flash('Note added!', category='success')      
    return render_template("reportlostitem.html",user=current_user)

@views.route('/user-settings')
@login_required
def usersettings():
    return render_template("usersettings.html",user=current_user)



