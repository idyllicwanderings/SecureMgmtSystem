from flask import Flask, render_template, redirect, url_for, Response
from flask_user import UserManager, user_registered, user_logged_in
from model import db, Person, Role, FREEUSER, PREMIUMUSER, MODERATOR, ADMIN
from project import SecurityException, init
from flask_principal import Principal, Identity, identity_loaded, identity_changed



app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['USER_APP_NAME'] = "Event Platform"
app.config['USER_ENABLE_EMAIL'] = False      
app.config['USER_ENABLE_USERNAME'] = True    
app.config['USER_REQUIRE_RETYPE_PASSWORD'] = False
app.config['SECRET_KEY'] = '_5#yfasQ8sansaxec/][#1'
app.config['USER_UNAUTHORIZED_ENDPOINT'] = 'error'

@app.route('/error')
def error():
    msg = "You are not allowed to access this page: Not a User"
    return render_template('error.html', message = msg)

@user_registered.connect_via(app)
def after_user_registered_hook(sender, user, **extra):
    role = Role.query.filter_by(name=FREEUSER).one()
    user.role=role
    db.session.commit()

db.init_app(app)


with app.app_context():
    db.create_all()
    roles = Role.query.all()
    if len(roles) == 0:
        db.session.add(Role(name=FREEUSER))
        db.session.add(Role(name=PREMIUMUSER))
        db.session.add(Role(name=MODERATOR))
        db.session.add(Role(name=ADMIN))
        db.session.commit()

user_manager = UserManager(app, db, Person)

principals = Principal(app)

@user_logged_in.connect_via(app)
def _after_login_hook(sender, user, **extra):
    identity_changed.send(app,identity=Identity(user.id))


@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
    from project import on_identity_loaded
    return on_identity_loaded(sender, identity) 


init()

