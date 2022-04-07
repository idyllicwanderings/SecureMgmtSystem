from ast import Or
from unicodedata import category
from flask import current_app, Response
from flask_login import login_user, AnonymousUserMixin
from flask_user import current_user
from model import db
from project import *
from dto import RESTRICTED

# This test suite is dedicated for visistors
# Tests that are applicable to VISITOR role.

def is_response(result):
    return type(result) == Response  

#Test Case	1	Create Person
# No test required as this is handle by Flask-User.

#Test Case	2	Update Person.username from null to smth
# No test required as this is handle by Flask-User.

#Test Case	3	Update Person.username from smth to smth'
# No test required as this is handle by Flask-User.

#Test Case	4	Update Person.password from null to smth
# No test required as this is handle by Flask-User.

#Test Case	5	Update Person.password from smth to smth'
# No test required as this is handle by Flask-User.

#Test Case	6	Update Person.role from null to null
# No test needed since a Person role should always be non-null.
# Testing this would require the initial configuration starts with a user with a None role 
# (which should be invalid configuration though)

#Test Case	7	Update Person.role from null to FREE
# No test needed since a Person role should always be non-null.
# Testing this would require the initial configuration starts with a user with a None role 
# (which should be invalid configuration though)

#Test Case	8	Update Person.role from null to NONE
# No test needed since a Person role should always be non-null.
# Testing this would require the initial configuration starts with a user with a None role 
# (which should be invalid configuration though)

#Test Case	9	Update Person.role from null to ADMIN
# No test needed since a Person role should always be non-null.
# Testing this would require the initial configuration starts with a user with a None role 
# (which should be invalid configuration though)

#Test Case	10	Update Person.role from FREE to null
# Not applicable

#Test Case	11	Update Person.role from FREE to NONE
# No test needed because we don't have NONE role in Flask

#Test Case	12	Update Person.role from FREE to PREMIUM
def test_case_12_VISITOR(app, request, user1, freeuserrole, premiumuserrole):
    with current_app.test_request_context(
        data={"id": user1.id, 
              "name": user1.name,
              "surname": user1.surname,
              "role": premiumuserrole.name}):
        # Scenario: a user user1 with FREEUSER role
        user1.role = freeuserrole
        db.session.add(user1)
        db.session.add(premiumuserrole)
        db.session.commit()
        # Test visitor accessing update_user()
        try:
            result = update_user()
        except SecurityException:
            assert True
        finally:
            assert user1.role.name == freeuserrole.name

#Test Case	13	Update Person.role from FREE to ADMIN
def test_case_13_VISITOR(app, request, user1, freeuserrole, adminrole):
    with current_app.test_request_context(
        data={"id": user1.id, 
              "name": user1.name,
              "surname": user1.surname,
              "role": adminrole.name}):
        # Scenario: a user user1 with FREEUSER role
        user1.role = freeuserrole
        db.session.add(user1)
        db.session.add(adminrole)
        db.session.commit()
        # Test visitor accessing update_user()
        try:
            result = update_user()
        except SecurityException:
            assert True
        finally:
            assert user1.role.name == freeuserrole.name

#Test Case	14	Read Person.username
def test_case_14_VISITOR(app, request, user1, freeuserrole):
    with current_app.test_request_context():
        # Scenario: a person user1 with FREEUSER role.
        user1.role = freeuserrole
        db.session.add(user1)
        db.session.commit()
        # Test visitor accessing user()
        try:
            result = user(user1.id)
            assert is_response(result) or \
                   result.get("user").username is RESTRICTED
        except SecurityException:
            assert True

#Test Case	15	Read Person.password
# No test needed because password is handled by Flask-User.

#Test Case	16	Read Person.role
def test_case_16_VISITOR(app, request, user1, freeuserrole):
    with current_app.test_request_context():
        # Scenario: a person user1 with FREEUSER role.
        user1.role = freeuserrole
        db.session.add(user1)
        db.session.commit()
        # Test visitor accessing user()
        try:
            result = user(user1.id)
            assert is_response(result) or \
                   result.get("user").role is RESTRICTED or \
                   result.get("user").role.name is RESTRICTED
        except SecurityException:
            assert True

#Test Case	17	Read Person.moderates
# Not applicable because there is no endpoint that discloses this information

#Test Case	18	Read Event.private
def test_case_18_VISITOR(app, request, user1, freeuserrole, publicevent1):
    with current_app.test_request_context():
        # Scenario: a person user1 with FREEUSER role.
        #           a public event owned by user1
        user1.role = freeuserrole
        db.session.add(user1)
        publicevent1.owner = user1 
        publicevent1.attendants.append(user1)
        publicevent1.managedBy.append(user1)
        db.session.add(publicevent1)
        db.session.commit()
        # Test visitor accessing view_event(): 
        try:
            result = view_event(publicevent1.id)
            assert is_response(result) or \
                   result.get("event").private == publicevent1.private
        except SecurityException:
            assert True

def test_case_18_VISITOR_1(app, request, user1, freeuserrole, publicevent1):
    with current_app.test_request_context():
        # Scenario: a person user1 with FREEUSER role.
        #           a public event owned by user1
        user1.role = freeuserrole
        db.session.add(user1)
        publicevent1.owner = user1 
        publicevent1.attendants.append(user1)
        publicevent1.managedBy.append(user1)
        db.session.add(publicevent1)
        db.session.commit()
        # Test visitor accessing edit_event()
        try:
            result = edit_event(publicevent1.id)
            assert is_response(result) or \
                   result.get("event").private == publicevent1.private
        except SecurityException:
            assert True

#Test Case	19	Read Event.categories
# Checking view_event
def test_case_19_VISITOR(app, request, user1, freeuserrole, publicevent1, category1):
    with current_app.test_request_context():
        # Scenario: a person user1 with FREEUSER role.
        #           a category category1
        #           a public event owned by user1, of category1
        user1.role = freeuserrole
        db.session.add(user1)
        publicevent1.owner = user1 
        publicevent1.attendants.append(user1)
        publicevent1.managedBy.append(user1)
        publicevent1.categories.append(category1)
        db.session.add(publicevent1)
        db.session.commit()
        # Test visitor accessing view_event(): 
        try:
            result = view_event(publicevent1.id)
            assert is_response(result) or \
                   (len(result.get("event").categories) == 1 and \
                    result.get("event").categories[0].name == category1.name)
        except SecurityException:
            assert True

#Test Case	20	Read Event.title of a public event
# Testing /events
def test_case_20_VISITOR(app, request, user1, freeuserrole, publicevent1):
    with current_app.test_request_context():
        # Scenario: a person user1 with FREEUSER role.
        #           a public event owned by user1
        user1.role = freeuserrole
        db.session.add(user1)
        publicevent1.owner = user1 
        publicevent1.attendants.append(user1)
        publicevent1.managedBy.append(user1)
        db.session.add(publicevent1)
        db.session.commit()
        # Test visitor accessing events():
        result = events()
        events_dto = result.get("events")
        assert len(events_dto) == 1
        assert events_dto[0].title == publicevent1.title

