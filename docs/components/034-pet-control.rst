Pet Control Component (34)
--------------------------

This component is likely responsible for managing the pets that the local player
has tamed. It is attached to the player as opposed to the multiple :doc:`026-pet`
attached to the individual pets.

Relevant Game Messages
......................

* :gm:`PetResponse`
* :gm:`RegisterPetId`
* :gm:`RegisterPetDbid`
* :gm:`AddPetToPlayer`
* :gm:`ShowPetActionButton`

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
