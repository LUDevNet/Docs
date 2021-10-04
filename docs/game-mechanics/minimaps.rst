Minimaps
--------

The background tiles for the minimaps are stored in the `client/res/maps/minimaps` folder. For each
:doc:`../file-structures/zone` file there is one folder. Each of these folders contains three zoom levels::

    $ ls
    zoom_0
    zoom_1
    zoom_2

Level 2 has the highest resolution, level 0 the lowest. Each of those folders contains multiple
256x256 pixel :samp:`image_XXXX.dds` tiles that make up the map when stiched together.

Manual Stitching
^^^^^^^^^^^^^^^^

You can use ImageMagick with the following command to stitch a single map. :samp:`W` and :samp:`H` need to be
replaced by the number of tiles per row and column respectively. Usually that's the square root of the total
number of tiles as all known maps are square.::

    $ montage -tile WxH -mode concatenate image_*.dds image.png
