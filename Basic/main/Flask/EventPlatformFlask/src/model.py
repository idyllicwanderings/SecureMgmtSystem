from flask_sqlalchemy import SQLAlchemy
from flask_user import UserMixin


db = SQLAlchemy()


# VISITOR = "VISITOR" # corresponds to current_user.is_authenticated == False
FREEUSER = "FREEUSER"
PREMIUMUSER = "PREMIUMUSER"
MODERATOR = "MODERATOR"
ADMIN = "ADMIN"
# NONE and SYSTEM roles are not needed explicitly


# Associations
mods = db.Table('mods',
        db.Column('category_id', db.Integer, db.ForeignKey('category.id'), nullable=False),
        db.Column('person_id', db.Integer, db.ForeignKey('person.id'), nullable=False)
)

subs = db.Table('subs',
        db.Column('category_id', db.Integer, db.ForeignKey('category.id'), nullable=False),
        db.Column('person_id', db.Integer, db.ForeignKey('person.id'), nullable=False)
)

evts = db.Table('evts',
        db.Column('event_id', db.Integer, db.ForeignKey('event.id'), nullable=False),
        db.Column('category_id', db.Integer, db.ForeignKey('category.id'), nullable=False)
)

atts = db.Table('atts',
        db.Column('person_id', db.Integer, db.ForeignKey('person.id'), nullable=False),
        db.Column('event_id', db.Integer, db.ForeignKey('event.id'), nullable=False)
)

mans = db.Table('mans',
        db.Column('person_id', db.Integer, db.ForeignKey('person.id'), nullable=False),
        db.Column('event_id', db.Integer, db.ForeignKey('event.id'), nullable=False)
)

reqs = db.Table('reqs',
        db.Column('person_id', db.Integer, db.ForeignKey('person.id'), nullable=False),
        db.Column('event_id', db.Integer, db.ForeignKey('event.id'), nullable=False)
)

# Entities
class Person(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')
    roles = db.relationship('Role', secondary='user_roles')
    
    name = db.Column(db.String(100, collation='NOCASE'))
    surname = db.Column(db.String(100, collation='NOCASE'))
    username = db.Column(db.String(100, collation='NOCASE'), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, server_default='')

    events = db.relationship('Event', backref='owner')
    manages = db.relationship('Event', secondary=mans, lazy='subquery', backref='managedBy')
    attends = db.relationship('Event', secondary=atts, lazy='subquery', backref='attendants')
    requests = db.relationship('Event', secondary=reqs, lazy='subquery', backref='requesters')

    # invitations = db.relationship('Invite', back_populates='invitee')
    # invites = db.relationship('Invite', back_populates='invitedBy')

    @property
    def role(self):
        return self.roles[0]
    @role.setter
    def role(self,r):
        self.roles = [r]
    @property
    def fullname(self):
        return f'{self.name} {self.surname}' 
    @property
    def managed(self):
        return list(set(self.events + self.manages))
    @property
    def is_authenticated(self):
        return True


class Invite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invitee_id = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=False)
    invitee = db.relationship('Person', foreign_keys=invitee_id,
 backref='invitations')
    invitedBy_id = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=False)
    invitedBy = db.relationship('Person', foreign_keys=invitedBy_id, backref='invites')
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    event = db.relationship('Event', foreign_keys=event_id, backref='invitations')


class Role(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)

class UserRoles(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('person.id'), unique=True)
    role_id = db.Column(db.Integer(), db.ForeignKey('role.id'))

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500))
    description = db.Column(db.String(2000))
    private = db.Column(db.Boolean)

    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))

    # invitations = db.relationship('Invite', back_populates='event')


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

    subscribers = db.relationship('Person', secondary=subs, lazy='subquery',
                                  backref=db.backref('subscriptions', lazy=True))
    moderators = db.relationship('Person', secondary=mods, lazy='subquery',
                                 backref=db.backref('moderates', lazy=True))
    events = db.relationship('Event', secondary=evts, lazy='subquery',
                             backref=db.backref('categories', lazy=True))

    @property
    def candidates(self):
        mr = Role.query.filter_by(name=MODERATOR).first()
        all = [m for m in Person.query.all() if mr in m.roles]
        return list(set(all) - set(self.moderators)) 

