Naming and Describing Models
----------------------------

While editing on properties, players have the ability to name and describe their models.
Players also have the ability to name and describe their property.

The following diagram shows the expected reply from a server in order to succeed in the naming/describing process

.. uml::

    @startuml
    ==Player Finished Naming/Describing Model==
    Client -> WorldServer: [<b>Game Message UpdatePropertyOrModelForFilterCheck</b>] 

    ==Property or Model Name/Description Has Been Moderated (reply can be in any order)==
    WorldServer -> Client: [<b>Game Message SetName</b>] Sent to the model in the world
    WorldServer -> Client: [<b>Item Component Serialization</b>] Description updated with moderated description
    @enduml

Networked message definitions:

* Game Message :gm:server:`UpdatePropertyOrModelForFilterCheck`

* Game Message :gm:client:`SetName`

Component serialization:

* Item Component :packet:`raknet/client/replica/item/struct.ItemConstruction`

Until the SetName message **and** Item Component serialization are sent, the client will be
unable to name or describe models until a time out occurs, upon which the client side name and description will revert
to their previous values.

The following will happen if the client does not receive **both** of these replies:

* The name will not be updated unless the SetName Game Message is sent from the WorldServer to the Client.
* The description will not be updated unless the Item Component Serialized with the moderated description. 


What should happen after receiving the Client message:
------------------------------------------------------

If a user successfully changes the name and/or description and the values are approved and are different from their defaults,
the model should become a user generated model and lose its default model property so that the name can be preserved
when the model is picked up.  While there is no live packet captures showing the FilterCheck Game Message being sent,
other live packet captures imply that even a simple name/description change did change the models LOT to :lot:`14`
and when placed back in the inventory, was changed to :lot:`6662`.


This can be assumed because Entity Construction Serialization from live packet captures would show
that models LOT would now be 14.  Even when an entity had no description and still had the default name,
the entity was still set to LOT 14.
