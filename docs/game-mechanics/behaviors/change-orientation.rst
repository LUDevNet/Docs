Change Orientation (39)
=======================

Details unknown

Parameters
----------

.. list-table::
   :widths: 15 30
   :header-rows: 1

   * - Name
     - Description
   * - orient_caster
     - If true, the :samp:`target_to_orient` is the caster and the target is :samp:`target_to_orient_to`. Otherwise flip the targets.
   * - to_angle
     - If true, orient the :samp:`target_to_orient` based on angle below
   * - angle
     - The angle in degrees to orient to
   * - relative
     - If true, apply the above angle orientation relative to the current orientation
   * - to_target
     - If true, orient the :samp:`target_to_orient` to the :samp:`target_to_orient_to`.

.. note:: 
	If Both :samp:`to_target` and :samp:`to_angle` are set to true, :samp:`to_target` will take priority if there is a :samp:`target_to_orient_to`.

Removed in 1.10.64
-------------------

.. list-table::
   :widths: 15 30
   :header-rows: 1

   * - Name
     - Description
   * - behavior 1
     - ???
   * - behavior 2
     - ???
   * - behavior 3
     - ???
   * - to_point
     - ???
   * - duration
     - ???

BitStream Serialization
-----------------------

.. todo:: investigate
