Manifest (.txt) 
^^^^^^^^^^^^^^^
(in :file:`/versions` folder)

| **[version]** section:
|   There is a single line in this section. The elements are:
|
|   1) version number
|   2) md5 hash of version number as text

| **[files]** section:
| 	Every line represents a file entry which consists of six values (in ASCII format), separated by a :samp:`,`
| 	
| 	1) filename
| 	2) filesize
| 	3) md5 hash of file
| 	4) compressed filesize
| 	5) md5 hash of compressed file
| 	6) md5 hash of values 1) to 5) (includes ‘,’ separators except the one preceding this value)
