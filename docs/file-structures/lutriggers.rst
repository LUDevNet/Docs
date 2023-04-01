Triggers (.lutriggers)
======================

plain text, xml structure

| **trigger** - A trigger
| 	**id** - as referenced in in the .lvl
| 	**event** - event type on which the trigger should fire 
| 		**id** - A EventID value
| 		**command** - command to be executed on trigger
| 			**id** - command type todo: document possible values
| 			**target**
| 				``self`` for the trigger,
|				``target`` for the object that triggered it,
|				``zone`` probably the ZoneControlObject,
|				``objGroup`` which instantiates another attribute called targetName
| 			**args** - command-specific arguments todo:

Possible Values (EventIDs)
--------------------------

.. hlist ::
	:columns: 3

	* OnDestroy
	* OnCustomEvent
	* OnEnter
	* OnExit
	* OnCreate
	* OnHit
	* OnTimerDone
	* OnRebuildComplete
	* OnActivated
	* OnDectivated [sic]
	* OnArrived
	* OnArrivedAtEndOfPath
	* OnZoneSummaryDismissed
	* OnArrivedAtDesiredWaypoint
	* OnPetOnSwitch
	* OnPetOffSwitch
	* OnInteract

Possible Values (Commands)
--------------------------

============================  =======================================================================================================
Command                       Parameters
============================  =======================================================================================================
zonePlayer                    [zone ID],(0 for non-instanced, 1 for instanced), (x, y, z position), (y rotation), (spawn point name)
fireEvent                     (String to send to the recipient)
destroyObj                    (0 for violent, 1 for silent)
toggleTrigger                 [0 to disable, 1 to enable]
resetRebuild                  (0 for normal reset, 1 for "failure" reset)
setPath                       [new path name],(starting point index),(0 for forward, 1 for reverse)
setPickType                   [new pick type, or -1 to disable picking]
moveObject                    [x offset],[y offset],[z offset]
rotateObject                  [x rotation],[y rotation],[z rotation]
pushObject                    [x direction],[y direction],[z direction]
repelObject                   (force multiplier)
setTimer                      [timer name],[duration in seconds]
cancelTimer                   [timer name]
playCinematic                 [cinematic name],(lead-in in seconds),("wait" to wait at end),("unlock" to NOT lock the player controls),("leavelocked" to leave player locked after cinematic finishes),("hideplayer" to make player invisible during cinematic
toggleBBB                     ("enter" or "exit" to force direction)
updateMission                 [taskType],[targetid],[value1],[value2],[wsValue]
setBouncerState               ["on" to activate bouncer or "off" to deactivate bouncer]
bounceAllOnBouncer            No Parameters Required
turnAroundOnPath              No Parameters Required
goForwardOnPath               No Parameters Required
goBackwardOnPath              No Parameters Required
stopPathing                   No Parameters Required
startPathing                  No Parameters Required
LockOrUnlockControls          ["lock" to lock controls or "unlock" to unlock controls]
PlayEffect                    [nameID],[effectID],[effectType],[priority(optional)]
StopEffect                    [nameID]
activateMusicCue              DEPRECATED.  Does nothing.
deactivateMusicCue            DEPRECATED.  Does nothing.
flashMusicCue                 DEPRECATED.  Does nothing.
setMusicParameter             DEPRECATED.  Does nothing.
play2DAmbientSound            DEPRECATED.  Does nothing.
stop2DAmbientSound            DEPRECATED.  Does nothing.
play3DAmbientSound            DEPRECATED.  Does nothing.
stop3DAmbientSound            DEPRECATED.  Does nothing.
activateMixerProgram          DEPRECATED.  Does nothing.
deactivateMixerProgram        DEPRECATED.  Does nothing.
CastSkill                     [skillID]
displayZoneSummary            [1 for zone start, 0 for zone end]
SetPhysicsVolumeEffect        ["Push", "Attract", "Repulse", "Gravity", "Friction"],[amount],(direction x, y, z),("True" or "False")(min distance)(max distance)
SetPhysicsVolumeStatus        [“On”, “Off”]
setModelToBuild               [template ID]
spawnModelBricks              [amount, from 0 to 1],[x],[y],[z]
ActivateSpawnerNetwork        [Spawner Network Name]
DeactivateSpawnerNetwork      [Spawner Network Name]
ResetSpawnerNetwork           [Spawner Network Name]
DestroySpawnerNetworkObjects  [Spawner Network Name]
Go_To_Waypoint                [Waypoint index],("true" to allow direction change, otherwise "false"),("true" to stop at waypoint, otherwise "false")
ActivatePhysics               "true" to activate and add to world, "false" to deactivate and remove from the world
============================  =======================================================================================================