# Testing /profile: 
# no test needed because there is no user authenticated.


# Testing /view_event
def test_case_20_VISITOR_2(app, request, user1, freeuserrole, publicevent1):
    with current_app.test_request_context():
        # Scenario: a person user1 with FREEUSER role.
        #           a public event owned by user1
        user1.role = freeuserrole
        db.session.add(user1)
        publicevent1.owner = user1 
        publicevent1.attendants.append(user1)
        publicevent1.managedBy.append(user1)
        db.session.add(publicevent1)
        db.session.commit()
        # Test visitor accessing view_event(): 
        try:
            result = view_event(publicevent1.id)
            assert is_response(result) or \
                   result.get("event").title == publicevent1.title
        except SecurityException:
            assert True

# Test edit_event
def test_case_20_VISITOR_3(app, request, user1, freeuserrole, publicevent1):
    with current_app.test_request_context():
        # Scenario: a person user1 with FREEUSER role.
        #           a public event owned by user1
        user1.role = freeuserrole
        db.session.add(user1)
        publicevent1.owner = user1 
        publicevent1.attendants.append(user1)
        publicevent1.managedBy.append(user1)
        db.session.add(publicevent1)
        db.session.commit()
        # Test visitor accessing edit_event()
        try:
            result = edit_event(publicevent1.id)
            assert is_response(result) or \
                   result.get("event").title == publicevent1.title
        except SecurityException:
            assert True

# Test view_category
def test_case_20_VISITOR_4(app, request, user1, freeuserrole, publicevent1, category1):
    with current_app.test_request_context():
        # Scenario: a person user1 with FREEUSER role.
        #           a category category1
        #           a public event owned by user1, of category1
        user1.role = freeuserrole
        db.session.add(user1)
        publicevent1.owner = user1 
        publicevent1.attendants.append(user1)
        publicevent1.managedBy.append(user1)
        publicevent1.categories.append(category1)
        db.session.add(publicevent1)
        db.session.commit()
        # Test visitor accessing view_category()
        try:
            result = view_category(category1.id)
            assert is_response(result) or \
                   (len(result.get("category").events) == 1 and \
                    result.get("category").events[0].title == publicevent1.title)
        except SecurityException:
            assert True

#Test Case	21	Read Event.title of a private event
def test_case_21_VISITOR(app, request, user1, premiumuserrole, privateevent1):
    with current_app.test_request_context():
        # Scenario: a person user1 with PREMIUMUSER role.
        #           a private event owned by user1
        user1.role = premiumuserrole
        db.session.add(user1)
        privateevent1.owner = user1 
        privateevent1.attendants.append(user1)
        privateevent1.managedBy.append(user1)
        db.session.add(privateevent1)
        db.session.commit()
        # Test visitor accessing events():
        result = events()
        events_dto = result.get("events")
        assert len(events_dto) == 0 or \
               (len(events_dto) == 1 and \
                events_dto[0].title is RESTRICTED)

# Testing /profile: no test needed because there is no user authenticated.

# Testing /view_event
def test_case_21_VISITOR_1(app, request, user1, premiumuserrole, privateevent1):
    with current_app.test_request_context():
        # Scenario: a person user1 with PREMIUMUSER role.
        #           a private event owned by user1
        user1.role = premiumuserrole
        db.session.add(user1)
        privateevent1.owner = user1 
        privateevent1.attendants.append(user1)
        privateevent1.managedBy.append(user1)
        db.session.add(privateevent1)
        db.session.commit()
        # Test visitor accessing view_event(): 
        try:
            result = view_event(privateevent1.id)
            assert is_response(result) or \
                   result.get("event").title is RESTRICTED
        except SecurityException:
            assert True

# Test edit_event
def test_case_21_VISITOR_2(app, request, user1, premiumuserrole, privateevent1):
    with current_app.test_request_context():
        # Scenario: a person user1 with PREMIUMUSER role.
        #           a private event owned by user1
        user1.role = premiumuserrole
        db.session.add(user1)
        privateevent1.owner = user1 
        privateevent1.attendants.append(user1)
        privateevent1.managedBy.append(user1)
        db.session.add(privateevent1)
        db.session.commit()
        # Test visitor accessing edit_event()
        try:
            result = edit_event(privateevent1.id)
            assert is_response(result) or \
                   result.get("event").title is RESTRICTED
        except SecurityException:
            assert True

# Test view_category
def test_case_21_VISITOR_3(app, request, user1, premiumuserrole, privateevent1, category1):
    with current_app.test_request_context():
        # Scenario: a person user1 with FREEUSER role.
        #           a category category1
        #           a public event owned by user1, of category1
        user1.role = premiumuserrole
        db.session.add(user1)
        privateevent1.owner = user1 
        privateevent1.attendants.append(user1)
        privateevent1.managedBy.append(user1)
        privateevent1.categories.append(category1)
        db.session.add(privateevent1)
        db.session.commit()
        # Test visitor accessing view_category()
        try:
            result = view_category(category1.id)
            assert is_response(result) or \
                   len(result.get("category").events) == 0 or \
                   (len(result.get("category").events) == 1 and \
                    result.get("category").events[0].title is RESTRICTED)
        except SecurityException:
            assert True

#Test Case	22	Read Event.description of a public event
# Testing /view_event
def test_case_22_VISITOR(app, request, user1, freeuserrole, publicevent1):
    with current_app.test_request_context():
        # Scenario: a person user1 with FREEUSER role.
        #           a public event owned by user1
        user1.role = freeuserrole
        db.session.add(user1)
        publicevent1.owner = user1 
        publicevent1.attendants.append(user1)
        publicevent1.managedBy.append(user1)
        db.session.add(publicevent1)
        db.session.commit()
        # Test visitor accessing view_event(): 
        try:
            result = view_event(publicevent1.id)
            assert is_response(result) or \
                   result.get("event").description == publicevent1.description
        except SecurityException:
            assert True

# Test edit_event
def test_case_22_VISITOR_1(app, request, user1, freeuserrole, publicevent1):
    with current_app.test_request_context():
        # Scenario: a person user1 with FREEUSER role.
        #           a public event owned by user1
        user1.role = freeuserrole
        db.session.add(user1)
        publicevent1.owner = user1 
        publicevent1.attendants.append(user1)
        publicevent1.managedBy.append(user1)
        db.session.add(publicevent1)
        db.session.commit()
        # Test visitor accessing edit_event()
        try:
            result = edit_event(publicevent1.id)
            assert is_response(result) or \
                   result.get("event").description == publicevent1.description
        except SecurityException:
            assert True

