Skill / Behavior System
=======================

You will receive a StartSkill and depending on the Skill a few messages of SyncSkill. Those GM’s contain a Bitstream which contains information about the skill, which the player used. You start with a SkillID. With the skillID you can get the first behaviorID from the “SkillBehavior” table from the :doc:`../database`.

To know what type the behaviorID is, you will have to query the “templateID” from the “BehaviorTemplate” table.
You can look up the name of the templateID from the “BehaviorTemplateName” table. With the behaviorID, you will have to load the parameters of the Skill from the “BehaviorParameter” table.
At the top of the :doc:`../game-messages` document you can find the structure of the templateID, which are parsed from the BitStream.
Depending on the template, you will get the next behaviorID either from the BitStream or the BehaviorParameter table. Some templates does split the bitstream into a SyncSkill-GameMessage.
To look them up, you can receive a handleID both from the SyncSkill, which contains the bitstream and from the SyncSkill-Bitstream, which instantiate the SyncSkill.
