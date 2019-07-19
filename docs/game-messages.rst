Game Messages
=============

.. note ::
	This is a read-the-docs port of the original google docs `lu_game_messages <https://docs.google.com/document/d/117F74OhLcdsykwRJ1wnpx4TahsFa2zGtOvMF6I3_afg>`_, written by humanoid, lcdr and others, ported by `@Xiphoseer <https://twitter.com/Xiphoseer>`_. This is currently a proof of concept and is not guaranteed to reflect the latest changes.

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

.. _gm-teleport:

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

.. _gm-drop-client-loot:

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

.. _gm-die:

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

.. _gm-request-die:

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

.. _gm-play-emote:

0029: PlayEmote
"""""""""""""""
| **[int]** - emoteID
| **[LWOOBJID]** - targetID

.. _gm-preload-animation:

002a: PreloadAnimation
""""""""""""""""""""""
| **[std::wstring]** - animationID
| **[bit]** - handled, default: false
| **[LWOOBJID]** - respondObjID
| **[LwoNameValue]** - userData

.. _gm-play-animation:

002b: PlayAnimation
"""""""""""""""""""
| **[std::wstring]** - animationID
| **[bit]** - bExpectAnimToExist, default: true
| **[bit]** - bPlayImmediate
| **[bit]** - bTriggerOnCompleteMsg, default: false
| **[float]** - fPriority, default: SECONDARY_PRIORITY
| **[float]** - fScale, default: 1.0f

.. _gm-control-behaviors:

0030: ControlBehaviors
""""""""""""""""""""""
| **[NDGFxValue]** - args
| **[std::string]** - command

.. _gm-set-name:

0048: SetName
"""""""""""""
| **[std::wstring]** - name

.. _gm-echo-start-skill:

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

.. _gm-start-skill:

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

.. _gm-caster-dead:

0078: CasterDead
""""""""""""""""
| **[LWOOBJID]** - i64Caster, default: LWOOBJID_EMPTY
| **[u32]** - uiSkillHandle, default: 0

.. _gm-verify-ack:

0079: VerifyAck
"""""""""""""""
| **[bit]** - bDifferent, default: false
| **[std::string]** - sBitStream
| **[u32]** - uiHandle, default: 0

.. _gm-select-skill:

007c: SelectSkill
"""""""""""""""""
| **[bit]** - bFromSkillSet, default: false
| **[int]** - skillID

.. _gm-add-skill:

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

.. _gm-remove-skill:

0080: RemoveSkill
"""""""""""""""""
| **[bit]** - bFromSkillSet, default: false
| **[TSkillID]** - skillID

.. _gm-set-currency:

0085: SetCurrency
"""""""""""""""""
| **[s64]** - currency
| **[int]** - lootType, default: LOOTTYPE_NONE
| **[NiPoint3]** - position
| **[LOT]** - sourceLOT, default: LOT_NULL
| **[LWOOBJID]** - sourceObject, default: LWOOBJID_EMPTY
| **[LWOOBJID]** - sourceTradeID, default: LWOOBJID_EMPTY
| **[int]** - sourceType, default: LOOTTYPE_NONE

.. _gm-pickup-currency:

0089: PickupCurrency
""""""""""""""""""""
| **[u32]** - currency
| **[NiPoint3]** - position

.. _gm-pickup-item:

008b: PickupItem
""""""""""""""""
| **[LWOOBJID]** - lootObjectID
| **[LWOOBJID]** - playerID

.. _gm-team-pickup-item:

008c: TeamPickupItem
""""""""""""""""""""
| **[LWOOBJID]** - lootID
| **[LWOOBJID]** - lootOwnerID

.. _gm-play-fx-effect:

009a: PlayFXEffect
""""""""""""""""""
| **[int]** - effectID, default: -1
| **[std::wstring]** - effectType
| **[float]** - fScale, default: 1.0f
| **[std::string]** - name
| **[float]** - priority, default: 1.0
| **[LWOOBJID]** - secondary, default: LWOOBJID_EMPTY
| **[bit]** - serialize, default: true

.. _gm-stop-fx-effect:

009b: StopFXEffect
""""""""""""""""""
| **[bit]** - bKillImmediate
| **[std::string]** - name

.. _gm-request-resurrect:

009f: RequestResurrect
""""""""""""""""""""""
|

.. _gm-resurrect:

00a0: Resurrect
"""""""""""""""
| **[bit]** - bRezImmediately, default: false

.. _gm-pop-equipped-items-state:

00c0: PopEquippedItemsState
"""""""""""""""""""""""""""
|

.. _gm-set-stunned:

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

.. _gm-set-stun-immunity:

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

.. _gm-knockback:

00ca: Knockback
"""""""""""""""
| **[LWOOBJID]** - Caster, default: LWOOBJID_EMPTY
| **[LWOOBJID]** - Originator, default: LWOOBJID_EMPTY
| **[int]** - iKnockBackTimeMS, default: 0
| **[NiPoint3]** - vector

.. _gm-rebuild-cancel:

00d1: RebuildCancel
"""""""""""""""""""
| **[bit]** - bEarlyRelease
| **[LWOOBJID]** - userID

.. _gm-enable-rebuild:

00d5: EnableRebuild
"""""""""""""""""""
| **[bit]** - bEnable
| **[bit]** - bFail
| **[bit]** - bSuccess
| **[FailReason]** - eFailReason, default: REASON_NOT_GIVEN
| **[float]** - fDuration
| **[LWOOBJID]** - user

.. _gm-move-item-in-inventory:

00e0: MoveItemInInventory
"""""""""""""""""""""""""
| **[int]** - destInvType, default: INVENTORY_INVALID
| **[LWOOBJID]** - iObjID
| **[int]** - inventoryType
| **[int]** - responseCode
| **[int]** - slot

.. _gm-add-item-to-inventory-client-sync:

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

.. _gm-remove-item-from-inventory:

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

.. _gm-equip-inventory:

00e7: EquipInventory
""""""""""""""""""""
| **[bit]** - bIgnoreCooldown, default: false
| **[bit]** - bOutSuccess
| **[LWOOBJID]** - itemtoequip


.. _gm-unequip-inventory:

00e9: UnEquipInventory
""""""""""""""""""""""
| **[bit]** - bEvenIfDead, default: false
| **[bit]** - bIgnoreCooldown, default: false
| **[bit]** - bOutSuccess
| **[LWOOBJID]** - itemtounequip
| **[LWOOBJID]** - replacementObjectID, default: LWOOBJID_EMPTY

.. _gm-offer-mission:

00f8: OfferMission
""""""""""""""""""
| **[int]** - missionID
| **[LWOOBJID]** - offerer

.. _gm-respond-to-mission:

00f9: RespondToMission
""""""""""""""""""""""
| **[int]** - missionID
| **[LWOOBJID]** - playerID
| **[LWOOBJID]** - receiver
| **[LOT]** - rewardItem, default: LOT_NULL

.. _gm-notify-mission:

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

.. _gm-notify-mission-task:

00ff: NotifyMissionTask
"""""""""""""""""""""""
| **[int]** - missionID
| **[int]** - taskMask
| taskMask is a bitmask with the bit corresponding to the task index (1<<(task index+1)) set.
| **[u8]** - length
| 	**[float]** - updates