#Test Case	23	Read Event.description of a private event
# Testing /view_event
def test_case_23_VISITOR(app, request, user1, premiumuserrole, privateevent1):
    with current_app.test_request_context():
        # Scenario: a person user1 with PREMIUMUSER role.
        #           a private event owned by user1
        user1.role = premiumuserrole
        db.session.add(user1)
        privateevent1.owner = user1 
        privateevent1.attendants.append(user1)
        privateevent1.managedBy.append(user1)
        db.session.add(privateevent1)
        db.session.commit()
        # Test visitor accessing view_event(): 
        try:
            result = view_event(privateevent1.id)
            assert is_response(result) or \
                   result.get("event").description is RESTRICTED
        except SecurityException:
            assert True

# Test edit_event
def test_case_23_VISITOR_1(app, request, user1, premiumuserrole, privateevent1):
    with current_app.test_request_context():
        # Scenario: a person user1 with PREMIUMUSER role.
        #           a private event owned by user1
        user1.role = premiumuserrole
        db.session.add(user1)
        privateevent1.owner = user1 
        privateevent1.attendants.append(user1)
        privateevent1.managedBy.append(user1)
        db.session.add(privateevent1)
        db.session.commit()
        # Test visitor accessing edit_event()
        try:
            result = edit_event(privateevent1.id)
            assert is_response(result) or \
                   result.get("event").description is RESTRICTED
        except SecurityException:
            assert True

#Test Case	24	Read Event.owner of a public event
# Test \events
def test_case_24_VISITOR(app, request, user1, freeuserrole, publicevent1):
    with current_app.test_request_context():
        # Scenario: a person user1 with FREEUSER role.
        #           a public event owned by user1
        user1.role = freeuserrole
        db.session.add(user1)
        publicevent1.owner = user1 
        publicevent1.attendants.append(user1)
        publicevent1.managedBy.append(user1)
        db.session.add(publicevent1)
        db.session.commit()
        # Test visitor accessing events():
        result = events()
        events_dto = result.get("events")
        assert len(events_dto) == 1
        assert events_dto[0].owner is RESTRICTED or \
               (events_dto[0].owner.name is RESTRICTED and \
                events_dto[0].owner.surname is RESTRICTED)

# Test \view_category
def test_case_24_VISITOR_1(app, request, user1, freeuserrole, publicevent1, category1):
    with current_app.test_request_context():
        # Scenario: a person user1 with FREEUSER role.
        #           a category category1
        #           a public event owned by user1, of category1
        user1.role = freeuserrole
        db.session.add(user1)
        publicevent1.owner = user1 
        publicevent1.attendants.append(user1)
        publicevent1.managedBy.append(user1)
        publicevent1.categories.append(category1)
        db.session.add(publicevent1)
        db.session.commit()
        # Test visitor accessing view_category()
        try:
            result = view_category(category1.id)
            assert is_response(result) or \
                   (len(result.get("category").events) == 1 and \
                    (result.get("category").events[0].owner is RESTRICTED or \
                     result.get("category").events[0].owner.name is RESTRICTED and \
                     result.get("category").events[0].owner.surname is RESTRICTED))
        except SecurityException:
            assert True

#Test Case	25	Read Event.owner of a private event
# Test \events
def test_case_25_VISITOR(app, request, user1, premiumuserrole, privateevent1):
    with current_app.test_request_context():
        # Scenario: a person user1 with PREMIUMUSER role.
        #           a private event owned by user1
        user1.role = premiumuserrole
        db.session.add(user1)
        privateevent1.owner = user1 
        privateevent1.attendants.append(user1)
        privateevent1.managedBy.append(user1)
        db.session.add(privateevent1)
        db.session.commit()
        # Test visitor accessing events():
        result = events()
        events_dto = result.get("events")
        assert len(events_dto) == 0 or \
               (len(events_dto) == 1 and \
                events_dto[0].owner is RESTRICTED or \
                (events_dto[0].owner.name is RESTRICTED and \
                 events_dto[0].owner.surname is RESTRICTED))

# Test view_category
def test_case_25_VISITOR_1(app, request, user1, premiumuserrole, privateevent1, category1):
    with current_app.test_request_context():
        # Scenario: a person user1 with PREMIUMUSER role.
        #           a category category1
        #           a private event owned by user1, of category1
        user1.role = premiumuserrole
        db.session.add(user1)
        privateevent1.owner = user1 
        privateevent1.attendants.append(user1)
        privateevent1.managedBy.append(user1)
        privateevent1.categories.append(category1)
        db.session.add(privateevent1)
        db.session.commit()
        # Test visitor accessing view_category()
        try:
            result = view_category(category1.id)
            assert is_response(result) or \
                   len(result.get("category").events) == 0 or \
                   (len(result.get("category").events) == 1 and \
                    (result.get("category").events[0].owner is RESTRICTED or \
                     (result.get("category").events[0].owner.name is RESTRICTED and \
                      result.get("category").events[0].owner.surname is RESTRICTED)))
        except SecurityException:
            assert True

#Test Case	26	Read Category.name
# Test \events
def test_case_26_VISITOR(app, request, category1):
    with current_app.test_request_context():
        # Scenario: a category1
        db.session.add(category1)
        db.session.commit()
        # Test visitor accessing events():
        result = events()
        categories_dto = result.get("categories")
        assert len(categories_dto) == 1
        assert categories_dto[0].name == category1.name

# Test \categories
def test_case_26_VISITOR_1(app, request, category1):
    with current_app.test_request_context():
        # Scenario: a category category1
        db.session.add(category1)
        db.session.commit()
        # Test visitor accessing categories()
        result = categories()
        assert len(result.get("categories")) == 1
        assert result.get("categories")[0].name == category1.name

# Testing /view_event
def test_case_26_VISITOR_2(app, request, user1, freeuserrole, publicevent1, category1):
    with current_app.test_request_context():
        # Scenario: a person user1 with FREEUSER role.
        #           a category category1
        #           a public event owned by user1, of category1
        user1.role = freeuserrole
        db.session.add(user1)
        publicevent1.owner = user1 
        publicevent1.attendants.append(user1)
        publicevent1.managedBy.append(user1)
        publicevent1.categories.append(category1)
        db.session.add(publicevent1)
        db.session.commit()
        # Test visitor accessing view_event(): 
        try:
            result = view_event(publicevent1.id)
            assert is_response(result) or \
                   (len(result.get("event").categories) == 1 and \
                    result.get("event").categories[0].name == category1.name)
        except SecurityException:
            assert True

# Testing /view_event
def test_case_26_VISITOR_3(app, request, user1, premiumuserrole, privateevent1, category1):
    with current_app.test_request_context():
        # Scenario: a person user1 with PREMIUMUSER role.
        #           a category category1
        #           a private event owned by user1, of category1
        user1.role = premiumuserrole
        db.session.add(user1)
        privateevent1.owner = user1 
        privateevent1.attendants.append(user1)
        privateevent1.managedBy.append(user1)
        privateevent1.categories.append(category1)
        db.session.add(privateevent1)
        db.session.commit()
        # Test visitor accessing view_event(): 
        try:
            result = view_event(privateevent1.id)
            assert is_response(result) or \
                   (len(result.get("event").categories) == 1 and \
                    result.get("event").categories[0].name == category1.name)
        except SecurityException:
            assert True

