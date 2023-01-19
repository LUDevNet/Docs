Area of Effect / AoE (7)
========================

This behavior calls the specified action on all / a maximum number of entities in the casters' radius.

Parameters
----------

.. list-table::
   :widths: 15 30
   :header-rows: 1

   * - Name
     - Description
   * - action
     - The behavior to be performed.
   * - ignore_faction
     - A faction to ignore during targetting.
   * - ignore_faction1
     - A faction to ignore during targetting.
   * - ignore_faction2
     - A faction to ignore during targetting.
   * - ignore_faction3
     - A faction to ignore during targetting.
   * - include_faction
     - A faction to include in targetting
   * - max targets
     - The maximum number of allowed targets.
   * - radius
     - The radius to check for targets in.
   * - target_enemy
     - Whether or not to target an enemy.
   * - target_friend
     - Whether or not to target a friend.
   * - target_self
     - Whether or not to target self.
   * - target_team
     - Whether or not to target a team.
   * - use_target_as_caster
     - Whether or not to use the target as the caster.
   * - use_target_position
     - Whether or not to use the targets' position.

BitStream Serialization
-----------------------

| **[u32]** - The number of targets.
|   **[s64]** - The target object id.
| **[for target in targets]**
|   -> action(target)
