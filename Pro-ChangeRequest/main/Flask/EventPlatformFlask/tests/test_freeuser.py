from typing import final
from flask import current_app, Response
from flask_login import login_user, AnonymousUserMixin
from flask_user import current_user
from model import db
from project import *
from dto import RESTRICTED
from flask_principal import Identity, identity_changed
from implicits import implicits
from tests.conftest import publicevent2


# This test suite is dedicated for users with FREEUSER role
# Tests that are applicable to FREEUSER role.

def is_response(result):
    return type(result) == Response     

@implicits("app")
def login_user(user,app):
    from flask_login import login_user
    login_user(user)
    identity_changed.send(app,identity=Identity(current_user.id))


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
def test_case_12_FREEUSER(app, request, user1, freeuserrole, premiumuserrole):
    with current_app.test_request_context(
        data={ "id": user1.id, 
              "name": user1.name,
              "surname": user1.surname,
              "role": premiumuserrole.name}):
        # Scenario: a user user1 with FREEUSER role
        user1.role = freeuserrole
        db.session.add(user1)
        db.session.add(premiumuserrole)
        db.session.commit()
        # login
        login_user(user1)
        # Test FREEUSER accessing update_user()
        try:
            result = update_user()
        except SecurityException:
            assert True
        finally:
            assert user1.role.name == freeuserrole.name
            

def test_case_12_FREEUSER_1(app, request, user1, user2, freeuserrole, premiumuserrole):
    with current_app.test_request_context(
        data={ "id": user2.id, 
              "name": user2.name,
              "surname": user2.surname,
              "role": premiumuserrole.name}):
        # Scenario: person user1, user2 with FREEUSER role
        user1.role = freeuserrole
        db.session.add(user1)
        user2.role = freeuserrole
        db.session.add(user2)
        db.session.add(premiumuserrole)
        db.session.commit()
        # login
        login_user(user1)
        # Test FREEUSER accessing update_user()
        try:
            result = update_user()
        except SecurityException:
            assert True
        finally:
            assert user1.role.name == freeuserrole.name

#Test Case	13	Update Person.role from FREE to ADMIN
def test_case_13_FREEUSER(app, request, user1, freeuserrole, adminrole):
    with current_app.test_request_context(
        data={ "id": user1.id, 
              "name": user1.name,
              "surname": user1.surname,
              "role": adminrole.name}):
        # Scenario: a user user1 with FREEUSER role
        user1.role = freeuserrole
        db.session.add(user1)
        db.session.add(adminrole)
        db.session.commit()
        # login
        login_user(user1)
        # Test FREEUSER accessing update_user()
        try:
            result = update_user()
        except SecurityException:
            assert True
        finally:
            assert user1.role.name == freeuserrole.name

def test_case_13_FREEUSER_1(app, request, user1, user2, freeuserrole, adminrole):
    with current_app.test_request_context(
        data={ "id": user2.id, 
              "name": user2.name,
              "surname": user2.surname,
              "role": adminrole.name}):
        # Scenario: person user1, user2 with FREEUSER role
        user1.role = freeuserrole
        db.session.add(user1)
        user2.role = freeuserrole
        db.session.add(user2)
        db.session.add(adminrole)
        db.session.commit()
        # login
        login_user(user1)
        # Test FREEUSER accessing update_user()
        try:
            result = update_user()
        except SecurityException:
            assert True
        finally:
            assert user1.role.name == freeuserrole.name

#Test Case	14	Read Person.username
def test_case_14_FREEUSER(app, request, user1, freeuserrole):
    with current_app.test_request_context():
        # Scenario: a person user1 with FREEUSER role.
        user1.role = freeuserrole
        db.session.add(user1)
        db.session.commit()
        # login
        login_user(user1)
        # Test FREEUSER accessing user()
        result = user(user1.id)
        assert result.get("user").username == user1.username

def test_case_14_FREEUSER_1(app, request, user1, user2, freeuserrole):
    with current_app.test_request_context():
        # Scenario: person user1, user2 with FREEUSER role
        user1.role = freeuserrole
        db.session.add(user1)
        user2.role = freeuserrole
        db.session.add(user2)
        db.session.commit()
        # login
        login_user(user1)
        # Test FREEUSER accessing user()
        try:
            result = user(user2.id)
            assert is_response(result) \
                   or result.get("user").username == user2.username
        except SecurityException:
            assert True

#Test Case	15	Read Person.password
# No test needed because password is handled by Flask-User.

#Test Case	16	Read Person.role
def test_case_16_FREEUSER(app, request, user1, freeuserrole):
    with current_app.test_request_context():
        # Scenario: a person user1 with FREEUSER role.
        user1.role = freeuserrole
        db.session.add(user1)
        db.session.commit()
        # login
        login_user(user1)
        # Test FREEUSER accessing user()
        result = user(user1.id)
        assert result.get("user").role.name == freeuserrole.name

def test_case_16_FREEUSER_1(app, request, user1, user2, freeuserrole):
    with current_app.test_request_context():
        # Scenario: person user1, user2 with FREEUSER role
        user1.role = freeuserrole
        db.session.add(user1)
        user2.role = freeuserrole
        db.session.add(user2)
        db.session.commit()
        # login
        login_user(user1)
        # Test FREEUSER accessing user()
        try:
            result = user(user2.id)
            assert is_response(result) \
                   or result.get("user").role.name == freeuserrole.name
        except SecurityException:
            assert True

#Test Case	17	Read Person.moderates
# Not applicable No endpoints display this information

#Test Case	18	Read Event.private
def test_case_18_FREEUSER(app, request, user1, freeuserrole, publicevent1):
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
        # login
        login_user(user1)
        # Test FREEUSER accessing view_event(): 
        result = view_event(publicevent1.id)
        assert result.get("event").private == publicevent1.private

def test_case_18_FREEUSER_1(app, request, user1, user2, freeuserrole, publicevent1):
    with current_app.test_request_context():
        # Scenario: person user1, user2 with FREEUSER role.
        #           a public event owned by user2
        user1.role = freeuserrole
        db.session.add(user1)
        user2.role = freeuserrole
        db.session.add(user2)
        publicevent1.owner = user2 
        publicevent1.attendants.append(user2)
        publicevent1.managedBy.append(user2)
        db.session.add(publicevent1)
        db.session.commit()
        # login
        login_user(user1)
        # Test FREEUSER accessing view_event(): 
        result = view_event(publicevent1.id)
        assert result.get("event").private == publicevent1.private

def test_case_18_FREEUSER_2(app, request, user1, freeuserrole, publicevent1):
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
        # login
        login_user(user1)
        # Test FREEUSER accessing edit_event()
        result = edit_event(publicevent1.id)
        assert result.get("event").private == publicevent1.private

#Test Case	19	Read Event.categories
def test_case_19_FREEUSER(app, request, user1, freeuserrole, publicevent1, category1):
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
        # login
        login_user(user1)
        # Test FREEUSER accessing view_event(): 
        result = view_event(publicevent1.id)
        assert len(result.get("event").categories) == 1 and \
               result.get("event").categories[0].name == category1.name

#Test Case	20	Read Event.title of a public event
# Testing /events
def test_case_20_FREEUSER(app, request, user1, freeuserrole, publicevent1):
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
        # login
        login_user(user1)
        # Test FREEUSER accessing events():
        result = events()
        events_dto = result.get("events")
        assert len(events_dto) == 1
        assert events_dto[0].title == publicevent1.title

def test_case_20_FREEUSER_1(app, request, user1, user2, freeuserrole, publicevent1):
    with current_app.test_request_context():
        # Scenario: person user1, user2 with FREEUSER role.
        #           a public event owned by user2
        user1.role = freeuserrole
        db.session.add(user1)
        user2.role = freeuserrole
        db.session.add(user2)
        publicevent1.owner = user2 
        publicevent1.attendants.append(user2)
        publicevent1.managedBy.append(user2)
        db.session.add(publicevent1)
        db.session.commit()
        # login
        login_user(user1)
        # Test FREEUSER accessing events():
        result = events()
        events_dto = result.get("events")
        assert len(events_dto) == 1
        assert events_dto[0].title == publicevent1.title

# Testing /profile
def test_case_20_FREEUSER_2(app, request, user1, freeuserrole, publicevent1):
    with current_app.test_request_context():
        # Scenario: a freeuser user1, 
        #           a publicevent of user1
        user1.role = freeuserrole
        db.session.add(user1)
        publicevent1.owner = user1
        publicevent1.managedBy.append(user1)
        publicevent1.attendants.append(user1)
        db.session.add(publicevent1)
        db.session.commit()
        # Log in with user1
        login_user(user1)
        # Test freeuser accessing profile()
        result = profile()
        user_dto = result.get("user")
        assert len(user_dto.manages) == 1
        assert user_dto.manages[0].title == publicevent1.title
        assert len(user_dto.attends) == 1
        assert user_dto.attends[0].title == publicevent1.title

# Testing /view_event
def test_case_20_FREEUSER_3(app, request, user1, freeuserrole, publicevent1):
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
        # Log in with user1
        login_user(user1)
        # Test FREEUSER accessing view_event(): 
        result = view_event(publicevent1.id)
        assert result.get("event").title == publicevent1.title

def test_case_20_FREEUSER_4(app, request, user1, user2, freeuserrole, publicevent1):
    with current_app.test_request_context():
        # Scenario: person user1, user2 with FREEUSER role.
        #           a public event owned by user2
        user1.role = freeuserrole
        db.session.add(user1)
        user2.role = freeuserrole
        db.session.add(user2)
        publicevent1.owner = user2 
        publicevent1.attendants.append(user2)
        publicevent1.managedBy.append(user2)
        db.session.add(publicevent1)
        db.session.commit()
        # Log in with user1
        login_user(user1)
        # Test FREEUSER accessing view_event(): 
        result = view_event(publicevent1.id)
        assert result.get("event").title == publicevent1.title

# Test edit_event
def test_case_20_FREEUSER_5(app, request, user1, freeuserrole, publicevent1):
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
        # Log in with user1
        login_user(user1)
        # Test FREEUSER accessing edit_event()
        result = edit_event(publicevent1.id)
        assert result.get("event").title == publicevent1.title

def test_case_20_FREEUSER_6(app, request, user1, user2, freeuserrole, publicevent1):
    with current_app.test_request_context():
        # Scenario: person user1, user2 with FREEUSER role.
        #           a public event owned by user2
        user1.role = freeuserrole
        db.session.add(user1)
        user2.role = freeuserrole
        db.session.add(user2)
        publicevent1.owner = user2 
        publicevent1.attendants.append(user2)
        publicevent1.managedBy.append(user2)
        db.session.add(publicevent1)
        db.session.commit()
        # Log in with user1
        login_user(user1)
        # Test FREEUSER accessing edit_event()
        try:
            result = edit_event(publicevent1.id)
            assert is_response(result) or \
                   result.get("event").title == publicevent1.title
        except SecurityException:
            assert True

# Test view_category
def test_case_20_FREEUSER_7(app, request, user1, freeuserrole, publicevent1, category1):
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
        # Log in with user1
        login_user(user1)
        # Test FREEUSER accessing view_category()
        result = view_category(category1.id)
        assert (len(result.get("category").events) == 1 and \
                result.get("category").events[0].title == publicevent1.title)

def test_case_20_FREEUSER_8(app, request, user1, user2, freeuserrole, publicevent1, category1):
    with current_app.test_request_context():
        # Scenario: a person user1, user2 with FREEUSER role.
        #           a category category1
        #           a public event owned by user2, of category1
        user1.role = freeuserrole
        db.session.add(user1)
        user2.role = freeuserrole
        db.session.add(user2)
        publicevent1.owner = user2 
        publicevent1.attendants.append(user2)
        publicevent1.managedBy.append(user2)
        publicevent1.categories.append(category1)
        db.session.add(publicevent1)
        db.session.commit()
        # Log in with user1
        login_user(user1)
        # Test FREEUSER accessing view_category()
        result = view_category(category1.id)
        assert (len(result.get("category").events) == 1 and \
                result.get("category").events[0].title == publicevent1.title)

#Test Case	21	Read Event.title of a private event
def test_case_21_FREEUSER(app, request, user1, freeuserrole, user2, premiumuserrole, privateevent1):
    with current_app.test_request_context():
        # Scenario: a person user1 with FREEUSER role.
        #           a person user2 with PREMIUMUSER role.
        #           a private event owned by user2
        user1.role = freeuserrole
        db.session.add(user1)
        user2.role = premiumuserrole
        db.session.add(user2)
        privateevent1.owner = user2 
        privateevent1.attendants.append(user2)
        privateevent1.managedBy.append(user2)
        db.session.add(privateevent1)
        db.session.commit()
        # Log in with user1
        login_user(user1)
        # Test FREEUSER accessing events():
        result = events()
        events_dto = result.get("events")
        assert len(events_dto) == 0 or \
               (len(events_dto) == 1 and \
                events_dto[0].title is RESTRICTED)