# Test edit_event
def test_case_26_VISITOR_4(app, request, user1, freeuserrole, publicevent1, category1):
    with current_app.test_request_context():
        # Scenario: a person user1 with FREEUSER role.
        #           a category category1
        #           a public event owned by user1, of category1
        user1.role = freeuserrole
        db.session.add(user1)
        publicevent1.owner = user1 
        publicevent1.attendants.append(user1)
        publicevent1.managedBy.append(user1)
        publicevent1.categories.append(category1)
        db.session.add(publicevent1)
        db.session.commit()
        # Test visitor accessing edit_event()
        try:
            result = edit_event(publicevent1.id)
            assert is_response(result) or \
                   (len(result.get("event").categories) == 1 and \
                    result.get("event").categories[0].name == category1.name)
        except SecurityException:
            assert True

# Test edit_event
def test_case_26_VISITOR_5(app, request, user1, premiumuserrole, privateevent1, category1):
    with current_app.test_request_context():
        # Scenario: a person user1 with PREMIUMUSER role.
        #           a category category1
        #           a private event owned by user1, of category1
        user1.role = premiumuserrole
        db.session.add(user1)
        privateevent1.owner = user1 
        privateevent1.attendants.append(user1)
        privateevent1.managedBy.append(user1)
        privateevent1.categories.append(category1)
        db.session.add(privateevent1)
        db.session.commit()
        # Test visitor accessing edit_event()
        try:
            result = edit_event(privateevent1.id)
            assert is_response(result) or \
                   (len(result.get("event").categories) == 1 and \
                    result.get("event").categories[0].name == category1.name)
        except SecurityException:
            assert True

# Test /user
def test_case_26_VISITOR_6(app, request, user1, moderatorrole, category1):
    with current_app.test_request_context():
        # Scenario: a person user1 with MODERATOR role.
        #           a category category1
        #           user1 is both moderator and subscriber of category1
        user1.role = moderatorrole
        db.session.add(user1)
        category1.moderators.append(user1)
        category1.subscribers.append(user1)
        db.session.add(category1)
        db.session.commit()
        # Test visitor accessing user()
        try:
            result = user(user1.id)
            assert is_response(result) or \
                   len(result.get("user").subscriptions) == 0
        except SecurityException:
            assert True

# Test view_category
def test_case_26_VISITOR_7(app, request, category1):
    with current_app.test_request_context():
        # Scenario: a category category1
        db.session.add(category1)
        db.session.commit()
        # Test visitor accessing view_category()
        try:
            result = view_category(category1.id)
            assert is_response(result) or \
                   result.get("category").name == category1.name
        except SecurityException:
            assert True

# Test edit_category
def test_case_26_VISITOR_8(app, request, category1):
    with current_app.test_request_context():
        # Scenario: a category category1
        db.session.add(category1)
        db.session.commit()
        # Test visitor accessing edit_category()
        try:
            result = edit_category(category1.id)
            assert is_response(result) or \
                   result.get("category").name == category1.name
        except SecurityException:
            assert True

#Test Case	27	Read Category.moderators
# Test edit_category
def test_case_27_VISITOR(app, request, user1, moderatorrole, category1):
    with current_app.test_request_context():
        # Scenario: a person user1 with MODERATOR role.
        #           a category category1
        #           user1 moderates category1
        user1.role = moderatorrole
        db.session.add(user1)
        category1.moderators.append(user1)
        db.session.add(category1)
        db.session.commit()
        # Test visitor accessing edit_category()
        try:
            result = edit_category(category1.id)
            assert is_response(result) or \
                   len(result.get("category").moderators) == 1
        except SecurityException:
            assert True

#Test Case	28	Read Category.events
# Test \categories
def test_case_28_VISITOR(app, request, user1, freeuserrole, publicevent1, category1):
    with current_app.test_request_context():
        # Scenario: a person user1 with FREEUSER role.
        #           a category category1
        #           a public event owned by user1, of category1
        user1.role = freeuserrole
        db.session.add(user1)
        publicevent1.owner = user1 
        publicevent1.attendants.append(user1)
        publicevent1.managedBy.append(user1)
        publicevent1.categories.append(category1)
        db.session.add(publicevent1)
        db.session.commit()
        # Test visitor accessing categories()
        result = categories()
        assert len(result.get("categories")) == 1
        assert len(result.get("categories")[0].events) == 1

# Test view_category
def test_case_28_VISITOR_1(app, request, user1, freeuserrole, publicevent1, category1):
    with current_app.test_request_context():
        # Scenario: a person user1 with FREEUSER role.
        #           a category category1
        #           a public event owned by user1, of category1
        user1.role = freeuserrole
        db.session.add(user1)
        publicevent1.owner = user1 
        publicevent1.attendants.append(user1)
        publicevent1.managedBy.append(user1)
        publicevent1.categories.append(category1)
        db.session.add(publicevent1)
        db.session.commit()
        # Test visitor accessing view_category()
        try:
            result = view_category(category1.id)
            assert is_response(result) or \
                   (len(result.get("category").events) == 1)
        except SecurityException:
            assert True

#Test Case	29	Create a public event
def test_case_29_VISITOR(app, request, publicevent1):
    with current_app.test_request_context(
        data={"title": publicevent1.title, 
              "description": publicevent1.description,
              "categories": publicevent1.categories}):
        db.session.commit()
        try:
            result = create_event()
        except SecurityException:
            assert True
        finally:
            assert len(Event.query.all()) == 0

#Test Case	30	Read core info of public event created by someone else
# Testing /events
def test_case_30_VISITOR(app, request, user1, freeuserrole, publicevent1):
    with current_app.test_request_context():
        # Scenario: a person user1 with FREEUSER role.
        #           a public event owned by user1
        user1.role = freeuserrole
        db.session.add(user1)
        publicevent1.owner = user1 
        publicevent1.attendants.append(user1)
        publicevent1.managedBy.append(user1)
        db.session.add(publicevent1)
        db.session.commit()
        # Test visitor accessing events():
        result = events()
        events_dto = result.get("events")
        assert len(events_dto) == 1
        assert events_dto[0].title == publicevent1.title
        assert events_dto[0].owner is RESTRICTED or \
               (events_dto[0].owner.name is RESTRICTED and \
                events_dto[0].owner.surname is RESTRICTED)

