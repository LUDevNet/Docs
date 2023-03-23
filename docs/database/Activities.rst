Activities
----------

.. list-table ::
   :widths: 15 15 30
   :header-rows: 1

  * - Column
    - Type
    - Description
  * - ActivityID
    - INTEGER
    - The activity ID (Primary Key)
  * - locStatus
    - INTEGER
    - The locale status of the activity
  * - instanceMapID
    - INTEGER
    - The instance map ID of the activity
  * - minTeams
    - INTEGER
    - The minimum number of teams needed to start the activity
  * - maxTeams
    - INTEGER
    - The maximum number of teams needed to start the activity
  * - minTeamSize
    - INTEGER
    - The minimum number of players allowed per team (for races this i used to put each player on their own team).
  * - maxTeamSize
    - INTEGER
    - The maximum number of players allowed per team (for races this i used to put each player on their own team).
  * - waitTime
    - INTEGER
    - The wait time in milliseconds before an activity starts.
  * - startDelay
    - INTEGER
    - If all players have readied up early, this is the remaining delay to wait before starting.
  * - requiresUniqueData
    - BOOLEAN
    - If true, the activity requires unique data.  Does not seem to be used in live maps and is only set for map 21.
  * - leaderboardType
    - INTEGER
    - The leaderboard type of the activity (TODO: make an enum for this)
  * - localize
    - BOOLEAN
    - If true, the activity is localized.
  * - optionalCostLOT
    - INTEGER
    - An item to take as an optional cost.
  * - optionalCostCount
    - INTEGER
    - The count of :samp:`optionalCostLOT` to take.
  * - showUIRewards
    - BOOLEAN
    - Seems to always be true except for 3 activities (:act:`116`, :act:`117`,:ac:`999`).
  * - CommunityActivityFlagID
    - INTEGER
    - Always null.
  * - gate_version
    - TEXT
    - The gate version to lock the activity behind.
  * - noTeamLootOnDeath
    - BOOLEAN
    - If true, players will not drop loot on death.
  * - optionalPercentage
    - FLOAT
    - Unknown.

256 Slots