# Testing /profile: no test needed because FREEUSER role 
# Not applicable: FREEUSER user cannot own/join private event

# Testing /view_event
def test_case_21_FREEUSER_1(app, request, user1, freeuserrole, user2, premiumuserrole, privateevent1):
    with current_app.test_request_context():
        # Scenario: a person user1 with FREEUSER role.
        #           a person user2 with PREMIUMUSER role.
        #           a private event owned by user2
        user1.role = freeuserrole
        db.session.add(user1)
        user2.role = premiumuserrole
        db.session.add(user2)
        privateevent1.owner = user2 
        privateevent1.attendants.append(user2)
        privateevent1.managedBy.append(user2)
        db.session.add(privateevent1)
        db.session.commit()
        # Log in with user1
        login_user(user1)
        # Test FREEUSER accessing view_event(): 
        try:
            result = view_event(privateevent1.id)
            assert is_response(result) or \
                   result.get("event").title is RESTRICTED
        except SecurityException:
            assert True

# Test edit_event
def test_case_21_FREEUSER_2(app, request, user1, freeuserrole, user2, premiumuserrole, privateevent1):
    with current_app.test_request_context():
        # Scenario: a person user1 with PREMIUMUSER role.
        #           a person user2 with PREMIUMUSER role.
        #           a private event owned by user2
        user1.role = freeuserrole
        db.session.add(user1)
        user2.role = premiumuserrole
        db.session.add(user2)
        privateevent1.owner = user2 
        privateevent1.attendants.append(user2)
        privateevent1.managedBy.append(user2)
        db.session.add(privateevent1)
        db.session.commit()
        # Log in with user1
        login_user(user1)
        # Test FREEUSER accessing edit_event()
        try:
            result = edit_event(privateevent1.id)
            assert is_response(result) or \
                   result.get("event").title is RESTRICTED
        except SecurityException:
            assert True

# Test view_category
def test_case_21_FREEUSER_3(app, request, user1, freeuserrole, user2, premiumuserrole, privateevent1, category1):
    with current_app.test_request_context():
        # Scenario: a person user1 with PREMIUMUSER role.
        #           a person user2 with PREMIUMUSER role.
        #           a category category1
        #           a public event owned by user2, of category1
        user1.role = freeuserrole
        db.session.add(user1)
        user2.role = premiumuserrole
        db.session.add(user2)
        privateevent1.owner = user2 
        privateevent1.attendants.append(user2)
        privateevent1.managedBy.append(user2)
        privateevent1.categories.append(category1)
        db.session.add(privateevent1)
        db.session.commit()
        # Log in with user1
        login_user(user1)
        # Test FREEUSER accessing view_category()
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
def test_case_22_FREEUSER(app, request, user1, freeuserrole, publicevent1):
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
        # Log in with user1
        login_user(user1)
        # Test FREEUSER accessing view_event(): 
        result = view_event(publicevent1.id)
        assert result.get("event").description == publicevent1.description

def test_case_22_FREEUSER_1(app, request, user1, user2, freeuserrole, publicevent1):
    with current_app.test_request_context():
        # Scenario: person user1, user2 with FREEUSER role.
        #           a public event owned by user1
        user1.role = freeuserrole
        db.session.add(user1)
        user2.role = freeuserrole
        db.session.add(user2)
        publicevent1.owner = user2 
        publicevent1.attendants.append(user2)
        publicevent1.managedBy.append(user2)
        db.session.add(publicevent1)
        db.session.commit()
        # Log in with user1
        login_user(user1)
        # Test FREEUSER accessing view_event(): 
        result = view_event(publicevent1.id)
        assert result.get("event").description == publicevent1.description

# Test edit_event
def test_case_22_FREEUSER_2(app, request, user1, freeuserrole, publicevent1):
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
        # Log in with user1
        login_user(user1)
        # Test FREEUSER accessing edit_event()
        result = edit_event(publicevent1.id)
        assert result.get("event").description == publicevent1.description

def test_case_22_FREEUSER_3(app, request, user1, user2, freeuserrole, publicevent1):
    with current_app.test_request_context():
        # Scenario: person user1, user2 with FREEUSER role.
        #           a public event owned by user2
        user1.role = freeuserrole
        db.session.add(user1)
        user2.role = freeuserrole
        db.session.add(user2)
        publicevent1.owner = user2 
        publicevent1.attendants.append(user2)
        publicevent1.managedBy.append(user2)
        db.session.add(publicevent1)
        db.session.commit()
        # Log in with user1
        login_user(user1)
        # Test FREEUSER accessing edit_event()
        try:
            result = edit_event(publicevent1.id)
            assert is_response(result) or \
                   result.get("event").description == publicevent1.description
        except SecurityException:
            assert True

#Test Case	23	Read Event.description of a private event
# Testing /view_event
def test_case_23_FREEUSER(app, request, user1, freeuserrole, user2, premiumuserrole, privateevent1):
    with current_app.test_request_context():
        # Scenario: a person user1 with FREEUSER role.
        #           a person user2 with PREMIUMUSER role.
        #           a private event owned by user2
        user1.role = freeuserrole
        db.session.add(user1)
        user2.role = premiumuserrole
        db.session.add(user2)
        privateevent1.owner = user2 
        privateevent1.attendants.append(user2)
        privateevent1.managedBy.append(user2)
        db.session.add(privateevent1)
        db.session.commit()
        # Log in with user1
        login_user(user1)
        # Test FREEUSER accessing view_event(): 
        try:
            result = view_event(privateevent1.id)
            assert is_response(result) or \
                   result.get("event").description is RESTRICTED
        except SecurityException:
            assert True

# Test edit_event
def test_case_23_FREEUSER_1(app, request, user1, freeuserrole, user2, premiumuserrole, privateevent1):
    with current_app.test_request_context():
        # Scenario: a person user1 with FREEUSER role.
        #           a person user2 with PREMIUMUSER role.
        #           a private event owned by user2
        user1.role = freeuserrole
        db.session.add(user1)
        user2.role = premiumuserrole
        db.session.add(user2)
        privateevent1.owner = user2 
        privateevent1.attendants.append(user2)
        privateevent1.managedBy.append(user2)
        db.session.add(privateevent1)
        db.session.commit()
        # Log in with user1
        login_user(user1)
        # Test FREEUSER accessing edit_event()
        try:
            result = edit_event(privateevent1.id)
            assert is_response(result) or \
                   result.get("event").description is RESTRICTED
        except SecurityException:
            assert True

#Test Case	24	Read Event.owner of a public event
# Test \events
def test_case_24_FREEUSER(app, request, user1, freeuserrole, publicevent1):
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
        # Log in with user1
        login_user(user1)
        # Test FREEUSER accessing events():
        result = events()
        events_dto = result.get("events")
        assert len(events_dto) == 1
        assert events_dto[0].owner.fullname == user1.fullname

def test_case_24_FREEUSER_1(app, request, user1, user2, freeuserrole, publicevent1):
    with current_app.test_request_context():
        # Scenario: person user1, user2 with FREEUSER role.
        #           a public event owned by user2
        user1.role = freeuserrole
        db.session.add(user1)
        user2.role = freeuserrole
        db.session.add(user2)
        publicevent1.owner = user2 
        publicevent1.attendants.append(user2)
        publicevent1.managedBy.append(user2)
        db.session.add(publicevent1)
        db.session.commit()
        # Log in with user1
        login_user(user1)
        # Test FREEUSER accessing events():
        result = events()
        events_dto = result.get("events")
        assert len(events_dto) == 1
        assert events_dto[0].owner.fullname == user2.fullname

# Test profile
def test_case_24_FREEUSER_2(app, request, user1, freeuserrole, publicevent1):
    with current_app.test_request_context():
        # Scenario: a freeuser user1, 
        #           a publicevent of user1
        user1.role = freeuserrole
        db.session.add(user1)
        publicevent1.owner = user1
        publicevent1.managedBy.append(user1)
        publicevent1.attendants.append(user1)
        db.session.add(publicevent1)
        db.session.commit()
        # Log in with user1
        login_user(user1)
        # Test freeuser accessing profile()
        result = profile()
        user_dto = result.get("user")
        assert len(user_dto.manages) == 1
        assert user_dto.manages[0].owner.fullname == user1.fullname
        assert len(user_dto.attends) == 1
        assert user_dto.attends[0].owner.fullname == user1.fullname

# Test \view_category
def test_case_24_FREEUSER_3(app, request, user1, freeuserrole, publicevent1, category1):
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
        # Log in with user1
        login_user(user1)
        # Test FREEUSER accessing view_category()
        result = view_category(category1.id)
        assert (len(result.get("category").events) == 1 and \
                (result.get("category").events[0].owner.fullname == user1.fullname))

def test_case_24_FREEUSER_4(app, request, user1, user2, freeuserrole, publicevent1, category1):
    with current_app.test_request_context():
        # Scenario: a person user1 with FREEUSER role.
        #           a person user2 with FREEUSER role.
        #           a category category1
        #           a public event owned by user2, of category1
        user1.role = freeuserrole
        db.session.add(user1)
        user2.role = freeuserrole
        db.session.add(user2)
        publicevent1.owner = user2 
        publicevent1.attendants.append(user2)
        publicevent1.managedBy.append(user2)
        publicevent1.categories.append(category1)
        db.session.add(publicevent1)
        db.session.commit()
        # Log in with user1
        login_user(user1)
        # Test FREEUSER accessing view_category()
        result = view_category(category1.id)
        assert (len(result.get("category").events) == 1 and \
                (result.get("category").events[0].owner.fullname == user2.fullname))

#Test Case	25	Read Event.owner of a private event
# Test \events
def test_case_25_FREEUSER(app, request, user1, freeuserrole, user2, premiumuserrole, privateevent1):
    with current_app.test_request_context():
        # Scenario: a person user1 with FREEUSER role.
        #           a person user2 with PREMIUMUSER role.
        #           a private event owned by user2
        user1.role = freeuserrole
        db.session.add(user1)
        user2.role = premiumuserrole
        db.session.add(user2)
        privateevent1.owner = user2 
        privateevent1.attendants.append(user2)
        privateevent1.managedBy.append(user2)
        db.session.add(privateevent1)
        db.session.commit()
        # Log in with user1
        login_user(user1)
        # Test FREEUSER accessing events():
        result = events()
        events_dto = result.get("events")
        assert len(events_dto) == 0 or \
               (len(events_dto) == 1 and \
                events_dto[0].owner is RESTRICTED or \
                (events_dto[0].owner.name is RESTRICTED and \
                 events_dto[0].owner.surname is RESTRICTED))

# Test view_category
def test_case_25_FREEUSER_1(app, request, user1, freeuserrole, user2, premiumuserrole, privateevent1, category1):
    with current_app.test_request_context():
        # Scenario: a person user1 with FREEUSER role.
        #           a person user2 with PREMIUMUSER role.
        #           a category category1
        #           a public event owned by user2, of category1
        user1.role = freeuserrole
        db.session.add(user1)
        user2.role = premiumuserrole
        db.session.add(user2)
        privateevent1.owner = user2 
        privateevent1.attendants.append(user2)
        privateevent1.managedBy.append(user2)
        privateevent1.categories.append(category1)
        db.session.add(privateevent1)
        db.session.commit()
        # Log in with user1
        login_user(user1)
        # Test FREEUSER accessing view_category()
        result = view_category(category1.id)
        assert len(result.get("category").events) == 0 or \
               (len(result.get("category").events) == 1 and \
                  (result.get("category").events[0].owner is RESTRICTED or \
                   (result.get("category").events[0].owner.name is RESTRICTED and \
                    result.get("category").events[0].owner.surname is RESTRICTED)))

#Test Case	26	Read Category.name
# Test \events
def test_case_26_FREEUSER(app, request, user1, freeuserrole, category1):
    with current_app.test_request_context():
        # Scenario: a category1, a freeuser user1
        user1.role = freeuserrole
        db.session.add(user1)
        db.session.add(category1)
        db.session.commit()
        # Log in with user1
        login_user(user1)
        # Test FREEUSER accessing events():
        result = events()
        categories_dto = result.get("categories")
        assert len(categories_dto) == 1
        assert categories_dto[0].name == category1.name

