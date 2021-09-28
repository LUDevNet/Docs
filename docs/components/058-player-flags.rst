Player Flags Component (58)
---------------------------

This component likely manages the player flags.

Relevant Database Tables
........................

This component uses the following tables:

* :doc:`../database/PlayerFlags`

Relevant Game Messages:
.......................

* :gm:`SetTooltipFlag`
* :gm:`SetFlag`
* :gm:`NotifyClientFlagChange`

XML Serialization :samp:`<flag>`
................................

This component is serialized to XML to store its data.

Flags :samp:`<f>`
'''''''''''''''''

Flags are serialized as blocks of 64 bit. The ID of such a block is
the common prefix you get when shifting all flags indices to the right
by 6 bits.

:id: The ID of the flag group
:v: The value of 64 flags
