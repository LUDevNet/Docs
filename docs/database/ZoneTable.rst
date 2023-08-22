ZoneTable
---------

This table contains information about a zone configuration.

.. list-table::
   :widths: 15 15 20
   :header-rows: 1

   * - Column
     - Type
     - Description
   * - zoneID                                              
     - INTEGER
     - A unique zone id
   * - locStatus                                           
     - INTEGER
     - The localization status
   * - zoneName                                            
     - TEXT
     - The zone name  
   * - scriptID                                            
     - INTEGER
     - The zone script ID
   * - ghostdistance_min                                   
     - FLOAT
     - The ghosting distance outer ring range.
   * - ghostdistance                                       
     - FLOAT
     - The ghosting distance inner ring range.
   * - population_soft_cap                                 
     - INTEGER
     - The maximum number of Civilians allowed in a zone.
   * - population_hard_cap                                 
     - INTEGER
     - The absolute maximum number of users allowed in a world. Not even a GameMaster can get in if the world population is at this value.
   * - DisplayDescription
     - TEXT
     - The display description of this zone.
   * - mapFolder
     - TEXT
     - Unknown use but is always NULL.
   * - smashableMinDistance                                
     - FLOAT
     - The minimum distance for a smashable to render? Only used in Shooting Galleries.
   * - smashableMaxDistance                                
     - FLOAT
     - The maximum distance for a smashable to render? Only used in Shooting Galleries.
   * - mixerProgram                                        
     - TEXT
     - Unknown definition.
   * - clientPhysicsFramerate                              
     - TEXT
     - The clients' physics framerate.  Has values of either NULL or high.
   * - serverPhysicsFramerate                              
     - TEXT
     - The servers' physics framerate.  Has values of either NULL or high.
   * - zoneControlTemplate                                 
     - INTEGER
     - The zone control LOT.
   * - widthInChunks                                       
     - INTEGER
     - The width of the zone in chunks. A zone is always a square but not necessarily a cube. A chunk is...
   * - heightInChunks                                      
     - INTEGER
     - The height of the zone in chunks. A chunk is...
   * - petsAllowed                                         
     - BOOLEAN
     - If true, pets are allowed to be deployed on this zone.
   * - localize                                            
     - BOOLEAN
     - Unknown definition
   * - fZoneWeight                                         
     - FLOAT
     - Unknown definition
   * - thumbnail                                           
     - TEXT
     - The thumbnail for this zone during rocket transitions.
   * - PlayerLoseCoinsOnDeath                              
     - BOOLEAN
     - If true, players lose their coins on death. The number of coins is controled by :doc:`WorldConfig`.
   * - disableSaveLoc                                      
     - BOOLEAN
     - If true, save the players location while in this world.
   * - teamRadius                                          
     - FLOAT
     - Unknown, values can be -1, 200 and NULL.  Avant Gardens is the only zone with a value of 200.
   * - gate_version                                        
     - TEXT
     - The gating version of this zone. 
   * - mountsAllowed                                       
     - BOOLEAN
     - If true, mounts are allowed to be used in this zone.

Hash bucket count: 2048 slots
