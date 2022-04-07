from flask import  Flask, Response, render_template, request, redirect, url_for
from model import ADMIN, FREEUSER, MODERATOR, PREMIUMUSER, Invite, db, Person, Role, Event, Category
from dto import RESTRICTED, PersonDTO, EventDTO, CategoryDTO, RoleDTO, InviteDTO
from email import message
from enum import Enum, auto
from flask_sqlalchemy import SQLAlchemy, models_committed
from flask_user import current_user, login_required, UserManager, UserMixin, user_logged_in
from flask_principal import Principal, Identity, Permission, UserNeed, RoleNeed, identity_loaded, identity_changed

from permission import JoinEventNeed, JoinEventPermission, SendInviteNeed, SendInvitePermission, ViewInviteEventNeed, ViewInviteEventPermission, admin,freeuser,premiumuser,moderator
from permission import AddManageNeed, AddManagePermission, AddModerateNeed, AddModeratePermission, AddSubscriptionNeed, AddSubscriptionPermission, EditEventCoreInfoNeed, EditEventCoreInfoPermission, JoinRequestNeed, JoinRequestPermission, LeaveAttendNeed, LeaveAttendPermission, RemoveAttendNeed, RemoveAttendPermission,RemoveModeratorCategoryPermission,RemoveModeratorCategoryNeed, RemoveCategoryNeed, RemoveCategoryPermission, RemoveManageNeed, RemoveManagePermission, RemoveModerateNeed, RemoveModeratePermission, RemoveRequestNeed, RemoveRequestPermission, RemoveSubscriptionNeed, RemoveSubscriptionPermission, SetEventInfoNeed, SetEventInfoPermission, ViewAttendEventNeed, ViewAttendEventPermission, ViewManageEventNeed, ViewManageEventPermission, ViewModerateCategoryNeed, ViewModerateCategoryPermission

