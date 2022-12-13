Player Flags Component (58)
---------------------------

This component manages the player flags.  See :doc:`../game-mechanics/flag-system` for the list of all known flags.

.. note::

    Tooltip flags are unrelated to this component.  See :doc:`004-character` for information regarding these.

Relevant Database Tables
........................

This component uses the following tables:

* :doc:`../database/PlayerFlags`

Relevant Game Messages
......................

* :gm:server:`SetFlag`
* :gm:client:`NotifyClientFlagChange`

Component XML Format
....................

| :samp:`flag` - Player Flag Component data
|     :samp:`f` - Player flag
|     :samp:`attr id` - This flags index
|     :samp:`attr v` - This flags value
|     :samp:`s` - Session flag
|     :samp:`attr si` - Session flag Id as a literal number (ex. 114).  Each session flag gets its own :samp:`s` element.

Flags are always saved as blocks of 64 bits.
When a flag is set, its index in the flags list is the flag id divided by 64, truncated to an int.
The position at the index calculated above is the flag id modulo 64.

Example code to set a player flag:

.. code-block:: python

    player_flags = {}
    def set_player_flag (flag_id, turn_flag_on):
        # First calculate the index, in this case it equals 17
        flag_index = int(flag_id / 64)
        # Then calculate the position, which is also 17, and set the bit at that position.
        flag_value_shifted = 1 << flag_id % 64
        # Then check if we already have flags at this flag index
        flag_to_update = player_flags.get(flag_index)
        if flag_to_update != None:
            if turn_flag_on == True:
                # Turn the bit at flag_value_shifted in flag_to_update to True
                flag_to_update = flag_to_update | flag_value_shifted
            else:
                # Turn the bit at flag_value_shifted in flag_to_update to False by inverting the binary
                # value of flag_value_shifted and ANDing with flag_to_update
                flag_to_update = flag_to_update & ~flag_value_shifted
            player_flags[flag_index] = flag_to_update
        else:
            # Create the new flag value and insert it into the dictionary of flags
            new_flag_value = flag_value_shifted
            player_flags[flag_index] = new_flag_value

    # Turns player flag 1105 on
    set_player_flag(1105, True)
    # {17: 131072}
    print(player_flags)
    # Does nothing since player flag 1105 is already on
    set_player_flag(1105, True)
    # {17: 131072}
    print(player_flags)
    # Turns player flag 2 on
    set_player_flag(2, True)
    # {17: 131072, 0: 4}
    print(player_flags)
    # Turns player flag 1105 off
    set_player_flag(1105, False)
    # {17: 0, 0: 4}
    print(player_flags)

Here is how flag changes are communicated between the client and the WorldServer:

.. uml::

    @startuml
    skinparam sequenceMessageAlign center
    group Client sets a flag
        Client -> WorldServer: [<b>Game Message SetFlag</b>]
    end

    WorldServer -> Client: [<b>Game Message NotifyClientFlagChange</b>]
    @enduml

If a flag is a session flag, it should be set for the duration of a session and when the player changes character
or logs out, these flags should be cleared.  A session flag can be found by querying the :doc:`../database/PlayerFlags`
table and if the :samp:`SessionOnly` boolean is set to true, the flag is set for the session.

There are two flags in live, flags :samp:`1110` and :samp:`2099` which have :samp:`SessionZoneOnly` set to true.
The use of :samp:`SessionZoneOnly` is guessed to be to detect if a player has done something in a zone this session.
