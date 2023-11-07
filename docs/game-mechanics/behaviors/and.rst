And (3)
=======

This behavior executes all of its component behaviors in parallel.

Parameters
----------

The valid parameters all take the form :samp:`behavior X` where
X is a number starting at 1. Then execute the behaviors in this order.
If there are more than 10, the client sorts the list by the behavior number.

Example
-------
The :Behavior:`1698` will execute the behaviors in the order 375 (behavior 1), 1700 (behavior 2), 1699 (behavior 3)


BitStream Serialization
-----------------------

| **[foreach behavior in behaviors]**
|  -> behavior