For collectibles the updates are of the form collectible_id+(world_id<<8)

.. _gm-rebuild-notify-state:

0150: RebuildNotifyState
""""""""""""""""""""""""
| **[int]** - iPrevState
| **[int]** - iState
| **[LWOOBJID]** - player

.. _gm-toggle-interaction-updates:

0164: ToggleInteractionUpdates
""""""""""""""""""""""""""""""
| **[bit]** - bEnable, default: false

.. _gm-terminate-interaction:

0165: TerminateInteraction
""""""""""""""""""""""""""
| **[LWOOBJID]** - ObjIDTerminator
| **[ETerminateType]** - type

.. _gm-server-terminate-interaction:

0166: ServerTerminateInteraction
""""""""""""""""""""""""""""""""
| **[LWOOBJID]** - ObjIDTerminator
| **[ETerminateType]** - type

.. _gm-request-use:

016c: RequestUse
""""""""""""""""
| **[bit]** - bIsMultiInteractUse
| **[u32]** - multiInteractID
| **[int]** - multiInteractType
| **[LWOOBJID]** - object
| **[bit]** - secondary, default: false

.. _gm-vendor-open-window:

0171: VendorOpenWindow
""""""""""""""""""""""
|

.. _gm-emote-played:

0173: EmotePlayed
"""""""""""""""""
| **[int]** - emoteID
| **[LWOOBJID]** - targetID

.. _gm-buy-from-vendor:

0175: BuyFromVendor
"""""""""""""""""""
| **[bit]** - confirmed, default: false
| **[int]** - count, default: 1
| **[LOT]** - item

.. _gm-sell-to-vendor:

0176: SellToVendor
""""""""""""""""""
| **[int]** - count, default: 1
| **[LWOOBJID]** - itemObjID

.. _gm-cancel-donation-on-player:

017b: CancelDonationOnPlayer
""""""""""""""""""""""""""""
|

.. _gm-team-set-off-world-flag:

017f: TeamSetOffWorldFlag
"""""""""""""""""""""""""
| **[LWOOBJID]** - i64PlayerID
| **[LWOZONEID]** - zoneID

.. _gm-set-inventory-size:

0185: SetInventorySize
""""""""""""""""""""""
| **[int]** - inventoryType
| **[int]** - size

.. _gm-acknowledge-possession:

0187: AcknowledgePossession
"""""""""""""""""""""""""""
| **[LWOOBJID]** - possessedObjID, default: LWOOBJID_EMPTY

.. _gm-request-activity-exit:

0194: RequestActivityExit
"""""""""""""""""""""""""
| **[bit]** - bUserCancel
| **[LWOOBJID]** - userID

.. _gm-activity-enter:

0195: ActivityEnter
"""""""""""""""""""
|

.. _gm-activity-exit:

0196: ActivityExit
""""""""""""""""""
|

.. _gm-activity-start:

0197: ActivityStart
"""""""""""""""""""
|

.. _gm-activity-stop:

0198: ActivityStop
""""""""""""""""""
| **[bit]** - bExit
| **[bit]** - bUserCancel

.. _gm-shooting-gallery-fire:

019b: ShootingGalleryFire
"""""""""""""""""""""""""
| **[NiPoint3]** - targetPos
| **[float]** - w
| **[float]** - x
| **[float]** - y
| **[float]** - z

.. _gm-request-vendor-status-update:

01a0: RequestVendorStatusUpdate
"""""""""""""""""""""""""""""""

.. _gm-vendor-status-update:

01a1: VendorStatusUpdate
""""""""""""""""""""""""
| **[bit]** - bUpdateOnly
| **[u32]** - inventoryList
|     **[int]** - LOT
|     **[int]** - sortPriority

.. _gm-cancel-mission:

01a2: CancelMission
"""""""""""""""""""
| **[int]** - missionID
| **[bit]** - resetCompleted

.. _gm-reset-mission:

01a3: ResetMissions
"""""""""""""""""""
| **[int]** - missionID, default: -1

.. _gm-notify-client-shooting-gallery-score:

01a9: NotifyClientShootingGalleryScore
""""""""""""""""""""""""""""""""""""""
| **[float]** - addTime
| **[int]** - score
| **[LWOOBJID]** - target
| **[NiPoint3]** - targetPos

.. _gm-client-item-consumed:

01ac: ClientItemConsumed
""""""""""""""""""""""""
| **[LWOOBJID]** - item

.. _gm-update-shooting-gallery-rotation:

01c0: UpdateShootingGalleryRotation
"""""""""""""""""""""""""""""""""""
| **[float]** - angle
| **[NiPoint3]** - facing
| **[NiPoint3]** - muzzlePos

.. _gm-set-user-ctrl-comp-pause:

01d2: SetUserCtrlCompPause
""""""""""""""""""""""""""
| **[bit]** - bPaused

.. _gm-set-tooltip-flag:

01d5: SetTooltipFlag
""""""""""""""""""""
| **[bit]** - bFlag
| **[int]** - iToolTip

.. _gm-set-flag:

01d7: SetFlag
"""""""""""""
| **[bit]** - bFlag
| **[int]** - iFlagID

.. _gm-notify-client-flag-change:

01d8: NotifyClientFlagChange
""""""""""""""""""""""""""""
| **[bit]** - bFlag
| **[int]** - iFlagID

.. _gm-help:

01db: Help
""""""""""
| **[int]** - iHelpID

.. _gm-vendor-transaction-result:

01dc: VendorTransactionResult
"""""""""""""""""""""""""""""
| **[int]** - iResult
| <Please Add Possible Result Codes>
| 0x02 = Success

.. _gm-has-been-collected:

01e6: HasBeenCollected
""""""""""""""""""""""
| **[LWOOBJID]** - playerID

.. _gm-has-been-collected-by-client:

01e7: HasBeenCollectedByClient
""""""""""""""""""""""""""""""
| **[LWOOBJID]** - playerID

.. _gm-despawn-pet:

01f3: DespawnPet
""""""""""""""""
| **[bit]** - bDeletePet

.. _gm-player-loaded:

01f9: PlayerLoaded
""""""""""""""""""
| **[LWOOBJID]** - playerID

.. _gm-player-ready:

01fd: PlayerReady
"""""""""""""""""

.. _gm-request-linked-mission:

0203: RequestLinkedMission
""""""""""""""""""""""""""
| **[LWOOBJID]** - playerID
| **[int]** - missionID
| **[bit]** - bMissionOffered, default: false

.. _gm-transfer-to-zone:

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

.. _gm-transfer-to-zone-checked-im:

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

.. _gm-invalid-zone-transfer-list:

0207: InvalidZoneTransferList
"""""""""""""""""""""""""""""
| **[std::wstring]** - CustomerFeedbackURL
| **[std::wstring]** - InvalidMapTransferList
| **[bit]** - bCustomerFeedbackOnExit
| **[bit]** - bCustomerFeedbackOnInvalidMapTransfer

