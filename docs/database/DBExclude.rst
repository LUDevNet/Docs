DBExclude
---------

This table marks what :samp:`columns` in what :samp:`table` to exclude from
the database. The column can be a :samp:`*` to denote to exclude the whole table.

.. list-table::
   :widths: 15 15 20
   :header-rows: 1

   * - Column
     - Type
     - Description
   * - table
     - TEXT
     - The table affected by the exclude
   * - column
     - TEXT
     - The column to exclude, or the whole table

Allocated rows: 128 Slots
