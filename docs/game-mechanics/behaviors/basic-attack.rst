Basic Attack (1)
================

This behavior is used to deal damage to a target.

Parameters 
----------

.. list-table::
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
     - The behavior to use on failure due to the target having armor.
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
     - Value to multiply velocity by when attacking(?).

It is unknown what the following variables are used for:
- dont_apply_immune
- dir_angle_xz
- dir_angle_y
- dir_force
- radius
- use_caster_velocity
- velocity_multiplier

BitStream Serialization
-----------------------

Align to the byte boundary

| **[u16]** - Number of bits used for this basic attack serialization and all sub-branches. (referred to as :samp:`allocatedSize`)
| Save the offset at this position for use later (referred to here as :samp:`startOffset`)

.. note::
  | If the target blocked the attack, :samp:`allocatedSize` would be a 1. If the target was immune it would be a 2. If the success state branches are reached, then this value also represents the
  | sum of all the sub behaviors!  

| **[bit]** - True if the attack was blocked, false otherwise.
| if blocked:
|   :samp:`on_fail_blocked`
|   align the bitStream to :samp:`startOffset + allocatedSize` and return
| **[bit]** - True if the the target is immune, false otherwise.
| if immune:
|   :samp:`on_fail_immune`
|   align the bitStream to :samp:`startOffset + allocatedSize` and return
| **[bit]** - True if the attack dealt any damage at all, false otherwise.
| if any damage was done at all:
|   **[u32]** - The amount of armor damage that was dealt.
|   **[u32]** - Amount of life damage that was dealt.
|   **[bit]** - Whether or not the target died from the basic attack.
| **[u8]**  - The success state of the attack.
| if success state == 1:
|   :samp:`on_success`
| else if success state == 2:
|   :samp:`on_fail_armor`
| else:
|     if success state != 3:
|       align the bitStream to :samp:`startOffset + allocatedSize` and return
|     else:
|       :samp:`on_fail_immune`
| align the bitStream to :samp:`startOffset + allocatedSize` and return

.. note::
 | For serializing the behavior, the success state is determined as follows:
 | if *any* health damage was done at all, the success state is 1.
 | if *zero* health damage was done and armor damage is greater than zero, the success state is 2. Has one caveat mentioned below.
 | if none of the above are true and any of the following are true, the success state is 3:
 | - armor damage was dealt but no :samp:`on_fail_armor` behavior was present.
 | - the attack was not successful i.e. zero damage was done, both in armor and in health

