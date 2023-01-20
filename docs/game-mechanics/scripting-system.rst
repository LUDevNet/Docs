Scripting (LUA)
===============

The client and world server used the LUA scripting language to implement
much of AI and special features, which are only used on some small amount
of objects. These scripts are attached via a :doc:`../components/005-script`
or the configuration in the :doc:`../file-structures/level` files.

Some considerable amount of the server side scripts have been removed from
the client files and only appear as :samp:`__removed` in the database.

As the scripting engine has access to some interface with the game engine,
documenting the relevant LUA-exposed functions can be of advantage in
understanding the game architeture as well as facilitate implementation
of a scripting engine in a server project, or even client modding.

Functions
---------

On every game message to an object, the scripting engine will call the
appropriate :file:`on{MessageName}` function in the scripts. When a lua
notfication is requested, the corresponding :file:`notify{Message}` will
be called.

Methods
-------

- Localize(key: string)

GameObject :samp:`obj`
----------------------
|   :samp:`function GetVar(key: string)`
|     Gets the variable associated with the key :samp:`key` attached to :samp:`obj`.  Example :script:`ai/RACING/OBJECTS/RACE_SMASH_SERVER.lua`.
|   :samp:`function SetVar(key: string, value: any)`
|     Sets a variable on the Entity :samp:`obj` with the key :samp:`key` and the value :samp:`value`.  Example :script:`ai/RACING/OBJECTS/RACE_SMASH_SERVER.lua`.
|   :samp:`function SetNetworkVar(key: string, value: any)`
|     Sets a networked variable on the Entity :samp:`obj` with the key :samp:`key` and the value :samp:`value`.  The message :gm:client:`ScriptNetworkVarUpdate` is then sent to the client to communicate this update.  Example :script:`ai/FV/L_FV_PANDA_SERVER.lua`.
|   :samp:`function GetNetworkVar(key: string) -> any`
|     Gets a networked variable associated with the key :samp:`key`.  Example :script:`02_client/Enemy/General/L_DRAGON_SMASHING_GOLEM_QB_CLIENT.lua`.
|   :samp:`function SendLuaNotificationRequest{requestTarget: GameObject, messageName: string}`
|     Adds the function :file:`notify{messageName}` to the :samp:`obj` so that function is called when the same :file:`on{messageName}` is called on :samp:`obj`.  Example :script:`equipmenttriggers/gempack.lua`.
|   :samp:`function SendLuaNotificationCancel{requestTarget: GameObject, messageName: string}`
|     Removes the function :file:`notify{messageName}` from :samp:`obj` notifications so the function is no longer called.  Example :script:`equipmenttriggers/gempack.lua`.
|   :samp:`function GetRotation() -> Rotation`
|     Gets the rotation of the :samp:`obj`.  The rotation is a :packet:`Quaternion <world/struct.Quaternion>`.  Example :script:`client/ai/AG/L_AG_CUSTOM_ROCKET.lua`.
|   :samp:`function SetRotation{x: float , y: float, z: float , w: float} or obj:SetRotation(Quaternion)`
|     Sets the rotation for the :samp:`obj`.  Example :script:`client/ai/AG/L_AG_CUSTOM_ROCKET.lua`.
|   :samp:`function Exists() -> bool`
|     Returns :samp:`true` of :samp:`obj` exists, :samp:`false` otherwise.  Example :script:`client/ai/NP/L_NP_NPC.lua`
|   :samp:`function GetFlag{iFlagID: int} -> Flag`
|     Gets the flag :samp:`iFlagID` from :samp:`obj`.  True if the flag is set, false otherwise.  See :doc:`flag-system` for more info.  Example :script:`02_client/Map/NT/L_NT_IMAGIMETER_VISIBILITY_CLIENT.lua`
|   :samp:`function GetLocationsVisited() -> Locations`
|     Gets the locations :samp:`obj` has visited.  Example :script:`02_client/Map/General/L_CHOOSE_YOUR_DESTINATION_NS_TO_NT_CLIENT.lua`
|   :samp:`function SetProximityRadius{iconID: int, radius: int, name: string, collisionGroup: int, shapeType: string, height: int}`
|     Sets a proximity radius for :samp:`obj` with radius :samp:`radius`, height :samp:`height`, the shape :samp:`shapeType` and attaches it to the collisionGroup :samp:`collisionGroup`. This new proximity radius also has the name :samp:`name` and an icon :samp:`iconID`.  Example :script:`ai/ACT/FootRace/L_ACT_BASE_FOOT_RACE_CLIENT.lua`
|   :samp:`function UnsetProximityRadius{name: string}`
|     Removes the proximity radius from the object with the name :samp:`name`.  Example :script:`ai/AG/L_AG_QB_Elevator.lua`
|   :samp:`function CheckListOfPreconditionsFromLua{PreconditionsToCheck: string? (there seems to be comparison of this var to ""), requestingID: GameObject}`
|     Checks whether the preconditions :samp:`PreconditionsToCheck` are met for the :samp:`obj`.  If a :samp:`requestingID` is provided, :samp:`requestingID` is the GameObject that is checking the preconditions. Example :script:`02_client/Map/AM/L_SKULLKIN_DRILL_CLIENT.lua`
|   :samp:`function RequestPickTypeUpdate()`
|     Used to update interactions? Example :script:`02_client/Map/AM/L_BLUE_X_CLIENT.lua`
|   :samp:`function GetID()`
|     Gets the GameObjectID of :samp:`obj`. Example :script:`o_ChoicebuildBonus.lua`
|   :samp:`function NotifyObject{ name: string, param1: int, ObjIDSender: ObjectID}`
|     Notifies the :samp:`obj` of the notification :samp:`name` with the optional parameter :samp:`param1` and the sender being :samp:`ObjIDSender`.  Example :script:`ai/FV/L_FV_CONSOLE_RIGHT_QUICKBUILD.lua`