# Test view_event
def test_case_30_VISITOR_1(app, request, user1, freeuserrole, publicevent1):
    with current_app.test_request_context():
        # Scenario: a person user1 with FREEUSER role.
        #           a public event owned by user1
        user1.role = freeuserrole
        db.session.add(user1)
        publicevent1.owner = user1 
        publicevent1.attendants.append(user1)
        publicevent1.managedBy.append(user1)
        db.session.add(publicevent1)
        db.session.commit()
        # Test visitor accessing view_event(): 
        try:
            result = view_event(publicevent1.id)
            assert is_response(result) or \
                   (result.get("event").title == publicevent1.title and \
                    result.get("event").description == publicevent1.description)
        except SecurityException:
            assert True

# Test edit_event
def test_case_30_VISITOR_2(app, request, user1, freeuserrole, publicevent1):
    with current_app.test_request_context():
        # Scenario: a person user1 with FREEUSER role.
        #           a public event owned by user1
        user1.role = freeuserrole
        db.session.add(user1)
        publicevent1.owner = user1 
        publicevent1.attendants.append(user1)
        publicevent1.managedBy.append(user1)
        db.session.add(publicevent1)
        db.session.commit()
        # Test visitor accessing edit_event()
        try:
            result = edit_event(publicevent1.id)
            assert is_response(result) or \
                   (result.get("event").title == publicevent1.title and \
                    result.get("event").description == publicevent1.description)
        except SecurityException:
            assert True

# Test view_category
def test_case_30_VISITOR_3(app, request, user1, freeuserrole, publicevent1, category1):
    with current_app.test_request_context():
        # Scenario: a person user1 with FREEUSER role.
        #           a category category1
        #           a public event owned by user1, of category1
        user1.role = freeuserrole
        db.session.add(user1)
        publicevent1.owner = user1 
        publicevent1.attendants.append(user1)
        publicevent1.managedBy.append(user1)
        publicevent1.categories.append(category1)
        db.session.add(publicevent1)
        db.session.commit()
        # Test visitor accessing view_category()
        try:
            result = view_category(category1.id)
            assert is_response(result) or \
                   (len(result.get("category").events) == 1 and \
                    result.get("category").events[0].title == publicevent1.title and \
                    (result.get("category").events[0].owner is RESTRICTED or \
                     (result.get("category").events[0].owner.name is RESTRICTED and \
                      result.get("category").events[0].owner.surname is RESTRICTED)))
        except SecurityException:
            assert True

#Test Case	31	Read core info of private event created by someone else and not participating
# Testing /events
def test_case_31_VISITOR(app, request, user1, premiumuserrole, privateevent1):
    with current_app.test_request_context():
        # Scenario: a person user1 with PREMIUMUSER role.
        #           a private event owned by user1
        user1.role = premiumuserrole
        db.session.add(user1)
        privateevent1.owner = user1 
        privateevent1.attendants.append(user1)
        privateevent1.managedBy.append(user1)
        db.session.add(privateevent1)
        db.session.commit()
        # Test visitor accessing events():
        result = events()
        events_dto = result.get("events")
        assert len(events_dto) == 0 or \
               (len(events_dto) == 1 and \
                events_dto[0].title is RESTRICTED and \
                (events_dto[0].owner is RESTRICTED or \
                 (events_dto[0].owner.name is RESTRICTED and \
                  events_dto[0].owner.surname is RESTRICTED)))

# Test view_event
def test_case_31_VISITOR_1(app, request, user1, premiumuserrole, privateevent1):
    with current_app.test_request_context():
        # Scenario: a person user1 with PREMIUMUSER role.
        #           a private event owned by user1
        user1.role = premiumuserrole
        db.session.add(user1)
        privateevent1.owner = user1 
        privateevent1.attendants.append(user1)
        privateevent1.managedBy.append(user1)
        db.session.add(privateevent1)
        db.session.commit()
        # Test visitor accessing view_event(): 
        try:
            result = view_event(privateevent1.id)
            assert is_response(result) or \
                   (result.get("event").title is RESTRICTED and \
                    result.get("event").description is RESTRICTED)
        except SecurityException:
            assert True

# Test edit_event
def test_case_31_VISITOR_2(app, request, user1, premiumuserrole, privateevent1):
    with current_app.test_request_context():
        # Scenario: a person user1 with PREMIUMUSER role.
        #           a private event owned by user1
        user1.role = premiumuserrole
        db.session.add(user1)
        privateevent1.owner = user1 
        privateevent1.attendants.append(user1)
        privateevent1.managedBy.append(user1)
        db.session.add(privateevent1)
        db.session.commit()
        # Test visitor accessing edit_event()
        try:
            result = edit_event(privateevent1.id)
            assert is_response(result) or \
                   (result.get("event").title is RESTRICTED and \
                    result.get("event").description is RESTRICTED)
        except SecurityException:
            assert True

# Test view_category
def test_case_31_VISITOR_3(app, request, user1, premiumuserrole, privateevent1, category1):
    with current_app.test_request_context():
        # Scenario: a person user1 with PREMIUMUSER role.
        #           a category category1
        #           a private event owned by user1, of category1
        user1.role = premiumuserrole
        db.session.add(user1)
        privateevent1.owner = user1 
        privateevent1.attendants.append(user1)
        privateevent1.managedBy.append(user1)
        privateevent1.categories.append(category1)
        db.session.add(privateevent1)
        db.session.commit()
        # Test visitor accessing view_category()
        try:
            result = view_category(category1.id)
            assert is_response(result) or \
                   len(result.get("category").events) == 0 or \
                   (len(result.get("category").events) == 1 and \
                    result.get("category").events[0].title is RESTRICTED and \
                    (result.get("category").events[0].owner is RESTRICTED or \
                     (result.get("category").events[0].owner.name is RESTRICTED and \
                      result.get("category").events[0].owner.surname is RESTRICTED)))
        except SecurityException:
            assert True

#Test Case	32	Read attendants of public event created by someone else
# Test view_event
def test_case_32_VISITOR(app, request, user1, freeuserrole, publicevent1):
    with current_app.test_request_context():
        # Scenario: a person user1 with FREEUSER role.
        #           a public event owned by user1
        user1.role = freeuserrole
        db.session.add(user1)
        publicevent1.owner = user1 
        publicevent1.attendants.append(user1)
        publicevent1.managedBy.append(user1)
        db.session.add(publicevent1)
        db.session.commit()
        # Test visitor accessing view_event(): 
        try:
            result = view_event(publicevent1.id)
            assert is_response(result) or \
                   len(result.get("event").attendants) == 0 or \
                   (len(result.get("event").attendants) == 1 and \
                    result.get("event").attendants[0].name is RESTRICTED and \
                    result.get("event").attendants[0].surname is RESTRICTED)
        except SecurityException:
            assert True

# Test manage_event
def test_case_32_VISITOR_1(app, request, user1, freeuserrole, publicevent1):
    with current_app.test_request_context():
        # Scenario: a person user1 with FREEUSER role.
        #           a public event owned by user1
        user1.role = freeuserrole
        db.session.add(user1)
        publicevent1.owner = user1 
        publicevent1.attendants.append(user1)
        publicevent1.managedBy.append(user1)
        db.session.add(publicevent1)
        db.session.commit()
        # Test visitor accessing manage_event()
        try:
            result = manage_event(publicevent1.id)
            assert is_response(result) or \
                   (len(result.get("event").attendants) == 0 or \
                    (len(result.get("event").attendants) == 1 and \
                     result.get("event").attendants[0].name is RESTRICTED and \
                     result.get("event").attendants[0].surname is RESTRICTED))
        except SecurityException:
            assert True

#Test Case	33	Read attendants of private event created by someone else and not participating
# Test view_event
def test_case_33_VISITOR(app, request, user1, premiumuserrole, privateevent1):
    with current_app.test_request_context():
        # Scenario: a person user1 with PREMIUMUSER role.
        #           a private event owned by user1
        user1.role = premiumuserrole
        db.session.add(user1)
        privateevent1.owner = user1 
        privateevent1.attendants.append(user1)
        privateevent1.managedBy.append(user1)
        db.session.add(privateevent1)
        db.session.commit()
        # Test visitor accessing view_event(): 
        try:
            result = view_event(privateevent1.id)
            assert is_response(result) or \
                   len(result.get("event").attendants) == 0 or \
                   (len(result.get("event").attendants) == 1 and \
                    result.get("event").attendants[0].name is RESTRICTED and \
                    result.get("event").attendants[0].surname is RESTRICTED)
        except SecurityException:
            assert True

# Test manage_event
def test_case_33_VISITOR_1(app, request, user1, premiumuserrole, privateevent1):
    with current_app.test_request_context():
        # Scenario: a person user1 with PREMIUMUSER role.
        #           a private event owned by user1
        user1.role = premiumuserrole
        db.session.add(user1)
        privateevent1.owner = user1 
        privateevent1.attendants.append(user1)
        privateevent1.managedBy.append(user1)
        db.session.add(privateevent1)
        db.session.commit()
        # Test visitor accessing manage_event()
        try:
            result = manage_event(privateevent1.id)
            assert is_response(result) or \
                   (len(result.get("event").attendants) == 0 or \
                    (len(result.get("event").attendants) == 1 and \
                     result.get("event").attendants[0].name is RESTRICTED and \
                     result.get("event").attendants[0].surname is RESTRICTED))
        except SecurityException:
            assert True


#Test Case	36	Edit others event if not manager
def test_case_36_VISITOR(app, request, user1, freeuserrole, publicevent1, category1):
    with current_app.test_request_context(
        data={ "id": publicevent1.id, 
              "title": "new title", 
              "description": "new description", 
              "categories": publicevent1.categories}):
        # Scenario: a person user1 with FREEUSER role.
        #           a public event owned by user1
        user1.role = freeuserrole
        db.session.add(user1)
        publicevent1.owner = user1 
        publicevent1.attendants.append(user1)
        publicevent1.managedBy.append(user1)
        db.session.add(publicevent1)
        db.session.commit()
        # Test visitor accessing update_event()
        try:
            result = update_event()
        except SecurityException:
            assert True
        finally:
            assert publicevent1.title == "event1"
            assert publicevent1.description == "event1"

#Test Case	37	Edit owner of event
# Not applicable: No provided functionality for this.

#Test Case	40	Demote manager for event not owned
def test_case_40_VISITOR(app, request, user1, user2, freeuserrole, publicevent1):
    with current_app.test_request_context():
        # Scenario: a user user1 with FREEUSER role
        #           a user user2 with FREEUSER role
        #           a public event
        #           user1 owns the event
        #           user2 manages the event
        user1.role = freeuserrole
        db.session.add(user1)
        user2.role = freeuserrole
        db.session.add(user2)
        publicevent1.owner = user1
        publicevent1.attendants.append(user1)
        publicevent1.managedBy.append(user1)
        publicevent1.attendants.append(user2)
        publicevent1.managedBy.append(user2)
        db.session.add(publicevent1)
        db.session.commit()
        # Test visitor accessing demote_manager()
        try:
            result = demote_manager(user2.id, publicevent1.id)
        except SecurityException:
            assert True
        finally:
            assert user2.id in [m.id for m in publicevent1.managedBy]

#Test Case	50	Non manager removes someone else from event
def test_case_50_VISITOR(app, request, user1, user2, freeuserrole, publicevent1):
    with current_app.test_request_context():
        # Scenario: a user user1 with FREEUSER role
        #           a user user2 with FREEUSER role
        #           a public event
        #           user1 owns the event
        #           user2 attends the event
        user1.role = freeuserrole
        db.session.add(user1)
        user2.role = freeuserrole
        db.session.add(user2)
        publicevent1.owner = user1
        publicevent1.attendants.append(user1)
        publicevent1.managedBy.append(user1)
        publicevent1.attendants.append(user2)
        db.session.add(publicevent1)
        db.session.commit()
        # Test visitor accessing remove_attendee()
        try:
            result = remove_attendee(user2.id, publicevent1.id)
        except SecurityException:
            assert True
        finally:
            assert user2.id in [m.id for m in publicevent1.attendants]

#Test Case	53	Reject request to join, non manager, non owner, non requester
def test_case_53_VISITOR(app, request, user1, user2, freeuserrole, publicevent1):
    with current_app.test_request_context():
        # Scenario: a user user1 with FREEUSER role
        #           a user user2 with FREEUSER role
        #           a public event
        #           user1 owns the event
        #           user2 requests the event
        #
        user1.role = freeuserrole
        db.session.add(user1)
        user2.role = freeuserrole
        db.session.add(user2)
        publicevent1.owner = user1
        publicevent1.attendants.append(user1)
        publicevent1.managedBy.append(user1)
        publicevent1.requesters.append(user2)
        db.session.add(publicevent1)
        db.session.commit()
        # Test visitor accessing reject_request()
        try:
            result = reject_request(user2.id, publicevent1.id)
        except SecurityException:
            assert True
        finally:
            assert user2.id in [m.id for m in publicevent1.requesters]

#Test Case	55	Request to join for someone else
# Not applicable, one can request to join for oneself.

#Test Case	56	Read core information of other users
# Test /main
# Not applicable since it shows "Welcome visitor"

# Test /events
# Duplicated with Event.owner checks

# Test /view_event
# Duplicated with Event.attendants checks

