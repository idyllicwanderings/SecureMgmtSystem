from flask_principal import Principal, Identity, Permission, UserNeed, RoleNeed, identity_loaded, identity_changed
from collections import namedtuple
from functools import partial



admin = Permission(RoleNeed('ADMIN'))
freeuser = Permission(RoleNeed('FREEUSER'))
premiumuser = Permission(RoleNeed('PREMIUMUSER'))
moderator = Permission(RoleNeed('MODERATOR'))

#Needs
#Person.events
#=================================================================================
EventNeed = namedtuple('Event', ['method', 'value'])

AddEventNeed = partial(EventNeed, 'add_event') #fix:all partial's names should be unique
class AddEventPermission(Permission):
    def __init__(self, tid):
        need = AddEventNeed(tid)
        super(AddEventPermission, self).__init__(need)

#Person.Manages
#=================================================================================
ManageNeed = namedtuple('Manage', ['method', 'value'])

RemoveManageNeed = partial(ManageNeed, 'remove_manage')
class RemoveManagePermission(Permission):
    def __init__(self, tid):
        need = RemoveManageNeed(tid)
        super(RemoveManagePermission, self).__init__(need)


AddManageNeed = partial(ManageNeed, 'add_manage')
class AddManagePermission(Permission):
    def __init__(self, tid):
        need = AddManageNeed(tid)
        super(AddManagePermission, self).__init__(need)


#Person.Attends
#=================================================================================
AttendNeed = namedtuple('Attend', ['method', 'value'])

RemoveAttendNeed = partial(AttendNeed, 'remove_attendant')
class RemoveAttendPermission(Permission):
    def __init__(self, tid):
        need = RemoveAttendNeed(tid)
        super(RemoveAttendPermission, self).__init__(need)


AddAttendNeed = partial(AttendNeed, 'add_attendant')
class AddAttendPermission(Permission):
    def __init__(self, tid):
        need = AddAttendNeed(tid)
        super(AddAttendPermission, self).__init__(need)


LeaveAttendNeed = partial(AttendNeed, 'leave_attendant')
class LeaveAttendPermission(Permission):
    def __init__(self, tid):
        need = LeaveAttendNeed(tid)
        super(LeaveAttendPermission, self).__init__(need)


#Person.Requests
#=================================================================================
RequestNeed = namedtuple('Request', ['method', 'value'])

RemoveRequestNeed = partial(RequestNeed, 'remove_req')
class RemoveRequestPermission(Permission):
    def __init__(self, tid):
        need = RemoveRequestNeed(tid)
        super(RemoveRequestPermission, self).__init__(need)


AddRequestNeed = partial(RequestNeed, 'add_req')
class AddRequestPermission(Permission):
    def __init__(self, tid):
        need = AddRequestNeed(tid)
        super(AddRequestPermission, self).__init__(need)


JoinRequestNeed = partial(RequestNeed, 'join_req')
class JoinRequestPermission(Permission):
    def __init__(self, tid):
        need = JoinRequestNeed(tid)
        super(JoinRequestPermission, self).__init__(need)




#=================================================================================
CategoryNeed = namedtuple('Category', ['method', 'value'])

RemoveCategoryNeed = partial(CategoryNeed, 'remove_category')
class RemoveCategoryPermission(Permission):
    def __init__(self, tid):
        need = RemoveCategoryNeed(tid)
        super(RemoveCategoryPermission, self).__init__(need)


RemoveModeratorCategoryNeed = partial(CategoryNeed, 'remove_mod_category')
class RemoveModeratorCategoryPermission(Permission):
    def __init__(self, tid):
        need = RemoveModeratorCategoryNeed(tid)
        super(RemoveModeratorCategoryPermission, self).__init__(need)

        
AddCategoryNeed = partial(CategoryNeed, 'add_category')
class AddCategoryPermission(Permission):
    def __init__(self, tid):
        need = AddCategoryNeed(tid)
        super(AddCategoryPermission, self).__init__(need)


#=================================================================================

ModerateNeed = namedtuple('Moderate', ['method', 'value'])

RemoveModerateNeed = partial(ModerateNeed, 'remove_moderate')
class RemoveModeratePermission(Permission):
    def __init__(self, tid):
        need = RemoveModerateNeed(tid)
        super(RemoveModeratePermission, self).__init__(need)

