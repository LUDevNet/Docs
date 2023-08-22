Interrupt (41)
==============

This behavior interrupts a :samp:`target` which is either the actual target of this behavior, or the caster.  This discrepency is controlled by the :samp:`target` parameter in the database.

Parameters
----------

.. list-table::
   :widths: 15 15 30
   :header-rows: 1

   * - Name
     - Type
     - Description
   * - interrupt_attack
     - int_bool
     - True to interrupt attacks
   * - interrupt_block
     - int_bool
     - True to interrupt blocks
   * - interrupt_charge
     - int_bool
     - True to interrupt charge-up
   * - interupt_attack
     - int_bool
     - typo, unused parameter in 1.10.64.
   * - interupt_charge
     - int_bool
     - type, unused parameter in 1.10.64.
   * - target
     - int_bool
     - True if you use the target of this branch, false to target caster.

BitStream Serialization
-----------------------

| if target != self:
| 	**[bit]** - True if target is immune to stuns. Return if this is true.
| if “interrupt_block” false:
| 	**[bit]** - True if target is blocking interrupts. Return if this is true.
| **[bit]** - Unused system from live that likely sent the skillUid that was interrupted?  If true, serialization is as follows.
|  **[bit]** Has another interrupted skillUid
|  **[u32]** Interrupted skillUid