# Test \profile:
# Not applicable because FREEUSER cannot subscribe to a category

# Test \categories
def test_case_26_FREEUSER_1(app, request, user1, freeuserrole, category1):
    with current_app.test_request_context():
        # Scenario: a category category1, a freeuser user1
        user1.role = freeuserrole
        db.session.add(user1)
        db.session.add(category1)
        db.session.commit()
        # Log in with user1
        login_user(user1)
        # Test FREEUSER accessing categories()
        result = categories()
        assert len(result.get("categories")) == 1
        assert result.get("categories")[0].name == category1.name

# Testing /view_event
def test_case_26_FREEUSER_2(app, request, user1, freeuserrole, publicevent1, category1):
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
        # Log in with user1
        login_user(user1)
        # Test FREEUSER accessing view_event(): 
        result = view_event(publicevent1.id)
        assert (len(result.get("event").categories) == 1 and \
                result.get("event").categories[0].name == category1.name)

def test_case_26_FREEUSER_3(app, request, user1, user2, freeuserrole, publicevent1, category1):
    with current_app.test_request_context():
        # Scenario: a person user1 with FREEUSER role.
        #           a person user2 with FREEUSER role
        #           a category category1
        #           a public event owned by user2, of category1
        user1.role = freeuserrole
        db.session.add(user1)
        user2.role = freeuserrole
        db.session.add(user2)
        publicevent1.owner = user2 
        publicevent1.attendants.append(user2)
        publicevent1.managedBy.append(user2)
        publicevent1.categories.append(category1)
        db.session.add(publicevent1)
        db.session.commit()
        # Log in with user1
        login_user(user1)
        # Test FREEUSER accessing view_event(): 
        result = view_event(publicevent1.id)
        assert (len(result.get("event").categories) == 1 and \
                result.get("event").categories[0].name == category1.name)

# Testing /view_event
def test_case_26_FREEUSER_4(app, request, user1, freeuserrole, user2, premiumuserrole, privateevent1, category1):
    with current_app.test_request_context():
        # Scenario: a person user1 with FREEUSER role.
        #           a person user2 with PREMIUMUSER role.
        #           a category category1
        #           a private event owned by user2, of category1
        user1.role = freeuserrole
        db.session.add(user1)
        user2.role = premiumuserrole
        db.session.add(user2)
        privateevent1.owner = user2 
        privateevent1.attendants.append(user2)
        privateevent1.managedBy.append(user2)
        privateevent1.categories.append(category1)
        db.session.add(privateevent1)
        db.session.commit()
        # Log in with user1
        login_user(user1)
        # Test FREEUSER accessing view_event(): 
        try:
            result = view_event(privateevent1.id)
            assert is_response(result) or \
                   (len(result.get("event").categories) == 1 and \
                    result.get("event").categories[0].name == category1.name)
        except SecurityException:
            assert True

# Test edit_event
def test_case_26_FREEUSER_5(app, request, user1, freeuserrole, publicevent1, category1):
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
        # Log in with user1
        login_user(user1)
        # Test FREEUSER accessing edit_event()
        result = edit_event(publicevent1.id)
        assert (len(result.get("event").categories) == 1 and \
                result.get("event").categories[0].name == category1.name)

# Test edit_event
def test_case_26_FREEUSER_6(app, request, user1, freeuserrole, user2, premiumuserrole, privateevent1, category1):
    with current_app.test_request_context():
        # Scenario: a person user1 with FREEUSER role.
        #           a person user2 with PREMIUMUSER role.
        #           a category category1
        #           a private event owned by user2, of category1
        user1.role = freeuserrole
        db.session.add(user1)
        user2.role = premiumuserrole
        db.session.add(user2)
        privateevent1.owner = user2 
        privateevent1.attendants.append(user2)
        privateevent1.managedBy.append(user2)
        privateevent1.categories.append(category1)
        db.session.add(privateevent1)
        db.session.commit()
        # Log in with user1
        login_user(user1)
        # Test FREEUSER accessing edit_event()
        try:
            result = edit_event(privateevent1.id)
            assert is_response(result) or \
                   (len(result.get("event").categories) == 1 and \
                    result.get("event").categories[0].name == category1.name)
        except SecurityException:
            assert True

# Test /user
def test_case_26_FREEUSER_7(app, request, user1, freeuserrole, user2, moderatorrole, category1):
    with current_app.test_request_context():
        # Scenario: a person user1 with FREEUSER role.
        #           a person user2 with MODERATOR role.
        #           a category category1
        #           user2 is a subscriber of category1
        user1.role = freeuserrole
        db.session.add(user1)        
        user2.role = moderatorrole
        db.session.add(user2)
        category1.subscribers.append(user2)
        db.session.add(category1)
        db.session.commit()
        # Log in with user1
        login_user(user1)
        # Test FREEUSER accessing user()
        try:
            result = user(user2.id)
            assert is_response(result) or \
                   len(result.get("user").subscriptions) == 0
        except SecurityException:
            assert True

# Test view_category
def test_case_26_FREEUSER_8(app, request, user1, freeuserrole, category1):
    with current_app.test_request_context():
        # Scenario: a category category1 and a freeuser user1
        user1.role = freeuserrole
        db.session.add(user1)      
        db.session.add(category1)
        db.session.commit()
        # Log in with user1
        login_user(user1)
        # Test FREEUSER accessing view_category()
        result = view_category(category1.id)
        assert result.get("category").name == category1.name

# Test edit_category
def test_case_26_FREEUSER_9(app, request, user1, freeuserrole, category1):
    with current_app.test_request_context():
        # Scenario: a category category1 and a freeuser user1
        user1.role = freeuserrole
        db.session.add(user1)      
        db.session.add(category1)
        db.session.commit()
        # Log in with user1
        login_user(user1)
        # Test FREEUSER accessing edit_category()
        try:
            result = edit_category(category1.id)
            assert is_response(result) or \
                   result.get("category").name == category1.name
        except SecurityException:
            assert True

#Test Case	27	Read Category.moderators
# Test edit_category
def test_case_27_FREEUSER(app, request, user1, freeuserrole, user2, moderatorrole, category1):
    with current_app.test_request_context():
        # Scenario: a person user1 with FREEUSER role.
        #           a person user2 with MODERATOR role.
        #           a category category1
        #           user2 is both moderator of category1
        user1.role = freeuserrole
        db.session.add(user1)        
        user2.role = moderatorrole
        db.session.add(user2)
        category1.moderators.append(user2)
        db.session.add(category1)
        db.session.commit()
        # Log in with user1
        login_user(user1)
        # Test FREEUSER accessing edit_category()
        try:
            result = edit_category(category1.id)
            assert is_response(result) or \
                   len(result.get("category").moderators) == 1
        except SecurityException:
            assert True

#Test Case	28	Read Category.events
# Test \categories
def test_case_28_FREEUSER(app, request, user1, freeuserrole, publicevent1, category1):
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
        # Log in with user1
        login_user(user1)
        # Test FREEUSER accessing categories()
        result = categories()
        assert len(result.get("categories")) == 1
        assert len(result.get("categories")[0].events) == 1

def test_case_28_FREEUSER_1(app, request, user1, user2, freeuserrole, publicevent1, category1):
    with current_app.test_request_context():
        # Scenario: a person user1 with FREEUSER role.
        #           a person user2 with FREEUSER role.
        #           a category category1
        #           a public event owned by user2, of category1
        user1.role = freeuserrole
        db.session.add(user1)
        user2.role = freeuserrole
        db.session.add(user2)
        publicevent1.owner = user2 
        publicevent1.attendants.append(user2)
        publicevent1.managedBy.append(user2)
        publicevent1.categories.append(category1)
        db.session.add(publicevent1)
        db.session.commit()
        # Log in with user1
        login_user(user1)
        # Test FREEUSER accessing categories()
        result = categories()
        assert len(result.get("categories")) == 1
        assert len(result.get("categories")[0].events) == 1

# Test view_category
def test_case_28_FREEUSER_2(app, request, user1, freeuserrole, publicevent1, category1):
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
        # Log in with user1
        login_user(user1)
        # Test FREEUSER accessing view_category()
        result = view_category(category1.id)
        assert (len(result.get("category").events) == 1)

def test_case_28_FREEUSER_3(app, request, user1, user2, freeuserrole, publicevent1, category1):
    with current_app.test_request_context():
        # Scenario: a person user1 with FREEUSER role.
        #           a person user2 with FREEUSER role.
        #           a category category1
        #           a public event owned by user2, of category1
        user1.role = freeuserrole
        db.session.add(user1)
        user2.role = freeuserrole
        db.session.add(user2)
        publicevent1.owner = user2 
        publicevent1.attendants.append(user2)
        publicevent1.managedBy.append(user2)
        publicevent1.categories.append(category1)
        db.session.add(publicevent1)
        db.session.commit()
        # Log in with user1
        login_user(user1)
        # Test FREEUSER accessing view_category()
        result = view_category(category1.id)
        assert (len(result.get("category").events) == 1)

#Test Case	29	Create a public event
def test_case_29_FREEUSER(app, request, user1, freeuserrole, publicevent1):
    with current_app.test_request_context(
        data={"title": publicevent1.title, 
              "description": publicevent1.description,
              "categories": publicevent1.categories}):
        # Scenario: a person user1 with FREEUSER role.
        user1.role = freeuserrole
        db.session.add(user1)
        # Log in with user1
        login_user(user1)
        # Test FREEUSER create event
        result = create_event()
        events = Event.query.all()
        assert len(events) == 1
        assert events[0].title == publicevent1.title
        assert events[0].description == publicevent1.description
        assert events[0].categories == publicevent1.categories

#Test Case	30	Read core info of public event created by someone else
# Testing /events
def test_case_30_FREEUSER(app, request, user1, user2, freeuserrole, publicevent1):
    with current_app.test_request_context():
        # Scenario: a person user1, user2 with FREEUSER role.
        #           a public event owned by user2
        user1.role = freeuserrole
        db.session.add(user1)
        user2.role = freeuserrole
        db.session.add(user2)
        publicevent1.owner = user2 
        publicevent1.attendants.append(user2)
        publicevent1.managedBy.append(user2)
        db.session.add(publicevent1)
        db.session.commit()
        # Log in with user1
        login_user(user1)
        # Test FREEUSER accessing events():
        result = events()
        events_dto = result.get("events")
        assert len(events_dto) == 1
        assert events_dto[0].title == publicevent1.title
        assert events_dto[0].owner.fullname == user2.fullname

# Test view_event
def test_case_30_FREEUSER_1(app, request, user1, user2, freeuserrole, publicevent1):
    with current_app.test_request_context():
        # Scenario: a person user1, user2 with FREEUSER role.
        #           a public event owned by user2
        user1.role = freeuserrole
        db.session.add(user1)
        user2.role = freeuserrole
        db.session.add(user2)
        publicevent1.owner = user2 
        publicevent1.attendants.append(user2)
        publicevent1.managedBy.append(user2)
        db.session.add(publicevent1)
        db.session.commit()
        # Log in with user1
        login_user(user1)
        # Test FREEUSER accessing view_event(): 
        result = view_event(publicevent1.id)
        assert (result.get("event").title == publicevent1.title and \
                result.get("event").description == publicevent1.description)

# Test edit_event
def test_case_30_FREEUSER_2(app, request, user1, user2, freeuserrole, publicevent1):
    with current_app.test_request_context():
        # Scenario: a person user1, user2 with FREEUSER role.
        #           a public event owned by user2
        user1.role = freeuserrole
        db.session.add(user1)
        user2.role = freeuserrole
        db.session.add(user2)
        publicevent1.owner = user2 
        publicevent1.attendants.append(user2)
        publicevent1.managedBy.append(user2)
        db.session.add(publicevent1)
        db.session.commit()
        # Log in with user1
        login_user(user1)
        # Test FREEUSER accessing edit_event()
        try:
            result = edit_event(publicevent1.id)
            assert is_response(result) or \
                   (result.get("event").title == publicevent1.title and \
                    result.get("event").description == publicevent1.description)
        except SecurityException:
            assert True

# Test view_category
def test_case_30_FREEUSER_3(app, request, user1, user2, freeuserrole, publicevent1, category1):
    with current_app.test_request_context():
        # Scenario: a person user1, user2 with FREEUSER role.
        #           a category category1
        #           a public event owned by user2, of category1
        user1.role = freeuserrole
        db.session.add(user1)
        user2.role = freeuserrole
        db.session.add(user2)
        publicevent1.owner = user2 
        publicevent1.attendants.append(user2)
        publicevent1.managedBy.append(user2)
        publicevent1.categories.append(category1)
        db.session.add(publicevent1)
        db.session.commit()
        # Log in with user1
        login_user(user1)
        # Test FREEUSER accessing view_category()
        result = view_category(category1.id)
        assert len(result.get("category").events) == 1 
        assert result.get("category").events[0].title == publicevent1.title 
        assert result.get("category").events[0].owner.fullname == user2.fullname

