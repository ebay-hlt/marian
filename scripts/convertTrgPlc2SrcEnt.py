#!/usr/bin/python 

# Converts the target placeholders to source entities via the source placeholders given the alignments between source and target
# paste SRC_WITH_ENTITIES SRC_WITH_PLC TRG_WITH_PLC_AND_ALIGN | awk -F$'\t' '{print $1" ||| "$2" ||| "$3}' | python convertTrgPlc2SrcEnt.py
# SRC_WITH_ENTITIES: Source file contain the entities i.e. without placeholders
# SRC_WITH_PLC: Source file used as input for translation
# TRG_WITH_PLC_AND_ALIGN: Target translation with alignments separated by three pipe delimiter ("|||")

# Copyright -- pramathur@ebay.com


import sys

BPE=1

for line in sys.stdin:
# chop the last char
    line = line[:-1]
# split line into three parts
    L = line.split("|||")
    raw_src = L[0].split()
    src = L[1]
    trg = L[2].split()
    align = L[3].split() 

# get mapping from BPE to noBPE
    map_bpe = {}
    if BPE==1:
        src_s = src.split()
        index1 = [n for n, s in enumerate(src_s)  if s.startswith('$')]
        noBPE = src.replace("@@ ", "").replace("@@","").split()
        index2 = [n for n, s in enumerate(noBPE) if s.startswith('$')]
        map_bpe = dict(zip(index1, index2))
        
# get the trg indices which are placeholders
    indx = [n for n, t in enumerate(trg) if t.startswith('$')]
# replace the target placeholders with source words
    for al in align:
        ta, sa = al.split("-")
        if int(ta) in indx:
            if BPE==1 and int(sa) in map_bpe.keys():
                trg[int(ta)] = raw_src[map_bpe[int(sa)]]
            elif BPE!=1:
                trg[int(ta)] = raw_src[int(sa)]

    print " ".join(trg)
        
