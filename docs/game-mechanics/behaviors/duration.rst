Duration (16)
=============

This behavior describes that the subsequent ones are active (only) for some stretch of time.

Parameters
----------

.. list-table ::
   :widths: 15 30
   :header-rows: 1

   * - Name
     - Description
   * - action
     - The behavior to execute next
   * - duration
     - How long the subsequent behaviors are active
   * - originator_is_owner
     - ???

Possibly deprecated
^^^^^^^^^^^^^^^^^^^

.. list-table ::
   :widths: 15 30
   :header-rows: 1

   * - Name
     - Description
   * - behavior 1
     - Subsequent behavior?
   * - behavior 2
     - Subsequent behavior?

Likely errors
^^^^^^^^^^^^^

.. list-table ::
   :widths: 15 30
   :header-rows: 1

   * - Name
     - Description
   * - strength
     - Belonging to another behavior?
   * - angle
     - Belonging to another behavior?
   * - delay
     - Should have been `duration`?

BitStream Serialization
-----------------------

.. todo:: investigate

| -> action