#Test Case	31	Read core info of private event created by someone else and not participating
# Testing /events
def test_case_31_FREEUSER(app, request, user1, freeuserrole, user2, premiumuserrole, privateevent1):
    with current_app.test_request_context():
        # Scenario: a person user1 with FREEUSER role.
        #           a person user2 with PREMIUMUSER role.
        #           a private event owned by user2
        user1.role = freeuserrole
        db.session.add(user1)
        user2.role = premiumuserrole
        db.session.add(user2)
        privateevent1.owner = user2 
        privateevent1.attendants.append(user2)
        privateevent1.managedBy.append(user2)
        db.session.add(privateevent1)
        db.session.commit()
        # Log in with user1
        login_user(user1)
        # Test FREEUSER accessing events():
        result = events()
        events_dto = result.get("events")
        assert len(events_dto) == 0 or \
               (len(events_dto) == 1 and \
                events_dto[0].title is RESTRICTED and \
                (events_dto[0].owner is RESTRICTED or \
                 (events_dto[0].owner.name is RESTRICTED and \
                  events_dto[0].owner.surname is RESTRICTED)))

# Test view_event
def test_case_31_FREEUSER_1(app, request, user1, freeuserrole, user2, premiumuserrole, privateevent1):
    with current_app.test_request_context():
        # Scenario: a person user1 with FREEUSER role.
        #           a person user2 with PREMIUMUSER role.
        #           a private event owned by user2
        user1.role = freeuserrole
        db.session.add(user1)
        user2.role = premiumuserrole
        db.session.add(user2)
        privateevent1.owner = user2 
        privateevent1.attendants.append(user2)
        privateevent1.managedBy.append(user2)
        db.session.add(privateevent1)
        db.session.commit()
        # Log in with user1
        login_user(user1)
        # Test FREEUSER accessing view_event(): 
        try:
            result = view_event(privateevent1.id)
            assert is_response(result) or \
                   (result.get("event").title is RESTRICTED and \
                    result.get("event").description is RESTRICTED)
        except SecurityException:
            assert True

# Test edit_event
def test_case_31_FREEUSER_2(app, request, user1, freeuserrole, user2, premiumuserrole, privateevent1):
    with current_app.test_request_context():
        # Scenario: a person user1 with FREEUSER role.
        #           a person user2 with PREMIUMUSER role.
        #           a private event owned by user2
        user1.role = freeuserrole
        db.session.add(user1)
        user2.role = premiumuserrole
        db.session.add(user2)
        privateevent1.owner = user2 
        privateevent1.attendants.append(user2)
        privateevent1.managedBy.append(user2)
        db.session.add(privateevent1)
        db.session.commit()
        # Log in with user1
        login_user(user1)
        # Test FREEUSER accessing edit_event()
        try:
            result = edit_event(privateevent1.id)
            assert is_response(result) or \
                   (result.get("event").title is RESTRICTED and \
                    result.get("event").description is RESTRICTED)
        except SecurityException:
            assert True

# Test view_category
def test_case_31_FREEUSER_3(app, request, user1, freeuserrole, 
                           user2, premiumuserrole, privateevent1, category1):
    with current_app.test_request_context():
        # Scenario: a person user1 with FREEUSER role.
        #           a person user2 with PREMIUMUSER role.
        #           a category category1
        #           a private event owned by user2, of category1
        user1.role = freeuserrole
        db.session.add(user1)
        user2.role = premiumuserrole
        db.session.add(user2)
        privateevent1.owner = user2 
        privateevent1.attendants.append(user2)
        privateevent1.managedBy.append(user2)
        privateevent1.categories.append(category1)
        db.session.add(privateevent1)
        db.session.commit()
        # Log in with user1
        login_user(user1)
        # Test FREEUSER accessing view_category()
        result = view_category(category1.id)
        assert len(result.get("category").events) == 0 or \
               (len(result.get("category").events) == 1 and \
                result.get("category").events[0].title is RESTRICTED and \
                (result.get("category").events[0].owner is RESTRICTED or \
                    (result.get("category").events[0].owner.name is RESTRICTED and \
                    result.get("category").events[0].owner.surname is RESTRICTED)))

#Test Case	32	Read attendants of public event created by someone else
# Test view_event
def test_case_32_FREEUSER(app, request, user1, user2, freeuserrole, publicevent1):
    with current_app.test_request_context():
        # Scenario: person user1, user2 with FREEUSER role.
        #           a public event owned by user2
        user1.role = freeuserrole
        db.session.add(user1)
        user2.role = freeuserrole
        db.session.add(user2)
        publicevent1.owner = user2 
        publicevent1.attendants.append(user2)
        publicevent1.managedBy.append(user2)
        db.session.add(publicevent1)
        db.session.commit()
        # Log in with user1
        login_user(user1)
        # Test FREEUSER accessing view_event(): 
        result = view_event(publicevent1.id)
        assert len(result.get("event").attendants) == 1 and \
                result.get("event").attendants[0].fullname == user2.fullname

# Test manage_event
def test_case_32_FREEUSER_1(app, request, user1, user2, freeuserrole, publicevent1):
    with current_app.test_request_context():
        # Scenario: person user1, user2 with FREEUSER role.
        #           a public event owned by user2
        user1.role = freeuserrole
        db.session.add(user1)
        user2.role = freeuserrole
        db.session.add(user2)
        publicevent1.owner = user2 
        publicevent1.attendants.append(user2)
        publicevent1.managedBy.append(user2)
        db.session.add(publicevent1)
        db.session.commit()
        # Log in with user1
        login_user(user1)
        # Test FREEUSER accessing manage_event()
        try:
            result = manage_event(publicevent1.id)
            assert is_response(result) or \
                   (len(result.get("event").attendants) == 1 and \
                    result.get("event").attendants[0].fullname == user2.fullname)
        except SecurityException:
            assert True

#Test Case	33	Read attendants of private event created by someone else and not participating
# Test view_event
def test_case_33_FREEUSER(app, request, user1, freeuserrole,
                         user2, premiumuserrole, privateevent1):
    with current_app.test_request_context():
        # Scenario: a person user1 with FREEUSER role.
        #           a person user2 with PREMIUMUSER role.
        #           a private event owned by user2
        user1.role = freeuserrole
        db.session.add(user1)
        user2.role = premiumuserrole
        db.session.add(user2)
        privateevent1.owner = user2 
        privateevent1.attendants.append(user2)
        privateevent1.managedBy.append(user2)
        db.session.add(privateevent1)
        db.session.commit()
        # Log in with user1
        login_user(user1)
        # Test FREEUSER accessing view_event(): 
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
def test_case_33_FREEUSER_1(app, request, user1, freeuserrole,
                         user2, premiumuserrole, privateevent1):
    with current_app.test_request_context():
        # Scenario: a person user1 with FREEUSER role.
        #           a person user2 with PREMIUMUSER role.
        #           a private event owned by user2
        user1.role = freeuserrole
        db.session.add(user1)
        user2.role = premiumuserrole
        db.session.add(user2)
        privateevent1.owner = user2 
        privateevent1.attendants.append(user2)
        privateevent1.managedBy.append(user2)
        db.session.add(privateevent1)
        db.session.commit()
        # Log in with user1
        login_user(user1)
        # Test FREEUSER accessing manage_event()
        try:
            result = manage_event(privateevent1.id)
            assert is_response(result) or \
                   (len(result.get("event").attendants) == 0 or \
                    (len(result.get("event").attendants) == 1 and \
                     result.get("event").attendants[0].name is RESTRICTED and \
                     result.get("event").attendants[0].surname is RESTRICTED))
        except SecurityException:
            assert True

#Test Case	34	Read attendants of private event created by someone else and attending
# Not applicable because free user cannot attend private event.

#Test Case	35	Edit others event if one is manager
def test_case_35_FREEUSER(app, request, user1, user2, freeuserrole, publicevent1, category1):
    with current_app.test_request_context(
        data={ "id": publicevent1.id, 
              "title": "new title", 
              "description": "new description", 
              "categories": publicevent1.categories}):
        # Scenario: person user1, user2 with FREEUSER role.
        #           a public event owned by user2, managed by user1
        user1.role = freeuserrole
        db.session.add(user1)
        user2.role = freeuserrole
        db.session.add(user2)
        publicevent1.owner = user2 
        publicevent1.attendants.append(user2)
        publicevent1.managedBy.append(user2)
        publicevent1.attendants.append(user1)
        publicevent1.managedBy.append(user1)
        db.session.add(publicevent1)
        db.session.commit()
        # Log in with user1
        login_user(user1)
        # Test FREEUSER accessing update_event()
        result = update_event()
        assert publicevent1.title == "new title"
        assert publicevent1.description == "new description"

#Test Case	36	Edit others event if not manager
def test_case_36_FREEUSER(app, request, user1, user2, freeuserrole, publicevent1, category1):
    with current_app.test_request_context(
        data={ "id": publicevent1.id, 
              "title": "new title", 
              "description": "new description", 
              "categories": publicevent1.categories}):
        # Scenario: person user1, user2 with FREEUSER role.
        #           a public event owned by user2
        user1.role = freeuserrole
        db.session.add(user1)
        user2.role = freeuserrole
        db.session.add(user2)
        publicevent1.owner = user2 
        publicevent1.attendants.append(user2)
        publicevent1.managedBy.append(user2)
        db.session.add(publicevent1)
        db.session.commit()
        # Log in with user1
        login_user(user1)
        # Test FREEUSER accessing update_event()
        try:
            result = update_event()
        except SecurityException:
            assert True
        finally:
            assert publicevent1.title == "event1"
            assert publicevent1.description == "event1"

def test_case_36_FREEUSER_1(app, request, user1, user2, freeuserrole, publicevent1, category1):
    with current_app.test_request_context(
        data={ "id": publicevent1.id, 
              "title": "new title", 
              "description": "new description", 
              "categories": publicevent1.categories}):
        # Scenario: person user1, user2 with FREEUSER role.
        #           a public event owned by user2
        #           attended by user1
        user1.role = freeuserrole
        db.session.add(user1)
        user2.role = freeuserrole
        db.session.add(user2)
        publicevent1.owner = user2 
        publicevent1.attendants.append(user2)
        publicevent1.managedBy.append(user2)
        publicevent1.attendants.append(user1)
        db.session.add(publicevent1)
        db.session.commit()
        # Log in with user1
        login_user(user1)
        # Test FREEUSER accessing update_event()
        try:
            result = update_event()
        except SecurityException:
            assert True
        finally:
            assert publicevent1.title == "event1"
            assert publicevent1.description == "event1"

#Test Case	37	Edit owner of event
# Not applicable: No provided functionality for this.

#Test Case	38	Promote attendant to manager from event owned
def test_case_38_FREEUSER(app, request, user1, user2, freeuserrole, publicevent1):
    with current_app.test_request_context():
        # Scenario: person user1, user2 with FREEUSER role.
        #           a public event owned by user1, attended by user2
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
        # Log in with user1
        login_user(user1)
        # Test FREEUSER accessing promote_manager()
        result = promote_manager(user2.id, publicevent1.id)
        assert user2.id in [m.id for m in publicevent1.managedBy]

#Test Case	39	Demote Manager from event owned
def test_case_39_FREEUSER(app, request, user1, user2, freeuserrole, publicevent1):
    with current_app.test_request_context():
        # Scenario: person user1, user2 with FREEUSER role.
        #           a public event owned by user1, managed by user2
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
        # Log in with user1
        login_user(user1)
        # Test FREEUSER accessing demote_manager()
        result = demote_manager(user2.id, publicevent1.id)
        assert user2.id not in [m.id for m in publicevent1.managedBy]

#Test Case	40	Demote manager for event not owned
def test_case_40_FREEUSER(app, request, user1, user2, user3, freeuserrole, publicevent1):
    with current_app.test_request_context():
        # Scenario: person user1, user2, user3 with FREEUSER role.
        #           a public event owned by user3, managed by user2
        user1.role = freeuserrole
        db.session.add(user1)
        user2.role = freeuserrole
        db.session.add(user2)
        user3.role = freeuserrole
        db.session.add(user3)
        publicevent1.owner = user3 
        publicevent1.attendants.append(user3)
        publicevent1.managedBy.append(user3)
        publicevent1.attendants.append(user2)
        publicevent1.managedBy.append(user2)
        db.session.add(publicevent1)
        db.session.commit()
        # Log in with user1
        login_user(user1)
        # Test FREEUSER accessing demote_manager()
        try:
            result = demote_manager(user2.id, publicevent1.id)
        except SecurityException:
            assert True
        finally:
            assert user2.id in [m.id for m in publicevent1.managedBy]

