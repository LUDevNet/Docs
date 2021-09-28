Inventory Component (17)
------------------------

The inventory component holds and manages which items an object
has on itself.

The inventory of the player. This is actually a collection of storage and does not only represent the backpack (e.g Vault items are also in here).

Relevant Database Tables
........................

This component uses the :doc:`../database/InventoryComponent` table.

Relevant Game Messages
......................

* :gm:`PopEquippedItemsState`
* :gm:`MoveItemInInventory`
* :gm:`AddItemToInventoryClientSync`
* :gm:`RemoveItemFromInventory`
* :gm:`EquipInventory`
* :gm:`UnequipInventory`
* :gm:`SetInventorySize`
* :gm:`UseNon-EquipmentItem`
* :gm:`MoveInventoryBatch`
* :gm:`MoveItemBetweenInventoryTypes`
* :gm:`NotifyNotEnoughInvSpace`
* :gm:`MarkInventoryItemAsActive`

XML Serialization :samp:`<inv>`
...............................

:csl: LOT of the item in the consumable slot ("consumable slot lot" ?)

Storage containers :samp:`<bag>`
''''''''''''''''''''''''''''''''
A storage container :samp:`<b>`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(e.g Items, Models, Vault Items, Behaviors)

:m: Size of the bag. (Amount of slots)
:t: Type of the bag. See InventoryType enum for values.

User Item groups :samp:`<grps>`
'''''''''''''''''''''''''''''''
This is used to selectively display models or bricks.

A group :samp:`<grp>`
~~~~~~~~~~~~~~~~~~~~~
:id: ID of the group. In the captures this was usually the literal string "user_group" and a unique number.
:l: LOTs of the items in this group, separated by spaces.
:n: Displayed name of the group.
:t: Type of the group. See bag types for values.
:u:

The contents of the "bags"/storage containers :samp:`<items>`
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
These don't actually have to be items, e.g models and bricks are listed here too.

:nn: (?)

Items in the storage container :samp:`<in>`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:t: Type of the bag. See InventoryType enum for values.

An item :samp:`<i>`
^^^^^^^^^^^^^^^^^^^

:b: Boolean whether the item is bound. If it isn't, this attribute isn't there at all, if it is, it's set to 1.
:c: Amount of items for stackable items.
:eq: Boolean whether the item is equipped. If it isn't, this attribute isn't there at all, if it is, it's set to 1.
:id: Object ID of the item.
:l: LOT of the item. See cdclient for correct values.
:s: Slot of the item. (0-indexed)
:sk: Some kind of ID for models. Investigate. Referred to by client strings as “subkey”?

Extra info :samp:`<x>`
++++++++++++++++++++++
:b:
:ma: Module assembly info
:ub:
:ud:
:ui:
:um:
:un: UGC name (?)
:uo:
:up:
