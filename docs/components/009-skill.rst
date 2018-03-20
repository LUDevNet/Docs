Skill Component (9)
-------------------

This component expresses, that the object can trigger a *skill* that
manipulates the world around it. A skill is, generally speaking, the
root of a behavior tree that may be executed.

Execution may be triggered in different ways, such as equipping an item,
attacking another object in the game, or clicking a button in the hotbar.

Skills also contain information on which icon this skill/attack has,
as well as what amount of damage the skill will deal or how much health,
armor or imaginagtion it will restore.

Relevant Database Tables
........................

This component uses the following tables:

* :doc:`../database/ObjectSkills`
* :doc:`../database/SkillBehavior`