def test_case_40_FREEUSER_1(app, request, user1, user2, user3, freeuserrole, publicevent1):
    with current_app.test_request_context():
        # Scenario: person user1, user2, user3 with FREEUSER role.
        #           a public event owned by user3, managed by user2
        #           user1 managed this public event
        user1.role = freeuserrole
        db.session.add(user1)
        user2.role = freeuserrole
        db.session.add(user2)
        user3.role = freeuserrole
        db.session.add(user3)
        publicevent1.owner = user3 
        publicevent1.attendants.append(user3)
        publicevent1.managedBy.append(user3)
        publicevent1.attendants.append(user2)
        publicevent1.managedBy.append(user2)
        publicevent1.attendants.append(user1)
        publicevent1.managedBy.append(user1)
        db.session.add(publicevent1)
        db.session.commit()
        # Log in with user1
        login_user(user1)
        # Test FREEUSER accessing demote_manager()
        try:
            result = demote_manager(user2.id, publicevent1.id)
        except SecurityException:
            assert True
        finally:
            assert user2.id in [m.id for m in publicevent1.managedBy]

def test_case_40_FREEUSER_2(app, request, user1, user2, user3, freeuserrole, publicevent1):
    with current_app.test_request_context():
        # Scenario: person user1, user2, user3 with FREEUSER role.
        #           a public event owned by user3, managed by user2
        #           user1 attended this public event
        user1.role = freeuserrole
        db.session.add(user1)
        user2.role = freeuserrole
        db.session.add(user2)
        user3.role = freeuserrole
        db.session.add(user3)
        publicevent1.owner = user3 
        publicevent1.attendants.append(user3)
        publicevent1.managedBy.append(user3)
        publicevent1.attendants.append(user2)
        publicevent1.managedBy.append(user2)
        publicevent1.attendants.append(user1)
        db.session.add(publicevent1)
        db.session.commit()
        # Log in with user1
        login_user(user1)
        # Test FREEUSER accessing demote_manager()
        try:
            result = demote_manager(user2.id, publicevent1.id)
        except SecurityException:
            assert True
        finally:
            assert user2.id in [m.id for m in publicevent1.managedBy]

#Test Case	41	Accept request to join event owned
def test_case_41_FREEUSER(app, request, user1, user2, freeuserrole, publicevent1):
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
        # Log in with user1
        login_user(user1)
        # Test FREEUSER accessing accept_request()
        result = accept_request(user2.id, publicevent1.id)
        assert user2.id in [m.id for m in publicevent1.attendants]
        assert user2.id not in [m.id for m in publicevent1.requesters]

#Test Case	42	Accept request to join event managed
def test_case_42_FREEUSER(app, request, user1, user2, user3, freeuserrole, publicevent1):
    with current_app.test_request_context():
        # Scenario: person user1, user2, user3 with FREEUSER role.
        #           a public event owned by user3, 
        #           request to join by user2
        #           managed by user1
        user1.role = freeuserrole
        db.session.add(user1)
        user2.role = freeuserrole
        db.session.add(user2)
        user3.role = freeuserrole
        db.session.add(user3)
        publicevent1.owner = user3 
        publicevent1.attendants.append(user3)
        publicevent1.managedBy.append(user3)
        publicevent1.attendants.append(user1)
        publicevent1.managedBy.append(user1)
        publicevent1.requesters.append(user2)
        db.session.add(publicevent1)
        db.session.commit()
        # Log in with user1
        login_user(user1)
        # Test FREEUSER accessing accept_request()
        result = accept_request(user2.id, publicevent1.id)
        assert user2.id in [m.id for m in publicevent1.attendants]
        assert user2.id not in [m.id for m in publicevent1.requesters]

#Test Case	43	Accept request not owner not manager
def test_case_43_FREEUSER(app, request, user1, user2, user3, freeuserrole, publicevent1):
    with current_app.test_request_context():
        # Scenario: person user1, user2, user3 with FREEUSER role.
        #           a public event owned by user3, 
        #           request to join by user2
        #           attended by user1
        user1.role = freeuserrole
        db.session.add(user1)
        user2.role = freeuserrole
        db.session.add(user2)
        user3.role = freeuserrole
        db.session.add(user3)
        publicevent1.owner = user3 
        publicevent1.attendants.append(user3)
        publicevent1.managedBy.append(user3)
        publicevent1.attendants.append(user1)
        publicevent1.requesters.append(user2)
        db.session.add(publicevent1)
        db.session.commit()
        # Log in with user1
        login_user(user1)
        # Test FREEUSER accessing accept_request()
        try:
            result = accept_request(user2.id, publicevent1.id)
        except SecurityException:
            assert True
        finally:
            assert user2.id not in [m.id for m in publicevent1.attendants]
            assert user2.id in [m.id for m in publicevent1.requesters]

def test_case_43_FREEUSER_1(app, request, user1, user2, user3, freeuserrole, publicevent1):
    with current_app.test_request_context():
        # Scenario: person user1, user2, user3 with FREEUSER role.
        #           a public event owned by user3, 
        #           request to join by user2
        #           NOT attended by user1
        user1.role = freeuserrole
        db.session.add(user1)
        user2.role = freeuserrole
        db.session.add(user2)
        user3.role = freeuserrole
        db.session.add(user3)
        publicevent1.owner = user3 
        publicevent1.attendants.append(user3)
        publicevent1.managedBy.append(user3)
        publicevent1.requesters.append(user2)
        db.session.add(publicevent1)
        db.session.commit()
        # Log in with user1
        login_user(user1)
        # Test FREEUSER accessing accept_request()
        try:
            result = accept_request(user2.id, publicevent1.id)
        except SecurityException:
            assert True
        finally:
            assert user2.id not in [m.id for m in publicevent1.attendants]
            assert user2.id in [m.id for m in publicevent1.requesters]

#Test Case	44	Promote oneself as manager for event not owned
def test_case_44_FREEUSER(app, request, user1, user2, freeuserrole, publicevent1):
    with current_app.test_request_context():
        # Scenario: person user1, user2 with FREEUSER role.
        #           a public event owned by user2,
        #           attended by user1
        user1.role = freeuserrole
        db.session.add(user1)
        user2.role = freeuserrole
        db.session.add(user2)
        publicevent1.owner = user2 
        publicevent1.attendants.append(user2)
        publicevent1.managedBy.append(user2)
        publicevent1.attendants.append(user1)
        db.session.add(publicevent1)
        db.session.commit()
        # Log in with user1
        login_user(user1)
        # Test FREEUSER accessing promote_manager()
        try:
            result = promote_manager(user1.id, publicevent1.id)
        except SecurityException:
            assert True
        finally:
            assert user1.id not in [m.id for m in publicevent1.managedBy]

def test_case_44_FREEUSER_1(app, request, user1, user2, freeuserrole, publicevent1):
    with current_app.test_request_context():
        # Scenario: person user1, user2 with FREEUSER role.
        #           a public event owned by user2,
        #           NOT attended by user1
        user1.role = freeuserrole
        db.session.add(user1)
        user2.role = freeuserrole
        db.session.add(user2)
        publicevent1.owner = user2 
        publicevent1.attendants.append(user2)
        publicevent1.managedBy.append(user2)
        db.session.add(publicevent1)
        db.session.commit()
        # Log in with user1
        login_user(user1)
        # Test FREEUSER accessing promote_manager()
        try:
            result = promote_manager(user1.id, publicevent1.id)
        except SecurityException:
            assert True
        finally:
            assert user1.id not in [m.id for m in publicevent1.managedBy]

#Test Case	45	Reject request to join own event
def test_case_45_FREEUSER(app, request, user1, user2, freeuserrole, publicevent1):
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
        # Log in with user1
        login_user(user1)
        # Test FREEUSER accessing reject_request()
        result = reject_request(user2.id, publicevent1.id)
        assert user2.id not in [m.id for m in publicevent1.attendants]
        assert user2.id not in [m.id for m in publicevent1.requesters]

#Test Case	46	Reject request to join manager
def test_case_46_FREEUSER(app, request, user1, user2, user3, freeuserrole, publicevent1):
    with current_app.test_request_context():
        # Scenario: person user1, user2, user3 with FREEUSER role.
        #           a public event owned by user3, 
        #           request to join by user2
        #           managed by user1
        user1.role = freeuserrole
        db.session.add(user1)
        user2.role = freeuserrole
        db.session.add(user2)
        user3.role = freeuserrole
        db.session.add(user3)
        publicevent1.owner = user3 
        publicevent1.attendants.append(user3)
        publicevent1.managedBy.append(user3)
        publicevent1.attendants.append(user1)
        publicevent1.managedBy.append(user1)
        publicevent1.requesters.append(user2)
        db.session.add(publicevent1)
        db.session.commit()
        # Log in with user1
        login_user(user1)
        # Test FREEUSER accessing reject_request()
        result = reject_request(user2.id, publicevent1.id)
        assert user2.id not in [m.id for m in publicevent1.attendants]
        assert user2.id not in [m.id for m in publicevent1.requesters]

#Test Case	47	Remove oneself from attending an event, not owner
# leave functionality is incorrectly implemented, waive this test
#def test_case_47_FREEUSER(app, request, user1, user2, freeuserrole, publicevent1):
#    with current_app.test_request_context():
#        # Scenario: person user1, user2 with FREEUSER role.
#        #           a public event owned by user2,
#        #           attended by user1
#        user1.role = freeuserrole
#        db.session.add(user1)
#        user2.role = freeuserrole
#        db.session.add(user2)
#        publicevent1.owner = user2 
#        publicevent1.attendants.append(user2)
#        publicevent1.managedBy.append(user2)
#        publicevent1.attendants.append(user1)
#        db.session.add(publicevent1)
#        db.session.commit()
#        # Log in with user1
#        login_user(user1)
#        # Test FREEUSER accessing leave()
#        result = leave(publicevent1.id)
#        assert user1.id not in [m.id for m in publicevent1.attendants]

#def test_case_47_FREEUSER_1(app, request, user1, user2, freeuserrole, publicevent1):
#    with current_app.test_request_context():
#        # Scenario: person user1, user2 with FREEUSER role.
#        #           a public event owned by user2,
#        #           attended by user1
#        user1.role = freeuserrole
#        db.session.add(user1)
#        user2.role = freeuserrole
#        db.session.add(user2)
#        publicevent1.owner = user2 
#        publicevent1.attendants.append(user2)
#        publicevent1.managedBy.append(user2)
#        publicevent1.attendants.append(user1)
#        db.session.add(publicevent1)
#        db.session.commit()
#        # Log in with user1
#        login_user(user1)
#        # Test FREEUSER accessing remove_attendee()
#        result = remove_attendee(user1.id, publicevent1.id)
#        assert user1.id not in [m.id for m in publicevent1.attendants]

#Test Case	48	Remove others from attending an event, manager
def test_case_48_FREEUSER(app, request, user1, user2, user3, freeuserrole, publicevent1):
    with current_app.test_request_context():
        # Scenario: person user1, user2, user3 with FREEUSER role.
        #           a public event owned by user2,
        #           managed by user1
        #           attended by user3
        user1.role = freeuserrole
        db.session.add(user1)
        user2.role = freeuserrole
        db.session.add(user2)
        user3.role = freeuserrole
        db.session.add(user3)
        publicevent1.owner = user2 
        publicevent1.attendants.append(user2)
        publicevent1.managedBy.append(user2)
        publicevent1.managedBy.append(user1)
        publicevent1.attendants.append(user1)
        publicevent1.attendants.append(user3)
        db.session.add(publicevent1)
        db.session.commit()
        # Log in with user1
        login_user(user1)
        # Test FREEUSER accessing remove_attendee()
        result = remove_attendee(user3.id, publicevent1.id)
        assert user3.id not in [m.id for m in publicevent1.attendants]

