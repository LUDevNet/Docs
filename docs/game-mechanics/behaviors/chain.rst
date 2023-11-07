Chain (38)
==========

Details unknown

Parameters
----------

.. list-table::
   :widths: 15 30 15
   :header-rows: 1

   * - Name
     - Description
     - Default value
   * - behavior X
     - Behavior to execute as a chain step, should be sequential starting from 1 and increasing by 1 for each behavior.
     - No default
   * - chain_delay
     - The delay to apply between each attack of the chain.
     - 0.5 if field is not present.

BitStream Serialization
-----------------------

| **[u32]** - The smallest behavior such that behavior n satisfies the following criteria
|			- :samp:`chain_delay * n < delay_since_first_behavior_called`
| -> :samp:`behavior X`

.. note:: 
	- Like with attack_delay, this delay should not be simulated on a server due to latency adding onto the delay.

