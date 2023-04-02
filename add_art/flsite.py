import sqlite3
import os
from flask import Flask, render_template, request, g, flash, abort
from FDataBase import FDataBase

# configurare
DATABASE = '/tmp/flsite.db'
DEBUG = True
SECRET_KEY = 'fdgfh78@#5?>gfhf89dx,j86p'
USERNAME = 'admin'
PASSWORD = '456'

###### app   ###################################
app = Flask(__name__)
app.config.from_object(__name__)

#####  definim calea DB   ######################
app.config.update(dict(DATABASE=os.path.join(app.root_path,'flsite.db')))

###### funct conectam DB ################################################
def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

### Funcția de ajutor pentru crearea tabelelor bazei de date, fara server  #########
def create_db():
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()

###   Conexiune DB dacă nu este deja stabilită    ########
def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db

###   Închidem conexiunea la baza de date, dacă a fost stabilită   ####
@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()

#########


@app.route("/")
def index():
    db = get_db()
    dbase = FDataBase(db)
    return render_template('index.html', menu=dbase.getMenu(), posts=dbase.getPostsAnonce())
######


@app.route("/add_post", methods=["POST", "GET"])
def addPost():
    db = get_db()
    dbase = FDataBase(db)

    if request.method == "POST":
        if len(request.form['name']) > 4 and len(request.form['post']) > 10:
            res = dbase.addPost(request.form['name'], request.form['post'], request.form['url'])
            if not res:
                flash('Eroarebla adaugarea articolului', category='error')
            else:
                flash('Articolul a fost adaugat cu succes', category='success')
        else:
            flash('Eroare la adaugarea articolului', category='error')

    return render_template('add_post.html', menu=dbase.getMenu(), title="Adauga noutati")

######  dupa ce so adugat articolul acesta func  il arata pe website  ###
@app.route("/post/<alias>")
def showPost(alias):
    db = get_db()
    dbase = FDataBase(db)
    title, post = dbase.getPost(alias)
    if not title:
        abort(404)

    return render_template('post.html', menu=dbase.getMenu(), title=title, post=post)

if __name__ == "__main__":
   app.run(debug=True)

### DB Browser for SQLite  ####
###  https://sqlitebrowser.org/dl/   ###

####  python console -> ctrl+shift+p =>##
# from flsite import create_db
#  create_db()
"""
From the Command Palette (Ctrl+Shift+P), select the Python: 
Start REPL command to open a REPL terminal for the currently 
selected Python interpreter. In the REPL, you can then enter 
and run lines of code one at a time.
"""
