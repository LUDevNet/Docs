Introduction
============

.. note ::
	This is a read-the-docs port of the original google docs `lu_packet_structs <https://docs.google.com/document/d/1v9GB1gNwO0C81Rhd4imbaLN7z-R0zpK5sYJMbxPP3Kc>`_, written by humanoid, lcdr and others, ported by `@Xiphoseer <https://twitter.com/Xiphoseer>`_. This is currently a proof of concept and is not guaranteed to reflect the latest changes.

Quick notes to get started
--------------------------

Client
^^^^^^

* This documentation is targeted towards the latest publicly released client (1.10.64) which you can download in its original form `here <https://mega.nz/#!zpQyzAyA!az8Omzz-mH-03nOT1-H5jpjm75x2ZyDAv9BikCUHxG8>`_ (recommended) or in its unpacked form `here <https://mega.nz/#!zhRzBa4C!B5eY94-6vYmjJYqXkDXDM5hiqkPhZ7yb9ShCHG3Lgo8>`_.
* To redirect the client to a different server simply change the :samp:`AUTHSERVERIP` host info in the :file:`boot.cfg` file to a new host.
* The client stores an additional config and a log file from the last session in the :file:`{SystemDrive}:\\Users\\{User}\\AppData\\Local\\LEGO Software\\LEGO Universe\\` folder.

Server
^^^^^^

