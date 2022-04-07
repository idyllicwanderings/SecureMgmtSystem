# from flask import current_app, Response
# from flask_login import login_user, AnonymousUserMixin
# from flask_user import current_user
# from model import db
# from project import *
# from dto import RESTRICTED
# from flask_principal import Identity, identity_changed
# from implicits import implicits
# from tests.conftest import invite1, premiumuserrole


# # This test suite is dedicated for users with PREMIUMUSER role
# # Tests that are applicable to PREMIUMUSER role.

# def is_response(result):
#     return type(result) == Response     

# @implicits("app")
# def login_user(user,app):
#     from flask_login import login_user
#     login_user(user)
#     identity_changed.send(app,identity=Identity(current_user.id))




# #Test Case	44	Promote oneself as manager for event not owned
# def test_case_1_FREEUSER(app, request, user1, user2, freeuserrole, publicevent1):
#     with current_app.test_request_context():
#         # Scenario: person user1, user2 with FREEUSER role.
#         #           a public event owned by user2,
#         #           attended by user1
#         user1.role = freeuserrole
#         db.session.add(user1)


#         user2.role = freeuserrole
#         db.session.add(user2)
#         publicevent1.owner = user2 
#         publicevent1.attendants.append(user2)
#         publicevent1.managedBy.append(user2)
#         publicevent1.attendants.append(user1)
#         db.session.add(publicevent1)
#         db.session.commit()
#         # Log in with user1
#         login_user(user2)
#         # Test FREEUSER accessing promote_manager()
#         result = send_invite(user1.id, publicevent1.id)
#         assert publicevent1.invitations[0].invitee.name == user1.name
#         assert publicevent1.invitations[0].invitedBy.name == user2.name
#         assert publicevent1.invitations[0].event.id == publicevent1.id

 
# def test_case_2_FREEUSER(app, request, user1, user2, freeuserrole, publicevent1):
#     with current_app.test_request_context():
#         # Scenario: person user1, user2 with FREEUSER role.
#         #           a public event owned by user2,
#         #           attended by user1
#         user1.role = freeuserrole
#         db.session.add(user1)


#         user2.role = freeuserrole
#         db.session.add(user2)
#         publicevent1.owner = user2 
#         publicevent1.attendants.append(user2)
#         publicevent1.managedBy.append(user2)
#         publicevent1.attendants.append(user1)
#         publicevent1.requesters.append(user1)
#         db.session.add(publicevent1)
#         db.session.commit()
#         # Log in with user1
#         login_user(user2)
#         try:
#             result = send_invite(user1.id, publicevent1.id)
#         except SecurityException:
#             assert True
#         finally:
#             assert len(publicevent1.invitations) == 0



 
# def test_case_3_FREEUSER(app, request, user1, user2, freeuserrole, publicevent1):
#     with current_app.test_request_context():
#         # Scenario: person user1, user2 with FREEUSER role.
#         #           a public event owned by user2,
#         #           attended by user1
#         user1.role = freeuserrole
#         db.session.add(user1)


#         user2.role = freeuserrole
#         db.session.add(user2)
#         publicevent1.owner = user2 
#         publicevent1.attendants.append(user2)
#         publicevent1.managedBy.append(user2)
#         publicevent1.attendants.append(user1)
#         publicevent1.requesters.append(user1)
#         db.session.add(publicevent1)
#         db.session.commit()
#         # Log in with user1
#         login_user(user1)
#         # Test FREEUSER accessing promote_manager()

#         try:
#             result = send_invite(user2.id, publicevent1.id)
#         except SecurityException:
#             assert True
#         finally:
#             assert len(publicevent1.invitations) == 0


# def test_case_4_FREEUSER(app, request, user1, user2, freeuserrole,invite1, publicevent1):
#     with current_app.test_request_context():
#         # Scenario: person user1, user2 with FREEUSER role.
#         #           a public event owned by user2,
#         #           attended by user1
#         user1.role = freeuserrole
#         db.session.add(user1)


#         user2.role = freeuserrole
#         db.session.add(user2)
#         publicevent1.owner = user2 
#         publicevent1.attendants.append(user2)
#         publicevent1.managedBy.append(user2)
#         publicevent1.attendants.append(user1)
#         db.session.add(invite1)
#         db.session.add(publicevent1)

#         invite1.event = publicevent1
#         invite1.invitee = user1
#         invite1.invitedBy = user2
#         db.session.commit()
#         # Log in with user1
#         login_user(user1)
#         # Test FREEUSER accessing promote_manager()
#         result = accept_invitation(invite1.id)
#         assert len(publicevent1.invitations) == 0
#         assert len(user2.invites) == 0




# def test_case_5_FREEUSER(app, request, user1, user2, freeuserrole,invite1, publicevent1):
#     with current_app.test_request_context():
#         # Scenario: person user1, user2 with FREEUSER role.
#         #           a public event owned by user2,
#         #           attended by user1
#         user1.role = freeuserrole
#         db.session.add(user1)


