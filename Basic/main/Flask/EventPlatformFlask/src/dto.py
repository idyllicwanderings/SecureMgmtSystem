"""Data Transfer Object (DTO)

This module defines a class of DTOs for every data
model class, e.g., PersonDTO is a DTO class for
the Person data model class. 

DTOs are used to build a subset of the data model, 
which is to be passed to a web page template and 
rendered/shown to a user. 

By building and passing a DTO instead of a data 
model class we ensure that the web page template 
can only use limited information and display it 
to the user.

Each DTO class has a constructor with key-value 
parameters, as well as a "copy" method.
The copy method takes an object of the 
correspoding data model class as a parameter and 
instantiates its DTO. Copy method also instantiates 
DTOs of the data model objects directly associated with
object passed as the parameter. Associations ends 
of the passed object are complete w.r.t. their data model
counterparts, whereas other instantiated DTO's may not
have complete association ends after copy terminates.

In other words copy(obj: Person) -> PersonDTO
instantiates DTOs coresponsing to the subset of the 
data model centered around obj.

For example, suppose we have the following data model 
objects 

p1: Person 
    attendants <------> attends e1: Event
                                    events <------> categories c1: Categories

PersonDTO.copy(p1) produces

p1': PersonDTO
     attendants <------> attends e1': EventDTO
                                      events = []

After creating DTOs (via constructors or the copy method)
one may assign the RESTRICTED object (see below) to its 
attributes or 0-1 association ends. Also, a 0-* association
end can be filtered, or restricted completely by assigning
[] to it.

"""
from flask_login import AnonymousUserMixin
from collections.abc import Iterator

class Restrict(Iterator):
    def __iter__(self):
        return [].__iter__()
    def __next__(self):
        return [].__next__()
    def __len__(self) -> int:
        return 0
    def __repr__(self):
        return "RESTRICTED"
    def __getattr__(self,attr):
        return self
    def __call__(self, *a, **b): 
        return self
        
RESTRICTED = Restrict()
"""RESTRICTED Object

Whenever some information (e.g., an attribute value) 
may not be used by a web page template, one can assign
the RESTRICTED object to it. 

"""

def _clear_cache():
    PersonDTO._cache = {}
    RoleDTO._cache = {}
    EventDTO._cache = {}
    CategoryDTO._cache = {}

class PersonDTO:
    _cache = {}

    def _clone(clone):
        if not clone.id in PersonDTO._cache:
            PersonDTO._cache[clone.id] = PersonDTO(clone.id,
                                                name=clone.name,
                                                surname=clone.surname,
                                                username=clone.username,
                                                password=clone.password) 
        return PersonDTO._cache[clone.id]
       

    def _clones(clones):
        return list(map(lambda o: PersonDTO._clone(o),clones))

    def copy(copy, bulk=False):
        if isinstance(copy,AnonymousUserMixin):
            return copy
        else:
            r = PersonDTO(copy.id,
                        name=copy.name,
                        surname=copy.surname,
                        username=copy.username,
                        password=copy.password,
                        roles=RoleDTO._clones(copy.roles),
                        events=EventDTO._clones(copy.events),
                        manages=EventDTO._clones(copy.manages),
                        attends=EventDTO._clones(copy.attends),
                        requests=EventDTO._clones(copy.requests),
                        subscriptions=CategoryDTO._clones(copy.subscriptions),
                        moderates=CategoryDTO._clones(copy.moderates),
                        invitations=InviteDTO._clones(copy.invitations),
                        invites=InviteDTO._clones(copy.invites))
            if not bulk:
                    _clear_cache()
            return r

    def copies(copies):
        r = list(map(lambda o: PersonDTO.copy(o,bulk=True),copies))
        _clear_cache()
        return r

    def __init__(self,id,
                name=RESTRICTED, 
                surname=RESTRICTED, 
                username=RESTRICTED, 
                password=RESTRICTED,
                roles=[RESTRICTED],
                events=[],
                manages=[],
                attends=[],
                requests=[],
                subscriptions=[],
                moderates=[],
                invitations=[],
                invites=[]):
        self.id=id
        self.name=name
        self.surname=surname
        self.username=username
        self.password=password
        self.roles=list(set(roles))
        self.events=list(set(events))
        for e in events:
                e.owner=self
        self.manages=list(set(manages))
        for e in manages:
                if self not in e.managedBy:
                        e.managedBy.append(self)
        self.attends=list(set(attends))
        for e in attends:
                if self not in e.attendants:
                        e.attendants.append(self)
        self.requests=list(set(requests))
        for e in requests:
                if self not in e.requesters:
                        e.requesters.append(self)
        self.subscriptions=list(set(subscriptions))
        for c in subscriptions:
                if self not in c.subscribers:
                        c.subscribers.append(self)
        self.moderates=list(set(moderates))
        for c in moderates:
                if self not in c.moderators:
                        c.moderators.append(self)
        self.invitations=list(set(invitations))
        for i in invitations:
            i.invitee=self
        self.invites=list(set(invites))
        for i in invites:
            i.invitedBy=self
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