def secure(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except SecurityException as se:
            db.session.rollback()
            return render_template(se.page, security_violation = True, msg = se.msg, **se.params)
    wrapper.__name__ = func.__name__
    return wrapper




@app.route('/')
@secure
def main():
    from project import main 
    result=main()
    if type(result) == Response:
        return result
    else: 
        return render_template('main.html', **result)
        

@app.route('/profile')
@secure
def profile():
    from project import profile 
    result=profile()
    if type(result) == Response:
        return result
    else: 
        return render_template('profile.html', **result)
        

@app.route('/events')
@secure
def events():
    from project import events 
    result=events()
    if type(result) == Response:
        return result
    else: 
        return render_template('events.html', **result)


@app.route('/view_event/<int:id>')
@secure
def view_event(id):
    from project import view_event 
    result=view_event(id)
    if type(result) == Response:
        return result
    else: 
        return render_template('view_event.html', **result)


@app.route('/edit_event/<int:id>')
@secure
def edit_event(id):
    from project import edit_event 
    result=edit_event(id)
    if type(result) == Response:
        return result
    else: 
        return render_template('edit_event.html', **result)


@app.post('/update_event')
@secure
def update_event():
    from project import update_event 
    result=update_event()
    if type(result) == Response:
        return result
    else: 
        return redirect(url_for('edit_event',id=result))



@app.route('/join/<int:id>')
@secure
def join(id):
    from project import join 
    result=join(id)
    if type(result) == Response:
        return result
    else: 
        return redirect(url_for('events'))


@app.route('/leave/<int:id>')
@secure
def leave(id):
    from project import leave 
    result=leave(id)
    if type(result) == Response:
        return result
    else: 
        return redirect(url_for('profile'))


@app.post('/create_event')
@secure
def create_event():
    from project import create_event 
    result=create_event()
    if type(result) == Response:
        return result
    else: 
        return redirect(url_for('events'))


@app.route('/manage_event/<int:id>')
@secure
def manage_event(id):
    from project import manage_event 
    result=manage_event(id)
    if type(result) == Response:
        return result
    else: 
        return render_template('manage_event.html', **result)


@app.route('/categories')
@secure
def categories():
    from project import categories 
    result=categories()
    if type(result) == Response:
        return result
    else: 
        return render_template('categories.html', **result)


@app.route('/view_category/<int:id>')
@secure
def view_category(id):
    from project import view_category 
    result=view_category(id)
    if type(result) == Response:
        return result
    else: 
        return render_template('view_category.html', **result)


@app.route('/remove_category/<int:id>/<int:c>')
@secure
def remove_category(id,c):
    from project import remove_category 
    result=remove_category(id,c)
    if type(result) == Response:
        return result
    else: 
        return redirect(url_for('view_category',id=c))


@app.route('/edit_category/<int:id>')
@secure
def edit_category(id):
    from project import edit_category 
    result=edit_category(id)
    if type(result) == Response:
        return result
    else: 
        return render_template('edit_category.html', **result)


@app.route('/add_moderator/<int:id>/<int:c>')
@secure
def add_moderator(id,c):
    from project import add_moderator 
    result=add_moderator(id,c)
    if type(result) == Response:
        return result
    else: 
        return redirect(url_for('edit_category',id=c))


@app.route('/remove_moderator/<int:id>/<int:c>')
@secure
def remove_moderator(id,c):
    from project import remove_moderator 
    result=remove_moderator(id,c)
    if type(result) == Response:
        return result
    else: 
        return redirect(url_for('edit_category',id=c))


@app.post('/update_category')
@secure
def update_category():
    from project import update_category 
    result=update_category()
    if type(result) == Response:
        return result
    else: 
        return redirect(url_for('edit_category',id=result))
    

@app.route('/subscribe/<int:id>')
@secure
def subscribe(id):
    from project import subscribe 
    result=subscribe(id)
    if type(result) == Response:
        return result
    else: 
        return redirect(url_for('categories'))


@app.route('/unsubscribe/<int:id>')
@secure
def unsubscribe(id):
    from project import unsubscribe 
    result=unsubscribe(id)
    if type(result) == Response:
        return result
    else: 
        return redirect(url_for('profile'))


@app.post('/create_category')
@secure
def create_category():
    from project import create_category 
    result=create_category()
    if type(result) == Response:
        return result
    else: 
        return redirect(url_for('categories'))


@app.route('/users')
@secure
def users():
    from project import users
    result=users()
    if type(result) == Response:
        return result
    else: 
        return render_template('users.html', **result) 
        

@app.route('/user/<int:id>')
@secure
def user(id):
    from project import user 
    result=user(id)
    if type(result) == Response:
        return result
    else: 
        return render_template('user.html', **result) 
        

@app.post('/update_user')
@secure
def update_user():
    from project import update_user 
    result=update_user()
    if type(result) == Response:
        return result
    else: 
        return redirect(url_for('user',id=result))


@app.route('/promote_manager/<int:id>/<int:e>')
@secure
def promote_manager(id,e):
    from project import promote_manager 
    result=promote_manager(id,e)
    if type(result) == Response:
        return result
    else: 
        return redirect(url_for('manage_event',id=e))


@app.route('/demote_manager/<int:id>/<int:e>')
@secure
def demote_manager(id,e):
    from project import demote_manager 
    result=demote_manager(id,e)
    if type(result) == Response:
        return result
    else: 
        return redirect(url_for('manage_event',id=e))


@app.route('/remove_attendee/<int:id>/<int:e>')
@secure
def remove_attendee(id,e):
    from project import remove_attendee 
    result=remove_attendee(id,e)
    if type(result) == Response:
        return result
    else: 
        return redirect(url_for('manage_event',id=e))


@app.route('/accept_request/<int:id>/<int:e>')
@secure
def accept_request(id,e):
    from project import accept_request 
    result=accept_request(id,e)
    if type(result) == Response:
        return result
    else: 
        return redirect(url_for('manage_event',id=e))


@app.route('/reject_request/<int:id>/<int:e>')
@secure
def reject_request(id,e):
    from project import reject_request 
    result=reject_request(id,e)
    if type(result) == Response:
        return result
    else: 
        return redirect(url_for('manage_event',id=e))



@app.route('/send_invite/<int:id>/<int:e>')
@secure
def send_invite(id,e):
    from project import send_invite 
    result=send_invite(id,e)
    if type(result) == Response:
        return result
    else: 
        return redirect(url_for('manage_event',id=e))




@app.route('/accept_invitation/<int:id>')
@secure
def accept_invitation(id):
    from project import accept_invitation 
    result=accept_invitation(id)
    if type(result) == Response:
        return result
    else: 
        return redirect(url_for('profile'))



@app.route('/decline_invitation/<int:id>')
@secure
def decline_invitation(id):
    from project import decline_invitation 
    result=decline_invitation(id)
    if type(result) == Response:
        return result
    else: 
        return redirect(url_for('profile'))