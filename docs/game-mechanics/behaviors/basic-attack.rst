Basic Attack (1)
================

This behavior is used to deal damage to the current target.

Parameters
----------

.. list-table ::
   :widths: 15 30
   :header-rows: 1

   * - Name
     - Description
   * - dir_angle_xz
     - The direction to modify the attackers angle by?  Currently unused in Darkflame Universe.
   * - dir_angle_y
     - The direction to modify the attackers angle by?  Currently unused in Darkflame Universe.
   * - dir_force
     - The amount of force to apply towards angle specified in :samp:`dir_angle_xz` or :samp:`dir_angle_y`?  Currently unused in Darkflame Universe.
   * - dont_apply_immune
     - Whether or not to apply immunity to the caster of the behavior.  Currently unused in Darkflame Universe.
   * - max damage
     - The maximum amount of damage to be dealt.
   * - min damage
     - The minimum amount of damage to be dealt.
   * - on_fail_armor
     - The behavior to use on failure due to armor.  Currently unused in Darkflame Universe.
   * - on_fail_blocked
     - The behavior to use on failure due to the attack being blocked.  Currently unused in Darkflame Universe.
   * - on_fail_immune
     - The behavior to use on failure due to the target being immune.  Currently unused in Darkflame Universe.
   * - on_success
     - The behavior to use on success of the attack.
   * - radius
     - The radius of the attack.  This is likely deprecated as only `one behavior <https://explorer.lu/skills/69>`_ currently uses this.  Currently unused in Darkflame Universe.
   * - use_caster_velocity
     - Whether or not to use the casters velocity.  Currently unused in Darkflame Universe.
   * - velocity_multiplier
     - Value to multiply velocity by when attacking.  Currently unused in Darkflame Universe.

BitStream Serialization
-----------------------

align to byte boundary

| **[u16]** - Required BitStream Padding.
| **[bit]** - True if the attack was blocked, false otherwise.
| **[bit]** - True if the the target is immune, false otherwise.
| **[bit]** - True if the attack was successful, false otherwise.
| **[u32]** - Required BitStream Padding.
| **[u32]** - Amount of damage that was dealt.
| **[bit]** - True if the target died from the attack.  False otherwise.
| **[u8]**  - The success state of the attack.

DarkFlame Universe Server Side Calculation Notes
------------------------------------------------

- The aligning to byte boundary is pointless but must be done.
- The padding in the BitStream is also pointless however it must be done.
- When doing server side calculations for the BitStream, the attack is never blocked, the target is never immune and the attack is always successful.
- The success state is always serialized as 1 as of February 11, 2022.