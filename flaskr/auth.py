# Blueprints and Views
'''
A view function is the code you write to respond to requests to your application.
Flask uses patterns to match（匹配） the incoming request URL(传入的请求YUL) to the view that should handle it.
The view returns data that Flask turns into an outgoing response(视图返回的数据将被Flask转换为传出响应).
Flask can also go the other direction and generate a URL to a view(到视图的URL) based on(根据) its name and arguments.
'''

'''
As you implement each view, keep the development server running. As you save your changes,
try going to the URL in your browser and testing them out.
'''

'''
A blueprint is a way to organize a group of related views and other code.
Rather than registering views and other code directly with an application,
they are registered with a blueprint. Then the blueprint is registered with the
application when it is available in the factory function.
'''
'''
This creates a Blueprint named auth.Like the application object,the
blueprint needs to know where it's defined, so __name__ is passed as 
the second argument.The url_prefix will be prepended(add something to the
beginning of something else) to all the URLs associated with the blueprint.
'''

import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')
'''
The authentication blueprint will have views to register new users 
and to log in and log out.
'''

'''
the register view will return HTML with a form for them to fill out.When they
submit the form,it will validate their input and either(要么) show the form
again with an error message or(要么) create the new user and go to the login page. 
'''

'''
@bp.route associates the URL/register with the register view function. 
When Flask receives a request to /auth/register, it will call the register 
view and use the return value as the response.
'''


@bp.route('/register', methods=('GET', 'POST'))
def register():
    '''
    If the user submitted the form,request.method will be 'POST'.
    In this case, start validating the input.
    '''
    if request.method == 'POST':
        '''
        request.form is a special type of dict mapping submitted form keys and values.
        The user will input their username and password.
        '''
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        '''
        Validate that username and password are not empty.
        Validate that username is not already registered 
        by querying the database and checking if a result is returned
        
        db.execute takes a SQL query with ? placeholders(占位符) for any
        user input(任何用户输入的), and a tuple of values to replace the placeholders
        with.(用来替换占位符的元组) The database library will take care of escaping(转义) the values
        so you are not vulnerable to a SQL injection attack.
        '''
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db.execute(
                'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)
        '''
        fetchone() returns 'one' row from the query.If the query returned
        no results, it returns None.Later,fetchall()is used,which returns 
        a list of all results. 
        '''
        if error is None:
            '''
            If validation succeeds,insert the new user data into the 
            database.For security,passwords should never be stored in 
            the database directly.Instead,generate_password_hash() is
            used to securely hash the password, and that hash is stored.
            Since this query modifies data, db.commit() needs to be called 
            afterwards to save the changes.          
            '''
            db.execute(
                'INSERT INTO user (username,password) VALUES(?,?)',
                (username, generate_password_hash(password))
            )
            db.commit()
            '''
            After storing the user,they are redirected to the login page.
            url_for() generates the URL for the login view based on its name.
            This is preferable to writing the URL directly as it allows you 
            to change the URL later without changing all code that links to it.
            (以后更改URL无需修改链接到该URL的所有代码)
            redirect() generates a redirect response to the generated URL.
            '''
            return redirect(url_for('auth.login'))
        '''
        If validation fails,the error is shown to the user.flash() stores 
        messages that can be retrieved (get or bring (something) back; regain possessing of)
        when rendering the template.
        '''
        flash(error)
    '''
    When the user initially navigates to auth/register, or there was
    a validation error,an HTML page with the registration form should
    be shown.render_template() will render a template containing the
    HTML, which you'll write in the next step of the tutorial.    
    '''
    return render_template('auth/register.html')


'''
This view follows the same pattern as the register view above.
'''


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        '''
        1. The user is queried first and stored in a variable for later use.
        '''
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        # 2. check_password_hash() hashes the submitted password in the save way
        # as the stored hash and securely compares them. If they match the password
        # is valid.
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            # session is a dict that stored data across requests.
            # When validation succeeds,the user's id is stored in a new session
            # The data is stored in a cookie that sent to the browser, and the browser
            # then sends it back with subsequent requests.Flask securely signs the data so that
            # it can't be tampered with(篡改).
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))
        flash(error)
    return render_template('auth/login.html')


'''
Now that the user's id is stored in the session. it will be available on
subsequent requests.At the beginning of each request,if a user is logged in, 
their information should be loaded and made available to other views.
'''

'''
bp.before_app_request() registers a function that runs before the view
function, no matter what URL is requested. load_logged_in_user checks if a user
id is stored in the session and gets that user's data from the database,
storing it on g.user, which lasts for the length of the request.If there is
no user id,or if the id doesn't exist,g.user will be None.
'''


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()


'''
To log out,you need to remove the user id from the session. Then 
load_logged_in_user won't load a user on subsequent requests.
'''


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


# Require Authentication in Other Views
'''
Creating,editing,and deleting blog posts will require a user to be logged in.A
decorator can be used to check this for each view it's applied to.
'''


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view


'''
This decorator returns a new view function that wraps the original view it's
applied to.(返回的函数包装了应用于它的原始视图)The new function checks if
 a user is loaded and redirects to the login page otherwise.
If a user is loaded the original view is called and continues normally.You'll use this decorator
when writing the blog views.
'''

'''
Endpoints and URLs
The url_for() function generates the URL to a view based on a name and 
arguments.The name associated with a view is also called the endpoint, 
and by default it's the same as the name of the view function.


For example,The hello() view that was added to the app factory earlier in the
tutorial has the name 'hello' and can be linked with url_for('hello').IF
it took an argument,which you'll see later, it would be linked to using
url_for('hello',who ='World')


When using a blueprint,the name of blueprint is prepended to the name of
the function,so the endpoint for the login function you wrote above is 
'auth.login' because you added it to the 'auth' blueprint. 
'''