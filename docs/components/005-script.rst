Script Component (5)
--------------------

The script component allows for very fine grained control over the behavior
of the object. Each object may have a server and client side script attached
which can recieve and send game messages, start and stop timers and
manipulate the world and other objects. These scripts are written in LUA
and some examples are found in the :file:`res/scripts` directory of an
unpacked client.

Relevant Database Tables
........................

This component uses the :doc:`../database/ScriptComponent` table.