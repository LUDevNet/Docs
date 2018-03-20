Projectile Attack (4)
=====================

This behavior is used to launch a projectile that can hit other objects.

Parameters
----------

.. list-table ::
   :widths: 15
   :header-rows: 1

   * - Name
   * - LOT_ID
   * - clear_provided_target
   * - max_distance
   * - no_ally_check
   * - notify_target
   * - offset_x
   * - offset_y
   * - offset_z
   * - projectile_speed
   * - projectile_type
   * - rotate_x_degrees
   * - spread_angle
   * - spread_count
   * - spread_z_load_fudge
   * - track_radius
   * - track_target
   * - unauth_impact
   * - use_high_arc
   * - use_mouseposit
   * - use_prediction

BitStream Serialization
-----------------------

| **[s64]** - target id
| projectile count = “spread_count” parameter, minimum 1
| **[projectile count]**
| 	**[s64]** - local projectile id
| 		used for projectile impact message (behavior of impact message determined by projectile LOT skill)