#         user2.role = freeuserrole
#         db.session.add(user2)
#         publicevent1.owner = user2 
#         publicevent1.attendants.append(user2)
#         publicevent1.managedBy.append(user2)
#         publicevent1.attendants.append(user1)
#         db.session.add(publicevent1)

#         invite1.event = publicevent1
#         invite1.invitee = user1
#         invite1.invitedBy = user2
#         db.session.add(invite1)
#         db.session.commit()
#         # Log in with user1
#         login_user(user1)
#         # Test FREEUSER accessing promote_manager()
#         result = decline_invitation(invite1.id)
#         assert len(publicevent1.invitations) == 0
#         assert len(user2.invites) == 0




# #profile
# #user1,invited By can see private event
# def test_case_6_FREEUSER(app, request, user1, user2, premiumuserrole,invite1, privateevent1):
#     with current_app.test_request_context():
#         # Scenario: person user1, user2 with FREEUSER role.
#         #           a public event owned by user2,
#         #           attended by user1
#         user1.role = premiumuserrole
#         db.session.add(user1)


#         user2.role = premiumuserrole
#         db.session.add(user2)
#         privateevent1.owner = user2 
#         privateevent1.attendants.append(user2)
#         privateevent1.managedBy.append(user2)
#         #publicevent1.attendants.append(user1)
#         db.session.add(privateevent1)

#         invite1.event = privateevent1
#         invite1.invitee = user1
#         invite1.invitedBy = user2
#         db.session.add(invite1)
#         db.session.commit()
#         # Log in with user1
#         login_user(user1)

#         # Test freeuser accessing profile()
#         result = profile()
#         user_dto = result.get("invitations")
#         assert len(user_dto) == 1
#         assert user_dto[0].event.title == privateevent1.title
#         assert user_dto[0].invitedBy.name == user2.name





# #profile
# #user1, not invited By, cannot see
# def test_case_7_FREEUSER(app, request, user1, user2, premiumuserrole,invite1, privateevent1):
#     with current_app.test_request_context():

#         user1.role = premiumuserrole
#         db.session.add(user1)


#         user2.role = premiumuserrole
#         db.session.add(user2)
#         privateevent1.owner = user2 
#         privateevent1.attendants.append(user2)
#         privateevent1.managedBy.append(user2)
#         #publicevent1.attendants.append(user1)
#         db.session.add(privateevent1)

#         invite1.event = privateevent1
#         invite1.invitee = user2
#         invite1.invitedBy = user2
#         db.session.add(invite1)
#         db.session.commit()
#         # Log in with user1
#         login_user(user1)

#         result = profile()
#         user_dto = result.get("invitations")
#         assert len(user_dto) == 0
#         user_dto = view_event(privateevent1.id)
#         result = user_dto.get("event")
#         assert result.title == RESTRICTED





# #manage_event
# def test_case_8_FREEUSER(app, request, user1, user2,freeuserrole, premiumuserrole,invite1, privateevent1):
#     with current_app.test_request_context():

#         #user 2 can see user 1 as invitees, 

#         user1.role = freeuserrole
#         db.session.add(user1)


#         user2.role = premiumuserrole
#         db.session.add(user2)
#         privateevent1.owner = user2 
#         privateevent1.attendants.append(user2)
#         privateevent1.managedBy.append(user2)
#         privateevent1.attendants.append(user1)
#         db.session.add(privateevent1)

#         invite1.event = privateevent1
#         invite1.invitee = user1
#         invite1.invitedBy = user2
#         db.session.add(invite1)
#         db.session.commit()
#         # Log in with user1
#         login_user(user2)

#         result = manage_event(privateevent1.id)
#         result = result.get("invitees")
#         assert len(result) == 1
#         assert result[0].name == user1.name
#         assert result[0].attends == []






# #manage_event
# def test_case_8_FREEUSER(app, request, user1, user2,freeuserrole, premiumuserrole,invite1, privateevent1):
#     with current_app.test_request_context():

#         #user 2 can see user 1 as invitees, 

#         user1.role = freeuserrole
#         db.session.add(user1)


#         user2.role = premiumuserrole
#         db.session.add(user2)
#         privateevent1.owner = user2 
#         privateevent1.attendants.append(user2)
#         privateevent1.managedBy.append(user2)
#         privateevent1.attendants.append(user1)
#         db.session.add(privateevent1)

#         invite1.event = privateevent1
#         invite1.invitee = user2
#         invite1.invitedBy = user2
#         db.session.add(invite1)
#         db.session.commit()
#         # Log in with user1
#         login_user(user2)

#         result = manage_event(privateevent1.id)
#         result = result.get("invitees")
#         assert len(result) == 1
#         assert result[0].name == user2.name
#         assert len(result[0].attends) == 1

