Skill / Behavior System
=======================

When an object in the game has a :doc:`../components/009-skill` attached, it has one or more
skills attached to it, which it can trigger. A skill is the root of a tree of behaviors that
get executed once the skill is triggered.

In the case of an attack by a player, these skills are executed on the client and the synchronized
to the server. The server may then interpret what the client has done (and possibly sanity-check it)
and execute any server side consequences of the attack. This includes updating the health of enemies
for all players and smashing an object once it has been killed.

For enemies, the Combat AI triggers the skill and as such the server must execute it. That information
is then synchronized to the clients for display.

Handling a behavior
-------------------

When a skill is triggered on the client, it will send a :any:`gm-start-skill` message. This message
contains a bitstream that represents all the decisions the client has made whenever a behavior has
multiple paths to continue. An example for this would be the _`Area of Effect``which will serialize
the amount of objects within the area, and then the object id and remaining bitstream for all of
these objects.

When a behavior is not completed immediately, it will serialize a :samp:`handleID`, which will then
later be used to identify a :any:`gm-sync-skill` message that serializes the continued execution. It
is possible that this happens multiple times for a single skill execution.

Behavior Templates
------------------

Via the :doc:`../database/BehaviorTemplate` table, each behavior is assigned a template. This template
defines what the behavior does, what it serializes to the bit stream and which subsequent actions
will be triggered. These templates are parameterized via the :doc:`../database/BehaviorParameter` table.

The following is a list of (networked) behavior templates.

.. toctree::
   :maxdepth: 1

   behaviors/basic-attack
   behaviors/tac-arc
   behaviors/and
   behaviors/projectile-attack
   behaviors/heal
   behaviors/movement-switch
   behaviors/aoe
   behaviors/play-effect
   behaviors/immunity
   behaviors/damage-buff
   behaviors/damage-absorption


Stun
^^^^
| if target != self:
| 	note that for some reason this does not work for projectiles, todo: investigate
| 	**[bit]** - ???, always False?


Knockback
^^^^^^^^^
**[bit]** - ???, always False?


Attack Delay, Switch
^^^^^^^^^^^^^^^^^^^^
seem to work the same; this behavior causes SyncSkill messages, which use the behavior handle as ID and “action” as the behavior to execute on SyncSkill

| **[u32]** - behavior handle


Switch
^^^^^^
| state = True
| if “imagination” parameter > 0 or not “isEnemyFaction” parameter:
| 	state= **[bit]** - switch state
| if state:
| 	-> action_true
| else:
| 	-> action_false


Chain
^^^^^
| **[u32]** - chain index, basically attack combo in attacks, 1-based
| -> relevant action


ForceMovement
^^^^^^^^^^^^^
| if any of “hit_action”, “hit_action_enemy”, “hit_action_faction” is not 0:
| 	**[u32]** - behavior handle
| 	-> SyncSkill, see AirMovement for details


Interrupt
^^^^^^^^^
| if target != self:
| 	**[bit]** - ???, always False?
| if “interrupt_block” parameter == 0:
| 	**[bit]** - ???, always False?
| **[bit]** - ???, always False?


SwitchMultiple
^^^^^^^^^^^^^^
mostly used for charge up action

| **[float]** - value
| if value <= “value_1” parameter:
| 	-> behavior_1
| else:
| 	-> behavior_2

AirMovement
^^^^^^^^^^^
like Attack Delay, this causes SyncSkill messages, which use the behavior handle as ID but have the behavior to execute specified in the SyncSkill bitstream

| **[u32]** - behavior handle
| *SyncSkill structure:*
| **[u32]** - behavior id
| **[u64]** - target object id