import logging

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
    identity.user = current_user

    if hasattr(current_user, 'id'):
        identity.provides.add(UserNeed(current_user.id))

    if hasattr(current_user, 'roles'):
        for role in current_user.roles:
            identity.provides.add(RoleNeed(role.name))

    #normal attends leaves
    if hasattr(current_user,'attends'): 
        for e in current_user.attends:
            if e.owner.id != current_user.id:
                if hasattr(current_user,'manages'):
                    if e not in current_user.manages:
                        identity.provides.add(LeaveAttendNeed(e.id))
                else:
                    identity.provides.add(LeaveAttendNeed(e.id))


    #1. manager remove their events
    #2. moderator remove any event from category
    if hasattr(current_user,'manages'):
        #manager
        for e in current_user.manages:
            identity.provides.add(RemoveCategoryNeed(e.id))

    if hasattr(current_user,'moderates'):
        es = Event.query.all()
        for c in current_user.moderates:
            for e in es:
                if c in e.categories:
                    identity.provides.add(RemoveModeratorCategoryNeed(e.id))

    #  an admin user can change the moderators moderating categroies
    if hasattr(current_user,'moderates'):
        if current_user.role == ADMIN:
            for c in Category.query.all():
                identity.provides.add(AddModerateNeed(c.id))
                #identity.provides.add(RemoveModerateNeed(c.id))
        for c in current_user.moderates:
            identity.provides.add(RemoveModerateNeed(c.id))
            

    # # a premium can add themselves to subscribe to categories 
    # if hasattr(current_user,'subscriptions'):
    #      if current_user.role != FREEUSER:
    #         for c in Category.query.all():
    #             identity.provides.add(AddSubscriptionNeed(c.id))
    #             identity.provides.add(RemoveSubscriptionNeed(c.id))

    #only a owner can promote 1. not themselves 2. not managers 3. attendants to managers
    if hasattr(current_user,'events'):
        for e in current_user.events:
            for u in e.attendants:
                if u.id != current_user.id: #TODO: can add owner to manager?
                    identity.provides.add(AddManageNeed(u.id))
            for u in e.managedBy:
                if u.id != current_user.id:
                    identity.provides.add(RemoveManageNeed(u.id))

    #manager/owner remove normal attadants
    if hasattr(current_user,'manages'):
        for e in current_user.manages:
            for u in e.attendants:
                if u not in e.managedBy and u.id != e.owner.id:
                    identity.provides.add(RemoveAttendNeed(u.id))

    # 1. manager/owner can accept requests: in requesters but not in attendants
    if hasattr(current_user,'manages'):
        for e in current_user.manages:
            for u in e.requesters:
                identity.provides.add(RemoveRequestNeed(u.id))

    #view the event's info
    if hasattr(current_user,'events'):
        for e in current_user.events:
            identity.provides.add(ViewManageEventNeed(e.id))
            identity.provides.add(EditEventCoreInfoNeed(e.id)) #edit event's core info

    if hasattr(current_user,'manages'):
        es = Event.query.all()
        for e in current_user.manages:
            identity.provides.add(ViewManageEventNeed(e.id))
            identity.provides.add(EditEventCoreInfoNeed(e.id)) #edit event's core info


    if hasattr(current_user,'attends'):
        es = Event.query.all()
        for e in es:
            if e in current_user.attends or not e.private:
                identity.provides.add(ViewAttendEventNeed(e.id))

    #view the category's info
    if hasattr(current_user,'moderates'):
        cs = Category.query.all()
        for c in cs:
            if c in current_user.moderates:
                identity.provides.add(ViewModerateCategoryNeed(c.id))


    #set owner,private
    if hasattr(current_user,'events'):
        for e in current_user.events:
            if e.private == None:
                print(e.id)
                identity.provides.add(SetEventInfoNeed(e.id))

    
    #new
    if hasattr(current_user,'manages'):
        for e in current_user.manages:
            # A user who is manager can send invites
            identity.provides.add(SendInviteNeed(e.id))

    #new: Users invited to a private event can read the event’s core information, its
    #attendants, and its managers.
    if hasattr(current_user,'invitations'):
        for i in current_user.invitations:
            identity.provides.add(ViewInviteEventNeed(i.event.id))

    if hasattr(current_user,'invitations'):
        for i in current_user.invitations: #i has already been invited to it
            identity.provides.add(JoinEventNeed(i.event.id))



# Use in case you need to initialize something
def init():
    # logging.basicConfig(level=logging.DEBUG,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # logger = logging.getLogger(__name__)
    pass




def viewCategory(category):
    #fix: private events cannot be read
    for e in category.events:
        e = viewEvent(e)
    if current_user.is_authenticated == False:
        category.subscribers = []
        return category
    try:
        permission = ViewModerateCategoryPermission(category.id)
        if permission.can():
            return category
    except:
        pass
    category.subscribers=[]
    return category

def setReadAttendEvent(event):
    event.requesters=[] #manager

def setReadNonEvent(event):
    event.attendants=[] #private+attendants
    event.managedBy =[] #private+attendants
    event.title = RESTRICTED
    event.description = RESTRICTED
    event.owner = RESTRICTED
    event.requesters=[] #manager

def setReadVisitEvent(event):
    event.attendants=[] #private+attendants
    event.managedBy =[] #private+attendants
    event.requesters=[] #manager

def viewEvent(event):
    viewPerson(event.owner) #fix: view the person indisde event's model
    #first check is_logined_in
    if current_user.is_authenticated == False:
        if event.private == False:
            setReadVisitEvent(event)
        else:
            setReadNonEvent(event)
        return event
    permission = ViewManageEventPermission(event.id)
    if permission.can():
        return event
    # except:
    #     pass
    permission = ViewAttendEventPermission(event.id)
    if permission.can():
        setReadAttendEvent(event)
        return event
    # except:
    #     pass   
    #new
    permission = ViewInviteEventPermission(event.id)
    if permission.can():
        setReadAttendEvent(event)
        return event
    setReadNonEvent(event)
    return event

