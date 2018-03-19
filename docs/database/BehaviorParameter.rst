BehaviorParameter
-----------------

This table contains the parameters for any behavior in
the game. Depending on the Template of the behavior, this may
be information on subsequent behaviors, durations, flags
or even imagination, armor or health to apply.

Usually, there will be multiple rows for a single :samp:`behaviorID`,
but all with a different :samp:`parameterID`.

==================================================  ==========
Column                                              Type      
==================================================  ==========
behaviorID                                          INTEGER   
parameterID                                         TEXT      
value                                               FLOAT     
==================================================  ==========

65536 Slots