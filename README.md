# *ByteWeiser* <img src="byteweiser.png" alt="ByteWeiser logo" height="128px" width="128px" align="right"/>

**Table of contents**
*   [Definition](#definition)
*   [Details](#details)
*   [Performance](#performance)
*   [Requirements](#requirements)
*   [Documentation](#documentation)
*   [Contact](#contact)
*   [Useless facts](#useless-facts)

----

## Definition

The *ByteWeiser* project is a simple file synchronization tool that compares two files blockwise and only replaces the different bytes to reduce write operations on the hard disk.

[Top](#byteweiser)

## Details

Initially developed to accelerate the backup of virtual machine images, *ByteWeiser* compares the binary data of two files, by running through them block by block. If the current block of the output file is different from that of the input file, the block of the output file will be overwritten with the one from the input file.

With its operating principle it reduces the write operations on the hard disk.

You could also use *rsync* with delta compression for that. However, *ByteWeiser* seems to be faster in some cases. Both tools have a completely different functional principle, where *ByteWeiser* is the one that "mindlessly" (simply) processes the data instead of using algorithms and checksums.

## Performance

The performance of *ByteWeiser* has been tested and compared with the results of *rsync*.

Details can be found [here](../../wiki/Performance) inside the [wiki](../../wiki).

[Top](#byteweiser)

## Requirements

### Runtime environment

In order to run *ByteWeiser*, the *Python* 3.x framework (version 3.2 or higher is recommended) must be installed on the system.

There is no official version for *Python* 2.x, but if you need that for whatever reason, you can try refactoring the syntax from *Python* 3.x to version 2.x using the *[3to2](https://pypi.python.org/pypi/3to2)* tool.

However, there is no guarantee that this works properly or at all.

### Operating system

The *ByteWeiser* project has been tested on *Linux* as well as *Windows*.

Nevertheless, it should work on other platforms, but also without any guarantee.

[Top](#byteweiser)

## Documentation

Inside the `docs` sub-directory, there are plain text files containing the documentation for each component with further information and usage examples.

[Top](#byteweiser)

## Contact

Any suggestions, questions, bugs to report or feedback to give?

You can contact me by sending an email to [dev@urbanware.org](mailto:dev@urbanware.org) or by opening a *GitHub* issue (which I would prefer if you have a *GitHub* account).

Further information can be found inside the `contact.txt` file.

[Top](#byteweiser)

## Useless facts

*   Actually, the project should be called "BlockWeiser", because the binary data is being processed blockwise instead of bytewise. If you wanted it bytewise, you would have to set the buffer size to `1`.

*   The project name is derived from the German adjective "byteweise" ("bytewise").

[Top](#byteweiser)
