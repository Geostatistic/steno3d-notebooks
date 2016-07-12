from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import glob
import os
import subprocess
import unittest


class TestNotebooks(unittest.TestCase):

    def test_notebooks(self):
        nbdir = os.path.abspath(__file__).split(os.path.sep)[:-2]
        nbs = glob.glob(os.path.sep.join(nbdir + ['*.ipynb']))
        testpyfile = os.path.sep.join(os.path.abspath(__file__).split(os.path.sep)[:-1] + ['nbtest.py'])
        for nb in nbs:
            print('Testing ' + nb.split(os.path.sep)[-1])
            in_code = False
            in_source = False
            in_comment = False
            with open(nb, 'r') as nbfile:
                with open(testpyfile, 'w') as testfile:
                    for nbline in nbfile:
                        nbline = nbline.strip()
                        if in_source and nbline == ']':
                            in_source = False
                            in_code = False
                            continue
                        if in_source and nbline.find('login') >= 0:
                            continue
                        if (in_source and not in_comment and
                                nbline.find('\\"\\"\\"') >= 0):
                            in_comment = True
                            continue
                        if (in_source and in_comment and
                                nbline.find('\\"\\"\\"') >= 0):
                            in_comment = False
                            continue
                        if in_source and not in_comment:
                            if len(nbline) > 0 and nbline[-1] == ',':
                                nbline = nbline[:-1]
                            if len(nbline) > 0 and nbline[0] == '"':
                                nbline = nbline[1:]
                            if len(nbline) > 0 and nbline[-1] == '"':
                                nbline = nbline[:-1]
                            if len(nbline) > 1 and nbline[-2:] == '\\n':
                                nbline = nbline[:-2]
                            if len(nbline) > 0 and nbline[0] != '%':
                                testfile.write(nbline + '\n')
                            continue
                        if in_code and nbline == '"source": [':
                            in_source = True
                            continue
                        if nbline == '"cell_type": "code",':
                            in_code = True
                assert subprocess.call(["python", testpyfile]) == 0
        os.remove(testpyfile)

if __name__ == '__main__':
    unittest.main()
