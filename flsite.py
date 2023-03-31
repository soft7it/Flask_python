from flask import Flask, render_template, url_for, request, flash, session, redirect, abort

app = Flask(__name__)
#  secret key pentru forma de contact, schimba cheia cit mai complikata
app.config['SECRET_KEY'] = 'fdgdfgdfggf786h0l65hfg6h7f'
menu = [{"name": "Установка", "url": "install-flask"},
        {"name": "Первое приложение", "url": "first-app"},
        {"name": "Обратная связь", "url": "contact"}]

@app.route("/")
def index():
    print( url_for('index'))
    return render_template('index.html', menu=menu)


@app.route("/about")
def about():
    print(url_for('about'))
    return render_template('about.html', title="О сайте", menu=menu)

# 
@app.route("/contact", methods=["POST", "GET"])
def contact():
       
    if request.method == 'POST':
        if len(request.form['username']) > 2:
            flash('Succes sent', category='success')
        else:
            flash('Eroare la trimitere', category='error')
        # print(request.form)
        # print(request.form['username']) # poti lua data so folosesti in alte scopuri dezvolt
    # print(url_for('contact'))
    return render_template('contact.html', title="Back connection", menu=menu)

# @app.route("/profile/<username>")
# def profile(username):
#     return f"Пользователь: {username}"

####### Acces login #############################################


@app.route("/profile/<username>")
def profile(username):
    if 'userLogged' not in session or session['userLogged'] != username:
        abort(401)

    return f"User: {username}"

@app.route("/login", methods=["POST", "GET"])
def login():
    if 'userLogged' in session:
        return redirect(url_for('profile', username=session['userLogged']))
    elif request.method =='POST' and request.form['username'] == "vasile" and request.form['psw'] == "654":
        session['userLogged'] = request.form['username']
        return redirect(url_for('profile', username=session['userLogged']))

    return render_template('login.html', title="autorizarea", menu=menu)
################  error page ###################
@app.errorhandler(404)
def pageNotFount(error):
    return render_template('page404.html', title="Page is not found", menu=menu), 404


# with app.test_request_context():
#     print(url_for('index'))
#     print(url_for('about'))
#     print(url_for('profile', username="Vitalie"))

if __name__ == "__main__":
   app.run(debug=True)

######################################################################
# https://jinja.palletsprojects.com/en/2.11.x/