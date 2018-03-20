Movement Switch (6)
===================

Calls different behaviors depending on what the current movement type of the originator object is.

Parameters
----------

.. list-table ::
   :widths: 15
   :header-rows: 1

   * - Name
   * - air_action
   * - double_jump_action
   * - falling_action
   * - ground_action
   * - jetpack_action
   * - jump_action
   * - moving_action

BitStream Serialization
-----------------------

.. todo:: Figure out what type id air and moving are

| **[u32]** - movement type, 1 -> ground, 2 -> jump, 3 -> falling, 4 -> double-jump, 6 -> jetpack
