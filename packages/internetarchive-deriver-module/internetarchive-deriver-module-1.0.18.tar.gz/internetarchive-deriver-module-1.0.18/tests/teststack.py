import derivermodule
import sys


path = sys.argv[1]
info = {'archive_type': sys.argv[2]}

for name, obj in derivermodule.imagestack.iterate_imagestack(path, info):
    print(name, obj)
