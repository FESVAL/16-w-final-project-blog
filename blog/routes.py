from flask import render_template, request
from faker import Faker
from blog import app
#from . import app   

from blog.models import Entry, db
from blog.forms import EntryForm
#from .models import Entry
#from . import db
#from .forms import EntryForm

#функция фейковых записей

#def generate_entries(how_many=10):
    #fake = Faker()
   
    #for i in range(how_many):
        #post = Entry(
            #title=fake.sentence(),
            #body='\n'.join(fake.paragraphs(15)),
            #is_published=True
        #)
        #db.session.add(post)
    #db.session.commit()
    #all_posts = Entry.query.all()
    #return all_posts


@app.route("/")
def index():
   all_posts = Entry.query.filter_by(is_published=True).order_by(Entry.pub_date.desc())
   return render_template("homepage.html", all_posts=all_posts)

#окрема функція створення нового запису - видалити після об'єднання
#@app.route("/new-post/", methods=["GET", "POST"])
#def create_entry():
   form = EntryForm()
   errors = None
   if request.method == 'POST':
       if form.validate_on_submit():
           entry = Entry(
               title=form.title.data,
               body=form.body.data,
               is_published=form.is_published.data,
           )
           db.session.add(entry)
           db.session.commit()
       else:
           errors = form.errors
   return render_template("entry_form.html", form=form, errors=errors)

#окрема функція коригування запису - видалити після об'єднання
#@app.route("/edit-post/<int:entry_id>", methods=["GET", "POST"])
#def edit_entry(entry_id):
   entry = Entry.query.filter_by(id=entry_id).first_or_404()
   form = EntryForm(obj=entry)
   errors = None
   if request.method == 'POST':
       if form.validate_on_submit():
           form.populate_obj(entry)
           db.session.commit()
       else:
           errors = form.errors
   return render_template("entry_form.html", form=form, errors=errors)

#!!!завдання - спільна функція створення та редагування запису 
@app.route("/posts/<int:entry_id>", methods=["GET", "POST"])
def create_edit_entry(entry_id):
   errors = None

   if entry_id==0: #создаем новую запись
       
    form = EntryForm()
    if request.method == 'POST':
       if form.validate_on_submit():
           entry = Entry(
               title=form.title.data,
               body=form.body.data,
               is_published=form.is_published.data,
           )
           db.session.add(entry)
           db.session.commit()
       else:
           errors = form.errors
   

    else:  # редактируем старую запись
       entry = Entry.query.filter_by(id=entry_id).first_or_404()
       form = EntryForm(obj=entry)
   
       if request.method == 'POST':
            if form.validate_on_submit():
                form.populate_obj(entry)
                db.session.commit()
            else:
                errors = form.errors


   return render_template("entry_form.html", form=form, errors=errors)