Game Messages
=============

.. note ::
	This is a read-the-docs port of the original google docs `lu_game_messages <https://docs.google.com/document/d/117F74OhLcdsykwRJ1wnpx4TahsFa2zGtOvMF6I3_afg>`_, written by humanoid, lcdr and others, ported by `@Xiphoseer <https://twitter.com/Xiphoseer>`_. This is currently a proof of concept and is not guaranteed to reflect the latest changes.


Skill / Behavior system bitstream structures
--------------------------------------------

For the IDs for the behavior names, see cdclient BehaviorTemplateName, for the parameters for the specific behaviors of an item, see cdclient BehaviorParameter (necessary for implementing skills).
For a basic explanation of how the Skill system works see the according section in the Game Mechanics document.


Basic Attack
^^^^^^^^^^^^
align to byte boundary (don’t ask me why, this (and the “padding” below) is completely pointless)

| **[u16]** - “padding”
| **[bit]** - ???, always False?
| **[bit]** - ???, always False?
| **[bit]** - ???, always True?
| **[u32]** - ???
| **[u32]** - damage
| **[bit]** - ???, maybe whether the attack is part of an Area of Effect attack?


TacArc
^^^^^^
| hit_something= **[bit]**
| if hit_something:
| 	if ``check_env`` parameter:
| 		**[bit]** - ???, always 0?
| 	**[u32]** - number of targets
| 		**[s64]** - target object id
| 	for each target:
| 		-> `action`
| else:
| 	if ``blocked_action`` parameter exists:
| 		**[bit]** - is blocked
| 		if blocked -> `blocked action`, else -> `miss action`
| 	else:
| 		-> miss action


Projectile Attack
^^^^^^^^^^^^^^^^^
| **[s64]** - target id
| projectile count = “spread_count” parameter, minimum 1
| **[projectile count]**
| 	**[s64]** - local projectile id
| 		used for projectile impact message (behavior of impact message determined by projectile LOT skill)


Movement Switch
^^^^^^^^^^^^^^^
| **[u32]** - movement type, 1 -> ground, 2 -> single-jump, 3 -> falling, 4 -> double-jump, 6 -> jetpack


Area of Effect
^^^^^^^^^^^^^^
| **[u32]** - number of targets
| 	**[s64]** - target object id
| -> action for targets


Stun
^^^^
| if target != self:
| 	note that for some reason this does not work for projectiles, todo: investigate
| 	**[bit]** - ???, always False?


Knockback
^^^^^^^^^
**[bit]** - ???, always False?


Attack Delay, Switch
^^^^^^^^^^^^^^^^^^^^
seem to work the same; this behavior causes SyncSkill messages, which use the behavior handle as ID and “action” as the behavior to execute on SyncSkill

| **[u32]** - behavior handle


Switch
^^^^^^
| state = True
| if “imagination” parameter > 0 or not “isEnemyFaction” parameter:
| 	state= **[bit]** - switch state
| if state:
| 	-> action_true
| else:
| 	-> action_false


Chain
^^^^^
| **[u32]** - chain index, basically attack combo in attacks, 1-based
| -> relevant action


ForceMovement
^^^^^^^^^^^^^
| if any of “hit_action”, “hit_action_enemy”, “hit_action_faction” is not 0:
| 	**[u32]** - behavior handle
| 	-> SyncSkill, see AirMovement for details


Interrupt
^^^^^^^^^
| if target != self:
| 	**[bit]** - ???, always False?
| if “interrupt_block” parameter == 0:
| 	**[bit]** - ???, always False?
| **[bit]** - ???, always False?


SwitchMultiple
^^^^^^^^^^^^^^
mostly used for charge up action

| **[float]** - value
| if value <= “value_1” parameter:
| 	-> behavior_1
| else:
| 	-> behavior_2

AirMovement
^^^^^^^^^^^
like Attack Delay, this causes SyncSkill messages, which use the behavior handle as ID but have the behavior to execute specified in the SyncSkill bitstream

| **[u32]** - behavior handle
| *SyncSkill structure:*
| **[u32]** - behavior id
| **[u64]** - target object id


Game Messages
-------------

.. note ::

	- the structure of a game message is the same for both client and server, however not all IDs can/should be sent by both (todo - mark which IDs are client/server/unified)
	- game messages are split into internal and networked messages, we’ll only cover the latter for our research (for obvious reasons), so gaps between the enumerated id numbers are to be expected
	- some structures have default values specified (marked blue below), these are preceded by an extra bit (if the structure isn’t a bit itself), if this bit is enabled the actual data structure will be omitted and the receiver of the message will use the default value, otherwise this bit is followed by the normal data structure
	- the IDs below are not listed in little endian format to allow for enumerated ID ordering, so the according endian conversion needs to be done before searching/using an ID in this list
	- in addition to the data types listed in the main document, some custom ones are added here, see below for their structure

Additional data types
^^^^^^^^^^^^^^^^^^^^^
All enums (types starting with “e”) are serialized as s32

:LWOOBJID: s64
:LwoNameValue: consists of

    | **[std::wstring]** - ldf in text form
    | 	see the ldf format documentation for format
    | if length of string > 0:
    | 	**[two 0 bytes as terminator]**
    | 		not sure why this is included but it is necessary to serialize it correctly

:NiPoint3: consists of

    | **[float]** - x
    | **[float]** - y
    | **[float]** - z

:NiQuaternion: consists of

	| **[float]** - x
	| **[float]** - y
	| **[float]** - z
	| **[float]** - w

:std\:\:string: consists of

    | **[u32]** - length of string in characters
    | 	**[char]**

:std\:\:wstring: consists of

	| **[u32]** - length of wstring in characters
	| 	**[wchar]**

:TSkillID: u32
:NDGFxValue: amf3-data

General structure
^^^^^^^^^^^^^^^^^
| **[LWOOBJID]** - object id of the target object of the message
| **[u16]** - game message id
| **[id specific data]** - see structures for the IDs listed below


ID-specific game message structure
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

0013: Teleport
""""""""""""""
| **[bit]** - NoGravTeleport
| **[bit]** - bIgnoreY, default: true
| **[bit]** - bSetRotation, default: false
| **[bit]** - bSkipAllChecks, default: false
| **[NiPoint3]** - pos
| **[bit]** - useNavmesh, default: false
| **[float]** - w, default: 1.0f
| **[float]** - x
| **[float]** - y
| **[float]** - z

001e: DropClientLoot
""""""""""""""""""""
| **[bit]** - bUsePosition, default: false
| **[NiPoint3]** - finalPosition, default: NiPoint3::ZERO
| **[int]** - iCurrency
| **[LOT]** - itemTemplate
| **[LWOOBJID]** - lootID
| **[LWOOBJID]** - owner
| **[LWOOBJID]** - sourceObj
| **[NiPoint3]** - spawnPosition, default: NiPoint3::ZERO

0025: Die
"""""""""
| **[bit]** - bClientDeath, default: false
| **[bit]** - bSpawnLoot, default: true
| **[std::wstring]** - deathType
| **[float]** - directionRelative_AngleXZ
| **[float]** - directionRelative_AngleY
| **[float]** - directionRelative_Force
| **[eKillType]** - killType, default: VIOLENT
| **[LWOOBJID]** - killerID
| **[LWOOBJID]** - lootOwnerID, default: LWOOBJID_EMPTY

0026: RequestDie
""""""""""""""""
| **[bit]** - unknown
| **[std::wstring]** - deathType
| **[float]** - directionRelative_AngleXZ
| **[float]** - directionRelative_AngleY
| **[float]** - directionRelative_Force
| **[eKillType]** - killType, default: VIOLENT
| **[LWOOBJID]** - killerID
| **[LWOOBJID]** - lootOwnerID

0029: PlayEmote
"""""""""""""""
| **[int]** - emoteID
| **[LWOOBJID]** - targetID

002a: PreloadAnimation
""""""""""""""""""""""
| **[std::wstring]** - animationID
| **[bit]** - handled, default: false
| **[LWOOBJID]** - respondObjID
| **[LwoNameValue]** - userData

002b: PlayAnimation
"""""""""""""""""""
| **[std::wstring]** - animationID
| **[bit]** - bExpectAnimToExist, default: true
| **[bit]** - bPlayImmediate
| **[bit]** - bTriggerOnCompleteMsg, default: false
| **[float]** - fPriority, default: SECONDARY_PRIORITY
| **[float]** - fScale, default: 1.0f