Game Messages
^^^^^^^^^^^^^

- SetStunned
- PlayAnimation
- PlayCinematic
- PlayNDAudioEmitter
- PlayFXEffect
- StopFXEffect
- TerminateInteraction
- PlayAnimation
- FireEventServerSide
- DisplayMessageBox

LEVEL
-----

- LEVEL:CLUTEffect(clut: string, fadeDuration: int, startIntensity: float, endIntensity: float, uiOverlay: bool)
- LEVEL:GetCinematicInfo(cinematicName: string)
- LEVEL:GetCurrentZoneID()
- LEVEL:SetLights(modifyAmbientColor: bool, ambientColor: int, modifyDirectionalColor: bool, directionalColor: int, modifySpecularColor: bool, specularColor: int, modifyUpperHemiColor: bool, upperHemiColor: int, modifyDirectionalDirection: bool, directionalDirection: {x: float, y: float, z: float}, modifyFogColor: bool, fogColor: int, modifyDrawDistance: bool, fogNearMin: float, fogNearMax: float, fogFarMin: float, fogFarMax: float, postFogSolidMin: float, postFogSolidMax: float, postFogFadeMin: float, postFogFadeMax: float, staticObjectCutoffMin: float, staticObjectCutoffMax: float, dynamicObjectCutoffMin: float, dynamicObjectCutoffMax: float, modifySkyDome: bool, skyDome: string, blendTime: float)
- LEVEL:SetSkyDome(skyDome: string)

GAMEOBJ
-------

- GAMEOBJ:GetControlledID() -> GameObject
- GAMEOBJ:GetZoneControlID()
- GAMEOBJ:GetTimer() -> Timer
- GAMEOBJ:GetObjectByID() -> GameObject
- GAMEOBJ:GetLocalCharID() -> ObjectID
- GAMEOBJ:DeleteObject(obj: GameObject)

UI
--

- UI:SendMessage(msg: string, data: NDGfxValue)

Timer
-----

- timer:AddTimerWithCancel(delay: float, message: string, object: GameObject)
- timer:CancelAllTimers(object: GameObject)

Flag
----

- flag.bFlag -> bool

Locations
---------

- locations.locations -> list<ZoneID>
