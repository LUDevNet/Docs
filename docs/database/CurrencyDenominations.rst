CurrencyDenominations
---------------------

This table contains the games coin currency denominations.
Each row maps a currency amount to a LOT which is the item that is spawned when said value is dropped.
An example is the :lot:`LOT for one coin <163>` which is what is spawned when 1 coin is dropped.

.. list-table::
   :widths: 15 15 20
   :header-rows: 1

   * - Column
     - Type
     - Description
   * - value
     - INTEGER
     - The currency amount in in game value
   * - objectid
     - INTEGER
     - The LOT of the coin this denomination represents

Allocated rows: 16 Slots