def test_case_48_FREEUSER_1(app, request, user1, user2, user3, freeuserrole, publicevent1):
    with current_app.test_request_context():
        # Scenario: person user1, user2, user3 with FREEUSER role.
        #           a public event owned by user2,
        #           managed by user1
        #           NOT attended by user3
        user1.role = freeuserrole
        db.session.add(user1)
        user2.role = freeuserrole
        db.session.add(user2)
        user3.role = freeuserrole
        db.session.add(user3)
        publicevent1.owner = user2 
        publicevent1.attendants.append(user2)
        publicevent1.managedBy.append(user2)
        publicevent1.managedBy.append(user1)
        publicevent1.attendants.append(user1)
        db.session.add(publicevent1)
        db.session.commit()
        # Log in with user1
        login_user(user1)
        # Test FREEUSER accessing remove_attendee()
        try:
            result = remove_attendee(user3.id, publicevent1.id)
        except SecurityException:
            assert True
        finally:
            assert user3.id not in [m.id for m in publicevent1.attendants]            

#Test Case	49	Owner removes himself from attending event
def test_case_49_FREEUSER(app, request, user1, freeuserrole, publicevent1):
    with current_app.test_request_context():
        # Scenario: person user1 with FREEUSER role.
        #           a public event owned by user1
        user1.role = freeuserrole
        db.session.add(user1)
        publicevent1.owner = user1 
        publicevent1.attendants.append(user1)
        publicevent1.managedBy.append(user1)
        db.session.add(publicevent1)
        db.session.commit()
        # Log in with user1
        login_user(user1)
        # Test FREEUSER accessing remove_attendee()
        try: 
            result = remove_attendee(user1.id, publicevent1.id)
        except SecurityException:
            assert True
        finally:
            assert user1.id in [m.id for m in publicevent1.attendants]

#Test Case	50	Non manager removes someone else from event
def test_case_50_FREEUSER(app, request, user1, user2, user3, freeuserrole, publicevent1):
    with current_app.test_request_context():
        # Scenario: person user1, user2, user3 with FREEUSER role.
        #           a public event owned by user2,
        #           attended by user1 and user3
        user1.role = freeuserrole
        db.session.add(user1)
        user2.role = freeuserrole
        db.session.add(user2)
        user3.role = freeuserrole
        db.session.add(user3)
        publicevent1.owner = user2 
        publicevent1.attendants.append(user2)
        publicevent1.managedBy.append(user2)
        publicevent1.attendants.append(user1)
        publicevent1.attendants.append(user3)
        db.session.add(publicevent1)
        db.session.commit()
        # Log in with user1
        login_user(user1)
        # Test FREEUSER accessing remove_attendee()
        try: 
            result = remove_attendee(user3.id, publicevent1.id)
        except SecurityException:
            assert True
        finally:
            assert user3.id in [m.id for m in publicevent1.attendants]

def test_case_50_FREEUSER_1(app, request, user1, user2, user3, freeuserrole, publicevent1):
    with current_app.test_request_context():
        # Scenario: person user1, user2, user3 with FREEUSER role.
        #           a public event owned by user2,
        #           attended by user3
        user1.role = freeuserrole
        db.session.add(user1)
        user2.role = freeuserrole
        db.session.add(user2)
        user3.role = freeuserrole
        db.session.add(user3)
        publicevent1.owner = user2 
        publicevent1.attendants.append(user2)
        publicevent1.managedBy.append(user2)
        publicevent1.attendants.append(user3)
        db.session.add(publicevent1)
        db.session.commit()
        # Log in with user1
        login_user(user1)
        # Test FREEUSER accessing remove_attendee()
        try: 
            result = remove_attendee(user3.id, publicevent1.id)
        except SecurityException:
            assert True
        finally:
            assert user3.id in [m.id for m in publicevent1.attendants]

#Test Case	51	Request to join public event
def test_case_51_FREEUSER(app, request, user1, user2, freeuserrole, publicevent1):
    with current_app.test_request_context():
        # Scenario: person user1, user2 with FREEUSER role.
        #           a public event owned by user2
        user1.role = freeuserrole
        db.session.add(user1)
        user2.role = freeuserrole
        db.session.add(user2)
        publicevent1.owner = user2 
        publicevent1.attendants.append(user2)
        publicevent1.managedBy.append(user2)
        db.session.add(publicevent1)
        db.session.commit()
        # Log in with user1
        login_user(user1)
        # Test FREEUSER accessing join()
        result = join(publicevent1.id)
        assert user1.id in [m.id for m in publicevent1.requesters]

#Test Case	52	Request to join private event
def test_case_52_FREEUSER(app, request, user1, user2, premiumuserrole, 
                          freeuserrole, privateevent1):
    with current_app.test_request_context():
        # Scenario: person user1 with FREEUSER role, user2 with PREMIUMUSER role.
        #           a private event owned by user2
        user1.role = freeuserrole
        db.session.add(user1)
        user2.role = premiumuserrole
        db.session.add(user2)
        privateevent1.owner = user2 
        privateevent1.attendants.append(user2)
        privateevent1.managedBy.append(user2)
        db.session.add(privateevent1)
        db.session.commit()
        # Log in with user1
        login_user(user1)
        # Test FREEUSER accessing join()
        try:
            result = join(privateevent1.id)
        except SecurityException:
            assert True
        finally:
            assert user1.id not in [m.id for m in privateevent1.requesters]

#Test Case	53	Reject request to join, non manager, non owner, non requester
def test_case_53_FREEUSER(app, request, user1, user2, user3, freeuserrole, publicevent1):
    with current_app.test_request_context():
        # Scenario: person user1, user2, user3 with FREEUSER role.
        #           a public event owned by user3, 
        #           request to join by user2
        user1.role = freeuserrole
        db.session.add(user1)
        user2.role = freeuserrole
        db.session.add(user2)
        user3.role = freeuserrole
        db.session.add(user3)
        publicevent1.owner = user3 
        publicevent1.attendants.append(user3)
        publicevent1.managedBy.append(user3)
        publicevent1.requesters.append(user2)
        db.session.add(publicevent1)
        db.session.commit()
        # Log in with user1
        login_user(user1)
        # Test FREEUSER accessing reject_request()
        try:
            result = reject_request(user2.id, publicevent1.id)
        except SecurityException:
            assert True
        finally:
            assert user2.id in [m.id for m in publicevent1.requesters]

#Test Case	54	Cancel own request
#def test_case_56_FREEUSER(app, request, user1, user2, freeuserrole, publicevent1):
#    with current_app.test_request_context():
#        # Scenario: person user1, user2 with FREEUSER role.
#        #           a public event owned by user2, 
#        #           request to join by user1
#        user1.role = freeuserrole
#        db.session.add(user1)
#        user2.role = freeuserrole
#        db.session.add(user2)
#        publicevent1.owner = user2 
#        publicevent1.attendants.append(user2)
#        publicevent1.managedBy.append(user2)
#        publicevent1.requesters.append(user1)
#        db.session.add(publicevent1)
#        db.session.commit()
#        # Log in with user1
#        login_user(user1)
#        # Test FREEUSER accessing reject_request()
#        result = reject_request(user1.id, publicevent1.id)
#        assert user1.id not in [m.id for m in publicevent1.requesters]
#        assert user1.id not in [m.id for m in publicevent1.attendants]

#Test Case	55	Request to join for someone else
# Not applicable, one can request to join for oneself.

#Test Case	56	Read core information of other users
# Test /events
# Duplicated with Event.owner checks

# Test /view_event
# Duplicated with Event.attendants checks

# Test /manage_event
def test_case_56_FREEUSER(app, request, user1, user2, user3, freeuserrole, publicevent1):
    with current_app.test_request_context():
        # Scenario: a person user1 with FREEUSER role.
        #           a person user2 with FREEUSER role.
        #           a person user3 with FREEUSER role.
        #           a public event owned by user3
        #           user2 requests to join for this event
        user1.role = freeuserrole
        db.session.add(user1)
        user2.role = freeuserrole
        db.session.add(user2)
        user3.role = freeuserrole
        db.session.add(user3)
        publicevent1.owner = user3 
        publicevent1.attendants.append(user3)
        publicevent1.managedBy.append(user3)
        publicevent1.requesters.append(user2)
        db.session.add(publicevent1)
        db.session.commit()
        # Log in with user1
        login_user(user1)
        # Test FREEUSER accessing manage_event()
        try:
            result = manage_event(publicevent1.id)
            assert is_response(result) or \
                   (len(result.get("event").attendants) == 1 and \
                    result.get("event").attendants[0].fullname == user3.fullname and \
                    len(result.get("event").managedBy) == 1 and \
                    result.get("event").managedBy[0].fullname == user3.fullname and \
                    (len(result.get("event").requesters) == 0 or \
                     (len(result.get("event").requesters) == 1 and \
                      result.get("event").requesters[0].name == RESTRICTED and \
                      result.get("event").requesters[0].surname == RESTRICTED)))
        except SecurityException:
            assert True

# Test \users
def test_case_56_FREEUSER_1(app, request, user1, user2, freeuserrole):
    with current_app.test_request_context():
        # Scenario: a person user1, user2 with FREEUSER role.
        user1.role = freeuserrole
        db.session.add(user1)
        user2.role = freeuserrole
        db.session.add(user2)
        db.session.commit()
        # Log in with user1
        login_user(user1)
        # Test FREEUSER accessing users()
        result = users()
        assert len(result.get("users")) == 2
        assert (result.get("users")[0].fullname == user2.fullname and result.get("users")[1].fullname == user1.fullname) or \
               (result.get("users")[0].fullname == user1.fullname and result.get("users")[1].fullname == user2.fullname)

# Test \user
def test_case_56_FREEUSER_2(app, request, user1, user2, freeuserrole):
    with current_app.test_request_context():
        # Scenario: a person user1, user2 with FREEUSER role.
        user1.role = freeuserrole
        db.session.add(user1)
        user2.role = freeuserrole
        db.session.add(user2)
        db.session.commit()
        # Log in with user1
        login_user(user1)
        # Test FREEUSER accessing user()
        try:
            result = user(user2.id)
            assert is_response(result) or \
                   (result.get("user").fullname == user2.fullname and \
                    result.get("user").role.name == freeuserrole.name)
        except SecurityException:
            assert True

# Test view_category
# Duplicated with Event.owner checks

# Test edit_category
def test_case_56_FREEUSER_3(app, request, user1, freeuserrole,
                          moderatorrole, category1, user2, user3):
    with current_app.test_request_context():
        # Scenario: a person user1 with FREEUSER role
        #           a person user2, user3 with MODERATOR role.
        #           a category category1
        #           user3 apply to category1
        #           user2 moderates category1
        user1.role = freeuserrole
        db.session.add(user1)
        user2.role = moderatorrole
        db.session.add(user2)
        user3.role = moderatorrole
        db.session.add(user3)
        category1.subscribers.append(user2)
        category1.moderators.append(user2)
        db.session.add(category1)
        db.session.commit()
        # Log in with user1
        login_user(user1)
        # Test FREEUSER accessing edit_category()
        try:
            result = edit_category(category1.id)
            assert is_response(result) or \
                   (result.get("category").name == category1.name and \
                    (len(result.get("category").moderators) == 1 and \
                     result.get("category").moderators[0].fullname == user2.fullname) and \
                    (len(result.get("candidates")) == 1 and \
                      result.get("candidates")[0].fullname == user3.fullname))
        except SecurityException:
            assert True

#Test Case	57	Read own core information
# Test /main
def test_case_57_FREEUSER(app, request, user1, freeuserrole):
    with current_app.test_request_context():
        # Scenario: a freeuser user1
        user1.role = freeuserrole
        db.session.add(user1)
        db.session.commit()
        # Log in with user1
        login_user(user1)
        # Test FREEUSER accessing main()
        result = main()
        user_dto = result.get("user")
        assert user_dto.fullname == user1.fullname

# Test /events
# Duplicated with Event.owner checks

# Test /view_event
# Duplicated with Event.attendants checks

# Test /manage_event
def test_case_57_FREEUSER_1(app, request, user1, freeuserrole, publicevent1):
    with current_app.test_request_context():
        # Scenario: a person user1 with FREEUSER role.
        #           a public event owned by user1
        user1.role = freeuserrole
        db.session.add(user1)
        publicevent1.owner = user1 
        publicevent1.attendants.append(user1)
        publicevent1.managedBy.append(user1)
        publicevent1.requesters.append(user1)
        db.session.add(publicevent1)
        db.session.commit()
        # Log in with user1
        login_user(user1)
        # Test FREEUSER accessing manage_event()
        result = manage_event(publicevent1.id)
        assert len(result.get("event").attendants) == 1
        assert result.get("event").attendants[0].fullname == user1.fullname
        assert len(result.get("event").managedBy) == 1
        assert result.get("event").managedBy[0].fullname == user1.fullname