def setReadPerson(user):
    user.password = RESTRICTED
    user.events=[]
    user.manages=[]
    user.attends=[]
    user.requests=[]
    user.subscriptions=[]

def setVisitorReadPerson(user):
    user.name = RESTRICTED
    user.surname = RESTRICTED
    user.username = RESTRICTED
    user.role = RESTRICTED
    user.password = RESTRICTED
    user.events=[]
    user.manages=[]
    user.attends=[]
    user.requests=[]
    user.subscriptions=[]

def viewPerson(user):
    if current_user.is_authenticated == False:
        setVisitorReadPerson(user)
        return user
    if current_user.id == user.id:
        return user
    setReadPerson(user)
    return user

#TEST 1
# read user's own info
def main():
    user = PersonDTO.copy(current_user) 
    return {'user' : user}

#TEST 2
# new
@login_required
def profile():
    user = PersonDTO.copy(current_user)
    for e in user.manages: 
        e.owner = PersonDTO.copy(Event.query.get(e.id).owner)
        viewPerson(e.owner)
        viewEvent(e)
    for e in user.attends:
        e.owner = PersonDTO.copy(Event.query.get(e.id).owner)
        viewPerson(e.owner)
        viewEvent(e)
    subs = CategoryDTO.copies(current_user.subscriptions)
    for s in subs:
        viewCategory(s)
        for e in s.events: #show categories and their subscriptions
            e.owner = PersonDTO.copy(Event.query.get(e.id).owner)
            viewPerson(e.owner)
            viewEvent(e)
    
    invs = InviteDTO.copies(current_user.invitations)
    for i in invs:
        #viewInvite
        e = i.event
        e.owner = PersonDTO.copy(Event.query.get(e.id).owner)
        viewPerson(e.owner)
        viewEvent(e)
        viewPerson(i.invitedBy)
        viewPerson(i.invitee)
    return {'user' : user, 'subs' : subs,'invitations':invs}

#TEST 3
#read events/categories' info
def events():   
    events = EventDTO.copies(Event.query.all())
    for e in events:
        e = viewEvent(e)
    categories = CategoryDTO.copies(Category.query.all())
    for c in categories:
        c = viewCategory(c)
    return {'events' : events, 'categories' : categories}

#TEST 4
def users():
    users = PersonDTO.copies(Person.query.all())
    for u in users:
        u = viewPerson(u)
    return {'users' : users}

#TEST 5
def user(id):
    user = PersonDTO.copy(Person.query.get(id))
    user = viewPerson(user)
    roles = RoleDTO.copies(Role.query.all()) 
    return {'user' : user, 'roles' : roles}

#TEST 6 
#read one event info
def view_event(id):
    event = EventDTO.copy(Event.query.get(id))
    event = viewEvent(event)
    return {'event' : event}

#TEST 7
def categories():
    categories = CategoryDTO.copies(Category.query.all())
    for c in categories:
        c = viewCategory(c)
    return {'categories' : categories}

#TEST 8 
def view_category(id):
    category = CategoryDTO.copy(Category.query.get(id))
    category = viewCategory(category)
    #fix: DTO inside category
    for e in category.events:
        e.owner = PersonDTO.copy(Event.query.get(e.id).owner)
        viewPerson(e.owner)
        viewEvent(e)
    return {'category' : category}


#TEST 9
@login_required
def create_category():
    name = request.form["name"]
    try:
        if name != None:
            try:
                # permission = Permission(RoleNeed('ADMIN'))
                if admin.can():
                    category = Category(name=name)
                    db.session.add(category)
                    db.session.commit()
                    return Response({"success":"yes"})
                else:
                    raise SecurityException("You are not not allowed to created a category: Not an admin")
            except SecurityException as se:
                raise SecurityException("You are not not allowed to created a category") 
    except: 
        raise SecurityException("You are not not allowed to created a category: parameters missing")
 

