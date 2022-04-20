import email
from flask import Blueprint, render_template, request, redirect, url_for, flash
from anime_inventory.models import User, db
from anime_inventory.forms import UserLoginForm

auth = Blueprint('auth', __name__, template_folder = 'auth_templates')

@auth.route('/signup', methods = ['GET', 'POST'])
def signup():
    form = UserLoginForm()

    try:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            print(email,password)

            user = User(email, password = password)
            db.session.add(user)
            db.session.commit()

            flash(f'You have succesfully created an account: {email}', 'user-created')
            

            return redirect(url_for('site.home'))
    except:
        raise Exception('invalid form data: please check your form')
    return render_template('signup.html', form = form)

@auth.route('/signin', methods = ['GET', 'POST'])
def signin():
    return render_template('signin.html')
