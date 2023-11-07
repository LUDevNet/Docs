Car Boost (19)
==============

Boost a player in a car for :samp:`time`.
If the player does not have any boosts active, you will cast :samp:`action` otherwise you will cast :samp:`action_failed`

Parameters
----------

.. list-table::
   :widths: 15 30
   :header-rows: 1

   * - Name
     - Description
   * - action
     - Action to execute on being able to add the boost.
   * - action_failed
     - Action to execute when the boost could not be activated.
   * - active
     - Unused in 1.10.64.
   * - time
     - The amount of time to add the boost for.


.. note::
	The effect played when you succeed in boosting is hard coded in the client. If the :samp:`time` is greater than 3.5, 
	:samp:`boostCam1` is played, otherwise if the :samp:`time` is greater than 2.0, :samp:`boostCam2` will play,
	otherwise :samp:`boostCam3` will play.


BitStream Serialization
-----------------------
**[bit]** - 1 if able to add active boost, 0 otherwise.
