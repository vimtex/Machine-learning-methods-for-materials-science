import commands
import os
import json
import numpy as np
from pylada import vasp
from pylada.crystal import read

jobdir = '/scratch/jyan/ML_natoms_10'

allcifs =  commands.getoutput("ls %s/*.cif"%(jobdir)).split('\n')
print "number of cif files", len(allcifs)

for cif in allcifs:
    icsdno = cif[-10:-4]
    if not os.path.exists('%s/%s'%(jobdir, icsdno)):
        continue
    subdirs = os.listdir('%s/%s'%(jobdir, icsdno))
    E = []
    dirs = []
    for subdir in subdirs:
        a = vasp.Extract('%s/%s/%s'%(jobdir,icsdno, subdir))
        if a.success:
            E.append(a.total_energy.magnitude)
            dirs.append(subdir)
#            print "%6s/%20s"%(icsdno,subdir), a.total_energy
#    print icsdno, len(E)
#    if len(E) > 0: print icsdno, min(E)
    if len(E) > 1:
        minidx = np.argsort(E)[0]
        minE = min(E)
        minEdir = dirs[minidx]
        E.pop(minidx)
        dirs.pop(minidx)
        if minEdir == "non-magnetic":
            if np.mean(E) - minE < 1 and np.std(E) > 0.05: # print the ones with energy difference smaller than 1 eV
                atoms = read.poscar('%s/%s/%s/CONTCAR'%(jobdir, icsdno, "hs-ferro/relax_cellshape/0"))
                print "%s/%20s,%6.2f, %3d, %6.2f, %6.2f"%(icsdno, minEdir, minE, len(E)+1, np.mean(E), np.std(E)/len(atoms))
        else:
            nonmagidx = [j for j in range(len(dirs)) if dirs[j] == "non-magnetic"][0]
            nonmagE = E[nonmagidx]
            E.pop(nonmagidx)
            if np.std(E) > 0.05:
                atoms = read.poscar('%s/%s/%s/CONTCAR'%(jobdir, icsdno, "hs-ferro/relax_cellshape/0"))
                print "%s/%20s,%6.2f, %3d, non-magnetic, %6.2f, %6.2f, %6.2f"%(icsdno, minEdir, minE, len(E)+2, nonmagE, np.mean(E), np.std(E)/len(atoms))
