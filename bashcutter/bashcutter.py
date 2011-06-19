#!/usr/bin/env python

import posixpath, ntpath, macpath
import shutil
import os
import sys
import pwd

class BashCutter:
    def __init__(self, buffer_dir):
        self.buffer_dir = buffer_dir
        if not os.path.exists(self.buffer_dir):
            os.makedirs(self.buffer_dir, 0700)
        if not os.path.isdir(self.buffer_dir):
            print('Error: buffer is not a directory')
            exit(-6)
        #print str(self._get_buffer_list())
        #print str(self._lookup_buff_path(0))

    def copy(self, path):
        if not os.path.exists(path):
            print 'Error: source does not exist'
            exit(-8)
        if os.path.exists(os.path.join(self.buffer_dir, path)):
            print 'Error accord, buffername might already be in use.'
            exit(-7)
        shutil.copy2(path, self.buffer_dir)

    def cut(self, path):
        if not os.path.exists(path):
            print 'Error: source does not exist'
            exit(-8)
        try:
            shutil.move(path, self.buffer_dir)
        except shutil.Error, e:
            print 'Error accord, buffername might already be in use.'
            exit(-7)

    def paste_buffer(self, buffer_nr, to_dir):
        path = self._lookup_buff_path(buffer_nr)
        shutil.copy2(path, to_dir)

    def move_buffer(self, buffer_nr, to_dir):
        path = self._lookup_buff_path(buffer_nr)
        shutil.move(path, to_dir)

    def remove_buffer(self, buffer_nr):
        path = self._lookup_buff_path(buffer_nr)
        os.remove(path)

    def _get_buffer_list(self):
        buffer_list = []
        buffer_list = os.listdir(self.buffer_dir)
        #for root, dirs, files in os.walk(self.buffer_dir):
            #for name in files:       
                #buffer_list += [name]
        return buffer_list

    def _lookup_buff_path(self, buffer_nr):
        list = self._get_buffer_list()
        if len(list) <= int(buffer_nr):
            print 'Error: Buffer unknown'
            exit(-5)
        filename = list[int(buffer_nr)]
        path = os.path.join(self.buffer_dir, filename)
        return path

    def list_buffer(self):
        buffers = self._get_buffer_list()
        i = 0
        length = len(buffers)
        while i < length:
            print '%3d)  "%s"' %(i, buffers[i])
            i+=1

def run():
    buffer_dir = '/tmp/bashcopy/%s' %(pwd.getpwuid( os.getuid() )[ 0 ])
    bc = BashCutter(buffer_dir)

    basename = ''
    origname = sys.argv[0]

    for pathmodule in [posixpath, ntpath, macpath]:
        temp = pathmodule.split(origname)[1]
        if temp != origname:
            basename = temp

    if len(sys.argv) < 2:
        if basename == 'cb' or basename == 'xb':
            print 'Error: source path missing!'
            exit(-1)
        elif basename == 'mb' or basename == 'pb' or basename == 'rmb':
            print 'Error: buffer number missing!'
            exit(-3)

    if basename == 'lb':
        bc.list_buffer()
        exit()
    elif basename == 'cb':
        cp_from = sys.argv[1]
        bc.copy(cp_from)
    elif basename == 'xb':
        cp_from = sys.argv[1]
        bc.cut(cp_from)
    elif basename == 'mb':
        buffer_nr = sys.argv[1]
        to_dir = sys.argv[2] if len(sys.argv) >= 3 else './'
        bc.move_buffer(buffer_nr, to_dir)
    elif basename == 'pb':
        buffer_nr = sys.argv[1]
        to_dir = sys.argv[2] if len(sys.argv) >= 3 else './'
        bc.paste_buffer(buffer_nr, to_dir)
    elif basename == 'rmb':
        buffer_nr = sys.argv[1]
        bc.remove_buffer(buffer_nr)
    else:
        print '%s: unknown command' %(basename)