* The client uses the RakNet network library (v3.25) to communicate with the server, therefore it is recommended to use it in the server if you want to work on one and are new to this project.
* You can download it `here <http://www.raknet.com/raknet/downloads/RakNet-3.25.zip>`_ (documentation and sample projects are included), note that later versions of the library won’t work due to changes in the network protocol. Alternatively lcdr wrote a python version with the minimum features needed to run a server for the game implemented, available `here <https://bitbucket.org/lcdr/pyraknet>`_ (no documentation yet so not recommended for inexperienced users)
* The listening port for the Authentication Server is hardcoded to 1001 (UDP), the ports for the following instances (char, world) depend on what the Authentication Server sends to the client but the port range used for the original servers was 2001-2200 (UDP)
* In order for the server to establish a working connection with the client it is required to set up a pre-set password in RakNet by calling :samp:`SetIncomingPassword("3.25 ND1", 8);` for the `RakPeerInterface` instance before listening for packets
* It seems that the server used the :samp:`SYSTEM_PRIORITY` and :samp:`RELIABLE_ORDERED` options for all outgoing packets to the client (though that's probably not a requirement)

Packet Captures
---------------

Thanks to pwjones we have access to quite a lot of (partial) traffic sessions of the original server which serve as a basis for this documentation, if you want to dig into them yourself, here is a `download link <https://mega.co.nz/#F!yxIyxCpR!rNJ5Uub4RJNL8c6ZgM-Q0w>`_.

Since the original captures (`*.pcap` files) were encrypted by RakNet it was required to decrypt them again (`*.bin` files stored in `*.zip` archives where each archive represents a session) which was only possible using a piece of information that RakNet exchanges at the beginning of a traffic.

However since more than half of the captured traffics only consist of a fraction of the entire session this information is missing for those captures (marked as `*_unresolved.pcap`), making them undecryptable at this point (they’re still included in the archives though, so all available captures are in one place).

There are a few exceptions where it was possible to decrypt them using the same information from other traffic sessions but the remaining ones can’t be decrypted with this method so they’ll remain unreadable for the time being.

The naming format used is:
:file:`[packet number]_[source port]-[destination port]_[packet header]_[optional].bin`
where :samp:`[optional]` is used to display game message ids or network ids and LOTs in round brackets for the according packet types.

Extracting the entire .zip capture(s) is not recommended, since this many files (several ten thousand) will have a huge overhead on the file system (because of things like last modified info, which isn’t applicable here anyways), resulting in a much larger file space consumption and slower access times when trying to list the files in the explorer.
If you want to search multiple captures for specific files, use this script: https://bitbucket.org/lcdr/utils/src find_packets.py

(The script also yields the binary content of the packets, which can be useful for further filtering or logging)
If you want to look at the raw data of a packet yourself (not recommended for inexperienced users) you can of course extract single files from the .zip archive using an archive extractor of your choice (I recommend 7-Zip).
Then you can open the extracted `*.bin` file(s) using a hex editor of your choice (for some packet types it might be useful to have an editor that can shift the bits in the data, no recommendation here).
Alternatively a graphical viewer for capture files is available at https://bitbucket.org/lcdr/utils/src/ captureviewer.py (takes the entire .zip archive of a traffic as input, no need to extract anything)


Appendix A: LEGO data format and data type IDs
----------------------------------------------

LDF is used in boot.cfg, client xml settings, .luz and .lvl files, and the binary part of the chardata packet.

This binary data format is used in various packets, for example the chardata packet.

:[u32]: number of keys

	:[u8]: key length in bytes
	:[wchar]: key
	:[u8]: data type (see below)
	:[according to data type]: data

The text format has the format: :samp:`key=type:value`

:0:   String (variable wstring?)
:1:   s32
:2:   ??? (haven’t found an occurrence of this type so far)
:3:   Float (32bit, signed)
:4:   ??? (Location&Size, appeared on lwo_override.xml)
:5:   u32
:6:   ??? (haven’t found an occurrence of this type so far)
:7:   Boolean (8bit, 0 or 1)
:8:   s64
:9:   s64, Used only for (object?) IDs?
:10:  ??? (haven’t found an occurrence of this type so far)
:11:  ??? (haven’t found an occurrence of this type so far)
:12:  ??? (haven’t found an occurrence of this type so far)
:13:  in chardata this was XML data, in client settings checksum, in lvl files strings/GUIDs (maybe it's for bytes)

Appendix B: Maps info and checksum
----------------------------------

Here are the checksums I found.  Probably need to go back through and find the different map instances if I can.

==========================  ==========  ==================================
Map Name                    Zone ID     Checksum
==========================  ==========  ==================================
Venture Explorer            1000        7c 08 b8 20
Return to Venture Explorer  1001        3c 0a 68 26
Avant Gardens               1100        11 55 52 49
Avant Gardens Survival      1101        e2 14 82 53
Spider Queen Battle         1102        da 03 d4 0f
Block Yard                  1150        da 03 d4 0f
Avant Grove                 1151        03 03 89 0a
Nimbus Station              1200        30 6b 1e da
Pet Cove                    1201        30 13 6e 47
Vertigo Loop Racetrack      1203        02 05 fc 10
Battle of Nimbus Station    1204        58 02 d4 07
Nimbus Rock                 1250        91 01 8d 05
Nimbus Isle                 1251        5d 04 4f 09
Frostburgh                  1260        currently disabled in the client
Gnarled Forest              1300        90 c2 ea 12
Canyon Cove                 1302        ef 02 77 0b
Keelhaul Canyon             1303        todo
Chantey Shantey             1350        5c 01 b6 04
Forbidden Valley            1400        0d 76 19 85
Forbidden Valley Dragon     1402        87 01 f5 02
Dragonmaw Chasm             1403        4e 0f 85 81
Raven Bluff                 1450        26 01 f0 03
Starbase 3001               1600        ee 02 c2 07
Deep Freeze                 1601        06 01 32 02
Robot City                  1602        7f 03 93 07
Moon Base                   1603        ad 01 3b 04
Portabello                  1604        dd 07 15 18
LEGO Club                   1700        38 01 04 02
Crux Prime                  1800        99 a3 17 4b
Nexus Tower                 1900        3c f4 4a 9e
Ninjago                     2000        74 2c 69 4d
Frakjaw Battle              2001        ef 00 eb 09
==========================  ==========  ==================================