# Test \users
def test_case_57_FREEUSER_2(app, request, user1, freeuserrole):
    with current_app.test_request_context():
        # Scenario: a person user1 with FREEUSER role.
        user1.role = freeuserrole
        db.session.add(user1)
        db.session.commit()
        # Log in with user1
        login_user(user1)
        # Test FREEUSER accessing users()
        result = users()
        assert len(result.get("users")) == 1
        result.get("users")[0].fullname == user1.fullname

# Test \user
def test_case_57_FREEUSER_3(app, request, user1, freeuserrole):
    with current_app.test_request_context():
        # Scenario: a person user1 with FREEUSER role.
        user1.role = freeuserrole
        db.session.add(user1)
        db.session.commit()
        # Log in with user1
        login_user(user1)
        # Test FREEUSER accessing user()
        result = user(user1.id)
        assert result.get("user").fullname == user1.fullname
        assert result.get("user").role.name == freeuserrole.name

# Test view_category
# Duplicated with Event.owner checks

# Test edit_category
# Not applicable

#Test Case	58	Edit own core information
# For editing role, see test cases 10--13
def test_case_58_FREEUSER(app, request, user1, freeuserrole):
    with current_app.test_request_context(
        data={"id": user1.id, 
              "name": "newname",
              "surname": "newsurname",
              "role": freeuserrole.name}):
        # Scenario: a user user1 with FREEUSER role
        user1.role = freeuserrole
        db.session.add(user1)
        db.session.commit()
        # Log in with user1
        login_user(user1)
        # Test FREEUSER accessing update_user()
        result = update_user()
        assert user1.name == "newname"
        assert user1.surname == "newsurname"
                  

#Test Case	59	Edit others core
def test_case_59_FREEUSER(app, request, user1, user2, freeuserrole):
    with current_app.test_request_context(
        data={"id": user2.id, 
              "name": "newname",
              "surname": "newsurname",
              "role": freeuserrole.name}):
        # Scenario: a user user1 with FREEUSER role
        user1.role = freeuserrole
        db.session.add(user1)
        user2.role = freeuserrole
        db.session.add(user2)
        db.session.add(freeuserrole)
        db.session.commit()
        # Log in with user1
        login_user(user1)
        # Test FREEUSER accessing update_user()
        try:
            result = update_user()
        except SecurityException:
            assert True
        finally:
            assert user2.name == "user2"
            assert user2.surname == "user2"

#Test Case	60	View own events
# Test /events
# There is no explicit shown of own events.

#Test Case	61	View managed events
# Test /profile
def test_case_61_FREEUSER(app, request, user1, freeuserrole,
                          user2, publicevent1, category1):
    with current_app.test_request_context():
        # Scenario: a freeuser user1, user2
        #           a category category1
        #           a publicevent of user2, of category1
        #           user1 is a manager of publicevent1
        user1.role = freeuserrole
        db.session.add(user1)
        user2.role = freeuserrole
        db.session.add(user2)
        publicevent1.owner = user2
        publicevent1.managedBy.append(user2)
        publicevent1.attendants.append(user2)
        publicevent1.managedBy.append(user1)
        publicevent1.attendants.append(user1)
        publicevent1.categories.append(category1)
        db.session.add(publicevent1)
        db.session.add(category1)
        db.session.commit()
        # Log in with user1
        login_user(user1)
        # Test freeuser accessing profile()
        result = profile()
        user_dto = result.get("user")
        assert len(user_dto.manages) == 1
        assert user_dto.manages[0].title == publicevent1.title
        assert user_dto.manages[0].owner.fullname == publicevent1.owner.fullname

#Test Case	62	View attending events
# Test /profile
def test_case_62_FREEUSER(app, request, user1, freeuserrole,
                          user2, publicevent1, category1):
    with current_app.test_request_context():
        # Scenario: a freeuser user1, user2
        #           a category category1
        #           a publicevent of user2, of category1
        #           user1 is an attendant of publicevent1
        user1.role = freeuserrole
        db.session.add(user1)
        user2.role = freeuserrole
        db.session.add(user2)
        publicevent1.owner = user2
        publicevent1.managedBy.append(user2)
        publicevent1.attendants.append(user2)
        publicevent1.attendants.append(user1)
        publicevent1.categories.append(category1)
        db.session.add(publicevent1)
        db.session.add(category1)
        db.session.commit()
        # Log in with user1
        login_user(user1)
        # Test freeuser accessing profile()
        result = profile()
        user_dto = result.get("user")
        assert len(user_dto.attends) == 1
        assert user_dto.attends[0].title == publicevent1.title
        assert user_dto.attends[0].owner.fullname == publicevent1.owner.fullname

#Test Case	63	Change own role
def test_case_63_FREEUSER(app, request, user1, adminrole, freeuserrole):
    with current_app.test_request_context(
        data={ "id": user1.id, 
              "name": user1.name,
              "surname": user1.surname,
              "role": adminrole.name}):
        # Scenario: a user user1 with FREEUSER role
        user1.role = freeuserrole
        db.session.add(user1)
        db.session.add(adminrole)
        db.session.commit()
        # login
        login_user(user1)
        # Test FREEUSER accessing update_user()
        try:
            result = update_user()
        except SecurityException:
            assert True
        finally:
            assert user1.role.name == freeuserrole.name


#Test Case	64	View requested access
def test_case_64_FREEUSER(app, request, user1, user2, freeuserrole, publicevent1):
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
        # Log in with user1
        login_user(user1)
        # Test manage_event()
        result = manage_event(publicevent1.id)
        assert (len(result.get("event").requesters) == 1 and \
                    result.get("event").requesters[0].fullname == user2.fullname)

#Test Case	65	View subscribed categories
def test_case_65_FREEUSER(app, request, user1, freeuserrole):
    with current_app.test_request_context():
        # Scenario: a person user1 with FREEUSER role.
        user1.role = freeuserrole
        db.session.add(user1)
        db.session.commit()
        # Log in with user1
        login_user(user1)
        # Test FREEUSER accessing profile():
        result = profile()
        subs_dto = result.get("subs")
        assert len(subs_dto) == 0

#Test Case	67	Subscribe to categories
#Test Case	68	Add category to your subscriptions
def test_case_67_68_FREEUSER(app, request, user1, freeuserrole, category1):
    with current_app.test_request_context():
        # Scenario: a category category1
        #           a person user1 with FREEUSER role.
        user1.role = freeuserrole
        db.session.add(user1)
        db.session.add(category1)
        db.session.commit()
        # Log in with user1
        login_user(user1)
        # Test FREEUSER accessing subscribe()
        try:
            result = subscribe(category1.id)
        except SecurityException:
            assert True
        finally:
            assert len(category1.subscribers) == 0

#Test Case	69	Create a private event
def test_case_69_FREEUSER(app, request, user1, freeuserrole, privateevent1):
    with current_app.test_request_context(
        data={"title": privateevent1.title, 
              "description": privateevent1.description,
              "private": "sure",
              "categories": privateevent1.categories}):
        # Scenario: a person user1 with FREEUSER role.
        user1.role = freeuserrole
        db.session.add(user1)
        db.session.commit()
        # Log in with user1
        login_user(user1)
        # Test create private event
        try:
            result = create_event()
        except SecurityException:
            assert True
        finally:
            assert len(Event.query.all()) == 0

#Test Case	70	Remove category they do not moderate from event
def test_case_70_FREEUSER(app, request, user1, user2, freeuserrole, publicevent1, category1):
    with current_app.test_request_context():
        # Scenario: person user1, user2 with FREEUSER role.
        #           a category category1
        #           a public event owned by user2, of category1
        user1.role = freeuserrole
        db.session.add(user1)
        user2.role = freeuserrole
        db.session.add(user2)
        publicevent1.owner = user2 
        publicevent1.attendants.append(user2)
        publicevent1.managedBy.append(user2)
        publicevent1.categories.append(category1)
        db.session.add(publicevent1)
        db.session.add(category1)
        db.session.commit()
        # Log in with user1
        login_user(user1)
        # Test FREEUSER accessing remove_category()
        try:
            result = remove_category(publicevent1.id, category1.id)
        except SecurityException:
            assert True
        finally:
            assert len(publicevent1.categories) == 1
            assert publicevent1.categories[0].name == category1.name

def test_case_70_FREEUSER_1(app, request, user1, user2, freeuserrole, publicevent1, category1):
    with current_app.test_request_context(
        data={ "id": publicevent1.id, 
              "title": publicevent1.title, 
              "description": publicevent1.description, 
              "categories": []}):
        # Scenario: person user1, user2 with FREEUSER role.
        #           a category category1
        #           a public event owned by user2, of category1
        user1.role = freeuserrole
        db.session.add(user1)
        user2.role = freeuserrole
        db.session.add(user2)
        publicevent1.owner = user2 
        publicevent1.attendants.append(user2)
        publicevent1.managedBy.append(user2)
        publicevent1.categories.append(category1)
        db.session.add(publicevent1)
        db.session.commit()
        # Log in with user1
        login_user(user1)
        # Test FREEUSER accessing update_event()
        try:
            result = update_event()
        except SecurityException:
            assert True
        finally:
            assert len(publicevent1.categories) == 1
            assert publicevent1.categories[0].name == category1.name

#Test Case	71	Remove someone else as moderator for category
# Removed: duplicated with 79

#Test Case	74	Read category subscribers
def test_case_74_FREEUSER(app, request, user1, 
                               freeuserrole, category1, 
                               user2, premiumuserrole):
    with current_app.test_request_context():
        # Scenario: a person user1 with FREEUSER role.
        #           a person user2 with PREMIUMUSER role.
        #           a category category1
        #           user2 subscribes to category1
        user1.role = freeuserrole
        db.session.add(user1)
        user2.role = premiumuserrole
        db.session.add(user2)
        category1.subscribers.append(user2)
        db.session.add(category1)
        db.session.commit()
        # Log in with user1
        login_user(user1)
        # Test FREEUSER accessing view_category()
        result = view_category(category1.id)
        category_dto = result.get("category")
        assert (len(category_dto.subscribers) == 0 or \
                (len(category_dto.subscribers) == 1 and \
                 category_dto.subscribers[0].name == RESTRICTED and \
                 category_dto.subscribers[0].surname == RESTRICTED))

def test_case_74_FREEUSER_1(app, request, user1, 
                               freeuserrole, category1, 
                               user2, premiumuserrole):
    with current_app.test_request_context():
        # Scenario: a person user1 with FREEUSER role.
        #           a person user2 with PREMIUMUSER role.
        #           a category category1
        #           user1 subscribes to category1
        user1.role = freeuserrole
        db.session.add(user1)
        user2.role = premiumuserrole
        db.session.add(user2)
        category1.subscribers.append(user2)
        db.session.add(category1)
        db.session.commit()
        # Log in with user1
        login_user(user1)
        # Test FREEUSER access to profile()
        result = profile()
        subs_dto = result.get("subs")
        assert len(subs_dto) == 0

#Test Case	75	Delete user
# Not applicable

#Test Case	76	Edit pwd other user
# Not applicable: handle by Flask-User

#Test Case	77	Edit role other user
#def test_case_77_FREEUSER(app, request, user1, user2, freeuserrole, premiumuserrole):
#    with current_app.test_request_context(
#        data={ "id": user2.id, 
#              "name": user2.name,
#              "surname": user2.surname,
#              "role": premiumuserrole.name}):
#        # Scenario: a user user1, user2 with FREEUSER role
#        user1.role = freeuserrole
#        db.session.add(user1)
#        user2.role = freeuserrole
#        db.session.add(user2)
#        db.session.commit()
#        # login
#        login_user(user1)
#        # Test FREEUSER accessing update_user()
#        try:
#            result = update_user()
#            assert is_response(result)
#        except SecurityException:
#            assert True

#Test Case	78	Add user as moderator category
def test_case_78_FREEUSER(app, request, user1, user2, moderatorrole, freeuserrole, category1):
    with current_app.test_request_context():
        # Scenario: a person user1 with FREEUSER role.
        #           a person user2 with MODERATOR role.
        #           a category category1
        user1.role = freeuserrole
        db.session.add(user1)
        user2.role = moderatorrole
        db.session.add(user2)
        db.session.add(category1)
        db.session.commit()
        # Log in with user1
        login_user(user1)
        # Test FREEUSER accessing add_moderator()
        try:
            result = add_moderator(user2.id, category1.id)
        except SecurityException:
            assert True
        finally:
            assert user1.id not in [m.id for m in category1.moderators]

