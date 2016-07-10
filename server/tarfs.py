#!/usr/bin/env python

"""Tar filesystem, relying on Python's tarfile.  In future, will
allow creating new memory-backed files within the filesystem."""

# This file should be available from
# http://www.pobox.com/~asl2/software/Pinefs
# and is licensed under the X Consortium license:
# Copyright (c) 2003, Aaron S. Lav, asl2@pobox.com
# All rights reserved. 

# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, and/or sell copies of the Software, and to permit persons
# to whom the Software is furnished to do so, provided that the above
# copyright notice(s) and this permission notice appear in all copies of
# the Software and that both the above copyright notice(s) and this
# permission notice appear in supporting documentation. 

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT
# OF THIRD PARTY RIGHTS. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
# HOLDERS INCLUDED IN THIS NOTICE BE LIABLE FOR ANY CLAIM, OR ANY SPECIAL
# INDIRECT OR CONSEQUENTIAL DAMAGES, OR ANY DAMAGES WHATSOEVER RESULTING
# FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
# NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION
# WITH THE USE OR PERFORMANCE OF THIS SOFTWARE. 

# Except as contained in this notice, the name of a copyright holder
# shall not be used in advertising or otherwise to promote the sale, use
# or other dealings in this Software without prior written authorization
# of the copyright holder. 

import rfc1094
import fsbase
import array
import tarfile

import memfs
import io
import os.path
import os


class FileObj(memfs.FileObj):
    pass

def make_tarfile(path):
    # If we're given a tarfile, open it
    # Otherwise treat it as a directory and make an in-memory file
    extension = os.path.splitext(path)[1]
    if extension == '.tar':
        try:
            tar_hdl = tarfile.open (path , 'r')
            return tar_hdl
        except (tarfile.TarError, IOError), exn:
            print "Error", exn, "opening", path
            return None
    else:
        file_like_object = io.BytesIO()
        tar = tarfile.open(fileobj=file_like_object, mode='w')
        for name in os.listdir(path):
            tar.add(os.path.join(path, name), arcname=name)
        tar.close()
        file_like_object.seek(0)
        tar = tarfile.open(fileobj=file_like_object, mode='r')
            
        return tar


class FileSystem (memfs.FileSystem):
    def __init__ (self, fh_ctr = fsbase.Ctr ()):
        self._fh_ctr = fh_ctr
        self._fils = {}
        
    def mount (self, path):
        tar_hdl = make_tarfile(path)
        new_root, root_fil = self.create_fil (None, '', type = rfc1094.NFDIR,
                                              size = 4,dir = {})
        members = tar_hdl.getmembers ()
        for member in members:
            nm = member.name.split ('/')
            # hack?
            # It seems as though tarfs has changed how it represents file names
            # since this was first written
            if member.isdir(): nm.append('')
            dirpath = nm[:-1]
            kw = {}
            for attrib in ['mode', 'uid', 'gid']:
                kw[attrib] = getattr (member, attrib)
            kw ['mtime'] = fsbase.mk_time (member.mtime, 0)
            if nm [-1] == '': # ends in '/', it's a directory
                self.make_dirs (new_root, dirpath)
            else:
                base_dir = self.find_dir (new_root, dirpath)
                # better to do this lazily
                if member.issym ():
                    self.create_fil (base_dir, nm[-1], type = rfc1094.NFLNK,
                                     data = member.linkname, **kw)
                elif member.isfile ():
                    data = tar_hdl.extractfile (member).read ()
                    self.create_fil (base_dir, nm[-1], type = rfc1094.NFREG,
                                     data = data, **kw)
                elif member.islnk ():
                    from_path = member.linkname.split ('/')
                    from_dir = self.find_dir (new_root, from_path[:-1])
                    from_dirfil = self.get_fil (from_dir)
                    from_fh = from_dirfil.get_dir ()[from_path[-1]]
                    base_fil = self.get_fil (base_dir)
                    base_fil.mk_link (nm[-1], from_fh)
                else:
                    print "unhandled type", member, member.type
                    # could be character device, block device, fifo
        tar_hdl.close ()
        return new_root
    def find_dir (self, root_fh, dirpath):
        cur_fh = root_fh
        for component in dirpath:
            cur = self.get_fil (cur_fh)
            next_fh = cur.get_dir () [component]
            cur_fh = next_fh
        return cur_fh
    def make_dirs (self, root_fh, dirpath):
        base = self.find_dir (root_fh, dirpath[:-1])
        self.create_fil (base, dirpath[-1], type = rfc1094.NFDIR, size=1)
        


                


