`Basic Attack (1) <https://github.com/DarkflameUniverse/DarkflameServer/blob/main/dGame/dBehaviors/BasicAttackBehavior.cpp>`_
=============================================================================================================================

This behavior is used to deal damage to the current target.

`Parameters <https://github.com/DarkflameUniverse/DarkflameServer/blob/main/dGame/dBehaviors/BasicAttackBehavior.cpp#L142>`_
----------------------------------------------------------------------------------------------------------------------------

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
     - The amount of force to apply towards angle specified in :samp:`dir_angle_xz` or :samp:`dir_angle_y`.
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

DarkFlame Universe Server Parameter Notes
-----------------------------------------

As of February 11, 2022, only the following parameters are used:

- max damage
- min damage
- on_success

The following parameters are not attached to any behavior trees or skills from live:

- dir_angle_xz
- dir_angle_y
- dir_force
- radius
- use_caster_velocity
- velocity_multiplier

It is unknown whether the following need to be used:

- on_fail_armor
- on_fail_blocked
- on_fail_immune
- dont_apply_immune

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

`DarkFlame Universe Server Side Calculation Notes <https://github.com/DarkflameUniverse/DarkflameServer/blob/42f6f2f10b5971dd13faa18e2018892ce21ce3c3/dGame/dBehaviors/BasicAttackBehavior.cpp#L79>`_
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

- The aligning to byte boundary is pointless but must be done.
- The padding in the BitStream is also pointless however it must be done.
- The attack is never blocked, the target is never immune and the attack is always successful.
- The success state is always serialized as 1 as of February 11, 2022.