Change Idle Flags (36)
======================

Changes the idle flags of the caster by turning the requested flags off/on.
No serialization.

Parameters
----------

.. list-table::
   :widths: 15 30
   :header-rows: 1

   * - Name
     - Description
   * - flags_on
     - The idle flag to turn on
   * - flags_off
     - The idle flag to turn off

.. note::
	The values in the flags are *not* literal numbers but rather bit indexes.
	This means the values in the flags *must* be between the values 0 and 32 inclusive.
	Anything outside of this range is undefined behavior.
	To add onto this, the behavior is as follows
	- If flag is zero, use 0.
	- Otherwise get a value that is :samp:`(1 << (flag - 1))` and set/unset that bit
