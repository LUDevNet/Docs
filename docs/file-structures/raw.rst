.raw
^^^^

.. note ::
	
	Used for terrain data.
	See also: http://legouniverse.wikia.com/wiki/User_blog:Jamesster.LEGO/Terrain_files 

| **[L:0x423b]** - chunk of data (seems to be always the same size?), needs to be further picked apart
| **[u32]** - size specifier for the following data
| 		*(shift amount, actual size is calculated by shifting 4 left, by two times the amount of zeroes before the bit of the specifier, e.g size specifier = 0x40 -> has 6 zeros -> size = 4 << (2*6)), should always be a power of two number?*
| 	**[u8]** - data
| 
| **[u32]** - ???
|	*(tocheck: is this value dependant on the size specifier? was 0xb38 for 0x40 and 0x338 for 0x20)*
| 
| **[chunkWidth * chunkHeight * images (always 2 so far)]**
| 	**[DDS_File] - [‘D’-’D’-’S’-0x20]** specifier followed by DDS Header info and image data

.. todo :: the rest of this, seems like there are a bunch more DDS_Files and more of that other data with the size specifiers, the only question is if they are in any particular order or random (possibly specified in the initial chunk of data)

* Portabello: 18 dds files in total
* Avant gardens: 242 dds files in total, so far they are ordered in chunk of image 1, chunk of image 2, chunk of image 1, chunk of image 2, ...