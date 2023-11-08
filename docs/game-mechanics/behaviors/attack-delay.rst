Attack Delay (18)
=================
When this node is reached in a behavior tree, the current traversal through this behavior branch is halted
and will :gm:server:`SyncSkill` after a :samp:`delay` :samp:`num_intervals` times.  The server is expected to keep track
of what behavior is waiting for a sync so the sync can be done at a later time.

The server is then expected to :gm:client:`EchoStartSkill` to all connected clients.

The attack is then continued later with a :gm:server:`SyncSkill` message from the client.

See the diagram in :doc:`../skill-system` for a diagram on how this interaction looks.

For skills cast by a client, it is not advised to predict whether or not the player was actually able to cast a skill in real time.
This is because you will get desync in what a client expects to happen vs what actually happened which will cause invisible enemies,
mis-match health bars and further issues.  

Parameters
----------

.. list-table::
   :widths: 15 15 30
   :header-rows: 1

   * - Name
     - Value
     - Description
   * - action
     - int32
     - The action to take when :samp:`delay` has passed
   * - delay
     - float
     - The delay between intervals
   * - ignore_interrupts
     - bool
     - Whether or not to ignore interrupts
   * - num_intervals
     - int32
     - The number of times to sync this behavior


Deprecated parameters
^^^^^^^^^^^^^^^^^^^^^
There is 1 singular behavior that has two extra parameters, :samp:`Behavior 1` and :samp:`Behavior 2`.

This :behavior:`25652`, whose root is this :behavior:`25607`, does not appear to be used by and scripts, has no
entry in the :doc:`../../database/SkillBehavior`

BitStream Serialization
-----------------------

| **[u32]** - behavior handle
