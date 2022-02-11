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

align to byte boundary (don’t ask me why, this (and the "padding" below) is completely pointless)

| **[u16]** - This is just :samp:`padding`.
| **[bit]** - True if the attack was :samp:`blocked`.  False otherwise.
| **[bit]** - True if the the target is :samp:`immune`.  False otherwise.
| **[bit]** - True if the attack was successful.  False otherwise.  
| **[u32]** - This is just :samp:`padding`.
| **[u32]** - Amount of damage that was dealt.
| **[bit]** - Whether the target has died?  This value is read in but is never used.
| **[u8]**  - The success state of the attack.