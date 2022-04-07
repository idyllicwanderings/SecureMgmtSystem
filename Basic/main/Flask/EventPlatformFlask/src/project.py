from flask import request
from flask_user import current_user
from model import db, Person, Role, Event, Category
from dto import PersonDTO, EventDTO, CategoryDTO, RoleDTO


# Throw this exception when action is not authorized 
# You can either use the default error page, or redirect to 
# another page (+ its params), which will then have a 
# notification at the bottom
class SecurityException(Exception):
    def __init__(self, msg = 'Not allowed', page = 'error.html', params = {}):
        self.msg = msg
        self.page = page
        self.params = params


def on_identity_loaded(sender, identity):
    pass


# Use in case you need to initialize something
def init():
    pass


def main():
    user=PersonDTO.copy(current_user) 
    return {'user' : user}


def profile():
    user=PersonDTO.copy(current_user) 
    for e in user.manages:
        e.owner = PersonDTO.copy(Event.query.get(e.id).owner)
    for e in user.attends:
        e.owner = PersonDTO.copy(Event.query.get(e.id).owner)
    subs=CategoryDTO.copies(current_user.subscriptions)
    for s in subs:
        for e in s.events:
            e.owner = PersonDTO.copy(Event.query.get(e.id).owner)
    return {'user' : user, 'subs' : subs}
        

def events():   
    events = EventDTO.copies(Event.query.all())
    categories = CategoryDTO.copies(Category.query.all())
    return {'events' : events, 'categories' : categories}


def view_event(id):
    event = EventDTO.copy(Event.query.get(id))
    return {'event' : event}


def edit_event(id):
    event = EventDTO.copy(Event.query.get(id))
    categories = CategoryDTO.copies(Category.query.all())
    return {'event' : event, 'categories' : categories}


def update_event():
    id = request.form["id"]
    event = Event.query.get(id)
    title = request.form["title"]
    description = request.form["description"]
    private = "private" in request.form
    categories = request.form.getlist("categories")
    categories = [Category.query.get(c) for c in categories]
    
    event.title = title
    event.private = private
    event.description = description
    event.categories = categories
    db.session.commit()
    return id


def join(id):
    event = Event.query.get(id)
    if current_user not in event.requesters:
        event.requesters.append(current_user)
        db.session.commit()
    

def leave(id):
    event = Event.query.get(id)
    if current_user in event.attendants:
        event.attendants.remove(current_user)
        db.session.commit()
    

def create_event():
    title = request.form["title"]
    description = request.form["description"]
    private = "private" in request.form
    owner = current_user
    categories = request.form.getlist("categories")
    categories = [Category.query.get(c) for c in categories]
    event = Event(title=title,
                  description=description,
                  private=private,
                  owner=owner,
                  categories=categories)
    event.managedBy.append(owner)
    event.attendants.append(owner)
    db.session.add(event)
    db.session.commit()
    

def manage_event(id):
    event = EventDTO.copy(Event.query.get(id))
    return {'event' : event}


def categories():
    categories = CategoryDTO.copies(Category.query.all())
    return {'categories' : categories}


def view_category(id):
    category = CategoryDTO.copy(Category.query.get(id))
    return {'category' : category}


def remove_category(id,c):
    event = Event.query.get(id)
    category = Category.query.get(c)
    if event in category.events:
        category.events.remove(event)
        db.session.commit()
    


def edit_category(id):
    cat = Category.query.get(id)
    category = CategoryDTO.copy(cat)
    candidates = PersonDTO.copies(cat.candidates)
    return {'category' : category, 'candidates' : candidates}


def add_moderator(id,c):
    user = Person.query.get(id)
    category = Category.query.get(c)
    if user not in category.moderators:
        category.moderators.append(user)
        db.session.commit()


def remove_moderator(id,c):
    user = Person.query.get(id)
    category = Category.query.get(c)
    if user in category.moderators:
        category.moderators.remove(user)
        db.session.commit()


def update_category():
    id = request.form["id"]
    category = Category.query.get(id)
    name = request.form["name"]
    category.name = name
    db.session.commit()
    return id


def subscribe(id):
    category = Category.query.get(id)
    if category not in current_user.subscriptions:
         current_user.subscriptions.append(category)
         db.session.commit()
    

def unsubscribe(id):
    category = Category.query.get(id)
    if category in current_user.subscriptions:
         current_user.subscriptions.remove(category)
         db.session.commit()
    

def create_category():
    name = request.form["name"]
    category = Category(name=name)
    db.session.add(category)
    db.session.commit()


def users():
    users = PersonDTO.copies(Person.query.all())
    return {'users' : users}


def user(id):
    user = PersonDTO.copy(Person.query.get(id))
    roles = RoleDTO.copies(Role.query.all())
    return {'user' : user, 'roles' : roles}

def update_user():
    id = request.form["id"]
    name = request.form["name"]
    surname = request.form["surname"]
    role = request.form["role"]

    user = Person.query.get(id)
    user.name = name
    user.surname = surname
    role = Role.query.filter_by(name=role).first()
    user.role = role
    db.session.commit()
    return id
        

def promote_manager(id,e):
    user = Person.query.get(id)
    event = Event.query.get(e)
    if user not in event.managedBy:
        event.managedBy.append(user)
        db.session.commit()  


def demote_manager(id,e):
    user = Person.query.get(id)
    event = Event.query.get(e)
    if user in event.managedBy:
        event.managedBy.remove(user)
        db.session.commit()


def remove_attendee(id,e):
    user = Person.query.get(id)
    event = Event.query.get(e)
    if user in event.attendants:
        event.attendants.remove(user)
        db.session.commit()


def accept_request(id,e):
    user = Person.query.get(id)
    event = Event.query.get(e)
    if user not in event.attendants:
        event.attendants.append(user)
    event.requesters.remove(user)
    db.session.commit()


def reject_request(id,e):
    user = Person.query.get(id)
    event = Event.query.get(e)
    event.requesters.remove(user)
    db.session.commit()

def send_invite(id,e):
    pass


def accept_invitation(id):
    pass


def decline_invitation(id):
    pass