.. _gm-mission-dialogue-ok:

0208: MissionDialogueOK
"""""""""""""""""""""""
| **[bit]** - bIsComplete
| **[int]** - iMissionState
| **[int]** - missionID
| **[LWOOBJID]** - responder

.. _gm-transfer-to-last-non-instance:

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

.. _gm-display-message-box:

0211: DisplayMessageBox
"""""""""""""""""""""""
| **[bit]** - bShow
| **[LWOOBJID]** - callbackClient
| **[std::wstring]** - identifier
| **[int]** - imageID
| **[std::wstring]** - text
| **[std::wstring]** - userData

.. _gm-message-box-respond:

0212: MessageBoxRespond
"""""""""""""""""""""""
| **[int]** - iButton
| **[std::wstring]** - identifier
| **[std::wstring]** - userData

.. _gm-choice-box-respond:

0213: ChoiceBoxRespond
""""""""""""""""""""""
| **[std::wstring]** - buttonIdentifier
| **[int]** - iButton
| **[std::wstring]** - identifier

.. _gm-smash:

0219: Smash
"""""""""""
| **[bit]** - bIgnoreObjectVisibility, default: false
| **[float]** - force
| **[float]** - ghostOpacity
| **[LWOOBJID]** - killerID

.. _gm-unsmash:

021a: UnSmash
"""""""""""""
| **[LWOOBJID]** - builderID, default: LWOOBJID_EMPTY
| **[float]** - duration, default: 3.0f

.. _gm-set-gravity-scale:

021d: SetGravityScale
"""""""""""""""""""""
| **[float]** - scale (accepted: between 0f - 2f [above sets it to 2f, lower sets it to 0f] normal: 1f)

.. _gm-place-model-response:

0223: PlaceModelResponse
""""""""""""""""""""""""
| **[NiPoint3]** - position, default: NiPoint3::ZERO
| **[LWOOBJID]** - propertyPlaqueID, default: LWOOBJID_EMPTY
| **[int]** - response, default: 0
| **[NiQuaternion]** - rotation, default: NiQuaternion::IDENTITY

.. _gm-set-jet-pack-mode:

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

.. _gm-register-pet-id:

0235: RegisterPetID
"""""""""""""""""""
| **[LWOOBJID]** - objID

.. _gm-register-pet-dbid:

0236: RegisterPetDBID
"""""""""""""""""""""
| **[LWOOBJID]** - petDBID

.. _gm-show-activity-countdown:

0238: ShowActivityCountdown
"""""""""""""""""""""""""""
| **[bit]** - bPlayAdditionalSound
| **[bit]** - bPlayCountdownSound
| **[std::wstring]** - sndName
| **[int]** - stateToPlaySoundOn

.. _gm-display-tooltip:

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

.. _gm-start-activity-time:

0240: StartActivityTime
"""""""""""""""""""""""
| **[float]** - startTime

.. _gm-activity-pause:

025a: ActivityPause
"""""""""""""""""""
| **[bit]** - bPause

.. _gm-use-non-equipment-item:

025b: UseNonEquipmentItem
"""""""""""""""""""""""""
| **[LWOOBJID]** - itemToUse

.. _gm-use-item-result:

025f: UseItemResult
"""""""""""""""""""
| **[LOT]** - m_ItemTemplateID
| **[bit]** - m_UseItemResult, default: false

.. _gm-fetch-model-metadata-request:

027e: FetchModelMetadataRequest
"""""""""""""""""""""""""""""""
| **[int]** - context
| **[LWOOBJID]** - objectID
| **[LWOOBJID]** - requestorID
| **[LWOOBJID]** - ugID

.. _gm-command-pet:

0280: CommandPet
""""""""""""""""
| **[NiPoint3]** - GenericPosInfo
| **[LWOOBJID]** - ObjIDSource
| **[int]** - iPetCommandType
| **[int]** - iTypeID
| **[bit]** - overrideObey, default: false

.. _gm-pet-response:

0281: PetResponse
"""""""""""""""""
| **[LWOOBJID]** - ObjIDPet
| **[int]** - iPetCommandType
| **[int]** - iResponse
| **[int]** - iTypeID

.. _gm-request-activity-summary-leaderboard-data:

0288: RequestActivitySummaryLeaderboardData
"""""""""""""""""""""""""""""""""""""""""""
| **[int]** - gameID, default: LWOOBJID_EMPTY
| **[int]** - queryType, default: 1
| **[int]** - resultsEnd, default: 10
| **[int]** - resultsStart, default: 0
| **[LWOOBJID]** - target
| **[bit]** - weekly

.. _gm-send-activity-summary-leaderboard-data:

0289: SendActivitySummaryLeaderboardData
""""""""""""""""""""""""""""""""""""""""
| **[int]** - gameID
| **[int]** - infoType
| **[LwoNameValue]** - leaderboardData
| **[bit]** - throttled
| **[bit]** - weekly

.. _gm-client-notify-pet:

0293: ClientNotifyPet
"""""""""""""""""""""
| **[LWOOBJID]** - ObjIDSource
| **[int]** - iPetNotificationType

.. _gm-notify-pet:

0294: NotifyPet
"""""""""""""""
| **[LWOOBJID]** - ObjIDSource
| **[LWOOBJID]** - ObjToNotifyPetAbout
| **[int]** - iPetNotificationType

.. _gm-notify-pet-taming-minigame:

0295: NotifyPetTamingMinigame
"""""""""""""""""""""""""""""
| **[LWOOBJID]** - PetID
| **[LWOOBJID]** - PlayerTamingID
| **[bit]** - bForceTeleport
| **[eNotifyType]** - notifyType
| **[NiPoint3]** - petsDestPos
| **[NiPoint3]** - telePos
| **[NiQuaternion]** - teleRot, default: NiQuaternion::IDENTITY

.. _gm-start-server-pet-minigame-timer:

0296: StartServerPetMinigameTimer
"""""""""""""""""""""""""""""""""
|

.. _gm-client-exit-taming-minigame:

0297: ClientExitTamingMinigame
""""""""""""""""""""""""""""""
| **[bit]** - bVoluntaryExit, default: true

.. _gm-pet-taming-minigame-result:

029b: PetTamingMinigameResult
"""""""""""""""""""""""""""""
| **[bit]** - bSuccess

.. _gm-pet-taming-try-build-result:

029c: PetTamingTryBuildResult
"""""""""""""""""""""""""""""
| **[bit]** - bSuccess, default: true
| **[int]** - iNumCorrect, default: 0

.. _gm-notify-taming-build-success:

02a1: NotifyTamingBuildSuccess
""""""""""""""""""""""""""""""
| **[NiPoint3]** - BuildPosition

.. _gm-notify-taming-model-loaded-on-server:

02a2: NotifyTamingModelLoadedOnServer
"""""""""""""""""""""""""""""""""""""
|

