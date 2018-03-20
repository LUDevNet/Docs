Basic Attack (1)
================

This behavior is used to deal damage to the current target.

Parameters
----------

.. list-table ::
   :widths: 15
   :header-rows: 1

   * - Name
   * - dir_angle_xz
   * - dir_angle_y
   * - dir_force
   * - dont_apply_immune
   * - max damage
   * - min damage
   * - on_fail_armor
   * - on_fail_blocked
   * - on_fail_immune
   * - on_success
   * - radius
   * - use_caster_velocity
   * - velocity_multiplier

BitStream Serialization
-----------------------

align to byte boundary (don’t ask me why, this (and the “padding” below) is completely pointless)

| **[u16]** - “padding”
| **[bit]** - ???, always False?
| **[bit]** - ???, always False?
| **[bit]** - ???, always True?
| **[u32]** - ???
| **[u32]** - damage
| **[bit]** - ???, maybe whether the attack is part of an Area of Effect attack?
