Basic Attack (1)
================

This behavior is used to deal damage to a target.

Parameters 
----------

.. list-table ::
   :widths: 15 30
   :header-rows: 1

   * - Name
     - Description
   * - dir_angle_xz
     - The direction to modify the attackers angle by.
   * - dir_angle_y
     - The direction to modify the attackers angle by.
   * - dir_force
     - The amount of force to apply towards angle specified in dir_angle_xz or dir_angle_y.
   * - dont_apply_immune
     - Whether or not to apply immunity to the caster of the behavior.
   * - max damage
     - The maximum amount of damage to be dealt.
   * - min damage
     - The minimum amount of damage to be dealt.
   * - on_fail_armor
     - The behavior to use on failure due to armor.
   * - on_fail_blocked
     - The behavior to use on failure due to the attack being blocked.
   * - on_fail_immune
     - The behavior to use on failure due to the target being immune.
   * - on_success
     - The behavior to use on success of the attack.
   * - radius
     - The radius of the attack.
   * - use_caster_velocity
     - Whether or not to use the casters velocity.
   * - velocity_multiplier
     - Value to multiply velocity by when attacking.

Darkflame Universe Parameter Notes
----------------------------------

As of February 11, 2022, only the following parameters are used:

- max damage
- min damage
- on_success

It is unknown whether the following need to be used:

- on_fail_armor
- on_fail_blocked
- on_fail_immune
- dont_apply_immune
- dir_angle_xz
- dir_angle_y
- dir_force
- radius
- use_caster_velocity
- velocity_multiplier

BitStream Serialization
-----------------------

Align to byte boundary.

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

- The aligning to byte boundary must be done.  The meaning of this alignment is currently unknown.
- The padding in the BitStream is required.  The meaning of the padding is also unknown.
- The attack is never blocked, the target is never immune and the attack is always successful.
- The success state is always serialized as 1 as of February 11, 2022.