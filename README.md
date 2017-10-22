# *ByteWeiser* <img src="byteweiser.png" alt="ByteWeiser logo" height="48px" width="48px" align="right"/>

**Table of contents**
* [Definition](#definition)
* [Details](#details)
* [Performance](#performance)
* [Requirements](#requirements)
* [Notice](#notice)
* [Useless facts](#useless-facts)

----

## Definition

The *ByteWeiser* project is a simple file synchronization tool that compares two files blockwise and replaces the different bytes.

[Top](#byteweiser-)

## Details

Initially developed to accelerate the backup of virtual machine images, *ByteWeiser* compares the binary data of two files, by running through them block by block. If the current block of the output file is different from that of the input file, the block of the output file will be overwritten with the one from the input file.

You could also use *rsync* with delta compression for that. However, *ByteWeiser* seems to be faster in some cases. Both tools have a completely different functional principle, where *ByteWeiser* is the one that "mindlessly" (simply) processes the data instead of using algorithms and checksums.

[Top](#byteweiser-)

## Performance

I have tested the performance of *ByteWeiser* and compared it with the results of *rsync*.

For that, I created a file (`file1`) and duplicated it. Then, I edited the duplicate (`file2`) using *Vim* (yes, seriously) and changed a single byte at the end of the file.

Notice that the elapsed times are average values, no liability assumed.

### Local system

#### Environment

The tests have been performed on my current system at work:

* *Intel Core i7-4770* CPU @ 3.40GHz
* 32 GigaByte DDR3 RAM
* *Seagate Barracuda ST2000DM001* harddisk
  * SATA 3Gb/s
  * 4K Sectors
  * *ext4* file system

#### 1 GigaByte

Tool | Version | Command | Elapsed time |
------------ | ------------- | ------------ | ------------
*rsync* | 3.0.6 | `rsync -avv file1 file2` | 00:11 min
*rsync* | 3.0.6 | `rsync -avv --no-whole-file file1 file2` | 00:10 min
*ByteWeiser* | 1.0.0-rc1 | `byteweiser.py -i file1 -o file2` | 00:03 min

#### 10 GigaByte

Tool | Version | Command | Elapsed time |
------------ | ------------- | ------------ | ------------
*rsync* | 3.0.6 | `rsync -avv file1 file2` | 03:12 min
*rsync* | 3.0.6 | `rsync -avv --no-whole-file file1 file2` | 03:52 min
*ByteWeiser* | 1.0.0-rc1 | `byteweiser.py -i file1 -o file2` | 02:42 min

### Remote system

Due to the fact, that *ByteWeiser* only supports local paths for the input and output files, the remote directory must be mounted locally (for example by using *CIFS* or *sshfs*).

For this test, the target file is located on a *CIFS* mount in `/mnt/foo`.

#### 1 GigaByte

Tool | Version | Command | Elapsed time |
------------ | ------------- | ------------ | ------------
*rsync* | 3.0.6 | `rsync -avv file1 /mnt/foo/file2` | 00:09 min
*rsync* | 3.0.6 | `rsync -avv --no-whole-file file1 /mnt/foo/file2` | 00:21 min
*ByteWeiser* | 1.0.0-rc1 | `byteweiser.py -i file1 -o /mnt/foo/file2` | 00:09 min

#### 10 GigaByte

Tool | Version | Command | Elapsed time |
------------ | ------------- | ------------ | ------------
*rsync* | 3.0.6 | `rsync -avv file1 /mnt/foo/file2` | 01:38 min
*rsync* | 3.0.6 | `rsync -avv --no-whole-file file1 /mnt/foo/file2` | 04:12 min
*ByteWeiser* | 1.0.0-rc1 | `byteweiser.py -i file1 -o /mnt/foo/file2` | 01:34 min

[Top](#byteweiser-)

## Requirements

In order to run *ByteWeiser*, the *Python* 3.x framework must be installed on the system.

There is no official version for *Python* 2.x, but if you need that for whatever reason, you can try refactoring the syntax from *Python* 3.x to version 2.x using the *[3to2](https://pypi.python.org/pypi/3to2)* tool.

However, there is no guarantee that this works properly or at all.

[Top](#byteweiser-)

## Notice

The *ByteWeiser* project has been written on *Linux* and only been tested on that platform, yet.

Nevertheless, it should work on other platforms, but also without any guarantee.

[Top](#byteweiser-)

## Usage

Inside the `docs` sub-directory, there are plain text files containing the documentation for each component with further information and usage examples.

[Top](#byteweiser-)

## Useless facts

* Actually, the project should be called "BlockWeiser", because the binary data is being processed blockwise instead of bytewise. If you want it bytewise, just set the buffer size to `1`.
* The project name is derived from the German adjective "byteweise" ("bytewise").

[Top](#byteweiser-)