0030: ControlBehaviors
""""""""""""""""""""""
| **[NDGFxValue]** - args
| **[std::string]** - command

0048: SetName
"""""""""""""
| **[std::wstring]** - name

0076: EchoStartSkill
""""""""""""""""""""
| **[bit]** - bUsedMouse, default: false
| **[float]** - fCasterLatency, default: 0.0f
| **[int]** - iCastType, default: 0
| **[NiPoint3]** - lastClickedPosit, default: NiPoint3::ZERO
| **[LWOOBJID]** - optionalOriginatorID
| **[LWOOBJID]** - optionalTargetID, default: LWOOBJID_EMPTY
| **[NiQuaternion]** - originatorRot, default: NiQuaternion::IDENTITY
| **[std::string]** - sBitStream
| **[TSkillID]** - skillID
| **[u32]** - uiSkillHandle, default: 0

0077: StartSkill
""""""""""""""""
| **[bit]** - bUsedMouse, default: false
| **[LWOOBJID]** - consumableItemID, default: LWOOBJID_EMPTY
| **[float]** - fCasterLatency, default: 0.0f
| **[int]** - iCastType, default: 0
| **[NiPoint3]** - lastClickedPosit, default: NiPoint3::ZERO
| **[LWOOBJID]** - optionalOriginatorID
| **[LWOOBJID]** - optionalTargetID, default: LWOOBJID_EMPTY
| **[NiQuaternion]** - originatorRot, default: NiQuaternion::IDENTITY
| **[std::string]** - sBitStream
| **[TSkillID]** - skillID
| **[u32]** - uiSkillHandle, default: 0

0078: CasterDead
""""""""""""""""
| **[LWOOBJID]** - i64Caster, default: LWOOBJID_EMPTY
| **[u32]** - uiSkillHandle, default: 0

0079: VerifyAck
"""""""""""""""
| **[bit]** - bDifferent, default: false
| **[std::string]** - sBitStream
| **[u32]** - uiHandle, default: 0

007c: SelectSkill
"""""""""""""""""
| **[bit]** - bFromSkillSet, default: false
| **[int]** - skillID

007f: AddSkill
""""""""""""""
| **[int]** - AICombatWeight, default: 0
| **[bit]** - bFromSkillSet, default: false
| **[int]** - castType, default: 0
| **[float]** - fTimeSecs, default: -1.0f
| **[int]** - iTimesCanCast, default: -1
| **[TSkillID]** - skillID
| **[int]** - slotID, default: -1
| **[bit]** - temporary, default: true

0080: RemoveSkill
"""""""""""""""""
| **[bit]** - bFromSkillSet, default: false
| **[TSkillID]** - skillID

0085: SetCurrency
"""""""""""""""""
| **[s64]** - currency
| **[int]** - lootType, default: LOOTTYPE_NONE
| **[NiPoint3]** - position
| **[LOT]** - sourceLOT, default: LOT_NULL
| **[LWOOBJID]** - sourceObject, default: LWOOBJID_EMPTY
| **[LWOOBJID]** - sourceTradeID, default: LWOOBJID_EMPTY
| **[int]** - sourceType, default: LOOTTYPE_NONE

0089: PickupCurrency
""""""""""""""""""""
| **[u32]** - currency
| **[NiPoint3]** - position

008b: PickupItem
""""""""""""""""
| **[LWOOBJID]** - lootObjectID
| **[LWOOBJID]** - playerID

008c: TeamPickupItem
""""""""""""""""""""
| **[LWOOBJID]** - lootID
| **[LWOOBJID]** - lootOwnerID

009a: PlayFXEffect
""""""""""""""""""
| **[int]** - effectID, default: -1
| **[std::wstring]** - effectType
| **[float]** - fScale, default: 1.0f
| **[std::string]** - name
| **[float]** - priority, default: 1.0
| **[LWOOBJID]** - secondary, default: LWOOBJID_EMPTY
| **[bit]** - serialize, default: true

009b: StopFXEffect
""""""""""""""""""
| **[bit]** - bKillImmediate
| **[std::string]** - name

009f: RequestResurrect
""""""""""""""""""""""
| 

00a0: Resurrect
"""""""""""""""
| **[bit]** - bRezImmediately, default: false

00c0: PopEquippedItemsState
"""""""""""""""""""""""""""
| 

00c6: SetStunned
""""""""""""""""
| **[LWOOBJID]** - Originator, default: LWOOBJID_EMPTY
| **[EStunState]** - StateChangeType
| **[bit]** - bCantAttack
| **[bit]** - bCantAttackOutChangeWasApplied, default: false
| **[bit]** - bCantEquip
| **[bit]** - bCantEquipOutChangeWasApplied, default: false
| **[bit]** - bCantInteract
| **[bit]** - bCantInteractOutChangeWasApplied, default: false
| **[bit]** - bCantJump
| **[bit]** - bCantJumpOutChangeWasApplied, default: false
| **[bit]** - bCantMove
| **[bit]** - bCantMoveOutChangeWasApplied, default: false
| **[bit]** - bCantTurn
| **[bit]** - bCantTurnOutChangeWasApplied, default: false
| **[bit]** - bCantUseItem, default: false
| **[bit]** - bCantUseItemOutChangeWasApplied, default: false
| **[bit]** - bDontTerminateInteract, default: false
| **[bit]** - bIgnoreImmunity, default: true

00c8: SetStunImmunity
"""""""""""""""""""""
| **[LWOOBJID]** - Caster, default: LWOOBJID_EMPTY
| **[EImmunityState]** - StateChangeType
| **[bit]** - bImmuneToStunAttack
| **[bit]** - bImmuneToStunEquip
| **[bit]** - bImmuneToStunInteract
| **[bit]** - bImmuneToStunJump
| **[bit]** - bImmuneToStunMove
| **[bit]** - bImmuneToStunTurn
| **[bit]** - bImmuneToStunUseItem

00ca: Knockback
"""""""""""""""
| **[LWOOBJID]** - Caster, default: LWOOBJID_EMPTY
| **[LWOOBJID]** - Originator, default: LWOOBJID_EMPTY
| **[int]** - iKnockBackTimeMS, default: 0
| **[NiPoint3]** - vector

00d1: RebuildCancel
"""""""""""""""""""
| **[bit]** - bEarlyRelease
| **[LWOOBJID]** - userID

00d5: EnableRebuild
"""""""""""""""""""
| **[bit]** - bEnable
| **[bit]** - bFail
| **[bit]** - bSuccess
| **[FailReason]** - eFailReason, default: REASON_NOT_GIVEN
| **[float]** - fDuration
| **[LWOOBJID]** - user

00e0: MoveItemInInventory
"""""""""""""""""""""""""
| **[int]** - destInvType, default: INVENTORY_INVALID
| **[LWOOBJID]** - iObjID
| **[int]** - inventoryType
| **[int]** - responseCode
| **[int]** - slot

00e3: AddItemToInventoryClientSync
""""""""""""""""""""""""""""""""""
| **[bit]** - bBound
| **[bit]** - bIsBOE
| **[bit]** - bIsBOP
| **[int]** - eLootTypeSource, default: LOOTTYPE_NONE
| **[LwoNameValue]** - extraInfo
| **[LOT]** - iObjTemplate
| **[LWOOBJID]** - iSubkey, default: LWOOBJID_EMPTY
| **[int]** - invType, default: INVENTORY_DEFAULT
| **[u32]** - itemCount, default: 1
| **[u32]** - itemsTotal, default: 0
| **[LWOOBJID]** - newObjID
| **[NiPoint3]** - ni3FlyingLootPosit
| **[bit]** - showFlyingLoot, default: true
| **[int]** - slotID

00e6: RemoveItemFromInventory
"""""""""""""""""""""""""""""
| **[bit]** - bConfirmed, default: false
| **[bit]** - bDeleteItem, default: true
| **[bit]** - bOutSuccess, default: false
| **[int]** - eInvType, default: INVENTORY_MAX
| **[int]** - eLootTypeSource, default: LOOTTYPE_NONE
| **[LwoNameValue]** - extraInfo
| **[bit]** - forceDeletion, default: true
| **[LWOOBJID]** - iLootTypeSourceID, default: LWOOBJID_EMPTY
| **[LWOOBJID]** - iObjID, default: LWOOBJID_EMPTY
| **[LOT]** - iObjTemplate, default: LOT_NULL
| **[LWOOBJID]** - iRequestingObjID, default: LWOOBJID_EMPTY
| **[u32]** - iStackCount, default: 1
| **[u32]** - iStackRemaining, default: 0
| **[LWOOBJID]** - iSubkey, default: LWOOBJID_EMPTY
| **[LWOOBJID]** - iTradeID, default: LWOOBJID_EMPTY

