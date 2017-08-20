.. LU Documentation documentation master file, created by
   sphinx-quickstart on Sun Aug 20 22:12:09 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to the Lego Universe technical documentation!
=====================================================

The purpose of this documentation is to list and protocol all the information about the network packets of the game LEGO Universe. For organization purposes the contents of the documentation is extended to the following documents:

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   client
   server
   replica

   game-messages
   game-mechanics

   file-structures

If any of these documents helped you in some way or another for one of your projects then please credit us and/or include a direct link to this document.

.. warning ::

	LEGO is in no way affiliated with the content of this and the aforementioned documents.
	Furthermore the creators of the just mentioned documents are not associated or involved with LEGO or any existing “official” private server websites for the game.


Contact Info
------------
Feel free to visit us on our IRC channel on freenode for a discussion about the game and its inner workings.

.. glossary::

	Channel
		`##luserver <https://webchat.freenode.net/?channels=%23%23luserver>`_ on irc.freenode.net

	Time frame
	    if not otherwise occupied we are online between 6:30 PM and 9:30 PM UTC


Quick Notes to get started
--------------------------

Client
^^^^^^

* This documentation is targeted towards the latest publicly released client (1.10.64) which you can download in its original form `here <https://mega.nz/#!zpQyzAyA!az8Omzz-mH-03nOT1-H5jpjm75x2ZyDAv9BikCUHxG8>`_ (recommended) or in its unpacked form `here <https://mega.nz/#!zhRzBa4C!B5eY94-6vYmjJYqXkDXDM5hiqkPhZ7yb9ShCHG3Lgo8>`_.
* To redirect the client to a different server simply change the :samp:`AUTHSERVERIP` host info in the :file:`boot.cfg` file to a new host.
* The client stores an additional config and a log file from the last session in the :file:`[SystemDrive]:\\Users\\[User]\\AppData\\Local\\LEGO Software\\LEGO Universe\\` folder.

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


Indices and tables
==================

* :ref:`genindex`
* :ref:`search`
