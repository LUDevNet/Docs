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

When a skill is triggered on the client, it will send a :gm:server:`StartSkill` message. This message
contains a bitstream that represents all the decisions the client has made whenever a behavior has
multiple paths to continue. An example for this would be the :doc:`behaviors/aoe` which will serialize
the amount of objects within the area, and then the object id and remaining bitstream for all of
these objects.

When a behavior is not completed immediately, it will serialize a :samp:`handleID`, which will then
later be used to identify a :gm:server:`SyncSkill` message that serializes the continued execution. It
is possible that this happens multiple times for a single skill execution.

.. uml ::

   @startuml
   Client -> Server: StartSkill
   Server -> Client: EchoStartSkill

   loop
       Client -> Server: SyncSkill
       Server -> Client: EchoSyncSkill
   end
   @enduml

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
   behaviors/over-time
   behaviors/imagination
   behaviors/target-caster
   behaviors/stun
   behaviors/duration
   behaviors/knockback
   behaviors/attack-delay
   behaviors/car-boost
   behaviors/fall-speed
   behaviors/shield
   behaviors/repair-armor
   behaviors/speed
   behaviors/dark-inspiration
   behaviors/loot-buff
   behaviors/venture-vision
   behaviors/spawn-object
   behaviors/lay-brick
   behaviors/switch
   behaviors/buff
   behaviors/jetpack
   behaviors/skill-event
   behaviors/consume-item
   behaviors/skill-cast-failed
   behaviors/imitation-skunk-stink
   behaviors/change-idle-flags
   behaviors/apply-buff
   behaviors/chain
   behaviors/change-orientation
   behaviors/force-movement
   behaviors/interrupt
   behaviors/alter-cooldown
   behaviors/charge-up
   behaviors/switch-multiple
   behaviors/start
   behaviors/end
   behaviors/alter-chain-delay
   behaviors/camera
   behaviors/remove-buff
   behaviors/grab
   behaviors/modular-build
   behaviors/npc-combat-skill
   behaviors/block
   behaviors/verify
   behaviors/taunt
   behaviors/air-movement
   behaviors/spawn-quickbuild
   behaviors/pull-to-point
   behaviors/property-rotate
   behaviors/damage-reduction
   behaviors/property-teleport
   behaviors/clear-target
   behaviors/take-picture
   behaviors/mount
   behaviors/skill-set