# Test /manage_event
def test_case_56_VISITOR(app, request, user1, user2, freeuserrole, publicevent1, moderatorrole):
    with current_app.test_request_context():
        # Scenario: a person user1 with FREEUSER role.
        #           a person user2 with MODERATOR role.
        #           a public event owned by user1
        #           user2 requests to join for this event
        user1.role = freeuserrole
        db.session.add(user1)
        user2.role = moderatorrole
        db.session.add(user2)
        publicevent1.owner = user1 
        publicevent1.attendants.append(user1)
        publicevent1.managedBy.append(user1)
        publicevent1.requesters.append(user2)
        db.session.add(publicevent1)
        db.session.commit()
        # Test visitor accessing manage_event()
        try:
            result = manage_event(publicevent1.id)
            assert is_response(result) or \
                   ((len(result.get("event").attendants) == 0 or \
                     (len(result.get("event").attendants) == 1 and \
                      result.get("event").attendants[0].name is RESTRICTED and \
                      result.get("event").attendants[0].surname is RESTRICTED)) and \
                     (len(result.get("event").managedBy) == 0 or \
                      (len(result.get("event").managedBy) == 1 and \
                       result.get("event").managedBy[0].name is RESTRICTED and \
                       result.get("event").managedBy[0].surname is RESTRICTED)) and \
                   (len(result.get("event").requesters) == 0 or \
                     (len(result.get("event").requesters) == 1 and \
                      result.get("event").requesters[0].name is RESTRICTED and \
                      result.get("event").requesters[0].surname is RESTRICTED)))
        except SecurityException:
            assert True

# Test \users
def test_case_56_VISITOR_1(app, request, user1, freeuserrole):
    with current_app.test_request_context():
        # Scenario: a person user1 with FREEUSER role.
        user1.role = freeuserrole
        db.session.add(user1)
        db.session.commit()
        # Test visitor accessing users()
        try:
            result = users()
            assert is_response(result) or \
                   (len(result.get("users")) == 0 or \
                    (len(result.get("users")) == 1 and \
                     result.get("users")[0].name is RESTRICTED and \
                     result.get("users")[0].surname is RESTRICTED))
        except SecurityException:
            assert True

# Test \user
def test_case_56_VISITOR_2(app, request, user1, freeuserrole):
    with current_app.test_request_context():
        # Scenario: a person user1 with FREEUSER role.
        user1.role = freeuserrole
        db.session.add(user1)
        db.session.commit()
        # Test visitor accessing user()
        try:
            result = user(user1.id)
            assert is_response(result) or \
                   (result.get("user").name is RESTRICTED and \
                    result.get("user").surname is RESTRICTED and \
                    result.get("user").username is RESTRICTED and \
                    (result.get("user").role is RESTRICTED or \
                     result.get("user").role.name is RESTRICTED))
        except SecurityException:
            assert True

# Test view_category
# Duplicated with Event.owner checks

# Test edit_category
def test_case_56_VISITOR_3(app, request, user1, moderatorrole, category1, user2):
    with current_app.test_request_context():
        # Scenario: a person user1, user2 with MODERATOR role.
        #           a category category1
        #           user1 apply to category1
        #           user2 moderates category1
        user1.role = moderatorrole
        db.session.add(user1)
        user2.role = moderatorrole
        db.session.add(user2)
        category1.subscribers.append(user2)
        category1.moderators.append(user2)
        db.session.add(category1)
        db.session.commit()
        # Test visitor accessing edit_category()
        try:
            result = edit_category(category1.id)
            assert is_response(result) or \
                   (result.get("category").name == category1.name and \
                    (len(result.get("category").moderators) == 1 and \
                     result.get("category").moderators[0].name is RESTRICTED and \
                     result.get("category").moderators[0].surname is RESTRICTED) and \
                    (result.get("candidates") == [] or \
                     (len(result.get("candidates")) == 1 and \
                      result.get("candidates")[0].name is RESTRICTED and \
                      result.get("candidates")[0].surname is RESTRICTED)))
        except SecurityException:
            assert True

#Test Case	59	Edit others core
def test_case_59_VISITOR(app, request, user1, freeuserrole):
    with current_app.test_request_context(
        data={ "id": user1.id, 
              "name": "new_value",
              "surname": "new_value",
              "role": freeuserrole.name}):
        # Scenario: a user user1 with FREEUSER role
        user1.role = freeuserrole
        db.session.add(user1)
        db.session.commit()
        # Test visitor accessing update_user()
        try:
            result = update_user()
        except SecurityException:
            assert True
        finally:
            assert user1.name == "user1"
            assert user1.surname == "user1"

#Test Case	67	Subscribe to categories
#Test Case	68	Add category to your subscriptions
def test_case_67_68_VISITOR(app, request, category1):
    with current_app.test_request_context():
        # Scenario: a category category1
        db.session.add(category1)
        db.session.commit()
        # Test visitor accessing subscribe()
        try:
            result = subscribe(category1.id)
        except SecurityException:
            assert True
        finally:
            assert len(category1.subscribers) == 0

#Test Case	69	Create a private event
def test_case_69_VISITOR(app, request, privateevent1):
    with current_app.test_request_context(
        data={"title": privateevent1.title, 
              "description": privateevent1.description,
              "private": "sure",
              "categories": privateevent1.categories}):
        try:
            result = create_event()
        except SecurityException:
            assert True
        finally:
            assert len(Event.query.all()) == 0

#Test Case	70	Remove category they do not moderate from event
def test_case_70_VISITOR(app, request, user1, freeuserrole, publicevent1, category1):
    with current_app.test_request_context():
        # Scenario: a person user1 with FREEUSER role.
        #           a category category1
        #           a public event owned by user1, of category1
        user1.role = freeuserrole
        db.session.add(user1)
        publicevent1.owner = user1 
        publicevent1.attendants.append(user1)
        publicevent1.managedBy.append(user1)
        publicevent1.categories.append(category1)
        db.session.add(publicevent1)
        db.session.commit()
        try:
            result = remove_category(publicevent1.id, category1.id)
        except SecurityException:
            assert True
        finally:
            assert len(publicevent1.categories) == 1
            assert publicevent1.categories[0].id == category1.id
            
def test_case_70_VISITOR_1(app, request, user1, freeuserrole, publicevent1, category1):
    with current_app.test_request_context(
        data={ "id": publicevent1.id, 
              "title": publicevent1.title, 
              "description": publicevent1.description, 
              "categories": []}):
        # Scenario: a person user1 with FREEUSER role.
        #           a public event owned by user1
        user1.role = freeuserrole
        db.session.add(user1)
        publicevent1.owner = user1 
        publicevent1.attendants.append(user1)
        publicevent1.managedBy.append(user1)
        publicevent1.categories.append(category1)
        db.session.add(publicevent1)
        db.session.commit()
        # Test visitor accessing update_event()
        try:
            result = update_event()
        except SecurityException:
            assert True
        finally:
            assert len(publicevent1.categories) == 1

#Test Case	71	Remove someone else as moderator for category
# Removed: duplicated with 79

