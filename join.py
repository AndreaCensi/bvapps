import sys, os, numpy as np
import subprocess

args = sys.argv[1:]
output = args[0]

if os.path.exists(output):
    os.unlink(output)

files = args[1:]

maxperbatch = 10
nbatches = int(np.ceil(len(files) * 1.0 / maxperbatch))

for b in range(nbatches):
    f1 = maxperbatch * b
    f2 = min(maxperbatch * (b + 1), len(files))
    fbatch = files[f1:f2]
    cmd = ['MP4Box']
    print(fbatch)
    for f in fbatch:
        cmd.append('-cat')
        cmd.append(f)
    cmd.append(output)
    print cmd
    subprocess.check_call(cmd)