00e7: EquipInventory
""""""""""""""""""""
| **[bit]** - bIgnoreCooldown, default: false
| **[bit]** - bOutSuccess
| **[LWOOBJID]** - itemtoequip

00e9: UnEquipInventory
""""""""""""""""""""""
| **[bit]** - bEvenIfDead, default: false
| **[bit]** - bIgnoreCooldown, default: false
| **[bit]** - bOutSuccess
| **[LWOOBJID]** - itemtounequip
| **[LWOOBJID]** - replacementObjectID, default: LWOOBJID_EMPTY

00f8: OfferMission
""""""""""""""""""
| **[int]** - missionID
| **[LWOOBJID]** - offerer

00f9: RespondToMission
""""""""""""""""""""""
| **[int]** - missionID
| **[LWOOBJID]** - playerID
| **[LWOOBJID]** - receiver
| **[LOT]** - rewardItem, default: LOT_NULL

00fe: NotifyMission
"""""""""""""""""""
| **[int]** - missionID
| **[int]** - missionState
| 	Unavailable = 0
| 	Available = 1
| 	Active = 2
| 	ReadyToComplete = 4
| 	Completed = 8
| 	*following are for daily/retakeable missions*
| 	CompletedAvailable = 9
| 	CompletedActive = 10
| 	CompletedReadyToComplete = 12
| **[bit]** - sendingRewards, default: false

.. hint :: Mission Task Types:

	.. hlist ::
		:columns: 3

		- KillEnemy = 0
		- Script = 1
		- QuickBuild = 2
		- Collect = 3
		- GoToNPC = 4
		- UseEmote = 5
		- UseConsumable = 9
		- UseSkill = 10
		- ObtainItem = 11
		- Discover = 12
		- MinigameAchievement = 14
		- Interact = 15
		- MissionComplete = 16
		- TamePet = 22
		- Racing? = 23
		- Flag = 24
		- NexusTowerBrickDonation = 32

00ff: NotifyMissionTask
"""""""""""""""""""""""
| **[int]** - missionID
| **[int]** - taskMask
| taskMask is a bitmask with the bit corresponding to the task index (1<<(task index+1)) set.
| **[u8]** - length
| 	**[float]** - updates

For collectibles the updates are of the form collectible_id+(world_id<<8)


0150: RebuildNotifyState
""""""""""""""""""""""""
| **[int]** - iPrevState
| **[int]** - iState
| **[LWOOBJID]** - player

0164: ToggleInteractionUpdates
""""""""""""""""""""""""""""""
| **[bit]** - bEnable, default: false

0165: TerminateInteraction
""""""""""""""""""""""""""
| **[LWOOBJID]** - ObjIDTerminator
| **[ETerminateType]** - type

0166: ServerTerminateInteraction
""""""""""""""""""""""""""""""""
| **[LWOOBJID]** - ObjIDTerminator
| **[ETerminateType]** - type

016c: RequestUse
""""""""""""""""
| **[bit]** - bIsMultiInteractUse
| **[u32]** - multiInteractID
| **[int]** - multiInteractType
| **[LWOOBJID]** - object
| **[bit]** - secondary, default: false

0171: VendorOpenWindow
""""""""""""""""""""""
| 

0173: EmotePlayed
"""""""""""""""""
| **[int]** - emoteID
| **[LWOOBJID]** - targetID

0175: BuyFromVendor
"""""""""""""""""""
| **[bit]** - confirmed, default: false
| **[int]** - count, default: 1
| **[LOT]** - item

0176: SellToVendor
""""""""""""""""""
| **[int]** - count, default: 1
| **[LWOOBJID]** - itemObjID

017b: CancelDonationOnPlayer
""""""""""""""""""""""""""""
| 

017f: TeamSetOffWorldFlag
"""""""""""""""""""""""""
| **[LWOOBJID]** - i64PlayerID
| **[LWOZONEID]** - zoneID

0185: SetInventorySize
""""""""""""""""""""""
| **[int]** - inventoryType
| **[int]** - size

0187: AcknowledgePossession
"""""""""""""""""""""""""""
| **[LWOOBJID]** - possessedObjID, default: LWOOBJID_EMPTY

0194: RequestActivityExit
"""""""""""""""""""""""""
| **[bit]** - bUserCancel
| **[LWOOBJID]** - userID

0195: ActivityEnter
"""""""""""""""""""
| 

0196: ActivityExit
""""""""""""""""""
| 

0197: ActivityStart
"""""""""""""""""""
| 

0198: ActivityStop
""""""""""""""""""
| **[bit]** - bExit
| **[bit]** - bUserCancel

019b: ShootingGalleryFire
"""""""""""""""""""""""""
| **[NiPoint3]** - targetPos
| **[float]** - w
| **[float]** - x
| **[float]** - y
| **[float]** - z

01a0: RequestVendorStatusUpdate
"""""""""""""""""""""""""""""""

01a1: VendorStatusUpdate
""""""""""""""""""""""""
| **[bit]** - bUpdateOnly
| **[u32]** - inventoryList
|     **[int]** - LOT
|     **[int]** - sortPriority

01a2: CancelMission
"""""""""""""""""""
| **[int]** - missionID
| **[bit]** - resetCompleted

01a3: ResetMissions
"""""""""""""""""""
| **[int]** - missionID, default: -1

01a9: NotifyClientShootingGalleryScore
""""""""""""""""""""""""""""""""""""""
| **[float]** - addTime
| **[int]** - score
| **[LWOOBJID]** - target
| **[NiPoint3]** - targetPos

01ac: ClientItemConsumed
""""""""""""""""""""""""
| **[LWOOBJID]** - item

01c0: UpdateShootingGalleryRotation
"""""""""""""""""""""""""""""""""""
| **[float]** - angle
| **[NiPoint3]** - facing
| **[NiPoint3]** - muzzlePos

01d2: SetUserCtrlCompPause
""""""""""""""""""""""""""
| **[bit]** - bPaused

01d5: SetTooltipFlag
""""""""""""""""""""
| **[bit]** - bFlag
| **[int]** - iToolTip

01d7: SetFlag
"""""""""""""
| **[bit]** - bFlag
| **[int]** - iFlagID

01d8: NotifyClientFlagChange
""""""""""""""""""""""""""""
| **[bit]** - bFlag
| **[int]** - iFlagID

01db: Help
""""""""""
| **[int]** - iHelpID

01dc: VendorTransactionResult
"""""""""""""""""""""""""""""
| **[int]** - iResult
| <Please Add Possible Result Codes>
| 0x02 = Success

01e6: HasBeenCollected
""""""""""""""""""""""
| **[LWOOBJID]** - playerID

01e7: HasBeenCollectedByClient
""""""""""""""""""""""""""""""
| **[LWOOBJID]** - playerID

01f3: DespawnPet
""""""""""""""""
| **[bit]** - bDeletePet

01f9: PlayerLoaded
""""""""""""""""""
| **[LWOOBJID]** - playerID

01fd: PlayerReady
"""""""""""""""""

0203: RequestLinkedMission
""""""""""""""""""""""""""
| **[LWOOBJID]** - playerID
| **[int]** - missionID
| **[bit]** - bMissionOffered, default: false
| 

0204: TransferToZone
""""""""""""""""""""
| **[bit]** - bCheckTransferAllowed, default: false
| **[LWOCLONEID]** - cloneID, default: LWOCLONEID_INVALID
| **[float]** - pos_x, default: FLT_MAX
| **[float]** - pos_y, default: FLT_MAX
| **[float]** - pos_z, default: FLT_MAX
| **[float]** - rot_w, default: 1
| **[float]** - rot_x, default: 0
| **[float]** - rot_y, default: 0
| **[float]** - rot_z, default: 0
| **[std::wstring]** - spawnPoint
| **[unsigned char]** - ucInstanceType
| **[LWOMAPID]** - zoneID, default: LWOMAPID_INVALID

0205: TransferToZoneCheckedIM
"""""""""""""""""""""""""""""
| **[bit]** - bIsThereaQueue, default: false
| **[LWOCLONEID]** - cloneID, default: LWOCLONEID_INVALID
| **[float]** - pos_x, default: FLT_MAX
| **[float]** - pos_y, default: FLT_MAX
| **[float]** - pos_z, default: FLT_MAX
| **[float]** - rot_w, default: 1
| **[float]** - rot_x, default: 0
| **[float]** - rot_y, default: 0
| **[float]** - rot_z, default: 0
| **[std::wstring]** - spawnPoint
| **[unsigned char]** - ucInstanceType
| **[LWOMAPID]** - zoneID, default: LWOMAPID_INVALID

0207: InvalidZoneTransferList
"""""""""""""""""""""""""""""
| **[std::wstring]** - CustomerFeedbackURL
| **[std::wstring]** - InvalidMapTransferList
| **[bit]** - bCustomerFeedbackOnExit
| **[bit]** - bCustomerFeedbackOnInvalidMapTransfer

