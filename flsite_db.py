import sqlite3
import os
from flask import Flask, render_template, request, g

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

######### 
@app.route("/")
def index():
    db = get_db()
    return render_template('index.html', menu=[])

###   Închideți conexiunea la baza de date, dacă a fost stabilită   ####
@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()


if __name__ == "__main__":
   app.run(debug=True)

### DB Browser for SQLite  ####
