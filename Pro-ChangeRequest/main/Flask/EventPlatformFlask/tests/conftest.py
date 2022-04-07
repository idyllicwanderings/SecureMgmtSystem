import pytest

from flask import Flask, render_template
from flask_user import UserManager
from model import MODERATOR, PREMIUMUSER, Invite, db, Person, Role, Event, Category, FREEUSER, ADMIN
from app import SecurityException
from flask_principal import Principal, identity_loaded

@pytest.fixture(scope='function')
def app(request):
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///testingapp.db'
    app.config['USER_APP_NAME'] = "Event Platform Testing"
    app.config['USER_ENABLE_EMAIL'] = False      
    app.config['USER_ENABLE_USERNAME'] = True    
    app.config['USER_REQUIRE_RETYPE_PASSWORD'] = False
    app.config['SECRET_KEY'] = '_5#yfasQ8sansaxec/][#1'
    app.config['USER_UNAUTHORIZED_ENDPOINT'] = 'error'
    app.config['SERVER_NAME'] = 'localhost'
    app.config['TESTING']=True

    principals = Principal(app)

    @identity_loaded.connect_via(app)
    def on_identity_loaded(sender, identity):
        from project import on_identity_loaded
        return on_identity_loaded(sender, identity)

    def secure(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except SecurityException as se:
                db.session.rollback()
                return render_template(se.page, security_violation = True, msg = se.msg, **se.params)
        wrapper.__name__ = func.__name__
        return wrapper

    @app.route('/error')
    def error():
        msg = "You are not allowed to access this page: Not a User"
        return render_template('error.html', message = msg)

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

    db.init_app(app)

    with app.app_context():
        db.drop_all()
        db.create_all()

    UserManager(app, db, Person, RoleClass=Role)

    # Establish an application context before running the tests.
    ctx = app.app_context()
    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)
    return app

@pytest.fixture
def freeuserrole():
    return Role(id=1, name=FREEUSER)

@pytest.fixture
def premiumuserrole():
    return Role(id=2, name=PREMIUMUSER)

@pytest.fixture
def moderatorrole():
    return Role(id=3, name=MODERATOR)

@pytest.fixture
def adminrole():
    return Role(id=4, name=ADMIN)

@pytest.fixture
def user1():
    return Person(id=1, name="user1", surname="user1", username="user1", password='secret1')

@pytest.fixture
def user2():
    return Person(id=2, name="user2", surname="user2", username="user2", password='secret2')

@pytest.fixture
def user3():
    return Person(id=3, name="user3", surname="user3", username="user3", password='secret3')

@pytest.fixture
def publicevent1():
    return Event(id=1, title='event1', description='event1', private=False)

@pytest.fixture
def publicevent2():
    return Event(id=2, title='event2', description='event2', private=False)

@pytest.fixture
def privateevent1():
    return Event(id=3, title='event3', description='event3', private=True)

@pytest.fixture
def privateevent2():
    return Event(id=4, title='event4', description='event4', private=True)

@pytest.fixture
def category1():
    return Category(id=1, name='category1')



@pytest.fixture
def invite1():
    return Invite(id=1)