0208: MissionDialogueOK
"""""""""""""""""""""""
| **[bit]** - bIsComplete
| **[int]** - iMissionState
| **[int]** - missionID
| **[LWOOBJID]** - responder

020f: TransferToLastNonInstance
"""""""""""""""""""""""""""""""
| **[bit]** - bUseLastPosition, default: true
| **[LWOOBJID]** - playerID
| **[float]** - pos_x, default: FLT_MAX
| **[float]** - pos_y, default: FLT_MAX
| **[float]** - pos_z, default: FLT_MAX
| **[float]** - rot_w, default: 1
| **[float]** - rot_x, default: 0
| **[float]** - rot_y, default: 0
| **[float]** - rot_z, default: 0

0211: DisplayMessageBox
"""""""""""""""""""""""
| **[bit]** - bShow
| **[LWOOBJID]** - callbackClient
| **[std::wstring]** - identifier
| **[int]** - imageID
| **[std::wstring]** - text
| **[std::wstring]** - userData

0212: MessageBoxRespond
"""""""""""""""""""""""
| **[int]** - iButton
| **[std::wstring]** - identifier
| **[std::wstring]** - userData

0213: ChoiceBoxRespond
""""""""""""""""""""""
| **[std::wstring]** - buttonIdentifier
| **[int]** - iButton
| **[std::wstring]** - identifier

0219: Smash
"""""""""""
| **[bit]** - bIgnoreObjectVisibility, default: false
| **[float]** - force
| **[float]** - ghostOpacity
| **[LWOOBJID]** - killerID

021a: UnSmash
"""""""""""""
| **[LWOOBJID]** - builderID, default: LWOOBJID_EMPTY
| **[float]** - duration, default: 3.0f

021d: SetGravityScale
"""""""""""""""""""""
| **[float]** - scale (accepted: between 0f - 2f [above sets it to 2f, lower sets it to 0f] normal: 1f)

0223: PlaceModelResponse
""""""""""""""""""""""""
| **[NiPoint3]** - position, default: NiPoint3::ZERO
| **[LWOOBJID]** - propertyPlaqueID, default: LWOOBJID_EMPTY
| **[int]** - response, default: 0
| **[NiQuaternion]** - rotation, default: NiQuaternion::IDENTITY

0231: SetJetPackMode
""""""""""""""""""""
| **[bit]** - bBypassChecks, default: false
| **[bit]** - bDoHover, default: false
| **[bit]** - bUse
| **[int]** - effectID, default: -1
| **[float]** - fAirspeed, default: 10
| **[float]** - fMaxAirspeed, default: 15
| **[float]** - fVertVel, default: 1
| **[int]** - iWarningEffectID, default: -1

0235: RegisterPetID
"""""""""""""""""""
| **[LWOOBJID]** - objID

0236: RegisterPetDBID
"""""""""""""""""""""
| **[LWOOBJID]** - petDBID

0238: ShowActivityCountdown
"""""""""""""""""""""""""""
| **[bit]** - bPlayAdditionalSound
| **[bit]** - bPlayCountdownSound
| **[std::wstring]** - sndName
| **[int]** - stateToPlaySoundOn

0239: DisplayTooltip
""""""""""""""""""""
| **[bit]** - DoOrDie, default: false
| **[bit]** - NoRepeat, default: false
| **[bit]** - NoRevive, default: false
| **[bit]** - bIsPropertyTooltip, default: false
| **[bit]** - bShow
| **[bit]** - bTranslate, default: false
| **[int]** - iTime
| **[std::wstring]** - id
| **[LwoNameValue]** - localizeParams
| **[std::wstring]** - strImageName
| **[std::wstring]** - strText

0240: StartActivityTime
"""""""""""""""""""""""
| **[float]** - startTime

025a: ActivityPause
"""""""""""""""""""
| **[bit]** - bPause

025b: UseNonEquipmentItem
"""""""""""""""""""""""""
| **[LWOOBJID]** - itemToUse

025f: UseItemResult
"""""""""""""""""""
| **[LOT]** - m_ItemTemplateID
| **[bit]** - m_UseItemResult, default: false

027e: FetchModelMetadataRequest
"""""""""""""""""""""""""""""""
| **[int]** - context
| **[LWOOBJID]** - objectID
| **[LWOOBJID]** - requestorID
| **[LWOOBJID]** - ugID

0280: CommandPet
""""""""""""""""
| **[NiPoint3]** - GenericPosInfo
| **[LWOOBJID]** - ObjIDSource
| **[int]** - iPetCommandType
| **[int]** - iTypeID
| **[bit]** - overrideObey, default: false

0281: PetResponse
"""""""""""""""""
| **[LWOOBJID]** - ObjIDPet
| **[int]** - iPetCommandType
| **[int]** - iResponse
| **[int]** - iTypeID

0288: RequestActivitySummaryLeaderboardData
"""""""""""""""""""""""""""""""""""""""""""
| **[int]** - gameID, default: LWOOBJID_EMPTY
| **[int]** - queryType, default: 1
| **[int]** - resultsEnd, default: 10
| **[int]** - resultsStart, default: 0
| **[LWOOBJID]** - target
| **[bit]** - weekly

0289: SendActivitySummaryLeaderboardData
""""""""""""""""""""""""""""""""""""""""
| **[int]** - gameID
| **[int]** - infoType
| **[LwoNameValue]** - leaderboardData
| **[bit]** - throttled
| **[bit]** - weekly

0293: ClientNotifyPet
"""""""""""""""""""""
| **[LWOOBJID]** - ObjIDSource
| **[int]** - iPetNotificationType

0294: NotifyPet
"""""""""""""""
| **[LWOOBJID]** - ObjIDSource
| **[LWOOBJID]** - ObjToNotifyPetAbout
| **[int]** - iPetNotificationType

0295: NotifyPetTamingMinigame
"""""""""""""""""""""""""""""
| **[LWOOBJID]** - PetID
| **[LWOOBJID]** - PlayerTamingID
| **[bit]** - bForceTeleport
| **[eNotifyType]** - notifyType
| **[NiPoint3]** - petsDestPos
| **[NiPoint3]** - telePos
| **[NiQuaternion]** - teleRot, default: NiQuaternion::IDENTITY

0296: StartServerPetMinigameTimer
"""""""""""""""""""""""""""""""""
| 

0297: ClientExitTamingMinigame
""""""""""""""""""""""""""""""
| **[bit]** - bVoluntaryExit, default: true

029b: PetTamingMinigameResult
"""""""""""""""""""""""""""""
| **[bit]** - bSuccess

029c: PetTamingTryBuildResult
"""""""""""""""""""""""""""""
| **[bit]** - bSuccess, default: true
| **[int]** - iNumCorrect, default: 0

02a1: NotifyTamingBuildSuccess
""""""""""""""""""""""""""""""
| **[NiPoint3]** - BuildPosition

02a2: NotifyTamingModelLoadedOnServer
"""""""""""""""""""""""""""""""""""""
| 

02a9: AddPetToPlayer
""""""""""""""""""""
| **[int]** - iElementalType
| **[std::wstring]** - name
| **[LWOOBJID]** - petDBID
| **[LOT]** - petLOT

02ab: RequestSetPetName
"""""""""""""""""""""""
| **[std::wstring]** - name

02ac: SetPetName
""""""""""""""""
| **[std::wstring]** - name
| **[LWOOBJID]** - petDBID, default: LWOOBJID_EMPTY

02ae: PetNameChanged
""""""""""""""""""""
| **[int]** - moderationStatus
| **[std::wstring]** - name
| **[std::wstring]** - ownerName

02b4: ShowPetActionButton
"""""""""""""""""""""""""
| **[int]** - ButtonLabel
| **[bit]** - bShow

02b5: SetEmoteLockState
"""""""""""""""""""""""
| **[bit]** - bLock
| **[int]** - emoteID

02bf: UseItemRequirementsResponse
"""""""""""""""""""""""""""""""""
| **[u32]** - eUseResponse

02c9: PlayEmbeddedEffectOnAllClientsNearObject
""""""""""""""""""""""""""""""""""""""""""""""
| **[std::wstring]** - effectName
| **[LWOOBJID]** - fromObjectID
| **[float]** - radius

02cd: QueryPropertyData
"""""""""""""""""""""""
| 

