Game Database
=============

The game database is a collection of information tables provided in the
latest game version via the `CDClient.fdb` :doc:`file-structures/database` file. It used to be
named `ivantest.fdb` and previous to that `ivantest.xml`.

It is used to describe the majority of content within the game, or rather
their registration and properties, relying on and defining the assets that
are present in the resource folder.

The client database is usually compressed within a :doc:`file-structures/pack` file, but may
be decompressed and manipulated to change the game's behavior.

As the table columns follow no common naming convention, this is very
much a system which must have evolved over time, with many people working
on getting all LU systems to be backed by the database.

The database is censored in some places where the client does not have
and does not need some information, such as server-side script files.
In those cases strings are replaced with a string like
:samp:`TableName__123__column__removed`.

.. toctree::
   :maxdepth: 2
   :caption: Tables

   database/AICombatRoles
   database/AccessoryDefaultLoc
   database/Activities
   database/ActivityRewards
   database/ActivityText
   database/AnimationIndex
   database/Animations
   database/BaseCombatAIComponent
   database/BehaviorEffect
   database/BehaviorParameter
   database/BehaviorTemplate
   database/BehaviorTemplateName
   database/Blueprints
   database/BrickColors
   database/BrickIDTable
   database/BuffDefinitions
   database/BuffParameters
   database/Camera
   database/CelebrationParameters
   database/ChoiceBuildComponent
   database/CollectibleComponent
   database/ComponentsRegistry
   database/ControlSchemes
   database/CurrencyDenominations
   database/CurrencyTable
   database/DBExclude
   database/DeletionRestrictions
   database/DestructibleComponent
   database/DevModelBehaviors
   database/Emotes
   database/EventGating
   database/ExhibitComponent
   database/Factions
   database/FeatureGating
   database/FlairTable
   database/Icons
   database/InventoryComponent
   database/ItemComponent
   database/ItemEggData
   database/ItemFoodData
   database/ItemSetSkills
   database/ItemSets
   database/JetPackPadComponent
   database/LUPExhibitComponent
   database/LUPExhibitModelData
   database/LUPZoneIDs
   database/LanguageType
   database/LevelProgressionLookup
   database/LootMatrix
   database/LootMatrixIndex
   database/LootTable
   database/LootTableIndex
   database/MinifigComponent
   database/MinifigDecals_Eyebrows
   database/MinifigDecals_Eyes
   database/MinifigDecals_Legs
   database/MinifigDecals_Mouths
   database/MinifigDecals_Torsos
   database/MissionEmail
   database/MissionNPCComponent
   database/MissionTasks
   database/MissionText
   database/Missions
   database/ModelBehavior
   database/ModularBuildComponent
   database/ModuleComponent
   database/MotionFX
   database/MovementAIComponent
   database/MovingPlatforms
   database/NpcIcons
   database/ObjectBehaviorXREF
   database/ObjectBehaviors
   database/ObjectSkills
   database/Objects
   database/PackageComponent
   database/PetAbilities
   database/PetComponent
   database/PetNestComponent
   database/PhysicsComponent
   database/PlayerFlags
   database/PlayerStatistics
   database/PossessableComponent
   database/Preconditions
   database/PropertyEntranceComponent
   database/PropertyTemplate
   database/ProximityMonitorComponent
   database/ProximityTypes
   database/RacingModuleComponent
   database/RailActivatorComponent
   database/RarityTable
   database/RarityTableIndex
   database/RebuildComponent
   database/RebuildSections
   database/Release_Version
   database/RenderComponent
   database/RenderComponentFlash
   database/RenderComponentWrapper
   database/RenderIconAssets
   database/ReputationRewards
   database/RewardCodes
   database/Rewards
   database/RocketLaunchpadControlComponent
   database/SceneTable
   database/ScriptComponent
   database/SkillBehavior
   database/SmashableChain
   database/SmashableChainIndex
   database/SmashableComponent
   database/SmashableElements
   database/SpeedchatMenu
   database/SubscriptionPricing
   database/SurfaceType
   database/TamingBuildPuzzles
   database/TextDescription
   database/TextLanguage
   database/TrailEffects
   database/UGBehaviorSounds
   database/VehiclePhysics
   database/VehicleStatMap
   database/VendorComponent
   database/WhatsCoolItemSpotlight
   database/WhatsCoolNewsAndTips
   database/WorldConfig
   database/ZoneLoadingTips
   database/ZoneSummary
   database/ZoneTable
   database/brickAttributes
   database/dtproperties
   database/mapAnimationPriorities
   database/mapAssetType
   database/mapIcon
   database/mapItemTypes
   database/mapRenderEffects
   database/mapShaders
   database/mapTextureResource
   database/map_BlueprintCategory
   database/sysdiagrams