### Introduction

Pinefs is a user-space NFS server, written entirely in Python. It
provides three sample filesystems: pyfs, which provides a view of the
entire Python namespace as a file system, allowing you to change
variables in a running Python program by writing to the corresponding
file, or to use Unix tools like find; memfs, a fairly trivial in-memory
filesystem; and **tarfs**, which populates **memfs** from a tar file specified
by the `mount` command (requires tarfile, included in Python 2.3, or
[available separately]). The package also includes `rpcgen.py`, a Python
compiler from ONC RPC IDL to Python source. Pinefs requires Python 2.2
or later, and has been developed on Linux and lightly tested on Win 98.
You can download it [here][pinefs_tar].

### Running the Pinefs pyfs Serve

`srv.py` takes a single option, `-f`, which defaults to `py` for the
Python filesystem, but can be ‘mem’ for the memory filesystem or ‘tar’
for the tar filesystem. When the Python filesystem is specified, the
server runs a Python interactive loop.

The mount server runs on port **`15555`**, and the NFS server on **`12049`**. (Both
register with the portmapper.) On my Linux box, I use the following
command to mount the server for pyfs:

    mount -t nfs -o noac 127.0.0.1:/ /mnt/nfs

Once the Python filesystem is mounted, you can try:

    echo 1 > <mount point>/rpchelp/trace_rpc

to set the global trace\_rpc in module rpchelp to 1, which causes
information about rpc calls to be printed. You should see trace
information for the NFSPROC\_WRITE call. After you’ve looked around the
filesystem for a bit, you can turn off tracing by either:

    echo 0 > <mount point>/rpchelp/trace_rpc

or typing into the Python interaction loop:

    import rpchelp
    rpchelp.trace_rpc = 0

See [here][1] for more information on the mapping implemented by pyfs.
The mapping isn’t perfect, but works well enough to use emacs, or to
untar, configure, and compile, e.g., my [Dissociated Studio] package.
(Note: if you want a production-quality monitoring/debugging system, you
should probably use something built for that purpose (like manhole from
[Twisted]), since you could get more functionality, Pinefs doesn’t
address synchronization issues, and pyfs filehandles aren’t persistent
across restarts).)

### Running the Pinefs tarfs Server

This works much as above, except that instead of `127.0.0.1:/`,
substitute for `/` the pathname to a tar file. Now you can,
change directory to the mount point and browse, or, if it’s a software
package, e.g., `./configure; make`.

### Running rpcgen.py

rpcgen.py takes an IDL filename as a parameter, and writes Python code
implementing that IDL on stdout. The generated code imports rpchelp and
rpc from the Pinefs distribution, which thus must be present at runtime.
rpcgen.py requires Dave Beazley’s [PLY package], licensed under the
LGPL. Pinefs includes a precompiled rfc1094.py (generated from
rfc1094.idl), so you don’t need PLY in order to run Pinefs. See [here]
for more information on rpcgen.

### Notes

There are several other related programs, of which I was unaware, partly
because they weren’t in [PyPI] orthe [Vaults of Parnassus], partly
because they weren’t in the first ten pages or so of google results (web
and comp.lang.python.\* search) when I initially looked, and partly
because I started from the Python 2.1 rather than 2.2 Demo/rpc
directory. (Consider this a plea for people to use Vaults or post to
comp.lang.python.announce.) I still think Pinefs may be of interest,
because it exposes the Python namespace via NFS, and the included rpcgen
handles nested structs and unions.

Here are the others:

-   [Pynfs], a NFSv4 client, server, and test suite, and rpcgen
-   [Zodbex NFS], a NFSv\[23\] implementation with an in-memory
    filesystem
-   Wim Lewis’s [rpcgen.py]

Pinefs is licensed under a MIT/X style license, except for rpc.py,
which, since my version is based on the Python 2.1 distribution, has the
Python license.

The name “Pinefs” is both a pun on PyNFS, the obvious name for such a
program, and allows me to make the quasi-obligatory [allusion]: “It’s
pining for the files!”

If you have any questions, you can reach me at [Aaron Lav] or [my website]

  [available separately]: http://www.gustaebel.de/lars/tarfile/
  [pinefs_tar]: http://www.panix.com/~asl2/software/Pinefs/Pinefs-1.1.tar.gz
  [1]: ftp://ftp.gwdg.de/pub/linux/mulinux/python/pyfs.html
  [Dissociated Studio]: http://www.pobox.com/~asl2/music/dissoc_studio/
  [Twisted]: http://www.twistedmatrix.com/
  [PLY package]: http://systems.cs.uchicago.edu/ply/
  [here]: http://www2.research.att.com/sw/download/man/man1U/rpcgen.html
  [PyPI]: http://www.python.org/pypi
  [Vaults of Parnassus]: http://www.vex.net/parnassus
  [Pynfs]: http://www.cendio.se/~peter/pynfs/
  [Zodbex NFS]: http://cvs.sourceforge.net/cgi-bin/viewcvs.cgi/zodbex/zodbex/nfs/
  [rpcgen.py]: http://www.omnigroup.com/~wiml/soft/stale-index.html#python
  [allusion]: http://www.mtholyoke.edu/~ebarnes/python/dead-parrot.htm
  [Aaron Lav]: mailto:asl2@pobox.com
  [my website]: http://www.pobox.com/~asl2/