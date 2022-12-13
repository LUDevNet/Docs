PlayerFlags
-----------

Configuration for the :doc:`../game-mechanics/flag-system`.

.. list-table ::
   :widths: 15 15 20
   :header-rows: 1

   * - Column
     - Type
     - Description
   * - id
     - INTEGER
     - A flag id.
   * - SessionOnly
     - BOOLEAN
     - Whether or not this flag is set only for a play session.
   * - OnlySetByServer
     - BOOLEAN
     - Whether or not this flag is only set by the server.
   * - SessionZoneOnly 
     - BOOLEAN
     - Whether or not this flag is only set for the session in the current zone(?)

Allocated space: 512 Slots