02d4: PropertyEditorBegin
"""""""""""""""""""""""""
| **[int]** - distanceType, default: 0
| **[LWOOBJID]** - propertyObjectID, default: LWOOBJID_EMPTY
| **[int]** - startMode, default: 1
| **[bit]** - startPaused, default: 0

02d5: PropertyEditorEnd
"""""""""""""""""""""""
| 

02e1: NotifyClientZoneObject
""""""""""""""""""""""""""""
| **[std::wstring]** - name
| **[int]** - param1
| **[int]** - param2
| **[LWOOBJID]** - paramObj
| **[std::string]** - paramStr

02ea: UpdateReputation
""""""""""""""""""""""
| **[s64]** - iReputation

02ee: PropertyRentalResponse
""""""""""""""""""""""""""""
| **[LWOCLONEID]** - cloneid
| **[int]** - code
| **[LWOOBJID]** - propertyID
| **[s64]** - rentdue

02f8: RequestPlatformResync
"""""""""""""""""""""""""""
| 

02f9: PlatformResync
""""""""""""""""""""
| **[bit]** - bReverse
| **[bit]** - bStopAtDesiredWaypoint
| **[int]** - eCommand
| **[int]** - eState
| **[int]** - eUnexpectedCommand
| **[float]** - fIdleTimeElapsed
| **[float]** - fMoveTimeElapsed
| **[float]** - fPercentBetweenPoints
| **[int]** - iDesiredWaypointIndex
| **[int]** - iIndex
| **[int]** - iNextIndex
| **[NiPoint3]** - ptUnexpectedLocation
| **[NiQuaternion]** - qUnexpectedRotation, default: NiQuaternion::IDENTITY

02fa: PlayCinematic
"""""""""""""""""""
| **[bit]** - allowGhostUpdates, default: true
| **[bit]** - bCloseMultiInteract
| **[bit]** - bSendServerNotify
| **[bit]** - bUseControlledObjectForAudioListener, default: false
| **[EndBehavior]** - endBehavior, default: RETURN
| **[bit]** - hidePlayerDuringCine, default: false
| **[float]** - leadIn, default: -1.0f
| **[bit]** - leavePlayerLockedWhenFinished, default: false
| **[bit]** - lockPlayer, default: true
| **[std::wstring]** - pathName
| **[bit]** - result, default: false
| **[bit]** - skipIfSamePath, default: false
| **[float]** - startTimeAdvance

02fb: EndCinematic
""""""""""""""""""
| **[float]** - leadOut, default: -1.0f
| **[bit]** - leavePlayerLocked, default: false
| **[std::wstring]** - pathName

02fc: CinematicUpdate
"""""""""""""""""""""
| **[CinematicEvent]** - event, default: STARTED
| **[float]** - overallTime, default: -1.0f
| **[std::wstring]** - pathName
| **[float]** - pathTime, default: -1.0f
| **[int]** - waypoint, default: -1

02ff: ToggleGhostReferenceOverride
""""""""""""""""""""""""""""""""""
| **[bit]** - override, default: false

0300: SetGhostReferencePosition
"""""""""""""""""""""""""""""""
| **[NiPoint3]** - pos
| 
| 0302: FireEventServerSide
| **[std::wstring]** - args
| **[int]** - param1, default: -1
| **[int]** - param2, default: -1
| **[int]** - param3, default: -1
| **[LWOOBJID]** - senderID

030d: ScriptNetworkVarUpdate
""""""""""""""""""""""""""""
| **[LwoNameValue]** - tableOfVars

0319: UpdateModelFromClient
"""""""""""""""""""""""""""
| **[LWOOBJID]** - modelID
| **[NiPoint3]** - position
| **[NiQuaternion]** - rotation, default: NiQuaternion::IDENTITY

031a: DeleteModelFromClient
"""""""""""""""""""""""""""
| **[LWOOBJID]** - modelID, default: LWOOBJID_EMPTY
| **[DeleteReason]** - reason, default: PICKING_MODEL_UP

0335: PlayNDAudioEmitter
""""""""""""""""""""""""
| **[s64]** - m_NDAudioCallbackMessageData, default: 0
| **[NDAudio::TNDAudioID]** - m_NDAudioEmitterID, default: NDAudio::g_NDAudioIDNone
| **[std::string]** - m_NDAudioEventGUID
| **[std::string]** - m_NDAudioMetaEventName
| **[bit]** - m_Result, default: false
| **[LWOOBJID]** - m_TargetObjectIDForNDAudioCallbackMessages, default: LWOOBJID_EMPTY

0336: StopNDAudioEmitter
""""""""""""""""""""""""
| **[bit]** - m_AllowNativeFadeOut, default: true
| **[NDAudio::TNDAudioID]** - m_NDAudioEmitterID, default: NDAudio::g_NDAudioIDNone
| **[std::string]** - m_NDAudioEventGUID
| **[std::string]** - m_NDAudioMetaEventName
| **[bit]** - m_Result, default: false

0348: EnterProperty1
""""""""""""""""""""
| **[int]** - index
| **[bit]** - returnToZone, default: true

034a: PropertyEntranceSync
""""""""""""""""""""""""""
| **[bit]** - bIncludeNullAddress
| **[bit]** - bIncludeNullDescription
| **[bit]** - bPlayersOwn
| **[bit]** - bUpdateUI
| **[int]** - lNumResults
| **[int]** - lReputationTime
| **[int]** - lSortMethod
| **[int]** - lStartIndex
| **[std::string]** - sfilterText

0352: ParseChatMessage
""""""""""""""""""""""
| **[int]** - iClientState
| **[std::wstring]** - wsString

0353: SetMissionTypeState
"""""""""""""""""""""""""
| **[EMissionLockState]** - state, default: NEW
| **[std::string]** - subtype
| **[std::string]** - type

035a: BroadcastTextToChatbox
""""""""""""""""""""""""""""
| **[LwoNameValue]** - attrs
| **[std::wstring]** - wsText

035d: OpenPropertyVendor
""""""""""""""""""""""""
| 

0364: ClientTradeRequest
""""""""""""""""""""""""
| **[bit]** - bNeedInvitePopUp, default: false
| **[LWOOBJID]** - i64Invitee

0366: ServerTradeInvite
"""""""""""""""""""""""
| **[bit]** - bNeedInvitePopUp, default: false
| **[LWOOBJID]** - i64Requestor
| **[std::wstring]** - wsName

0369: ServerTradeInitialReply
"""""""""""""""""""""""""""""
| **[LWOOBJID]** - i64Invitee
| **[eResultType]** - resultType
| **[std::wstring]** - wsName

036a: ServerTradeFinalReply
"""""""""""""""""""""""""""
| **[bit]** - bResult
| **[LWOOBJID]** - i64Invitee
| **[std::wstring]** - wsName

036e: ClientTradeCancel
"""""""""""""""""""""""
| 

0370: ClientTradeAccept
"""""""""""""""""""""""
| **[bit]** - bFirst, default: false

0374: ServerTradeAccept
"""""""""""""""""""""""
| **[bit]** - bFirst, default: false

0378: ReadyForUpdates
"""""""""""""""""""""
| **[LWOOBJID]** - objectID

037a: SetLastCustomBuild
""""""""""""""""""""""""
| **[std::wstring]** - tokenizedLOTList

037b: GetLastCustomBuild
""""""""""""""""""""""""
| **[std::wstring]** - tokenizedLOTList

0387: SetIgnoreProjectileCollision
""""""""""""""""""""""""""""""""""
| **[bit]** - bShouldIgnore, default: false

0389: OrientToObject
""""""""""""""""""""
| **[LWOOBJID]** - objID

