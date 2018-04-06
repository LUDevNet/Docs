Loading a world
===============

This diagram describes the packets required to load a world in the client.
The systems involved are an Auth Server (NetID 1), a world server (NetID 4)
and a Client (NetID 5).

.. uml::

   == Login ==

   Client -> AuthServer: [<b>53-00-00-00</b>] Handshake
   AuthServer -> Client: [<b>53-00-00-00</b>] Handshake
   Client -> AuthServer: [<b>53-01-00-00</b>] Login Request
   AuthServer -> Client: [<b>53-05-00-00</b>] Login Info

   == CharacterSelection ==

   Client -> WorldServer: [<b>53-00-00-00</b>] Handshake
   WorldServer -> Client: [<b>53-00-00-00</b>] Handshake
   Client -> WorldServer: [<b>53-04-00-01</b>] Client Validation
   Client -> WorldServer: [<b>53-04-00-02</b>] CharList Request
   WorldServer -> Client: [<b>53-05-00-06</b>] CharList Response
   Client -> WorldServer: [<b>53-04-00-04</b>] Client Login Request
   WorldServer -> Client: [<b>53-05-00-0E</b>] RedirectToServer

   == WorldLoading ==

   Client -> WorldServer: [<b>53-00-00-00</b>] Handshake
   WorldServer -> Client: [<b>53-00-00-00</b>] Handshake
   Client -> WorldServer: [<b>53-04-00-01</b>] Client Validation
   WorldServer -> Client: [<b>53-05-00-02</b>] Load World
   Client -> WorldServer: [<b>53-04-00-19</b>] Load Complete
   WorldServer -> Client: [<b>53-05-00-04</b>] Chardata
   WorldServer -> Client: ReplicaManager Packets