#TEST 10
#did not check None values
#TODO: the test, categories' sequence cannot be gauranteed
@login_required
def create_event():
    title = request.form["title"]
    description = request.form["description"]
    private = "private" in request.form
    owner = current_user
    categories = request.form.getlist("categories")
    categories = [Category.query.get(int(c)) for c in categories]
    try:
        if isinstance(private, bool) and title != None:
            try:
                permission = (freeuser.can() and not private) or admin.can() or premiumuser.can() or moderator.can()
                if permission:
                    event = Event(title=title,
                                    description=description,
                                    private=private,
                                    owner=owner,
                                    categories=categories)
                    if owner is not None: 
                        event.managedBy.append(owner)
                        event.attendants.append(owner)
                    db.session.add(event)
                    db.session.commit()
                    return Response("Success: You created an event")
                else:
                    raise SecurityException("You are not not allowed to created an event: not an admin") 
            except SecurityException as se:
                raise SecurityException("You are not not allowed to created an event") 
    except: 
        raise SecurityException("You are not not allowed to created an event: parameters missing")
 


#TEST 11
# can you only change one item? Some are forbidden and some are not. 
# NO. it is not allowed by HTTP request. 
@login_required
def update_event():
    id = request.form["id"]
    event = Event.query.get(id)
    #
    title = request.form["title"]
    description = request.form["description"]
    private = "private" in request.form #only owner: but private is always a value
    categories = request.form.getlist("categories")
    categories = [Category.query.get(c) for c in categories]
    changed = False
    try:
        if event != None:
            try:
                core_check = EditEventCoreInfoPermission(int(id))
                owner_check = SetEventInfoPermission(int(id))
                if core_check.can() or owner_check.can():
                    if title != None:
                        event.title = title
                        changed = True
                    if description != None:
                        event.description = description
                        changed = True
                    if categories != None: 
                        event.categories = categories 
                        changed = True
                if owner_check.can():
                    if not(freeuser.can() and private):
                        event.private = private
                        changed = True
                db.session.commit()
                if not changed:
                    raise SecurityException("You are not not allowed to updated an event: no inputs")
                return id
            except SecurityException as se:
                raise SecurityException("You are not not allowed to updated an event") 
    except: 
        raise SecurityException("You are not not allowed to updated an event: parameters missing")

#TEST 12
@login_required
def update_user():
    id = request.form["id"]
    name = request.form["name"]
    surname = request.form["surname"]
    role = request.form["role"]
    user = Person.query.get(id)
    role = Role.query.filter_by(name=role).first()

    changed = False
    try:
        if user != None:
            try:
                self_check = (current_user.id == int(id))
                if self_check and name != None: 
                    user.name = name
                    changed = True
                if self_check and surname != None:
                    user.surname = surname
                    changed = True

                only_role = user.surname == surname and user.name == name
                if admin.can() and only_role and role != None: #QUESION:???
                    user.role = role
                    changed = True
                db.session.commit()
                if not changed:
                    raise SecurityException("You are not not allowed to updated an event: ")
                return id
            except SecurityException as se:
                raise SecurityException("You are not not allowed to updated an event") 
    except: 
        raise SecurityException("You are not not allowed to updated an event: parameters missing")


#TEST 13
@login_required
def update_category():
    id = request.form["id"]
    category = Category.query.get(id)
    name = request.form["name"]
    try:
        if category != None:
            try:
                if name != None and admin.can():
                    category.name = name
                    db.session.commit()
                else:
                    raise SecurityException("You are not not allowed to updated a category: not an admin")
                return id
            except SecurityException as se:
                raise SecurityException("You are not not allowed to updated a category") 
    except: 
        raise SecurityException("You are not not allowed to updated a category: parameters missing")


#TEST 14
#edit_category is the index for editing attributes in category
@login_required
def edit_category(id):
    cat = Category.query.get(id)
    category = CategoryDTO.copy(cat)
    
    candidates = PersonDTO.copies(cat.candidates) #candidates are not their moderators
    for c in candidates:
        c = viewPerson(c)
    category = viewCategory(category)
    return {'category' : category, 'candidates' : candidates}