AddModerateNeed = partial(ModerateNeed, 'add_moderate')
class AddModeratePermission(Permission):
    def __init__(self, tid):
        need = AddModerateNeed(tid)
        super(AddModeratePermission, self).__init__(need)



#=================================================================================


SubscriptionNeed = namedtuple('Subscription', ['method', 'value'])

RemoveSubscriptionNeed = partial(SubscriptionNeed, 'remove_subs')
class RemoveSubscriptionPermission(Permission):
    def __init__(self, tid):
        need = RemoveSubscriptionNeed(tid)
        super(RemoveSubscriptionPermission, self).__init__(need)

AddSubscriptionNeed = partial(SubscriptionNeed, 'add_subs')
class AddSubscriptionPermission(Permission):
    def __init__(self, tid):
        need = AddSubscriptionNeed(tid)
        super(AddSubscriptionPermission, self).__init__(need)

#=================================================================================
ViewEventNeed = namedtuple('ViewEvent', ['method', 'value'])

ViewManageEventNeed = partial(ViewEventNeed, 'view_manage')
class ViewManageEventPermission(Permission):
    def __init__(self, tid):
        need = ViewManageEventNeed(tid)
        super(ViewManageEventPermission, self).__init__(need)


ViewAttendEventNeed = partial(ViewEventNeed, 'view_attend')
class ViewAttendEventPermission(Permission):
    def __init__(self, tid):
        need = ViewAttendEventNeed(tid)
        super(ViewAttendEventPermission, self).__init__(need)

#=================================================================================
ViewCategoryNeed = namedtuple('ViewCategory', ['method', 'value'])

ViewModerateCategoryNeed = partial(ViewCategoryNeed, 'viewModerateCategory')
class ViewModerateCategoryPermission(Permission):
    def __init__(self, tid):
        need = ViewModerateCategoryNeed(tid)
        super(ViewModerateCategoryPermission, self).__init__(need)

#=================================================================================

CreateCategoryNeed = partial(CategoryNeed, 'CreateCategory')
class CreateCategoryPermission(Permission):
    def __init__(self, tid):
        need = CreateCategoryNeed(tid)
        super(CreateCategoryPermission, self).__init__(need)

#=================================================================================

CreateEventNeed = partial(EventNeed, 'CreateEvent')
class CreateEventPermission(Permission):
    def __init__(self, tid):
        need = CreateEventNeed(tid)
        super(CreateEventPermission, self).__init__(need)


# #=================================================================================
# Edit/Set Event's info Permission
EventInfoNeed = namedtuple('EventInfo', ['method', 'value'])

EditEventCoreInfoNeed = partial(EventInfoNeed,'EditEventCoreInfo')
class EditEventCoreInfoPermission(Permission):
    def __init__(self, tid):
        need = EditEventCoreInfoNeed(tid)
        super(EditEventCoreInfoPermission, self).__init__(need)

SetEventInfoNeed = partial(EventInfoNeed,'SetEventInfo')
class SetEventInfoPermission(Permission):
    def __init__(self, tid):
        need = SetEventInfoNeed(tid)
        super(SetEventInfoPermission, self).__init__(need)


# #=================================================================================
# New Requests

InviteCreateNeed = namedtuple('Invite_create', ['method', 'value'])

SendInviteNeed = partial(InviteCreateNeed,'send_invite')
class SendInvitePermission(Permission):
    def __init__(self, tid):
        need = SendInviteNeed(tid)
        super(SendInvitePermission, self).__init__(need)


# InviteNeed = namedtuple('Invite', ['method', 'value'])
# AcceptInviteNeed = partial(InviteNeed,'accept_invite')
# class AcceptInvitePermission(Permission):
#     def __init__(self, tid):
#         need = AcceptInviteNeed(tid)
#         super(AcceptInvitePermission, self).__init__(need)


ViewInviteEventNeed = partial(ViewEventNeed,'view_invite_need')
class ViewInviteEventPermission(Permission):
    def __init__(self, tid):
        need = ViewInviteEventNeed(tid)
        super(ViewInviteEventPermission, self).__init__(need)


JoinEventNeed = partial(EventNeed,'event_invite')
class JoinEventPermission(Permission):
    def __init__(self, tid):
        need = JoinEventNeed(tid)
        super(JoinEventPermission, self).__init__(need)