Stardust RPG
============

.. image:: https://travis-ci.org/johnthagen/stardust-rpg.svg
    :target: https://travis-ci.org/johnthagen/stardust-rpg

.. image:: https://codeclimate.com/github/johnthagen/stardust-rpg/badges/gpa.svg
   :target: https://codeclimate.com/github/johnthagen/stardust-rpg

.. image:: https://codeclimate.com/github/johnthagen/stardust-rpg/badges/issue_count.svg
   :target: https://codeclimate.com/github/johnthagen/stardust-rpg

.. image:: https://img.shields.io/pypi/v/stardust-rpg.svg
    :target: https://pypi.python.org/pypi/stardust-rpg

.. image:: https://img.shields.io/pypi/status/stardust-rpg.svg
    :target: https://pypi.python.org/pypi/stardust-rpg

.. image:: https://img.shields.io/pypi/pyversions/stardust-rpg.svg
    :target: https://pypi.python.org/pypi/stardust-rpg/

.. image:: https://img.shields.io/pypi/dm/stardust-rpg.svg
    :target: https://pypi.python.org/pypi/stardust-rpg/

Stardust RPG is a tactical d20 role-playing game designed to provide a variety of progression
options for players and encourage teamwork.  Baseline content is based off the Stardust book
series by John Hagen but is adaptable to a variety of fantasy settings.

Features
--------

- Cross platform.  Run the server on any platform that supports Python.  Clients can
  connect and manage their characters using a standard web browser with no install required.
- Roll20 integration. Players can to automatically sync their character stats and
  automatically generated weapon and ability macros right into a Roll20 campaign. Special thanks
  to `@theandrewdavis <https://github.com/theandrewdavis>`_ for his analysis of the roll20.net API.
- Extensible. Easily add new content, such as classes, weapons, or abilities.
- Persistent. Store characters in a persistent database for easy reuse.

Usage
=====

Installation
------------

You can install, upgrade, and uninstall ``stardust-rpg`` with these commands:

.. code:: shell-session

    $ pip3 install stardust-rpg
    $ pip3 install --upgrade stardust-rpg
    $ pip3 uninstall stardust-rpg

Server Setup
------------

Create an environment variable named ``SECRET_KEY`` and populate it with a
`large random value <https://docs.djangoproject.com/en/dev/howto/deployment/checklist/#secret-key>`_.

Configuration
-------------

Initialize the database:

.. code:: shell-session

    $ stardust-rpg makemigrations
    $ stardust-rpg migrate

Create an admin account:

.. code:: shell-session

    $ stardust-rpg createsuperuser


Production Execution
~~~~~~~~~~~~~~~~~~~~

.. warning::

    ``--insecure`` is used to serve static files in the absense of a
    web server (e.g. NGINX) running in front of Django.

.. code:: shell-session

    $ stardust-rpg runserver 0.0.0.0:80 --insecure

Debug Execution
~~~~~~~~~~~~~~~

.. warning::

    `Debug mode should not be used in production <https://docs.djangoproject.com/en/dev/ref/settings/#debug>`_.

.. code:: shell-session

    $ stardust-rpg runserver 0.0.0.0:80 --settings=app.debug_settings

Game Setup
----------

Log into the admin interface by browsing to http://localhost/admin

Add ``Users`` for each player.  Configure the following fields:

======================= ==============================================
Field                   Value
======================= ==============================================
``Username``            Stardust RPG server username.
``Password``            Initial user password
``Email Address``       Player's Roll20 email address.
======================= ==============================================

Add a ``Party`` for the group.  Configure the following fields:

======================= ==============================================
Field                   Value
======================= ==============================================
``Name``                Name of the character.  Must match name of character in Roll20.
``Roll20 campaign id``  The 6 digit ID (e.g. https://app.roll20.net/campaigns/details/CAMPAIGN_ID/CAMPAIGN_NAME) assigned to the campaign found at https://app.roll20.net/campaigns/search
======================= ==============================================

Add ``Characters`` for each character in the game.  Configure the following fields:

======================= ==============================================
Field                   Value
======================= ==============================================
``User``                Player who has modification rights to the character.
``Name``                Name of the character.  Must match name of character in Roll20.
``Party``               The ``Party`` this character is a part of.
``Class``               The class assigned to this ``Character``.
======================= ==============================================

Roll20 Campaign Setup
~~~~~~~~~~~~~~~~~~~~~

In the Settings page for the Roll20 campaign, under **Character Sheet Template**, select
``5th Edition (Community Contributed)``. ``stardust-rpg`` uses specific macro templates defined
in character sheet to enhance macro visuals.

Rules
=====

Combat
------

Combat Round (``RND``)
~~~~~~~~~~~~~~~~~~~~~~

#. At the start of combat, roll a d20 + Maximum Speed (``SPEED``) to determine turn order.

    #. If your character is surprised, take no actions during the first ``RND``.

#. Do the following actions in any order. A Full Action (``FullA``) requires consuming all these
   actions. A Free Action (``FreeA``) does not consume any of these actions.

    #. Move Action (``MovA``)

        #. Move your character up to Maximum Speed (``SPEED``).

            #. You may move through squares occupied by allies, but may not move through grid
               squares occupied by enemies.

        #. After performing a ``StdA`` or ``AbA``, you may consume the remaining ``SPEED`` that has
           not be used during this ``RND``.

    #. Standard Action (``StdA``)

        #. Perform a single melee or ranged weapon attack

            #. Roll a d20 and ``PDAM`` dice.  If d20 + ``PAC`` ≥ target ``PDEF``, apply ``PDAM``.

                #. If d20 ≥ Critical Range (``CRAN``), automatic hit, apply CDAM.
                #. if d20 = 1, automatic miss.

    #. Ability Action (``AbA``)

        #. Cast a single ability that requires ``AbA``

            #. Subtract the MP Cost from your Current ``MP``.  Current ``MP`` cannot drop below 0.
            #. Roll a d20 and ``MDAM`` dice. If d20 + ``MAC`` ≥ target ``MDEF``, apply
               ``MDAM`` and Effect.

                #. If d20 = 20, automatic hit, choose one of the following:
                   2x [``MDAM``, Effect, Area, OR Duration].

                #. If d20 = 1, automatic miss.

            #. If casting a combo, the ally who is casting the combo with must also subtract the
               MP Cost and spend whatever Time is required to cast.  This time is deducted from
               their next turn.

#. At the conclusion of your turn, roll a d20 and Regeneration Dice (``RD``)

    #. If d20 + Magic Regeneration (``REG``) ≥ 18, restore ``RD`` MP.

        #. If d20 = 20, restore 2x ``RD`` MP.
        #. If d20 = 1, automatic failure.

Incapacitation (``KO``)
~~~~~~~~~~~~~~~~~~~~~~~

- If ``HP`` ≤ 0, unconscious status.
- If ``HP`` ≤ -(50% Maximum ``HP``), death status.

Status Effects
~~~~~~~~~~~~~~

=========== ===================================================================================
Status      Effect
=========== ===================================================================================
Immobilize  Cannot take ``MovA``.
Silence     Cannot take ``AbA`` (i.e. any action that targets with ``MAC`` or consumes ``MP``).
Stagger     Cannot take ``StdA``.
Disable     Cannot take ``StdA`` or ``AbA``.
Stun        Cannot take ``StdA``, ``AbA``, or ``MovA``.
Sleep       Cannot take ``StdA``, ``AbA``, or ``MovA``.  Woken by physical or magical attack.
Fear        Must expend ``MovA`` to move in opposite direction of the source of fear.
Allure      Must expend ``MovA`` to move towards the source of the allure.
Blind       Maximum range of physical and magic attacks reduced to 1.  ``VIS`` reduced to 1.
Inhibit     Max ``MP`` reduced to 0.  ``MRED`` reduced to 0.
=========== ===================================================================================

=========== ===================================================================================
Condition   Effect
=========== ===================================================================================
Unconscious Cannot take anymore actions until revived.
Death       Creature is dead.
=========== ===================================================================================

Advantage / Disadvantage
~~~~~~~~~~~~~~~~~~~~~~~~

======================= ===========================================================================
State                   Effect
======================= ===========================================================================
Advantage (``ADV``)     Roll twice and use the higher of the two rolls.
Disadvantage (``DADV``) Roll twice and use the lower of the two rolls.
======================= ===========================================================================

Vulnerabilities and Resistances
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

======================= ==============================================
Property                Effect
======================= ==============================================
Vulnerability (``VUL``) Take 2x from a particular damage type.
Resistance (``RES``)    Take ½ from a particular damage type.
Immunity (``IMU``)      Take no damage from a particular damage type.
======================= ==============================================

Skills
------

======================= ===================================================================
Skill                   Example Actions
======================= ===================================================================
Athletics (``ATH``)     Climb, Jump, Swim, Grapple, Reflex, Balance, Fall
Stealth (``STE``)       Sneak, Hide, Sleight of Hand, Disguise, Escape, Detect Trap
Fortitude (``FOR``)     Endurance, Resist Status Effect, Death Save, Survival
Aptitude (``APT``)      Knowledge, Heal, Operate Device, Pick Lock, Forgery, Scan, Utility
Perception (``PER``)    Spot, Listen, Search, Touch, Smell, Taste
Speech (``SPE``)        Diplomacy, Intimidate, Bluff, Persuasion
======================= ===================================================================

Attribute Effects
-----------------

+-----------+------------------------+---------------------------+---------------------------+
| Attribute | General                | Offensive                 | Defensive                 |
+===========+========================+===========================+===========================+
| ``STR``   | Feet Unlock            | | ``1PAC``                | | Chest Unlock            |
|           |                        | | Weapon Damage           | | Shield Unlock           |
|           |                        | | (``0.5-1.5DAM``)        |                           |
+-----------+------------------------+---------------------------+---------------------------+
| ``DEX``   | ``0.5SPEED``           | Weapon Unlock             | ``1PDEF``                 |
+-----------+------------------------+---------------------------+---------------------------+
| ``CON``   | ``0.5VIS``             |                           | | ``1.5HP`` per ``LVL``   |
|           |                        |                           | | ``0.5PRED``             |
+-----------+------------------------+---------------------------+---------------------------+
| ``INT``   | | ``1SP`` per ``LVL``  | | ``1MP`` per ``LVL``     | ``0.5MRED``               |
|           | | ``10%SEL``           | | Head Unlock             |                           |
|           | | Utility Unlock       |                           |                           |
+-----------+------------------------+---------------------------+---------------------------+
| ``WIS``   |                        | | ``1AP``                 | ``1MDEF``                 |
|           |                        | | Magic Power             |                           |
|           |                        | | Neck Unlock             |                           |
+-----------+------------------------+---------------------------+---------------------------+
| ``CHA``   | ``7%BUY``              | | ``1AP``                 |                           |
|           |                        | | ``1MAC``                |                           |
|           |                        | | ``1REG``                |                           |
|           |                        | | ``0.25RD``              |                           |
|           |                        | | Hand Unlock             |                           |
+-----------+------------------------+---------------------------+---------------------------+

Releases
========

2.0.0
-----

- Numerous updates and new features.
- Support Python 3.6

1.0.0
-----

- Initial Release
