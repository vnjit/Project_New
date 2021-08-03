from typing import List, Dict
import simplejson as json
from flask import Flask, request, Response, redirect, render_template, url_for, Blueprint, flash
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from models import User

from forms import SignupForm, LoginForm


app = Flask(__name__)
app.config.from_object('config.Config')


db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
db.init_app(app)


mysql = MySQL(cursorclass=DictCursor)
mysql.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    """Check if user is logged-in upon page load."""
    if user_id is not None:
        # Get User by Email
        cursor = mysql.get_db().cursor()
        cursor.execute('SELECT * FROM `flasklogin-users` WHERE id = %s', user_id)
        result = cursor.fetchall()
        if len(result) != 0:
            my_id = result[0]['id']
            name = result[0]['name']
            email = result[0]['email']
            password = result[0]['password']
            return User(my_id, name, email, password)
        else:
            return None
    return None


@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    flash('You must be logged in to view that page.')
    return redirect(url_for('login'))


# User authentication is below...
# Sign Up Page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """User sign-up form for account creation."""
    form = SignupForm()
    if form.validate_on_submit():

        # Get Form Fields
        name = form.name.data
        email = form.email.data
        password = form.password.data

        # Get User by Email
        cursor = mysql.get_db().cursor()
        cursor.execute('SELECT * FROM `flasklogin-users` WHERE email = %s', email)
        result = cursor.fetchall()
        if len(result) == 0:  # User does not exist yet
            # Encrypt Password
            hashed_password = generate_password_hash(
                password,
                method='sha256'
            )

            # Add User to DB
            insert_cursor = mysql.get_db().cursor()
            input_data = (name, email, hashed_password)
            sql_insert_query = """INSERT INTO `flasklogin-users` (name, email, password) VALUES (%s, %s, %s) """
            insert_cursor.execute(sql_insert_query, input_data)
            mysql.get_db().commit()

            # Add User to session
            cursor = mysql.get_db().cursor()
            cursor.execute('SELECT * FROM `flasklogin-users` WHERE email = %s', email)
            result = cursor.fetchall()
            user_id = result[0]['id']
            user = User(user_id, name, email, hashed_password)
            login_user(user)  # Log in as newly created user
            return redirect('/')
        flash('A user already exists with that email address.')
    return render_template(
        'signup.html',
        title='Create an Account.',
        form=form,
        template='signup-page',
        body="Sign up for a user account."
    )


# Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login form for account creation."""
    form = LoginForm()

    if form.validate_on_submit():

        # Get Form Fields
        email = form.email.data
        password = form.password.data

        # Hash the password
        hashed_password = generate_password_hash(password, method='sha256')

        # Get User by Email and Hashed Password
        cursor = mysql.get_db().cursor()
        cursor.execute('SELECT * FROM `flasklogin-users` WHERE email = %s AND password = %s', (email, hashed_password))
        result = cursor.fetchall()
        if len(result) != 0:  # User found
            # Add User to session
            user_id = result[0]['id']
            name = result[0]['name']
            user = User(user_id, name, email, hashed_password)
            login_user(user)  # Log in as newly created user
            return redirect('/')
        flash('User Not Found! Please re-check email and/or password.')
    return render_template(
        'login.html',
        title='Login to Account.',
        form=form,
        template='login-page',
        body="Login to your account."
    )
#HTML page

@app.route('/', methods=['GET'])
def index():
    user = {'username': 'Data Project'}
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblCitiesImport')
    result = cursor.fetchall()
    return render_template('index.html', title='Home', user=user, cities=result)


@app.route('/view/<int:city_id>', methods=['GET'])
def record_view(city_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblCitiesImport WHERE id=%s', city_id)
    result = cursor.fetchall()
    return render_template('view.html', title='View Data', city=result[0])

@app.route('/cities/new', methods=['GET'])
@login_required
def form_insert_get():
    return render_template('new.html', title='New Data Form')

@app.route('/cities/new', methods=['POST'])
@login_required
def form_update_post(city_id):
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('fldheight'), request.form.get('fldweight'), city_id)
    sql_update_query = """UPDATE tblCitiesImport t SET t.fldheight = %s, t.fldweight = %s WHERE t.id = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/edit/<int:city_id>', methods=['GET'])
@login_required
def form_edit_get(city_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblCitiesImport WHERE id=%s', city_id)
    result = cursor.fetchall()
    return render_template('edit.html', title='Edit Data', city=result[0])


@app.route('/edit/<int:city_id>', methods=['POST'])
@login_required
def form_update_post(city_id):
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('fldheight'), request.form.get('fldweight'), city_id)
    sql_update_query = """UPDATE tblCitiesImport t SET t.fldheight = %s, t.fldweight = %s WHERE t.id = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/delete/<int:city_id>', methods=['POST'])
@login_required
def form_delete_post(city_id):
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM tblCitiesImport WHERE id = %s """
    cursor.execute(sql_delete_query, city_id)
    mysql.get_db().commit()
    return redirect("/", code=302)


# API Request

@app.route('/api/v1/cities', methods=['GET'])
def api_browse() -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblCitiesImport')
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/cities/<int:city_id>', methods=['GET'])
def api_retrieve(city_id) -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblCitiesImport WHERE id=%s', city_id)
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/cities', methods=['POST'])
def api_add() -> str:

    content = request.json

    cursor = mysql.get_db().cursor()
    inputData = (content['fldheight'], content['fldweight'])
    sql_insert_query = """INSERT INTO tblCitiesImport (fldheight,fldweight) VALUES (%s, %s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    resp = Response(status=201, mimetype='application/json')
    return resp


@app.route('/api/v1/cities/<int:city_id>', methods=['PUT'])
def api_edit(city_id) -> str:
    cursor = mysql.get_db().cursor()
    content = request.json
    inputData = (content['fldheight'], content['fldweight'],city_id)
    sql_update_query = """UPDATE tblCitiesImport t SET t.fldheight = %s, t.fldweight = %s WHERE t.id = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    resp = Response(status=200, mimetype='application/json')
    return resp

@app.route('/api/v1/cities/<int:city_id>', methods=['DELETE'])
def api_delete(city_id) -> str:
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM tblCitiesImport WHERE id = %s """
    cursor.execute(sql_delete_query, city_id)
    mysql.get_db().commit()
    resp = Response(status=200, mimetype='application/json')
    return resp

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5006, debug=True)