038a: OrientToPosition
""""""""""""""""""""""
| **[NiPoint3]** - ni3Posit

038b: OrientToAngle
"""""""""""""""""""
| **[bit]** - bRelativeToCurrent
| **[float]** - fAngle

0393: PropertyModerationAction
""""""""""""""""""""""""""""""
| **[LWOOBJID]** - characterID, default: 0
| **[std::wstring]** - info
| **[int]** - newModerationStatus, default: -1

0395: PropertyModerationStatusUpdate
""""""""""""""""""""""""""""""""""""
| **[int]** - newModerationStatus, default: -1
| **[std::wstring]** - rejectionReason

03a4: BounceNotification
""""""""""""""""""""""""
| **[LWOOBJID]** - ObjIDBounced
| **[LWOOBJID]** - ObjIDBouncer
| **[bit]** - bSuccess

03a6: RequestClientBounce
"""""""""""""""""""""""""
| **[LWOOBJID]** - BounceTargetID
| **[NiPoint3]** - BounceTargetPosOnServer
| **[NiPoint3]** - BouncedObjLinVel
| **[LWOOBJID]** - RequestSourceID
| **[bit]** - bAllBounced
| **[bit]** - bAllowClientOverride

03ae: BouncerActiveStatus
"""""""""""""""""""""""""
| **[bit]** - bActive

03bd: MoveInventoryBatch
""""""""""""""""""""""""
| **[bit]** - bAllowPartial, default: false
| **[bit]** - bOutSuccess, default: false
| **[u32]** - count, default: 1
| **[int]** - dstBag, default: 0
| **[LOT]** - moveLOT, default: LOT_NULL
| **[LWOOBJID]** - moveSubkey, default: LWOOBJID_EMPTY
| **[bit]** - showFlyingLoot, default: false
| **[int]** - srcBag, default: 0
| **[LWOOBJID]** - startObjectID, default: LWOOBJID_EMPTY

03d4: ObjectActivatedClient
"""""""""""""""""""""""""""
| **[LWOOBJID]** - activatorID
| **[LWOOBJID]** - objectActivatedID

03e4: SetBBBAutosave
""""""""""""""""""""
| **[BinaryBuffer]** - lxfmlDataCompressed

03e8: BBBLoadItemRequest
""""""""""""""""""""""""
| **[LWOOBJID]** - itemID

03e9: BBBSaveRequest
""""""""""""""""""""
| **[LWOOBJID]** - localID
| **[BinaryBuffer]** - lxfmlDataCompressed
| **[u32]** - timeTakenInMS

03ec: BBBResetMetadataSourceItem
""""""""""""""""""""""""""""""""
| 

0412: NotifyClientObject
""""""""""""""""""""""""
| **[std::wstring]** - name
| **[int]** - param1
| **[int]** - param2
| **[LWOOBJID]** - paramObj
| **[std::string]** - paramStr

0413: DisplayZoneSummary
""""""""""""""""""""""""
| **[bit]** - isPropertyMap, default: false
| **[bit]** - isZoneStart, default: false
| **[LWOOBJID]** - sender, default: LWOOBJID_EMPTY

0414: ZoneSummaryDismissed
""""""""""""""""""""""""""
| **[LWOOBJID]** - playerID

0416: ModifyPlayerZoneStatistic
"""""""""""""""""""""""""""""""
| **[bit]** - bSet, default: false
| **[std::wstring]** - statName
| **[int]** - statValue, default: 0
| **[LWOMAPID]** - zoneID, default: LWOMAPID_INVALID

041d: ActivityStateChangeRequest
""""""""""""""""""""""""""""""""
| **[LWOOBJID]** - i64ObjID
| **[int]** - iNumValue1
| **[int]** - iNumValue2
| **[std::wstring]** - wsStringValue

0421: StartBuildingWithItem
"""""""""""""""""""""""""""
| **[bit]** - bFirstTime, default: true
| **[bit]** - bSuccess
| **[int]** - sourceBAG
| **[LWOOBJID]** - sourceID
| **[LOT]** - sourceLOT
| **[int]** - sourceTYPE
| **[LWOOBJID]** - targetID
| **[LOT]** - targetLOT
| **[NiPoint3]** - targetPOS
| **[int]** - targetTYPE

0425: StartArrangingWithItem
""""""""""""""""""""""""""""
| **[bit]** - bFirstTime, default: true
| **[LWOOBJID]** - buildAreaID, default: LWOOBJID_EMPTY
| **[NiPoint3]** - buildStartPOS
| **[int]** - sourceBAG
| **[LWOOBJID]** - sourceID
| **[LOT]** - sourceLOT
| **[int]** - sourceTYPE
| **[LWOOBJID]** - targetID
| **[LOT]** - targetLOT
| **[NiPoint3]** - targetPOS
| **[int]** - targetTYPE

0426: FinishArrangingWithItem
"""""""""""""""""""""""""""""
| **[LWOOBJID]** - buildAreaID, default: LWOOBJID_EMPTY
| **[int]** - newSourceBAG
| **[LWOOBJID]** - newSourceID
| **[LOT]** - newSourceLOT
| **[int]** - newSourceTYPE
| **[LWOOBJID]** - newTargetID
| **[LOT]** - newTargetLOT
| **[int]** - newTargetTYPE
| **[NiPoint3]** - newtargetPOS
| **[int]** - oldItemBAG
| **[LWOOBJID]** - oldItemID
| **[LOT]** - oldItemLOT
| **[int]** - oldItemTYPE

0427: DoneArrangingWithItem
"""""""""""""""""""""""""""
| **[int]** - newSourceBAG
| **[LWOOBJID]** - newSourceID
| **[LOT]** - newSourceLOT
| **[int]** - newSourceTYPE
| **[LWOOBJID]** - newTargetID
| **[LOT]** - newTargetLOT
| **[int]** - newTargetTYPE
| **[NiPoint3]** - newtargetPOS
| **[int]** - oldItemBAG
| **[LWOOBJID]** - oldItemID
| **[LOT]** - oldItemLOT
| **[int]** - oldItemTYPE

042c: SetBuildMode
""""""""""""""""""
| **[bit]** - bStart
| **[int]** - distanceType, default: -1
| **[bit]** - modePaused, default: false
| **[int]** - modeValue, default: 1
| **[LWOOBJID]** - playerID
| **[NiPoint3]** - startPos, default: NiPoint3::ZERO

042d: BuildModeSet
""""""""""""""""""
| **[bit]** - bStart
| **[int]** - distanceType, default: -1
| **[bit]** - modePaused, default: false
| **[int]** - modeValue, default: 1
| **[LWOOBJID]** - playerID
| **[NiPoint3]** - startPos, default: NiPoint3::ZERO

0430: BuildExitConfirmation
"""""""""""""""""""""""""""
| **[LWOOBJID]** - playerID

0431: SetBuildModeConfirmed
"""""""""""""""""""""""""""
| **[bit]** - bStart
| **[bit]** - bWarnVisitors, default: true
| **[bit]** - modePaused, default: false
| **[int]** - modeValue, default: 1
| **[LWOOBJID]** - playerID
| **[NiPoint3]** - startPos, default: NiPoint3::ZERO

0433: BuildModeNotificationReport
"""""""""""""""""""""""""""""""""
| **[bit]** - bStart
| **[int]** - numSent

0435: SetModelToBuild
"""""""""""""""""""""
| **[LOT]** - templateID, default: -1

0436: SpawnModelBricks
""""""""""""""""""""""
| **[float]** - amount, default: 0.0f
| **[NiPoint3]** - pos, default: NiPoint3::ZERO

0439: NotifyClientFailedPrecondition
""""""""""""""""""""""""""""""""""""
| **[std::wstring]** - FailedReason
| **[int]** - PreconditionID

0445: MoveItemBetweenInventoryTypes
"""""""""""""""""""""""""""""""""""
| **[int]** - inventoryTypeA
| **[int]** - inventoryTypeB
| **[LWOOBJID]** - objectID
| **[bit]** - showFlyingLoot, default: true
| **[u32]** - stackCount, default: 1
| **[LOT]** - templateID, default: LOT_NULL
| 
| 0448 - ModularBuildMoveAndEquip
| """""""""""""""""""""""""""""""
| **[LOT]** - templateID 

0449: ModularBuildFinish
""""""""""""""""""""""""
| Note: this is all one parameter to the game message
| **[u8]** - count
|     **[s32]** - module lot

0469: MissionDialogueCancelled
""""""""""""""""""""""""""""""
| **[bit]** - bIsComplete
| **[int]** - iMissionState
| **[int]** - missionID
| **[LWOOBJID]** - responder

046b: ModuleAssemblyDBDataForClient
"""""""""""""""""""""""""""""""""""
| **[LWOOBJID]** - assemblyID
| **[std::wstring]** - blob

046c: ModuleAssemblyQueryData
"""""""""""""""""""""""""""""
| 

0478: EchoSyncSkill
"""""""""""""""""""
| **[bit]** - bDone, default: false
| **[std::string]** - sBitStream
| **[u32]** - uiBehaviorHandle
| **[u32]** - uiSkillHandle

0479: SyncSkill
"""""""""""""""
| **[bit]** - bDone, default: false
| **[std::string]** - sBitStream
| **[u32]** - uiBehaviorHandle
| **[u32]** - uiSkillHandle

047c: RequestServerProjectileImpact
"""""""""""""""""""""""""""""""""""
| **[LWOOBJID]** - i64LocalID, default: LWOOBJID_EMPTY
| **[LWOOBJID]** - i64TargetID, default: LWOOBJID_EMPTY
| **[std::string]** - sBitStream