#Test Case	74	Read category subscribers
def test_case_74_VISITOR(app, request, user1, premiumuserrole, category1):
    with current_app.test_request_context():
        # Scenario: a person user1 with PREMIUMUSER role.
        #           a category category1, subscribed by user1
        user1.role = premiumuserrole
        db.session.add(user1)
        category1.subscribers.append(user1)
        db.session.add(category1)
        db.session.commit()
        # Test visitor accessing view_category()
        try:
            result = view_category(category1.id)
            assert is_response(result) or \
                   (len(result.get("category").subscribers) == 0 or \
                    (len(result.get("category").subscribers) == 1 and \
                     result.get("category").subscribers[0].name is RESTRICTED and \
                     result.get("category").subscribers[0].surname is RESTRICTED))
        except SecurityException:
            assert True

#Test Case	75	Delete user
# Not applicable: Flask-User handles this

#Test Case	76	Edit pwd other user
# Not applicable: Flask-User handles this

#Test Case	77	Edit role other user
# Duplicate with the test cases 10--13

#Test Case	78	Add user as moderator category
def test_case_78_VISITOR(app, request, user1, moderatorrole, category1):
    with current_app.test_request_context():
        # Scenario: a person user1 with MODERATOR role.
        #           a category category1
        #           user1 apply to category1
        user1.role = moderatorrole
        db.session.add(user1)
        category1.candidates.append(user1)
        db.session.add(category1)
        db.session.commit()
        # Test visitor accessing add_moderator()
        try:
            result = add_moderator(user1.id, category1.id)
        except SecurityException:
            assert True
        finally:
            assert user1.id not in [m.id for m in category1.moderators]

#Test Case	79	Remove user as moderator category
def test_case_79_VISITOR(app, request, user1, moderatorrole, category1):
    with current_app.test_request_context():
        # Scenario: a person user1 with MODERATOR role.
        #           a category category1
        #           user1 moderates category1
        user1.role = moderatorrole
        db.session.add(user1)
        category1.moderators.append(user1)
        db.session.add(category1)
        db.session.commit()
        # Test visitor accessing remove_moderator()
        try:
            result = remove_moderator(user1.id, category1.id)
        except SecurityException:
            assert True
        finally:
            assert user1.id in [m.id for m in category1.moderators]

#Test Case	80	Create Category
def test_case_80_VISITOR(app, request, category1):
    with current_app.test_request_context(
        data={"name": category1.name}):
        # Scenario: empty database
        # Test visitor accessing create_category()
        try:
            result = create_category()
        except SecurityException:
            assert True
        finally:
            assert len(Category.query.all()) == 0

#Test Case	81	Delete Category
# Not applicable

#Test Case	82	Change Category Name
def test_case_82_VISITOR(app, request, category1):
    with current_app.test_request_context(
        data={ "id": category1.id, 
              "name": "new name"}):
        # Scenario: a category category1
        db.session.add(category1)
        db.session.commit()
        # Test visitor accessing update_category()
        try:
            result = update_category()
        except SecurityException:
            assert True
        finally:
            assert category1.name == "category1"

#Test Case	89	Update Person.role from FREE to VISITOR
# Not applicable

#Test Case	90	Accept someone else's request, not owner not manager
def test_case_90_VISITOR(app, request, user1, user2, freeuserrole, publicevent1):
    with current_app.test_request_context():
        # Scenario: person user1, user2 with FREEUSER role.
        #           a public event owned by user1, request to join by user2
        user1.role = freeuserrole
        db.session.add(user1)
        user2.role = freeuserrole
        db.session.add(user2)
        publicevent1.owner = user1 
        publicevent1.attendants.append(user1)
        publicevent1.managedBy.append(user1)
        publicevent1.requesters.append(user2)
        db.session.add(publicevent1)
        db.session.commit()
        # Test VISITOR accessing accept_request()
        try:
            result = accept_request(user2.id, publicevent1.id)
        except SecurityException:
            assert True
        finally:
            assert user2.id not in [m.id for m in publicevent1.attendants]
            assert user2.id in [m.id for m in publicevent1.requesters]

#Test Case	91	Edit event's categories, manager
# Not applicable

#Test Case	92	Edit event's categories, not manager
def test_case_92_VISITOR(app, request, user1, freeuserrole, publicevent1, category1):
    with current_app.test_request_context(
        data={ "id": publicevent1.id, 
              "title": publicevent1.title, 
              "description": publicevent1.description, 
              "categories": []}):
        # Scenario: a person user1 with FREEUSER role.
        #           a public event owned by user1
        user1.role = freeuserrole
        db.session.add(user1)
        publicevent1.owner = user1 
        publicevent1.attendants.append(user1)
        publicevent1.managedBy.append(user1)
        publicevent1.categories.append(category1)
        db.session.add(publicevent1)
        db.session.commit()
        # Test visitor accessing update_event()
        try:
            result = update_event()
        except SecurityException:
            assert True
        finally:
            assert len(publicevent1.categories) == 1
            assert publicevent1.categories[0].id == category1.id

#Test Case	93	Read Event.private for private event
def test_case_93_VISITOR(app, request, user1, premiumuserrole, privateevent1):
    with current_app.test_request_context():
        # Scenario: a person user1 with PREMIUMUSER role.
        #           a private event owned by user1
        user1.role = premiumuserrole
        db.session.add(user1)
        privateevent1.owner = user1 
        privateevent1.attendants.append(user1)
        privateevent1.managedBy.append(user1)
        db.session.add(privateevent1)
        db.session.commit()
        # Test visitor accessing view_event(): 
        try:
            result = view_event(privateevent1.id)
            assert is_response(result) or \
                   result.get("event").private == privateevent1.private
        except SecurityException:
            assert True

def test_case_93_VISITOR_1(app, request, user1, premiumuserrole, privateevent1):
    with current_app.test_request_context():
        # Scenario: a person user1 with PREMIUMUSER role.
        #           a private event owned by user1
        user1.role = premiumuserrole
        db.session.add(user1)
        privateevent1.owner = user1 
        privateevent1.attendants.append(user1)
        privateevent1.managedBy.append(user1)
        db.session.add(privateevent1)
        db.session.commit()
        # Test visitor accessing edit_event()
        try:
            result = edit_event(privateevent1.id)
            assert is_response(result) or \
                   result.get("event").private == privateevent1.private
        except SecurityException:
            assert True

#Test Case	94	Read Event.categories of a private event
def test_case_94_VISITOR(app, request, user1, premiumuserrole, privateevent1, category1):
    with current_app.test_request_context():
        # Scenario: a person user1 with PREMIUMUSER role.
        #           a category category1
        #           a private event owned by user1, of category1
        user1.role = premiumuserrole
        db.session.add(user1)
        privateevent1.owner = user1 
        privateevent1.attendants.append(user1)
        privateevent1.managedBy.append(user1)
        privateevent1.categories.append(category1)
        db.session.add(privateevent1)
        db.session.commit()
        # Test visitor accessing view_event(): 
        try:
            result = view_event(privateevent1.id)
            assert is_response(result) or \
                   (len(result.get("event").categories) == 1 and \
                    result.get("event").categories[0].name == category1.name)
        except SecurityException:
            assert True
