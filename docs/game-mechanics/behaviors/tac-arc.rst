TacArc (2)
==========

This behavior executes the action on a group of object nearby which
fit the given parameters.

Parameters
----------

.. list-table ::
   :widths: 15
   :header-rows: 1

   * - Name
   * - action
   * - affects_caster
   * - angle
   * - angle_weight
   * - blocked action
   * - check_env
   * - clear_provided_target
   * - defers_smashables
   * - distance_weight
   * - far_height
   * - far_width
   * - first_within_range
   * - height
   * - ignore_faction
   * - ignore_faction_1
   * - include_faction
   * - include_faction1
   * - include_faction2
   * - include_faction3
   * - include_faction_1
   * - include_faction_2
   * - include_faction_3
   * - lower_bound
   * - max range
   * - max target
   * - max targets
   * - max_range
   * - method
   * - min range
   * - miss action
   * - near_height
   * - near_width
   * - offset_x
   * - offset_y
   * - offset_z
   * - prefers_enemies
   * - radius
   * - run_speed
   * - target_enemy
   * - target_friend
   * - target_self
   * - target_team
   * - upper_bound
   * - use_attack_priority
   * - use_picked_target
   * - use_target_position

BitStream Serialization
-----------------------

| hit_something= **[bit]**
| if hit_something:
| 	if ``check_env`` parameter:
| 		**[bit]** - ???, always 0?
| 	**[u32]** - number of targets
| 		**[s64]** - target object id
| 	for each target:
| 		-> `action`
| else:
| 	if ``blocked_action`` parameter exists:
| 		**[bit]** - is blocked
| 		if blocked -> `blocked action`, else -> `miss action`
| 	else:
| 		-> miss action