047f: DoClientProjectileImpact
""""""""""""""""""""""""""""""
| **[LWOOBJID]** - i64OrgID, default: LWOOBJID_EMPTY
| **[LWOOBJID]** - i64OwnerID, default: LWOOBJID_EMPTY
| **[LWOOBJID]** - i64TargetID, default: LWOOBJID_EMPTY
| **[std::string]** - sBitStream

048d: SetPlayerAllowedRespawn
"""""""""""""""""""""""""""""
| **[bit]** - dontPromptForRespawn

048e: ToggleSendingPositionUpdates
""""""""""""""""""""""""""""""""""
| **[bit]** - bSendUpdates, default: false

0492: PlacePropertyModel
""""""""""""""""""""""""
| **[LWOOBJID]** - modelID

04a0: UIMessageServerToSingleClient
"""""""""""""""""""""""""""""""""""
| **[NDGFxValue]** - args
| **[std::string]** - strMessageName
| 
| 04ae - ReportBug
| """"""""""""""""
| **[std::wstring]** - body
| **[std::string]** - clientVersion
| **[std::string]** - nOtherPlayerID
| **[std::string]** - selection

04b2: RequestSmashPlayer
""""""""""""""""""""""""

04b6: UncastSkill
"""""""""""""""""
| **[int]** - skillID

04bd: FireEventClientSide
"""""""""""""""""""""""""
| **[std::wstring]** - args
| **[LWOOBJID]** - object
| **[s64]** - param1, default: 0
| **[int]** - param2, default: -1
| **[LWOOBJID]** - senderID

04c7: ChangeObjectWorldState
""""""""""""""""""""""""""""
| **[eObjectWorldState]** - newState, default: WORLDSTATE_INWORLD

04ce: VehicleLockInput
""""""""""""""""""""""
| **[bit]** - bLockWheels, default: true
| **[bit]** - bLockedPowerslide, default: false
| **[float]** - fLockedX, default: 0.0f
| **[float]** - fLockedY, default: 0.0f

04cf: VehicleUnlockInput
""""""""""""""""""""""""
| **[bit]** - bLockWheels, default: true

04d6: ResyncEquipment
"""""""""""""""""""""
| 

04e4: RacingResetPlayerToLastReset
""""""""""""""""""""""""""""""""""
| **[LWOOBJID]** - playerID

04e6: RacingSetPlayerResetInfo
""""""""""""""""""""""""""""""
| **[int]** - currentLap
| **[u32]** - furthestResetPlane
| **[LWOOBJID]** - playerID
| **[NiPoint3]** - respawnPos
| **[u32]** - upcomingPlane

04e7: RacingPlayerInfoResetFinished
"""""""""""""""""""""""""""""""""""
| **[LWOOBJID]** - playerID

04ec: LockNodeRotation
""""""""""""""""""""""
| **[std::string]** - nodeName

04f9: VehicleSetWheelLockState
""""""""""""""""""""""""""""""
| **[bit]** - bExtraFriction, default: true
| **[bit]** - bLocked, default: false

04fc: NotifyVehicleOfRacingObject
"""""""""""""""""""""""""""""""""
| **[LWOOBJID]** - racingObjectID, default: LWOOBJID_EMPTY

0510: PlayerReachedRespawnCheckpoint
""""""""""""""""""""""""""""""""""""
| **[NiPoint3]** - pos
| **[NiQuaternion]** - rot, default: NiQuaternion::IDENTITY

0514: HandleUGCEquipPostDeleteBasedOnEditMode
"""""""""""""""""""""""""""""""""""""""""""""
| **[LWOOBJID]** - invItem
| **[int]** - itemsTotal, default: 0

0515: HandleUGCEquipPreCreateBasedOnEditMode
""""""""""""""""""""""""""""""""""""""""""""
| **[bit]** - bOnCursor
| **[int]** - modelCount
| **[LWOOBJID]** - modelID

0519: PropertyContentsFromClient
""""""""""""""""""""""""""""""""
| **[bit]** - queryDB, default: false

051d: MatchResponse
"""""""""""""""""""
| **[int]** - response

051e: MatchUpdate
"""""""""""""""""
| **[LwoNameValue]** - data
| **[int]** - type

053a: ChangeIdleFlags
"""""""""""""""""""""
| **[int]** - off, default: 0
| **[int]** - on, default: 0

053c: VehicleAddPassiveBoostAction
""""""""""""""""""""""""""""""""""
| 

053d: VehicleRemovePassiveBoostAction
"""""""""""""""""""""""""""""""""""""
| 

053e: VehicleNotifyServerAddPassiveBoostAction
""""""""""""""""""""""""""""""""""""""""""""""
| 

053f: VehicleNotifyServerRemovePassiveBoostAction
"""""""""""""""""""""""""""""""""""""""""""""""""
| 

055a: ZonePropertyModelRotated
""""""""""""""""""""""""""""""
| **[LWOOBJID]** - playerID, default: LWOOBJID_EMPTY
| **[LWOOBJID]** - propertyID, default: LWOOBJID_EMPTY

055b: ZonePropertyModelRemovedWhileEquipped
"""""""""""""""""""""""""""""""""""""""""""
| **[LWOOBJID]** - playerID, default: LWOOBJID_EMPTY
| **[LWOOBJID]** - propertyID, default: LWOOBJID_EMPTY

055c: ZonePropertyModelEquipped
"""""""""""""""""""""""""""""""
| **[LWOOBJID]** - playerID, default: LWOOBJID_EMPTY
| **[LWOOBJID]** - propertyID, default: LWOOBJID_EMPTY

056e: NotifyRacingClient
""""""""""""""""""""""""
| **[eRacingClientNotificationType]** - EventType, default: INVALID
| **[int]** - param1
| **[LWOOBJID]** - paramObj
| **[std::wstring]** - paramStr
| **[LWOOBJID]** - singleClient

0570: RacingPlayerLoaded
""""""""""""""""""""""""
| **[LWOOBJID]** - playerID
| **[LWOOBJID]** - vehicleID

0571: RacingClientReady
"""""""""""""""""""""""
| **[LWOOBJID]** - playerID

057e: ResetPropertyBehaviors
""""""""""""""""""""""""""""
| **[bit]** - bForce, default: true
| **[bit]** - bPause, default: false

0581: SetConsumableItem
"""""""""""""""""""""""
| **[LOT]** - itemTemplateID

058b: UsedInformationPlaque
"""""""""""""""""""""""""""
| **[LWOOBJID]** - i64Plaque

059b: SetStatusImmunity
"""""""""""""""""""""""
| **[EImmunityState]** - StateChangeType
| **[bit]** - bImmuneToBasicAttack
| **[bit]** - bImmuneToDOT
| **[bit]** - bImmuneToImaginationGain
| **[bit]** - bImmuneToImaginationLoss
| **[bit]** - bImmuneToInterrupt
| **[bit]** - bImmuneToKnockback
| **[bit]** - bImmuneToPullToPoint
| **[bit]** - bImmuneToQuickbuildInterrupt
| **[bit]** - bImmuneToSpeed

059e: ActivateBrickMode
"""""""""""""""""""""""
| **[LWOOBJID]** - buildObjectID, default: LWOOBJID_EMPTY
| **[EBuildType]** - buildType, default: BUILD_ON_PROPERTY
| **[bit]** - enterBuildFromWorld, default: true
| **[bit]** - enterFlag, default: true

05a8: SetPetNameModerated
"""""""""""""""""""""""""
| **[LWOOBJID]** - PetDBID, default: LWOOBJID_EMPTY
| **[int]** - nModerationStatus

05ab: CancelSkillCast
"""""""""""""""""""""
| 

05b3: ModifyLegoScore
"""""""""""""""""""""
| **[s64]** - score
| **[int]** - sourceType, default: LOOTTYPE_NONE

05bc: RestoreToPostLoadStats
""""""""""""""""""""""""""""
| 

05bf: SetRailMovement
"""""""""""""""""""""
| **[bit]** - pathGoForward
| **[std::wstring]** - pathName
| **[u32]** - pathStart
| **[int]** - railActivatorComponentID, default: -1
| **[LWOOBJID]** - railActivatorObjID, default: LWOOBJID_EMPTY

05c0: StartRailMovement
"""""""""""""""""""""""
| **[bit]** - bDamageImmune, default: true
| **[bit]** - bNoAggro, default: true
| **[bit]** - bNotifyActivator, default: false
| **[bit]** - bShowNameBillboard, default: true
| **[bit]** - cameraLocked, default: true
| **[bit]** - collisionEnabled, default: true
| **[std::wstring]** - loopSound
| **[bit]** - pathGoForward, default: true
| **[std::wstring]** - pathName
| **[u32]** - pathStart, default: 0
| **[int]** - railActivatorComponentID, default: -1
| **[LWOOBJID]** - railActivatorObjID, default: LWOOBJID_EMPTY
| **[std::wstring]** - startSound
| **[std::wstring]** - stopSound
| **[bit]** - useDB, default: true