#TEST 15
#edit_event is the index for updating attributes in event
@login_required
def edit_event(id):
    event = EventDTO.copy(Event.query.get(id))
    event = viewEvent(event)
    categories = CategoryDTO.copies(Category.query.all())
    for c in categories:
        c = viewCategory(c)
    return {'event' : event, 'categories' : categories}

#TEST 16
#new
@login_required
def manage_event(id):
    event = EventDTO.copy(Event.query.get(id))
    event = viewEvent(event)

    #TODO: how to get all invitee's unique names?
    invs = set()
    for i in Event.query.get(id).invitations:
        invs.add(i.invitee)

    invitees = PersonDTO.copies(invs)
    for i in invitees:
        viewPerson(i)
    return {'event' : event,'invitees':invitees}





#TEST 17
# add to requests
#free user can join a public, preimum& others can join private

# new: if a user has been invited to an event, they cannot request to join the event.
@login_required
def join(id):
    event = Event.query.get(id)
    user = Person.query.get(current_user.id)
    try:
        if event != None:
            try:
                permission = not(freeuser.can() and event.private)
                not_invited = not(JoinEventPermission(id))
                if permission and not_invited and user not in event.requesters:
                        event.requesters.append(user)
                        db.session.commit()
                        return Response("Success: You sent a request to join the event")
                else:
                    raise SecurityException("You are not not allowed to sent a request to join the event: Not an admin")
            except SecurityException as se:
                raise SecurityException("You are not not allowed to sent a request to join the event") 
    except: 
        raise SecurityException("You are not not allowed to send a request to join the event: parameters missing")


#TEST 18
#you CANNOT user current_user(dto) directly.
@login_required
def leave(id):
    event = Event.query.get(id)
    user = Person.query.get(current_user.id) #IMPORTANT!
    try:
        if event != None:
            try:
                permission = LeaveAttendPermission(id)
                if permission.can() and user in event.attendants:
                    event.attendants.remove(user)
                    db.session.commit()
                    return Response("Success: You left the event")
                else:
                    raise SecurityException("You are not not allowed to leave the event: Not an admin")
            except SecurityException as se:
                raise SecurityException("You are not not allowed to leave the event") 
    except: 
        raise SecurityException("You are not not allowed to leave the event: parameters missing")


#TEST 19
#1. manager remove their events
#2. moderator(mod and admin) can remove their event from category
@login_required
def remove_category(id,c):
    event = Event.query.get(id)
    category = Category.query.get(c)
    try:
        if category != None and event != None:
            try:
                per2 = RemoveCategoryPermission(id)
                per1 = RemoveModeratorCategoryPermission(id)
                role_check = moderator.can() or admin.can()
                if (per2.can() or (per1.can() and role_check)) \
                    and event in category.events:
                        category.events.remove(event)
                        db.session.commit()
                        print(per1.can())
                        print(per2.can())
                        print(role_check)
                        return Response("Success: You removed the category from the event")
                else:
                    print(per1.can())
                    print(per2.can())
                    print(role_check)
                    raise SecurityException("You are not not allowed to removed the category from the event: permission denied") 
            except SecurityException as se:
                raise SecurityException("You are not not allowed to removed the category from the event") 
    except: 
        raise SecurityException("You are not not allowed to removed the category from the event: parameters missing")


#TEST 20
# 1. an admin user can change the moderators moderating categroies
@login_required
def add_moderator(id,c):
    user = Person.query.get(id)
    category = Category.query.get(c)
    try:
        if category != None and user != None:
            try:
                if admin.can() and user not in category.moderators:
                        category.moderators.append(user)
                        db.session.commit()
                        return Response("Success: You added the moderator")
                else:
                    raise SecurityException("You are not not allowed to add the moderator: Not an admin")
            except SecurityException as se:
                raise SecurityException("You are not not allowed to add the moderator") 
    except: 
        raise SecurityException("You are not not allowed to add the moderator: parameters missing")