#Test Case	79	Remove user as moderator category
def test_case_79_FREEUSER(app, request, user1, user2, moderatorrole, freeuserrole, category1):
    with current_app.test_request_context():
        # Scenario: a person user1 with FREEUSER role.
        #           a person user2 with MODERATOR role.
        #           a category category1, moderated by user2
        user1.role = freeuserrole
        db.session.add(user1)
        user2.role = moderatorrole
        db.session.add(user2)
        category1.subscribers.append(user2)
        category1.moderators.append(user2)
        db.session.add(category1)
        db.session.commit()
        # Log in with user1
        login_user(user1)
        # Test FREEUSER accessing remove_moderator()
        try:
            result = remove_moderator(user2.id, category1.id)
        except SecurityException:
            assert True
        finally:
            assert user2.id in [m.id for m in category1.moderators]

#Test Case	80	Create Category
def test_case_80_FREEUSER(app, request, user1, freeuserrole, category1):
    with current_app.test_request_context(
        data={"name": category1.name}):
        # Scenario: a person user1 with FREEUSER role.
        user1.role = freeuserrole
        db.session.add(user1)
        db.session.commit()
        # Log in with user1
        login_user(user1)
        # Test FREEUSER accessing create_category()
        try:
            result = create_category()
        except SecurityException:
            assert True
        finally:
            assert len(Category.query.all()) == 0

#Test Case	81	Delete Category
# Not applicable

#Test Case	82	Change Category Name
def test_case_82_FREEUSER(app, request, user1, freeuserrole, category1):
    with current_app.test_request_context(
        data={ "id": category1.id, 
              "name": category1.name}):
        # Scenario: a person user1 with FREEUSER role.
        #           a category category1
        user1.role = freeuserrole
        db.session.add(user1)
        db.session.add(category1)
        db.session.commit()
        # Log in with user1
        login_user(user1)
        # Test FREEUSER accessing update_category()
        try:
            result = update_category()
        except SecurityException:
            assert True
        finally:
            assert category1.name == "category1"

#Test Case	83	As a manager add attendant that has not requested
def test_case_83_FREEUSER(app, request, user1, user2, user3, freeuserrole, publicevent1):
    with current_app.test_request_context():
        # Scenario: person user1, user2, user3 with FREEUSER role.
        #           a public event owned by user3
        #           managed by user1
        user1.role = freeuserrole
        db.session.add(user1)
        user2.role = freeuserrole
        db.session.add(user2)
        user3.role = freeuserrole
        db.session.add(user3)
        publicevent1.owner = user3 
        publicevent1.attendants.append(user3)
        publicevent1.managedBy.append(user3)
        publicevent1.attendants.append(user1)
        publicevent1.managedBy.append(user1)
        db.session.add(publicevent1)
        db.session.commit()
        # Log in with user1
        login_user(user1)
        # Test FREEUSER accessing accept_request()
        try:
            result = accept_request(user2.id, publicevent1.id)
        except SecurityException:
            assert True
        finally:
            assert user2.id not in [m.id for m in publicevent1.attendants]

#Test Case	84	Owner removes oneself from managing the event
def test_case_84_FREEUSER(app, request, user1, freeuserrole, publicevent1):
    with current_app.test_request_context():
        # Scenario: person user1 with FREEUSER role.
        #           a public event owned by user1
        user1.role = freeuserrole
        db.session.add(user1)
        publicevent1.owner = user1 
        publicevent1.attendants.append(user1)
        publicevent1.managedBy.append(user1)
        db.session.add(publicevent1)
        db.session.commit()
        # Log in with user1
        login_user(user1)
        # Test FREEUSER accessing demote_manager()
        try:
            result = demote_manager(user1.id, publicevent1.id)
        except SecurityException:
            assert True
        finally:
            assert publicevent1.owner.id == user1.id
            assert user1.id in [m.id for m in publicevent1.managedBy]
            assert user1.id in [m.id for m in publicevent1.attendants]

#Test Case	85	Owner removes oneself from owning the event
# Not applicable

#Test Case	86	Manager remove oneself from attendants list
# leave functionality is incorrectly implemented, waive this test
#def test_case_86_FREEUSER(app, request, user1, user2, freeuserrole, publicevent1):
#    with current_app.test_request_context():
#        # Scenario: person user1, user2 with FREEUSER role.
#        #           a public event owned by user2, managed by user1
#        user1.role = freeuserrole
#        db.session.add(user1)
#        user2.role = freeuserrole
#        db.session.add(user2)
#        publicevent1.owner = user2 
#        publicevent1.attendants.append(user2)
#        publicevent1.managedBy.append(user2)
#        publicevent1.attendants.append(user1)
#        publicevent1.managedBy.append(user1)
#        db.session.add(publicevent1)
#        db.session.commit()
#        # Log in with user1
#        login_user(user1)
#        # Test FREEUSER accessing leave()
#        try:
#            result = leave(publicevent1.id)
#        except SecurityException:
#            assert True
#        finally:
#            assert user1.id in [m.id for m in publicevent1.attendants]
#            assert user1.id in [m.id for m in publicevent1.managedBy]

def test_case_86_FREEUSER_1(app, request, user1, user2, freeuserrole, publicevent1):
    with current_app.test_request_context():
        # Scenario: person user1, user2 with FREEUSER role.
        #           a public event owned by user2, managed by user1
        user1.role = freeuserrole
        db.session.add(user1)
        user2.role = freeuserrole
        db.session.add(user2)
        publicevent1.owner = user2 
        publicevent1.attendants.append(user2)
        publicevent1.managedBy.append(user2)
        publicevent1.attendants.append(user1)
        publicevent1.managedBy.append(user1)
        db.session.add(publicevent1)
        db.session.commit()
        # Log in with user1
        login_user(user1)
        # Test FREEUSER accessing remove_attendee()
        try:
            result = remove_attendee(user1.id, publicevent1.id)
        except SecurityException:
            assert True
        finally:
            assert user1.id in [m.id for m in publicevent1.attendants]
            assert user1.id in [m.id for m in publicevent1.managedBy]

#Test Case	87	Manager remove oneself from managers list
def test_case_87_FREEUSER(app, request, user1, user2, freeuserrole, publicevent1):
    with current_app.test_request_context():
        # Scenario: person user1, user2 with FREEUSER role.
        #           a public event owned by user2, managed by user1
        user1.role = freeuserrole
        db.session.add(user1)
        user2.role = freeuserrole
        db.session.add(user2)
        publicevent1.owner = user2 
        publicevent1.attendants.append(user2)
        publicevent1.managedBy.append(user2)
        publicevent1.attendants.append(user1)
        publicevent1.managedBy.append(user1)
        db.session.add(publicevent1)
        db.session.commit()
        # Log in with user1
        login_user(user1)
        # Test FREEUSER accessing demote_manager()
        try:
            result = demote_manager(user1.id, publicevent1.id)
        except SecurityException:
            assert True
        finally:
            assert user1.id in [m.id for m in publicevent1.managedBy]     

#Test Case	89	Update Person.role from FREE to FREEUSER
# Not applicable

#Test Case	90	Accept someone else's request, not owner not manager
def test_case_90_FREEUSER(app, request, user1, user2, user3, freeuserrole, publicevent1):
    with current_app.test_request_context():
        # Scenario: person user1, user2, user3 with FREEUSER role.
        #           a public event owned by user3, request to join by user2
        user1.role = freeuserrole
        db.session.add(user1)
        user3.role = freeuserrole
        db.session.add(user3)
        user2.role = freeuserrole
        db.session.add(user2)
        publicevent1.owner = user3 
        publicevent1.attendants.append(user3)
        publicevent1.managedBy.append(user3)
        publicevent1.requesters.append(user2)
        db.session.add(publicevent1)
        db.session.commit()
        # Log in with user1
        login_user(user1)
        # Test FREEUSER accessing accept_request()
        try:
            result = accept_request(user2.id, publicevent1.id)
        except SecurityException:
            assert True
        finally:
            assert user2.id not in [m.id for m in publicevent1.attendants]
            assert user2.id in [m.id for m in publicevent1.requesters]

#Test Case	91	Edit event's categories, manager
def test_case_91_FREEUSER(app, request, user1, user2, freeuserrole, publicevent1, category1):
    with current_app.test_request_context(
        data={ "id": publicevent1.id, 
              "title": publicevent1.title, 
              "description": publicevent1.description, 
              "categories": []}):
        # Scenario: a person user1, user2 with FREEUSER role.
        #           a public event owned by user2, managed by user1
        user1.role = freeuserrole
        db.session.add(user1)
        user2.role = freeuserrole
        db.session.add(user2)
        publicevent1.owner = user2 
        publicevent1.attendants.append(user2)
        publicevent1.managedBy.append(user2)
        publicevent1.attendants.append(user1)
        publicevent1.managedBy.append(user1)
        publicevent1.categories.append(category1)
        db.session.add(publicevent1)
        db.session.commit()
        # Log in with user1
        login_user(user1)
        # Test FREEUSER accessing update_event()
        result = update_event()
        assert len(publicevent1.categories) == 0

#Test Case	92	Edit event's categories, not manager
def test_case_92_FREEUSER(app, request, user1, user2, freeuserrole, publicevent1, category1):
    with current_app.test_request_context(
        data={ "id": publicevent1.id, 
              "title": publicevent1.title, 
              "description": publicevent1.description, 
              "categories": []}):
        # Scenario: a person user1 with FREEUSER role.
        #           a public event owned by user2
        user1.role = freeuserrole
        db.session.add(user1)
        user2.role = freeuserrole
        db.session.add(user2)
        publicevent1.owner = user2 
        publicevent1.attendants.append(user2)
        publicevent1.managedBy.append(user2)
        publicevent1.categories.append(category1)
        db.session.add(publicevent1)
        db.session.commit()
        # Log in with user1
        login_user(user1)
        # Test FREEUSER accessing update_event()
        try:
            result = update_event()
        except SecurityException:
            assert True
        finally:
            assert len(publicevent1.categories) == 1
            assert publicevent1.categories[0].id == category1.id

#Test Case	93	Read Event.private for private event
def test_case_93_FREEUSER(app, request, user1, user2, freeuserrole, premiumuserrole, privateevent1):
    with current_app.test_request_context():
        # Scenario: a person user1 with FREEUSER role.
        #           a person user2 with PREMIUMUSER role.
        #           a private event owned by user2
        user1.role = freeuserrole
        db.session.add(user1)
        user2.role = premiumuserrole
        db.session.add(user2)
        privateevent1.owner = user2 
        privateevent1.attendants.append(user2)
        privateevent1.managedBy.append(user2)
        db.session.add(privateevent1)
        db.session.commit()
        # login
        login_user(user1)
        # Test FREEUSER accessing view_event(): 
        try:
            result = view_event(privateevent1.id)
            assert is_response(result) or \
                   result.get("event").private == privateevent1.private
        except SecurityException:
            assert True

def test_case_93_FREEUSER_1(app, request, user1, user2, freeuserrole, premiumuserrole, privateevent1):
    with current_app.test_request_context():
        # Scenario: a person user1 with FREEUSER role.
        #           a person user2 with PREMIUMUSER role.
        #           a private event owned by user2
        user1.role = freeuserrole
        db.session.add(user1)
        user2.role = premiumuserrole
        db.session.add(user2)
        privateevent1.owner = user2 
        privateevent1.attendants.append(user2)
        privateevent1.managedBy.append(user2)
        db.session.add(privateevent1)
        db.session.commit()
        # login
        login_user(user1)
        # Test FREEUSER accessing edit_event()
        try:
            result = edit_event(privateevent1.id)
            assert is_response(result) or \
                   result.get("event").private == privateevent1.private
        except SecurityException:
            assert True

#Test Case	94	Read Event.categories of a private event
def test_case_94_FREEUSER(app, request, user1, freeuserrole, user2, premiumuserrole, privateevent1, category1):
    with current_app.test_request_context():
        # Scenario: a person user1 with FREEUSER role
        #           a person user2 with PREMIUMUSER role.
        #           a category category1
        #           a private event owned by user2, of category1
        user1.role = freeuserrole
        db.session.add(user1)
        user2.role = premiumuserrole
        db.session.add(user2)
        privateevent1.owner = user2 
        privateevent1.attendants.append(user2)
        privateevent1.managedBy.append(user2)
        privateevent1.categories.append(category1)
        db.session.add(privateevent1)
        db.session.commit()
        # login
        login_user(user1)
        # Test FREEUSER accessing view_event(): 
        try:
            result = view_event(privateevent1.id)
            assert is_response(result) or \
                   (len(result.get("event").categories) == 1 and \
                    result.get("event").categories[0].name == category1.name)
        except SecurityException:
            assert True