05c2: CancelRailMovement
""""""""""""""""""""""""
| **[bit]** - bImmediate, default: false

05c4: ClientRailMovementReady
"""""""""""""""""""""""""""""
| 

05c5: PlayerRailArrivedNotification
"""""""""""""""""""""""""""""""""""
| **[std::wstring]** - pathName
| **[int]** - waypointNumber

05c6: NotifyRailActivatorStateChange
""""""""""""""""""""""""""""""""""""
| **[bit]** - bActive, default: true

05c7: RequestRailActivatorState
"""""""""""""""""""""""""""""""
| 

05c8: NotifyRewardMailed
""""""""""""""""""""""""
| **[LWOOBJID]** - objectID
| **[NiPoint3]** - startPoint
| **[LWOOBJID]** - subkey
| **[LOT]** - templateID

05c9: UpdatePlayerStatistic
"""""""""""""""""""""""""""
| **[int]** - updateID
| **[s64]** - updateValue, default: 1

05cd: ModifyGhostingDistance
""""""""""""""""""""""""""""
| **[float]** - fDistanceScalar, default: 1.0f

05d3: RequeryPropertyModels
"""""""""""""""""""""""""""
| 

05da: ModularAssemblyNIFCompleted
"""""""""""""""""""""""""""""""""
| **[LWOOBJID]** - objectID

05e7: GetHotPropertyData
""""""""""""""""""""""""
| 

05ec: NotifyNotEnoughInvSpace
"""""""""""""""""""""""""""""
| **[u32]** - freeSlotsNeeded
| **[u32]** - inventoryType, default: INVENTORY_DEFAULT

060a: NotifyPropertyOfEditMode
""""""""""""""""""""""""""""""
| **[bit]** - bEditingActive

060b: UpdatePropertyPerformanceCost
"""""""""""""""""""""""""""""""""""
| **[float]** - performanceCost, default: 0.0f

0611: PropertyEntranceBegin
"""""""""""""""""""""""""""
| 

0615: TeamSetLeader
"""""""""""""""""""
| **[LWOOBJID]** - i64PlayerID

0616: TeamInviteConfirm
"""""""""""""""""""""""
| **[bit]** - bLeaderIsFreeTrial, default: false
| **[LWOOBJID]** - i64LeaderID
| **[LWOZONEID]** - i64LeaderZoneID
| **[BinaryBuffer]** - sTeamBuffer
| **[unsigned char]** - ucLootFlag
| **[unsigned char]** - ucNumOfOtherPlayers
| **[unsigned char]** - ucResponseCode
| **[std::wstring]** - wsLeaderName

0617: TeamGetStatusResponse
"""""""""""""""""""""""""""
| **[LWOOBJID]** - i64LeaderID
| **[LWOZONEID]** - i64LeaderZoneID
| **[BinaryBuffer]** - sTeamBuffer
| **[unsigned char]** - ucLootFlag
| **[unsigned char]** - ucNumOfOtherPlayers
| **[std::wstring]** - wsLeaderName

061a: TeamAddPlayer
"""""""""""""""""""
| **[bit]** - bIsFreeTrial, default: false
| **[bit]** - bLocal, default: false
| **[bit]** - bNoLootOnDeath, default: false
| **[LWOOBJID]** - i64PlayerID
| **[std::wstring]** - wsPlayerName
| **[LWOZONEID]** - zoneID, default: LWOZONEID_INVALID

061b: TeamRemovePlayer
""""""""""""""""""""""
| **[bit]** - bDisband
| **[bit]** - bIsKicked
| **[bit]** - bIsLeaving
| **[bit]** - bLocal, default: false
| **[LWOOBJID]** - i64LeaderID
| **[LWOOBJID]** - i64PlayerID
| **[std::wstring]** - wsName

0629: SetEmotesEnabled
""""""""""""""""""""""
| **[bit]** - bEnableEmotes, default: true

0637: SetResurrectRestoreValues
"""""""""""""""""""""""""""""""
| **[int]** - iArmorRestore, default: -1
| **[int]** - iHealthRestore, default: -1
| **[int]** - iImaginationRestore, default: -1

063a: SetPropertyModerationStatus
"""""""""""""""""""""""""""""""""
| **[int]** - moderationStatus, default: -1

063b: UpdatePropertyModelCount
""""""""""""""""""""""""""""""
| **[u32]** - modelCount, default: 0

0646: VehicleNotifyHitImaginationServer
"""""""""""""""""""""""""""""""""""""""
| **[LWOOBJID]** - pickupObjID, default: LWOOBJID_EMPTY
| **[LWOOBJID]** - pickupSpawnerID, default: LWOOBJID_EMPTY
| **[int]** - pickupSpawnerIndex, default: -1
| **[NiPoint3]** - vehiclePosition, default: NiPoint3::ZERO

0651: VehicleStopBoost
""""""""""""""""""""""
| **[bit]** - bAffectPassive, default: true

0652: StartCelebrationEffect
""""""""""""""""""""""""""""
| **[std::wstring]** - animation
| **[LOT]** - backgroundObject, default: 11164
| **[LOT]** - cameraPathLOT, default: 12458
| **[float]** - celeLeadIn, default: 1.0f
| **[float]** - celeLeadOut, default: 0.8f
| **[int]** - celebrationID, default: -1
| **[float]** - duration
| **[u32]** - iconID
| **[std::wstring]** - mainText
| **[std::string]** - mixerProgram
| **[std::string]** - musicCue
| **[std::string]** - pathNodeName
| **[std::string]** - soundGUID
| **[std::wstring]** - subText

0660: CelebrationCompleted
""""""""""""""""""""""""""
| **[std::wstring]** - animation
| **[int]** - celebrationID, default: -1

0664: SetLocalTeam
""""""""""""""""""
| **[bit]** - bIsLocal, default: false

066a: ServerDoneLoadingAllObjects
"""""""""""""""""""""""""""""""""
| 

066f: AddBuff
"""""""""""""
| **[bit]** - bAddedByTeammate
| **[bit]** - bApplyOnTeammates
| **[bit]** - bCancelOnDamageAbsorbRanOut
| **[bit]** - bCancelOnDamaged
| **[bit]** - bCancelOnDeath, default: true
| **[bit]** - bCancelOnLogOut
| **[bit]** - bCancelOnMove
| **[bit]** - bCancelOnRemoveBuff, default: true
| **[bit]** - bCancelOnUI
| **[bit]** - bCancelOnUnEquip
| **[bit]** - bCancelOnZone
| **[bit]** - bIgnoreImmunities
| **[bit]** - bIsImmunity
| **[bit]** - bUseRefCount
| **[LWOOBJID]** - casterID
| **[LWOOBJID]** - i64AddedBy
| **[u32]** - uiBuffID
| **[u32]** - uiDurationMS

0670: RemoveBuff
""""""""""""""""
| **[bit]** - bFromRemoveBehavior
| **[bit]** - bFromUnEquip
| **[bit]** - bRemoveImmunity
| **[u32]** - uiBuffID

068c: PlayerSetCameraCyclingMode
""""""""""""""""""""""""""""""""
| **[bit]** - bAllowCyclingWhileDeadOnly, default: true
| **[eCyclingMode]** - cyclingMode, default: ALLOW_CYCLE_TEAMMATES

06be: SetMountInventoryID
"""""""""""""""""""""""""
| **[LWOOBJID]** - inventoryMountID, default: LWOOBJID_EMPTY

06c6: NotifyServerLevelProcessingComplete
"""""""""""""""""""""""""""""""""""""""""
| 

06c7: NotifyLevelRewards
""""""""""""""""""""""""
| **[int]** - level
| **[bit]** - sendingRewards, default: false

06d2: ServerCancelMoveSkill
"""""""""""""""""""""""""""
| 

06d3: ClientCancelMoveSkill
"""""""""""""""""""""""""""
| 

06dc: DismountComplete
""""""""""""""""""""""
| **[LWOOBJID]** - mountID

06e7: MarkInventoryItemAsActive
"""""""""""""""""""""""""""""""
| **[bit]** - bActive, default: false
| **[int]** - iType, default: 0
| **[LWOOBJID]** - itemID, default: LWOOBJID_EMPTY