#TEST 21
# an admin can remove moderators from categroies
@login_required
def remove_moderator(id,c): #QUESTION:test moderator 72
    user = Person.query.get(id)
    category = Category.query.get(c)
    try:
        if category != None and user != None:
            try:
                permission = RemoveModeratePermission(c).can() and current_user.id == id
                if (admin.can() or permission) and user in category.moderators:
                        category.moderators.remove(user)
                        db.session.commit()
                        return Response("Success: You removed the moderator")
                else:
                    raise SecurityException("You are not not allowed to remove the moderator: Not an admin")
            except SecurityException as se:
                raise SecurityException("You are not not allowed to remove the moderator") 
    except: 
        raise SecurityException("You are not not allowed to remove the moderator: parameters missing")



#TEST 22
# a premium can add themselves to subscribe to categories 
@login_required
def subscribe(id):
    category = Category.query.get(id)
    user = Person.query.get(current_user.id)
    try:
        if category != None:
            try:
                permission = admin.can() or moderator.can() or premiumuser.can()
                if permission and category not in user.subscriptions:
                        user.subscriptions.append(category)
                        db.session.commit()
                        return Response("Success: You subscribed to the category")
                else:
                    raise SecurityException("You are not not allowed to subscribe to the category: Not an admin")
            except SecurityException as se:
                raise SecurityException("You are not not allowed to subscribe to the category") 
    except: 
        raise SecurityException("You are not not allowed to subscribe to the category: parameters missing")


#TEST 23
@login_required
def unsubscribe(id):
    category = Category.query.get(id)
    user = Person.query.get(current_user.id)
    try:
        if category != None:
            try:
                permission = admin.can() or moderator.can() or premiumuser.can()
                if permission and category in user.subscriptions:
                        user.subscriptions.remove(category)
                        db.session.commit()
                        return Response("Success: You unsubscribed to the category")
                else:
                    raise SecurityException("You are not not allowed to unsubscribe to the category: Not an admin")
            except SecurityException as se:
                raise SecurityException("You are not not allowed to unsubscribe to the category") 
    except: 
        raise SecurityException("You are not not allowed to unsubscribe to the category: parameters missing")


   
#TEST 24
#only a owner can promote 1. not themselves 2. not managers 3. attendants to managers
@login_required
def promote_manager(id,e):
    user = Person.query.get(id)
    event = Event.query.get(e)
    try:
        if user != None and event != None:
            try:
                permission = AddManagePermission(id)
                if permission.can() and user not in event.managedBy:
                        event.managedBy.append(user)
                        db.session.commit()
                        return Response("Success: You promoted a managedBy")
                else:
                    raise SecurityException("You are not not allowed to promote a managedBy: Not an admin")
            except SecurityException as se:
                raise SecurityException("You are not not allowed to promote a managedBy") 
    except: 
        raise SecurityException("You are not not allowed to promote a managedBy: parameters missing")


#TEST 25
#only an owner can demote managedBy (except for owner himself)
@login_required
def demote_manager(id,e):
    user = Person.query.get(id)
    event = Event.query.get(e)
    # if user in event.managedBy:
    #     event.managedBy.remove(user)
    #     db.session.commit()
    #     user = Person.query.get(id) 
    try:
        if user != None and event != None:
            try:
                permission = RemoveManagePermission(id)
                if permission.can() and user in event.managedBy:
                        event.managedBy.remove(user)
                        db.session.commit()
                        return Response("Success: You demoted a managedBy")
                else:
                    raise SecurityException("You are not not allowed to demote a managedBy: Not an admin")
            except SecurityException as se:
                raise SecurityException("You are not not allowed to demote a managedBy") 
    except: 
        raise SecurityException("You are not not allowed to demote a managedBy: parameters missing")