.. _gm-add-pet-to-player:

02a9: AddPetToPlayer
""""""""""""""""""""
| **[int]** - iElementalType
| **[std::wstring]** - name
| **[LWOOBJID]** - petDBID
| **[LOT]** - petLOT

.. _gm-request-set-pet-name:

02ab: RequestSetPetName
"""""""""""""""""""""""
| **[std::wstring]** - name

.. _gm-set-pet-name:

02ac: SetPetName
""""""""""""""""
| **[std::wstring]** - name
| **[LWOOBJID]** - petDBID, default: LWOOBJID_EMPTY

.. _gm-pet-name-changed:

02ae: PetNameChanged
""""""""""""""""""""
| **[int]** - moderationStatus
| **[std::wstring]** - name
| **[std::wstring]** - ownerName

.. _gm-show-pet-action-button:

02b4: ShowPetActionButton
"""""""""""""""""""""""""
| **[int]** - ButtonLabel
| **[bit]** - bShow

.. _gm-set-emote-lock-state:

02b5: SetEmoteLockState
"""""""""""""""""""""""
| **[bit]** - bLock
| **[int]** - emoteID

.. _gm-use-item-requirements-response:

02bf: UseItemRequirementsResponse
"""""""""""""""""""""""""""""""""
| **[u32]** - eUseResponse

.. _gm-play-embedded-effect-on-all-clients-near-object:

02c9: PlayEmbeddedEffectOnAllClientsNearObject
""""""""""""""""""""""""""""""""""""""""""""""
| **[std::wstring]** - effectName
| **[LWOOBJID]** - fromObjectID
| **[float]** - radius

.. _gm-query-property-data:

02cd: QueryPropertyData
"""""""""""""""""""""""
|

.. _gm-property-editor-begin:

02d4: PropertyEditorBegin
"""""""""""""""""""""""""
| **[int]** - distanceType, default: 0
| **[LWOOBJID]** - propertyObjectID, default: LWOOBJID_EMPTY
| **[int]** - startMode, default: 1
| **[bit]** - startPaused, default: 0

.. _gm-property-editor-end:

02d5: PropertyEditorEnd
"""""""""""""""""""""""
|

.. _gm-notify-client-zone-object:

02e1: NotifyClientZoneObject
""""""""""""""""""""""""""""
| **[std::wstring]** - name
| **[int]** - param1
| **[int]** - param2
| **[LWOOBJID]** - paramObj
| **[std::string]** - paramStr

.. _gm-update-reputation:

02ea: UpdateReputation
""""""""""""""""""""""
| **[s64]** - iReputation

.. _gm-property-rental-response:

02ee: PropertyRentalResponse
""""""""""""""""""""""""""""
| **[LWOCLONEID]** - cloneid
| **[int]** - code
| **[LWOOBJID]** - propertyID
| **[s64]** - rentdue

.. _gm-request-platform-resync:

02f8: RequestPlatformResync
"""""""""""""""""""""""""""
|

.. _gm-platform-resync:

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

.. _gm-play-cinematic:

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

.. _gm-end-cinematic:

02fb: EndCinematic
""""""""""""""""""
| **[float]** - leadOut, default: -1.0f
| **[bit]** - leavePlayerLocked, default: false
| **[std::wstring]** - pathName

.. _gm-cinematic-update:

02fc: CinematicUpdate
"""""""""""""""""""""
| **[CinematicEvent]** - event, default: STARTED
| **[float]** - overallTime, default: -1.0f
| **[std::wstring]** - pathName
| **[float]** - pathTime, default: -1.0f
| **[int]** - waypoint, default: -1

.. _gm-toggle-ghost-reference-override:

02ff: ToggleGhostReferenceOverride
""""""""""""""""""""""""""""""""""
| **[bit]** - override, default: false

.. _gm-set-ghost-reference-position:

0300: SetGhostReferencePosition
"""""""""""""""""""""""""""""""
| **[NiPoint3]** - pos
|

.. _gm-fire-event-server-side:

0302: FireEventServerSide
"""""""""""""""""""""""""
| **[std::wstring]** - args
| **[int]** - param1, default: -1
| **[int]** - param2, default: -1
| **[int]** - param3, default: -1
| **[LWOOBJID]** - senderID

.. _gm-script-network-var-update:

030d: ScriptNetworkVarUpdate
""""""""""""""""""""""""""""
| **[LwoNameValue]** - tableOfVars

.. _gm-update-model-from-client:

0319: UpdateModelFromClient
"""""""""""""""""""""""""""
| **[LWOOBJID]** - modelID
| **[NiPoint3]** - position
| **[NiQuaternion]** - rotation, default: NiQuaternion::IDENTITY

.. _gm-delete-model-from-client:

031a: DeleteModelFromClient
"""""""""""""""""""""""""""
| **[LWOOBJID]** - modelID, default: LWOOBJID_EMPTY
| **[DeleteReason]** - reason, default: PICKING_MODEL_UP

.. _gm-play-nd-audio-emitter:

0335: PlayNDAudioEmitter
""""""""""""""""""""""""
| **[s64]** - m_NDAudioCallbackMessageData, default: 0
| **[NDAudio::TNDAudioID]** - m_NDAudioEmitterID, default: NDAudio::g_NDAudioIDNone
| **[std::string]** - m_NDAudioEventGUID
| **[std::string]** - m_NDAudioMetaEventName
| **[bit]** - m_Result, default: false
| **[LWOOBJID]** - m_TargetObjectIDForNDAudioCallbackMessages, default: LWOOBJID_EMPTY

.. _gm-stop-nd-audio-emitter:

0336: StopNDAudioEmitter
""""""""""""""""""""""""
| **[bit]** - m_AllowNativeFadeOut, default: true
| **[NDAudio::TNDAudioID]** - m_NDAudioEmitterID, default: NDAudio::g_NDAudioIDNone
| **[std::string]** - m_NDAudioEventGUID
| **[std::string]** - m_NDAudioMetaEventName
| **[bit]** - m_Result, default: false

.. _gm-enter-property-1:

0348: EnterProperty1
""""""""""""""""""""
| **[int]** - index
| **[bit]** - returnToZone, default: true

.. _gm-property-entrance-sync:

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

.. _gm-parse-chat-message:

0352: ParseChatMessage
""""""""""""""""""""""
| **[int]** - iClientState
| **[std::wstring]** - wsString

.. _gm-set-mission-type-state:

0353: SetMissionTypeState
"""""""""""""""""""""""""
| **[EMissionLockState]** - state, default: NEW
| **[std::string]** - subtype
| **[std::string]** - type

.. _gm-broadcast-text-to-chatbox:

035a: BroadcastTextToChatbox
""""""""""""""""""""""""""""
| **[LwoNameValue]** - attrs
| **[std::wstring]** - wsText

.. _gm-open-property-vendor:

035d: OpenPropertyVendor
""""""""""""""""""""""""
|

.. _gm-client-trade-request:

0364: ClientTradeRequest
""""""""""""""""""""""""
| **[bit]** - bNeedInvitePopUp, default: false
| **[LWOOBJID]** - i64Invitee

.. _gm-server-trade-invite:

0366: ServerTradeInvite
"""""""""""""""""""""""
| **[bit]** - bNeedInvitePopUp, default: false
| **[LWOOBJID]** - i64Requestor
| **[std::wstring]** - wsName

.. _gm-server-trade-intial-reply:

0369: ServerTradeInitialReply
"""""""""""""""""""""""""""""
| **[LWOOBJID]** - i64Invitee
| **[eResultType]** - resultType
| **[std::wstring]** - wsName

.. _gm-server-trade-final-reply:

036a: ServerTradeFinalReply
"""""""""""""""""""""""""""
| **[bit]** - bResult
| **[LWOOBJID]** - i64Invitee
| **[std::wstring]** - wsName

.. _gm-client-trade-cancel:

036e: ClientTradeCancel
"""""""""""""""""""""""
|

.. _gm-client-trade-accept:

0370: ClientTradeAccept
"""""""""""""""""""""""
| **[bit]** - bFirst, default: false

.. _gm-server-trade-accept:

0374: ServerTradeAccept
"""""""""""""""""""""""
| **[bit]** - bFirst, default: false

.. _gm-ready-for-updates:

0378: ReadyForUpdates
"""""""""""""""""""""
| **[LWOOBJID]** - objectID

.. _gm-set-last-custom-build:

037a: SetLastCustomBuild
""""""""""""""""""""""""
| **[std::wstring]** - tokenizedLOTList

.. _gm-get-last-custom-build:

037b: GetLastCustomBuild
""""""""""""""""""""""""
| **[std::wstring]** - tokenizedLOTList

.. _gm-set-ignore-projectile-collision:

0387: SetIgnoreProjectileCollision
""""""""""""""""""""""""""""""""""
| **[bit]** - bShouldIgnore, default: false

.. _gm-orient-to-object:

0389: OrientToObject
""""""""""""""""""""
| **[LWOOBJID]** - objID

.. _gm-orient-to-position:

038a: OrientToPosition
""""""""""""""""""""""
| **[NiPoint3]** - ni3Posit

.. _gm-orient-to-angle:

038b: OrientToAngle
"""""""""""""""""""
| **[bit]** - bRelativeToCurrent
| **[float]** - fAngle

.. _gm-property-moderation-action:

0393: PropertyModerationAction
""""""""""""""""""""""""""""""
| **[LWOOBJID]** - characterID, default: 0
| **[std::wstring]** - info
| **[int]** - newModerationStatus, default: -1

.. _gm-property-moderation-status-update:

0395: PropertyModerationStatusUpdate
""""""""""""""""""""""""""""""""""""
| **[int]** - newModerationStatus, default: -1
| **[std::wstring]** - rejectionReason

.. _gm-bounce-notification:

03a4: BounceNotification
""""""""""""""""""""""""
| **[LWOOBJID]** - ObjIDBounced
| **[LWOOBJID]** - ObjIDBouncer
| **[bit]** - bSuccess

.. _gm-request-client-bounce:

03a6: RequestClientBounce
"""""""""""""""""""""""""
| **[LWOOBJID]** - BounceTargetID
| **[NiPoint3]** - BounceTargetPosOnServer
| **[NiPoint3]** - BouncedObjLinVel
| **[LWOOBJID]** - RequestSourceID
| **[bit]** - bAllBounced
| **[bit]** - bAllowClientOverride

.. _gm-bouncer-active-status:

03ae: BouncerActiveStatus
"""""""""""""""""""""""""
| **[bit]** - bActive

.. _gm-move-inventory-batch:

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

.. _gm-object-activated-client:

03d4: ObjectActivatedClient
"""""""""""""""""""""""""""
| **[LWOOBJID]** - activatorID
| **[LWOOBJID]** - objectActivatedID

.. _gm-set-bbb-autosave:

03e4: SetBBBAutosave
""""""""""""""""""""
| **[BinaryBuffer]** - lxfmlDataCompressed

.. _gm-bbb-load-item-request:

03e8: BBBLoadItemRequest
""""""""""""""""""""""""
| **[LWOOBJID]** - itemID

.. _gm-bbb-save-request:

03e9: BBBSaveRequest
""""""""""""""""""""
| **[LWOOBJID]** - localID
| **[BinaryBuffer]** - lxfmlDataCompressed
| **[u32]** - timeTakenInMS

.. _gm-bbb-reset-metadata-source-item:

03ec: BBBResetMetadataSourceItem
""""""""""""""""""""""""""""""""
|

.. _gm-notify-client-object:

0412: NotifyClientObject
""""""""""""""""""""""""
| **[std::wstring]** - name
| **[int]** - param1
| **[int]** - param2
| **[LWOOBJID]** - paramObj
| **[std::string]** - paramStr

.. _gm-display-zone-summary:

0413: DisplayZoneSummary
""""""""""""""""""""""""
| **[bit]** - isPropertyMap, default: false
| **[bit]** - isZoneStart, default: false
| **[LWOOBJID]** - sender, default: LWOOBJID_EMPTY

.. _gm-zone-summary-dismissed:

0414: ZoneSummaryDismissed
""""""""""""""""""""""""""
| **[LWOOBJID]** - playerID

.. _gm-modify-player-zone-statistic:

0416: ModifyPlayerZoneStatistic
"""""""""""""""""""""""""""""""
| **[bit]** - bSet, default: false
| **[std::wstring]** - statName
| **[int]** - statValue, default: 0
| **[LWOMAPID]** - zoneID, default: LWOMAPID_INVALID

.. _gm-activity-state-change-request:

041d: ActivityStateChangeRequest
""""""""""""""""""""""""""""""""
| **[LWOOBJID]** - i64ObjID
| **[int]** - iNumValue1
| **[int]** - iNumValue2
| **[std::wstring]** - wsStringValue

.. _gm-start-building-with-item:

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

.. _gm-start-arranging-with-item:

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

.. _gm-finish-arranging-with-item:

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

.. _gm-done-arranging-with-item:

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

.. _gm-set-build-mode:

042c: SetBuildMode
""""""""""""""""""
| **[bit]** - bStart
| **[int]** - distanceType, default: -1
| **[bit]** - modePaused, default: false
| **[int]** - modeValue, default: 1
| **[LWOOBJID]** - playerID
| **[NiPoint3]** - startPos, default: NiPoint3::ZERO

.. _gm-build-mode-set:

042d: BuildModeSet
""""""""""""""""""
| **[bit]** - bStart
| **[int]** - distanceType, default: -1
| **[bit]** - modePaused, default: false
| **[int]** - modeValue, default: 1
| **[LWOOBJID]** - playerID
| **[NiPoint3]** - startPos, default: NiPoint3::ZERO

.. _gm-build-exit-confirmation:

0430: BuildExitConfirmation
"""""""""""""""""""""""""""
| **[LWOOBJID]** - playerID

.. _gm-set-build-mode-confirmed:

0431: SetBuildModeConfirmed
"""""""""""""""""""""""""""
| **[bit]** - bStart
| **[bit]** - bWarnVisitors, default: true
| **[bit]** - modePaused, default: false
| **[int]** - modeValue, default: 1
| **[LWOOBJID]** - playerID
| **[NiPoint3]** - startPos, default: NiPoint3::ZERO

.. _gm-build-mode-notification-report:

0433: BuildModeNotificationReport
"""""""""""""""""""""""""""""""""
| **[bit]** - bStart
| **[int]** - numSent

.. _gm-set-model-to-build:

0435: SetModelToBuild
"""""""""""""""""""""
| **[LOT]** - templateID, default: -1

.. _gm-spawn-model-bricks:

0436: SpawnModelBricks
""""""""""""""""""""""
| **[float]** - amount, default: 0.0f
| **[NiPoint3]** - pos, default: NiPoint3::ZERO

.. _gm-notify-client-failed-precondition:

0439: NotifyClientFailedPrecondition
""""""""""""""""""""""""""""""""""""
| **[std::wstring]** - FailedReason
| **[int]** - PreconditionID

.. _gm-move-item-between-inventory-types:

0445: MoveItemBetweenInventoryTypes
"""""""""""""""""""""""""""""""""""
| **[int]** - inventoryTypeA
| **[int]** - inventoryTypeB
| **[LWOOBJID]** - objectID
| **[bit]** - showFlyingLoot, default: true
| **[u32]** - stackCount, default: 1
| **[LOT]** - templateID, default: LOT_NULL

.. _gm-modular-build-move-and-equip:

0448: - ModularBuildMoveAndEquip
""""""""""""""""""""""""""""""""
| **[LOT]** - templateID

.. _gm-modular-build-finish:

0449: ModularBuildFinish
""""""""""""""""""""""""
| Note: this is all one parameter to the game message
| **[u8]** - count
|     **[s32]** - module lot

.. _gm-mission-dialogue-cancelled:

0469: MissionDialogueCancelled
""""""""""""""""""""""""""""""
| **[bit]** - bIsComplete
| **[int]** - iMissionState
| **[int]** - missionID
| **[LWOOBJID]** - responder

.. _gm-module-assembly-db-data-for-client:

046b: ModuleAssemblyDBDataForClient
"""""""""""""""""""""""""""""""""""
| **[LWOOBJID]** - assemblyID
| **[std::wstring]** - blob

.. _gm-module-assembly-query-data:

046c: ModuleAssemblyQueryData
"""""""""""""""""""""""""""""
|

.. _gm-echo-sync-skill:

0478: EchoSyncSkill
"""""""""""""""""""
| **[bit]** - bDone, default: false
| **[std::string]** - sBitStream
| **[u32]** - uiBehaviorHandle
| **[u32]** - uiSkillHandle

.. _gm-sync-skill:

0479: SyncSkill
"""""""""""""""
| **[bit]** - bDone, default: false
| **[std::string]** - sBitStream
| **[u32]** - uiBehaviorHandle
| **[u32]** - uiSkillHandle

.. _gm-request-server-projectile-impact:

047c: RequestServerProjectileImpact
"""""""""""""""""""""""""""""""""""
| **[LWOOBJID]** - i64LocalID, default: LWOOBJID_EMPTY
| **[LWOOBJID]** - i64TargetID, default: LWOOBJID_EMPTY
| **[std::string]** - sBitStream

.. _gm-do-client-projectile-impact:

047f: DoClientProjectileImpact
""""""""""""""""""""""""""""""
| **[LWOOBJID]** - i64OrgID, default: LWOOBJID_EMPTY
| **[LWOOBJID]** - i64OwnerID, default: LWOOBJID_EMPTY
| **[LWOOBJID]** - i64TargetID, default: LWOOBJID_EMPTY
| **[std::string]** - sBitStream

.. _gm-set-player-allowed-respawn:

048d: SetPlayerAllowedRespawn
"""""""""""""""""""""""""""""
| **[bit]** - dontPromptForRespawn

.. _gm-toggle-sending-position-updates:

048e: ToggleSendingPositionUpdates
""""""""""""""""""""""""""""""""""
| **[bit]** - bSendUpdates, default: false

.. _gm-place-property-model:

0492: PlacePropertyModel
""""""""""""""""""""""""
| **[LWOOBJID]** - modelID

.. _gm-ui-message-server-to-single-client:

04a0: UIMessageServerToSingleClient
"""""""""""""""""""""""""""""""""""
| **[NDGFxValue]** - args
| **[std::string]** - strMessageName

.. _gm-report-bug:

04ae: ReportBug
"""""""""""""""
| **[std::wstring]** - body
| **[std::string]** - clientVersion
| **[std::string]** - nOtherPlayerID
| **[std::string]** - selection

.. _gm-request-smash-player:

04b2: RequestSmashPlayer
""""""""""""""""""""""""

.. _gm-uncast-skill:

04b6: UncastSkill
"""""""""""""""""
| **[int]** - skillID

.. _gm-fire-event-client-side:

04bd: FireEventClientSide
"""""""""""""""""""""""""
| **[std::wstring]** - args
| **[LWOOBJID]** - object
| **[s64]** - param1, default: 0
| **[int]** - param2, default: -1
| **[LWOOBJID]** - senderID

.. _gm-change-object-world-state:

04c7: ChangeObjectWorldState
""""""""""""""""""""""""""""
| **[eObjectWorldState]** - newState, default: WORLDSTATE_INWORLD

.. _gm-vehicle-lock-input:

04ce: VehicleLockInput
""""""""""""""""""""""
| **[bit]** - bLockWheels, default: true
| **[bit]** - bLockedPowerslide, default: false
| **[float]** - fLockedX, default: 0.0f
| **[float]** - fLockedY, default: 0.0f

.. _gm-vehicle-unlock-input:

04cf: VehicleUnlockInput
""""""""""""""""""""""""
| **[bit]** - bLockWheels, default: true

.. _gm-resync-equipment:

04d6: ResyncEquipment
"""""""""""""""""""""
|

.. _gm-racing-reset-player-to-last-reset:

04e4: RacingResetPlayerToLastReset
""""""""""""""""""""""""""""""""""
| **[LWOOBJID]** - playerID

.. _gm-racing-set-player-reset-info:

04e6: RacingSetPlayerResetInfo
""""""""""""""""""""""""""""""
| **[int]** - currentLap
| **[u32]** - furthestResetPlane
| **[LWOOBJID]** - playerID
| **[NiPoint3]** - respawnPos
| **[u32]** - upcomingPlane

.. _gm-racing-player-info-reset-finished:

04e7: RacingPlayerInfoResetFinished
"""""""""""""""""""""""""""""""""""
| **[LWOOBJID]** - playerID

.. _gm-lock-node-rotation:

04ec: LockNodeRotation
""""""""""""""""""""""
| **[std::string]** - nodeName

.. _gm-vehicle-set-wheel-lock-state:

04f9: VehicleSetWheelLockState
""""""""""""""""""""""""""""""
| **[bit]** - bExtraFriction, default: true
| **[bit]** - bLocked, default: false

.. _gm-notify-vehicle-of-racing-object:

04fc: NotifyVehicleOfRacingObject
"""""""""""""""""""""""""""""""""
| **[LWOOBJID]** - racingObjectID, default: LWOOBJID_EMPTY

.. _gm-player-reached-respawn-checkpoint:

0510: PlayerReachedRespawnCheckpoint
""""""""""""""""""""""""""""""""""""
| **[NiPoint3]** - pos
| **[NiQuaternion]** - rot, default: NiQuaternion::IDENTITY

.. _gm-handle-ugc-equip-post-delete-based-on-edit-mode:

0514: HandleUGCEquipPostDeleteBasedOnEditMode
"""""""""""""""""""""""""""""""""""""""""""""
| **[LWOOBJID]** - invItem
| **[int]** - itemsTotal, default: 0

.. _gm-handle-ugc-equip-pre-create-based-on-edit-mode:

0515: HandleUGCEquipPreCreateBasedOnEditMode
""""""""""""""""""""""""""""""""""""""""""""
| **[bit]** - bOnCursor
| **[int]** - modelCount
| **[LWOOBJID]** - modelID

.. _gm-property-contents-from-client:

0519: PropertyContentsFromClient
""""""""""""""""""""""""""""""""
| **[bit]** - queryDB, default: false

.. _gm-match-response:

051d: MatchResponse
"""""""""""""""""""
| **[int]** - response

.. _gm-match-update:

051e: MatchUpdate
"""""""""""""""""
| **[LwoNameValue]** - data
| **[int]** - type

.. _gm-change-idle-flags:

053a: ChangeIdleFlags
"""""""""""""""""""""
| **[int]** - off, default: 0
| **[int]** - on, default: 0

.. _gm-vehicle-add-passive-boost-action:

053c: VehicleAddPassiveBoostAction
""""""""""""""""""""""""""""""""""
|

.. _gm-vehicle-remove-passive-boost-action:

053d: VehicleRemovePassiveBoostAction
"""""""""""""""""""""""""""""""""""""
|

.. _gm-vehicle-notify-server-add-passive-boost-action:

053e: VehicleNotifyServerAddPassiveBoostAction
""""""""""""""""""""""""""""""""""""""""""""""
|

.. _gm-vehicle-notify-server-remove-passive-boost-action:

053f: VehicleNotifyServerRemovePassiveBoostAction
"""""""""""""""""""""""""""""""""""""""""""""""""
|

.. _gm-zone-property-model-rotated:

055a: ZonePropertyModelRotated
""""""""""""""""""""""""""""""
| **[LWOOBJID]** - playerID, default: LWOOBJID_EMPTY
| **[LWOOBJID]** - propertyID, default: LWOOBJID_EMPTY

.. _gm-zone-property-model-removed-while-equipped:

055b: ZonePropertyModelRemovedWhileEquipped
"""""""""""""""""""""""""""""""""""""""""""
| **[LWOOBJID]** - playerID, default: LWOOBJID_EMPTY
| **[LWOOBJID]** - propertyID, default: LWOOBJID_EMPTY

.. _gm-zone-property-model-equipped:

055c: ZonePropertyModelEquipped
"""""""""""""""""""""""""""""""
| **[LWOOBJID]** - playerID, default: LWOOBJID_EMPTY
| **[LWOOBJID]** - propertyID, default: LWOOBJID_EMPTY

.. _gm-notify-racing-client:

056e: NotifyRacingClient
""""""""""""""""""""""""
| **[eRacingClientNotificationType]** - EventType, default: INVALID
| **[int]** - param1
| **[LWOOBJID]** - paramObj
| **[std::wstring]** - paramStr
| **[LWOOBJID]** - singleClient

.. _gm-racing-player-loaded:

0570: RacingPlayerLoaded
""""""""""""""""""""""""
| **[LWOOBJID]** - playerID
| **[LWOOBJID]** - vehicleID

.. _gm-racing-client-ready:

0571: RacingClientReady
"""""""""""""""""""""""
| **[LWOOBJID]** - playerID

.. _gm-reset-property-behaviors:

057e: ResetPropertyBehaviors
""""""""""""""""""""""""""""
| **[bit]** - bForce, default: true
| **[bit]** - bPause, default: false

.. _gm-set-consumable-item:

0581: SetConsumableItem
"""""""""""""""""""""""
| **[LOT]** - itemTemplateID

.. _gm-used-information-plaque:

058b: UsedInformationPlaque
"""""""""""""""""""""""""""
| **[LWOOBJID]** - i64Plaque

.. _gm-set-status-immunity:

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

.. _gm-activate-brick-mode:

059e: ActivateBrickMode
"""""""""""""""""""""""
| **[LWOOBJID]** - buildObjectID, default: LWOOBJID_EMPTY
| **[EBuildType]** - buildType, default: BUILD_ON_PROPERTY
| **[bit]** - enterBuildFromWorld, default: true
| **[bit]** - enterFlag, default: true

.. _gm-set-pet-name-moderated:

05a8: SetPetNameModerated
"""""""""""""""""""""""""
| **[LWOOBJID]** - PetDBID, default: LWOOBJID_EMPTY
| **[int]** - nModerationStatus

.. _gm-cancel-skill-cast:

05ab: CancelSkillCast
"""""""""""""""""""""
|

.. _gm-modify-lego-score:

05b3: ModifyLegoScore
"""""""""""""""""""""
| **[s64]** - score
| **[int]** - sourceType, default: LOOTTYPE_NONE

.. _gm-restore-to-post-load-stats:

05bc: RestoreToPostLoadStats
""""""""""""""""""""""""""""
|

.. _gm-set-rail-movement:

05bf: SetRailMovement
"""""""""""""""""""""
| **[bit]** - pathGoForward
| **[std::wstring]** - pathName
| **[u32]** - pathStart
| **[int]** - railActivatorComponentID, default: -1
| **[LWOOBJID]** - railActivatorObjID, default: LWOOBJID_EMPTY

.. _gm-start-rail-movement:

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

.. _gm-cancel-rail-movement:

05c2: CancelRailMovement
""""""""""""""""""""""""
| **[bit]** - bImmediate, default: false

.. _gm-client-rail-movement-ready:

05c4: ClientRailMovementReady
"""""""""""""""""""""""""""""
|

.. _gm-player-rail-arrived-notification:

05c5: PlayerRailArrivedNotification
"""""""""""""""""""""""""""""""""""
| **[std::wstring]** - pathName
| **[int]** - waypointNumber

.. _gm-notify-rail-activator-state-change:

05c6: NotifyRailActivatorStateChange
""""""""""""""""""""""""""""""""""""
| **[bit]** - bActive, default: true

.. _gm-request-rail-activator-state:

05c7: RequestRailActivatorState
"""""""""""""""""""""""""""""""
|

.. _gm-notify-reward-mailed:

05c8: NotifyRewardMailed
""""""""""""""""""""""""
| **[LWOOBJID]** - objectID
| **[NiPoint3]** - startPoint
| **[LWOOBJID]** - subkey
| **[LOT]** - templateID

.. _gm-update-player-statistics:

05c9: UpdatePlayerStatistic
"""""""""""""""""""""""""""
| **[int]** - updateID
| **[s64]** - updateValue, default: 1

.. _gm-modify-ghosting-distance:

05cd: ModifyGhostingDistance
""""""""""""""""""""""""""""
| **[float]** - fDistanceScalar, default: 1.0f

.. _gm-requery-property-models:

05d3: RequeryPropertyModels
"""""""""""""""""""""""""""
|

.. _gm-modular-assembly-nif-completed:

05da: ModularAssemblyNIFCompleted
"""""""""""""""""""""""""""""""""
| **[LWOOBJID]** - objectID

.. _gm-get-hot-property-data:

05e7: GetHotPropertyData
""""""""""""""""""""""""
|

.. _gm-notify-not-enough-inv-space:

05ec: NotifyNotEnoughInvSpace
"""""""""""""""""""""""""""""
| **[u32]** - freeSlotsNeeded
| **[u32]** - inventoryType, default: INVENTORY_DEFAULT

.. _gm-notify-property-of-edit-mode:

060a: NotifyPropertyOfEditMode
""""""""""""""""""""""""""""""
| **[bit]** - bEditingActive

.. _gm-update-property-performance-cost:

060b: UpdatePropertyPerformanceCost
"""""""""""""""""""""""""""""""""""
| **[float]** - performanceCost, default: 0.0f

.. _gm-property-entrance-begin:

0611: PropertyEntranceBegin
"""""""""""""""""""""""""""
|

.. _gm-team-set-leader:

0615: TeamSetLeader
"""""""""""""""""""
| **[LWOOBJID]** - i64PlayerID

.. _gm-team-invite-confirm:

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

.. _gm-team-get-status-response:

0617: TeamGetStatusResponse
"""""""""""""""""""""""""""
| **[LWOOBJID]** - i64LeaderID
| **[LWOZONEID]** - i64LeaderZoneID
| **[BinaryBuffer]** - sTeamBuffer
| **[unsigned char]** - ucLootFlag
| **[unsigned char]** - ucNumOfOtherPlayers
| **[std::wstring]** - wsLeaderName

.. _gm-team-add-player:

061a: TeamAddPlayer
"""""""""""""""""""
| **[bit]** - bIsFreeTrial, default: false
| **[bit]** - bLocal, default: false
| **[bit]** - bNoLootOnDeath, default: false
| **[LWOOBJID]** - i64PlayerID
| **[std::wstring]** - wsPlayerName
| **[LWOZONEID]** - zoneID, default: LWOZONEID_INVALID

.. _gm-team-remove-player:

061b: TeamRemovePlayer
""""""""""""""""""""""
| **[bit]** - bDisband
| **[bit]** - bIsKicked
| **[bit]** - bIsLeaving
| **[bit]** - bLocal, default: false
| **[LWOOBJID]** - i64LeaderID
| **[LWOOBJID]** - i64PlayerID
| **[std::wstring]** - wsName

.. _gm-set-emotes-enabled:

0629: SetEmotesEnabled
""""""""""""""""""""""
| **[bit]** - bEnableEmotes, default: true

.. _gm-resurrect-restore-values:

0637: SetResurrectRestoreValues
"""""""""""""""""""""""""""""""
| **[int]** - iArmorRestore, default: -1
| **[int]** - iHealthRestore, default: -1
| **[int]** - iImaginationRestore, default: -1

.. _gm-set-property-moderation-status:

063a: SetPropertyModerationStatus
"""""""""""""""""""""""""""""""""
| **[int]** - moderationStatus, default: -1

.. _gm-update-property-model-count:

063b: UpdatePropertyModelCount
""""""""""""""""""""""""""""""
| **[u32]** - modelCount, default: 0

.. _gm-vehicle-notify-hit-imagination-server:

0646: VehicleNotifyHitImaginationServer
"""""""""""""""""""""""""""""""""""""""
| **[LWOOBJID]** - pickupObjID, default: LWOOBJID_EMPTY
| **[LWOOBJID]** - pickupSpawnerID, default: LWOOBJID_EMPTY
| **[int]** - pickupSpawnerIndex, default: -1
| **[NiPoint3]** - vehiclePosition, default: NiPoint3::ZERO

.. _gm-vehicle-stop-boost:

0651: VehicleStopBoost
""""""""""""""""""""""
| **[bit]** - bAffectPassive, default: true

.. _gm-start-celebration-effect:

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

.. _gm-celebration-completed:

0660: CelebrationCompleted
""""""""""""""""""""""""""
| **[std::wstring]** - animation
| **[int]** - celebrationID, default: -1

.. _gm-set-local-team:

0664: SetLocalTeam
""""""""""""""""""
| **[bit]** - bIsLocal, default: false

.. _gm-server-done-loading-all-objects:

066a: ServerDoneLoadingAllObjects
"""""""""""""""""""""""""""""""""
|

.. _gm-add-buff:

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

.. _gm-remove-buff:

0670: RemoveBuff
""""""""""""""""
| **[bit]** - bFromRemoveBehavior
| **[bit]** - bFromUnEquip
| **[bit]** - bRemoveImmunity
| **[u32]** - uiBuffID

.. _gm-player-set-camera-cycling-mode:

068c: PlayerSetCameraCyclingMode
""""""""""""""""""""""""""""""""
| **[bit]** - bAllowCyclingWhileDeadOnly, default: true
| **[eCyclingMode]** - cyclingMode, default: ALLOW_CYCLE_TEAMMATES

.. _gm-set-mount-inventory-id:

06be: SetMountInventoryID
"""""""""""""""""""""""""
| **[LWOOBJID]** - inventoryMountID, default: LWOOBJID_EMPTY

.. _gm-notify-server-level-processing-complete:

06c6: NotifyServerLevelProcessingComplete
"""""""""""""""""""""""""""""""""""""""""
|

.. _gm-notify-level-rewards:

06c7: NotifyLevelRewards
""""""""""""""""""""""""
| **[int]** - level
| **[bit]** - sendingRewards, default: false

.. _gm-server-cancel-move-skill:

06d2: ServerCancelMoveSkill
"""""""""""""""""""""""""""
|

.. _gm-client-cancel-move-skill:

06d3: ClientCancelMoveSkill
"""""""""""""""""""""""""""
|

.. _gm-dismount-complete:

06dc: DismountComplete
""""""""""""""""""""""
| **[LWOOBJID]** - mountID

.. _gm-mark-inventory-item-as-active:

06e7: MarkInventoryItemAsActive
"""""""""""""""""""""""""""""""
| **[bit]** - bActive, default: false
| **[int]** - iType, default: 0
| **[LWOOBJID]** - itemID, default: LWOOBJID_EMPTY
