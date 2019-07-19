Pet Control Component (34)
--------------------------

This component is likely responsible for managing the pets that the local player
has tamed. It is attached to the player as opposed to the multiple :doc:`026-pet`
attached to the individual pets.

Relevant Game Messages
......................

* :ref:`gm-pet-response`
* :ref:`gm-register-pet-id`
* :ref:`gm-register-pet-dbid`
* :ref:`gm-add-pet-to-player`
* :ref:`gm-show-pet-action-button`

XML Serialization :samp:`<pet>`
...............................

This component is serialized to XML to store its data.

:a: (?)

A pet :samp:`<p>`
'''''''''''''''''

:id: Pet ObjectID
:l: Pet LOT
:m: (?)
:n: Pet Name
:t: (?)
