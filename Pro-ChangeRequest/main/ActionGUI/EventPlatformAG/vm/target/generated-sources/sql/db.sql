CREATE DATABASE IF NOT EXISTS EventPlatformAG;
USE EventPlatformAG;
-- ----------------------------------------------------
-- This table represents the class'Category'
-- ----------------------------------------------------
CREATE table IF NOT EXISTS Category(
	pk INT NOT NULL auto_increment,
	name text NULL,
	primary key (pk)
) ENGINE=InnoDB;

--
-- This table represents the association 'Category.subscribers'
--
CREATE table IF NOT EXISTS Category_subscribers__Person_subscriptions(
	Category_subscribers INT NULL,
	Person_subscriptions INT NULL
) ENGINE=InnoDB;

--
-- This table represents the association 'Category.events'
--
CREATE table IF NOT EXISTS Category_events__Event_categories(
	Category_events INT NULL,
	Event_categories INT NULL
) ENGINE=InnoDB;

--
-- This table represents the association 'Category.moderators'
--
CREATE table IF NOT EXISTS Category_moderators__Person_moderates(
	Category_moderators INT NULL,
	Person_moderates INT NULL
) ENGINE=InnoDB;



-- ----------------------------------------------------
-- This table represents the class'Event'
-- ----------------------------------------------------
CREATE table IF NOT EXISTS Event(
	pk INT NOT NULL auto_increment,
	private bool NULL,
	description text NULL,
	title text NULL,
	owner int NULL,
	primary key (pk)
) ENGINE=InnoDB;

--
-- This table represents the association 'Event.attendants'
--
CREATE table IF NOT EXISTS Event_attendants__Person_attends(
	Event_attendants INT NULL,
	Person_attends INT NULL
) ENGINE=InnoDB;

--
-- This table represents the association 'Event.requesters'
--
CREATE table IF NOT EXISTS Event_requesters__Person_requests(
	Event_requesters INT NULL,
	Person_requests INT NULL
) ENGINE=InnoDB;

--
-- This table represents the association 'Event.managedBy'
--
CREATE table IF NOT EXISTS Event_managedBy__Person_manages(
	Event_managedBy INT NULL,
	Person_manages INT NULL
) ENGINE=InnoDB;

--
-- This table represents the association 'Event.invitations'
--
CREATE table IF NOT EXISTS Event_invitations__Invite_event(
	Event_invitations INT NULL,
	Invite_event INT NULL
) ENGINE=InnoDB;



-- ----------------------------------------------------
-- This table represents the class'Invite'
-- ----------------------------------------------------
CREATE table IF NOT EXISTS Invite(
	pk INT NOT NULL auto_increment,
	invitedBy int NULL,
	event int NULL,
	invitee int NULL,
	primary key (pk)
) ENGINE=InnoDB;



-- ----------------------------------------------------
-- This table represents the class'Person'
-- ----------------------------------------------------
CREATE table IF NOT EXISTS Person(
	pk INT NOT NULL auto_increment,
	role int NULL,
	password text NULL,
	surname text NULL,
	name text NULL,
	username text NULL,
	primary key (pk)
) ENGINE=InnoDB;

--
-- This table represents the association 'Person.invitations'
--
CREATE table IF NOT EXISTS Invite_invitee__Person_invitations(
	Invite_invitee INT NULL,
	Person_invitations INT NULL
) ENGINE=InnoDB;

--
-- This table represents the association 'Person.invites'
--
CREATE table IF NOT EXISTS Invite_invitedBy__Person_invites(
	Invite_invitedBy INT NULL,
	Person_invites INT NULL
) ENGINE=InnoDB;

--
-- This table represents the association 'Person.events'
--
CREATE table IF NOT EXISTS Event_owner__Person_events(
	Event_owner INT NULL,
	Person_events INT NULL
) ENGINE=InnoDB;