#TEST 26
#manager/owner remove normal attadants
@login_required
def remove_attendee(id,e):
    user = Person.query.get(id)
    event = Event.query.get(e)
    try:
        if user != None and event != None:
            try:
                permission = RemoveAttendPermission(id)
                print(permission)
                print(permission.can())
                if permission.can() and user in event.attendants:
                        print("what")
                        event.attendants.remove(user)
                        db.session.commit()
                        return Response("Success: You removed an attendant")
                else:
                    raise SecurityException("You are not not allowed to remove an attendant: Not an admin")
            except SecurityException as se:
                raise SecurityException("You are not not allowed to remove an attendant") 
    except: 
        raise SecurityException("You are not not allowed to remove an attendant: parameters missing")



#TEST 27
# 1. manager/owner can accept requests
@login_required
def accept_request(id,e):
    user = Person.query.get(id)
    event = Event.query.get(e)
    try:
        if user != None and event != None:
            try:
                permission = RemoveRequestPermission(id)
                if permission.can() and user not in event.attendants and user in event.requesters:
                        event.attendants.append(user)
                        event.requesters.remove(user)
                        db.session.commit()
                        return Response("Success: You accepted a request to join")
                else:
                    raise SecurityException("You are not not allowed to reject a request to join: Not an admin")
            except SecurityException as se:
                raise SecurityException("YYou are not not allowed to reject a request to join") 
    except: 
        raise SecurityException("You are not not allowed to reject a request to join: parameters missing")


#TEST 28
# 1. only manager can accept or deny requests
@login_required
def reject_request(id,e):
    user = Person.query.get(id)
    event = Event.query.get(e)
    try:
        if user != None and event != None:
            try:
                permission = RemoveRequestPermission(id)
                if permission.can() and user in event.requesters:
                        event.requesters.remove(user)
                        db.session.commit()
                        return Response("Success: You rejected a request")
                else:
                    raise SecurityException("You are not reject a request: Not an admin")
            except SecurityException as se:
                raise SecurityException("You are not reject a request: Not an admin") 
    except: 
        raise SecurityException("You are not reject a request: parameters missing")


#current user send invitation to id
# Only event managers can associate invitations to events they manage. 
# Only event managers can invite users as invitees in the invitation.

# A user who already requested to join an event cannot be invited to it.
@login_required
def send_invite(id,e):
    user = Person.query.get(id)
    event = Event.query.get(e)
    invitedBy = Person.query.get(current_user.id)
    try:
        if user != None and event != None:
            try:
                is_manager = SendInvitePermission(e) 
                not_requester = not(user in event.requesters)

                print(is_manager)
                print(not_requester)

                if is_manager.can() and not_requester:
                        invite = Invite(event = event, 
                            invitee = user, 
                            invitedBy = invitedBy)
                        db.session.add(invite)
                        db.session.commit()
                        return Response("Success")
                else:
                    raise SecurityException("You are not an admin")
            except SecurityException as se:
                raise SecurityException("You are not an admin") 
    except: 
        raise SecurityException("You are not an admin")


#An invited user can accept or decline the invitation 
# (in both cases, the invitation is deleted).
@login_required
def accept_invitation(id):
    invite = Invite.query.get(id)
    try:
        if invite != None:
            try:
                permission = invite.invitee.id == current_user.id
                if permission:
                    db.session.delete(invite)
                    db.session.commit()
                    return Response("Success")
                else:
                    raise SecurityException("You are not an admin")
            except SecurityException as se:
                raise SecurityException("You are not an admin") 
    except: 
        raise SecurityException("You are not an admin")



#An invited user can accept or decline the invitation 
# (in both cases, the invitation is deleted).
@login_required
def decline_invitation(id):
    invite = Invite.query.get(id)
    try:
        if invite != None:
            try:
                permission = invite.invitee.id == current_user.id

                if permission:
                    db.session.delete(invite)
                    db.session.commit()
                    return Response("Success")
                else:
                    raise SecurityException("You are not an admin")
            except SecurityException as se:
                raise SecurityException("You are not an admin") 
    except: 
        raise SecurityException("You are not an admin")


#TODO: no? Any user can add themselves as attendant to an event, if they have been invited to the event.