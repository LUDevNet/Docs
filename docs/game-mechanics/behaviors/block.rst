Block (53)
==========

Blocks :samp:`num_attacks_can_block` attacks and casts the :samp:`break_action`
when you have reached the limit of attacks you can block.

Parameters
----------

.. list-table::
   :widths: 15 30
   :header-rows: 1

   * - Name
     - Description
   * - block_damage
     - True to block basic attack behaviors
   * - block_knockback
     - True to block knockback behaviors
   * - block_knockbacks
     - True to block knockback behaviors
   * - block_stuns
     - True to block stun behaviors
   * - break_action
     - The behavior to cast when the damage blocked is greater than the amount of damage this behavior allowed you to block
   * - num_attacks_can_block
     - The number of attacks that can be blocked

BitStream Serialization
-----------------------
| No serialization