class RoleDTO:
    _cache = {}

    def _clone(clone):
        if not clone.id in RoleDTO._cache:
            RoleDTO._cache[clone.id] = RoleDTO(clone.id,clone.name) 
        return RoleDTO._cache[clone.id]
       

    def _clones(clones):
        return list(map(lambda o: RoleDTO._clone(o),clones))

    def copy(copy, bulk=False):
        r = RoleDTO(copy.id,copy.name)
        if not bulk:
            _clear_cache()
        return r

    def copies(copies):
        return list(map(lambda o: RoleDTO.copy(o, bulk=True),copies))

    def __init__(self, id, name):
        self.id=id
        self.name=name
           

class EventDTO:
    _cache = {}

    def _clone(clone):
        if not clone.id in EventDTO._cache:
            EventDTO._cache[clone.id] = EventDTO(clone.id,
                                                title=clone.title,
                                                description=clone.description,
                                                private=clone.private) 
        return EventDTO._cache[clone.id]
       

    def _clones(clones):
        return list(map(lambda o: EventDTO._clone(o),clones))


    def copy(copy, bulk=False):
        r = EventDTO(copy.id,
                     title=copy.title,
                     description=copy.description,
                     private=copy.private,
                     owner=PersonDTO._clone(copy.owner),
                     categories=CategoryDTO._clones(copy.categories),
                     managedBy=PersonDTO._clones(copy.managedBy),
                     attendants=PersonDTO._clones(copy.attendants),
                     requesters=PersonDTO._clones(copy.requesters),
                     invitations=InviteDTO._clones(copy.invitations))
        if not bulk:
                _clear_cache()
        return r

    def copies(copies):
        r = list(map(lambda o: EventDTO.copy(o,bulk=True),copies))
        _clear_cache()
        return r

    def __init__(self,id,
                title=RESTRICTED,
                description=RESTRICTED,
                private=RESTRICTED,
                owner=RESTRICTED,
                categories=[],
                managedBy=[],
                attendants=[],
                requesters=[],
                invitations=[]):
        self.id=id
        self.title=title
        self.description=description
        self.private=private
        self.owner=owner
        # add
        if owner != RESTRICTED:
            if self not in owner.events:
                owner.events.append(self)
        self.categories=list(set(categories))
        for c in categories:
                if self not in c.events:
                        c.events.append(self)
        self.managedBy=list(set(managedBy))
        for u in managedBy:
                if self not in u.manages:
                        u.manages.append(self)
        self.attendants=list(set(attendants))
        for u in attendants:
                if self not in u.attends:
                        u.attends.append(self)
        self.requesters=list(set(requesters))
        for u in requesters:
                if self not in u.requests:
                        u.requests.append(self)
        self.invitations=list(set(invitations))
        for i in invitations:
            i.event=self

class CategoryDTO:
    _cache = {}

    def _clone(clone):
        if not clone.id in CategoryDTO._cache:
            CategoryDTO._cache[clone.id] = CategoryDTO(clone.id,
                                                name=clone.name) 
        return CategoryDTO._cache[clone.id]
       

    def _clones(clones):
        return list(map(lambda o: CategoryDTO._clone(o),clones))

    def copy(copy, bulk=False):
        r = CategoryDTO(copy.id,
                     name=copy.name,
                     subscribers=PersonDTO._clones(copy.subscribers),
                     moderators=PersonDTO._clones(copy.moderators),
                     events=EventDTO._clones(copy.events))
        if not bulk:
                _clear_cache()
        return r

    def copies(copies):
        r = list(map(lambda o: CategoryDTO.copy(o,bulk=True),copies))
        _clear_cache()
        return r

    def __init__(self,id,
                name=RESTRICTED,
                subscribers=[],
                moderators=[],
                events=[]):
        self.id=id
        self.name=name
        self.subscribers=list(set(subscribers))
        for u in subscribers:
                if self not in u.subscriptions:
                        u.subscriptions.append(self)
        self.moderators=list(set(moderators))
        for u in moderators:
                if self not in u.moderates:
                        u.moderates.append(self)
        self.events=list(set(events))
        for e in events:
                if self not in e.categories:
                        e.categories.append(self)



class InviteDTO:
    _cache = {}

    def _clone(clone):
        if not clone.id in InviteDTO._cache:
            InviteDTO._cache[clone.id] = InviteDTO(clone.id) 
        return InviteDTO._cache[clone.id]
       

    def _clones(clones):
        return list(map(lambda o: InviteDTO._clone(o),clones))

    def copy(copy, bulk=False):
        r = InviteDTO(copy.id,
                     event=EventDTO._clone(copy.event),
                     invitee=PersonDTO._clone(copy.invitee),
                     invitedBy=PersonDTO._clone(copy.invitedBy))
        if not bulk:
                _clear_cache()
        return r

    def copies(copies):
        r = list(map(lambda o: InviteDTO.copy(o,bulk=True),copies))
        _clear_cache()
        return r

    def __init__(self,id,
                event=RESTRICTED,
                invitee=RESTRICTED,
                invitedBy=RESTRICTED):
        self.id=id
        self.event=event
        if event != RESTRICTED:
            if self not in event.invitations:
                event.invitations.append(self)
        self.invitee=invitee
        if invitee != RESTRICTED:
            if self not in invitee.invitations:
                invitee.invitations.append(self)
        self.invitedBy=invitedBy
        if invitedBy != RESTRICTED:
            if self not in invitedBy.invites:
                invitedBy.invites.append(self)




