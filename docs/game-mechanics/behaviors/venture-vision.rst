Venture Visison (26)
====================

This behavior manages whether or not the player can see minibosses or collectibles on their personal minimap.
Pet digs seem to be disabled altogether however.  In the 1.10.64 client, this behavior is referenced as :samp:`ShowMinimapExtrasBehavior`

Parameters
----------

.. list-table::
   :widths: 15 15 30
   :header-rows: 1

   * - Name
     - Type
     - Description
   * - show_collectibles
     - Boolean
     - Whether or not to show collectibles.
   * - show_minibosses
     - Boolean
     - Whether or not to show minibosses.
   * - show_pet_digs
     - Boolean
     - Whether or not to show pet digs.  Non-functional during live.

Relevant Game Messages
----------------------

:gm:client:`UiMessageServerToSingleClient`

Amf3 Serialization
------------------

| In an amf3 Array:
| Associative map:
|   :samp:`bShowPetDigs`: boolean
|   :samp:`bShowMinibosses`: boolean
|   :samp:`bShowCollectibles`: boolean
