Area of Effect / AoE (7)
========================

This behavior calls the specified action on all / a maximum of players
around it.

Parameters
----------

.. list-table ::
   :widths: 15
   :header-rows: 1

   * - Name
   * - action
   * - ignore_faction
   * - ignore_faction1
   * - ignore_faction2
   * - ignore_faction3
   * - include_faction
   * - max targets
   * - radius
   * - target_enemy
   * - target_friend
   * - target_self
   * - target_team
   * - use_target_as_caster
   * - use_target_position

BitStream Serialization
-----------------------

| **[u32]** - number of targets
| 	**[s64]** - target object id
| **[for target in targets]**
|   -> action(target)
