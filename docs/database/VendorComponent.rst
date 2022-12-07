VendorComponent
---------------

This table tells a Vendor Component information about the vendor.
The loot matrix index is the items the vendor sells, for example.

.. list-table ::
   :widths: 15 15 20
   :header-rows: 1

   * - Column
     - Type
     - Description
   * - id
     - INTEGER
     - The component id
   * - buyScalar
     - FLOAT
     - The multiplier to apply to items sold by this vendor
   * - sellScalar
     - FLOAT
     - The multiplier to apply to items sold to this vendor
   * - refreshTimeSeconds
     - FLOAT
     - The amount of time in seconds it takes this vendors' inventory to refresh
   * - LootMatrixIndex
     - INTEGER
     - The loot matrix index of the inventory of this vendor

Allocated rows: 128 Slots
