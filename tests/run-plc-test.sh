#!/bin/bash
paste SRC_WITH_ENTITIES SRC_WITH_PLC TRG_WITH_PLC_AND_ALIGN |  awk -F$'\t' '{print $1" ||| "$2" ||| "$3}' | python ../scripts/convertTrgPlc2SrcEnt.py > OUT

diff  OUT TRG_WITH_ENTITIES.REF
