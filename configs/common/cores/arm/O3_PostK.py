# Copyright (c) 2012 The Regents of The University of Michigan
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met: redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer;
# redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution;
# neither the name of the copyright holders nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# Authors: Ron Dreslinski


from m5.objects import *

# ALU Instructions have a latency of 1
class O3_ARM_PostK_Int_A(FUDesc):
    opList = [ OpDesc(opClass='IntAlu', opLat=1),
               #OpDesc(opClass='IntAlu2', opLat=2),
               #OpDesc(opClass='SimdPredAlu', opLat=3),
               #OpDesc(opClass='SimdPredCmp', opLat=4),
               #OpDesc(opClass='IntShift', opLat=2, pipelined=True),
               #OpDesc(opClass='IntShiftLong', opLat=3, pipelined=True),
               #OpDesc(opClass='IntMFlow', opLat=1, pipelined=True),
               OpDesc(opClass='IntMult', opLat=5, pipelined=True),
               OpDesc(opClass='IprAccess', opLat=3, pipelined=True)]
    count = 1

class O3_ARM_PostK_Int_B(FUDesc):
    opList = [ OpDesc(opClass='IntAlu', opLat=1),
               #OpDesc(opClass='IntAlu2', opLat=2),
               #OpDesc(opClass='IntShift', opLat=2, pipelined=True),
               #OpDesc(opClass='IntShiftLong', opLat=3, pipelined=True),
               #OpDesc(opClass='IntMFlow', opLat=1, pipelined=True),
               #OpDesc(opClass='IntDiv4', opLat=26, pipelined=False),
               #OpDesc(opClass='IntDiv8', opLat=42, pipelined=False),
               OpDesc(opClass='IntDiv', opLat=12, pipelined=False),
               OpDesc(opClass='IprAccess', opLat=3, pipelined=True)]
    count = 1

class O3_ARM_PostK_Int_C(FUDesc):
    opList = [ OpDesc(opClass='IntAlu', opLat=1),
               OpDesc(opClass='IprAccess', opLat=3, pipelined=True) ]
    count = 1

# Floating point and SIMD instructions
class O3_ARM_PostK_FLA(FUDesc):
    opList = [ OpDesc(opClass='SimdAdd', opLat=4),
               #OpDesc(opClass='SimdAddAcc', opLat=8, cyclesPerOp=2),
               OpDesc(opClass='SimdAddAcc', opLat=8),
               OpDesc(opClass='SimdAlu', opLat=4),
               OpDesc(opClass='SimdCmp', opLat=4),
               #OpDesc(opClass='SimdDiv', opLat=178, pipelined=False),
               #OpDesc(opClass='SimdDivS', opLat=114, pipelined=False),
               OpDesc(opClass='SimdMisc', opLat=4),
               #OpDesc(opClass='SimdMisc2', opLat=8, cyclesPerOp=2),
               OpDesc(opClass='SimdCvt', opLat=9),
               OpDesc(opClass='SimdMult',opLat=9),
               OpDesc(opClass='SimdMultAcc',opLat=9),

               #OpDesc(opClass='SimdReduceAdd', opLat=42, cyclesPerOp=9),
               #OpDesc(opClass='SimdReduceAlu', opLat=34, cyclesPerOp=7),
               #OpDesc(opClass='SimdReduceCmp', opLat=34, cyclesPerOp=7),
               #OpDesc(opClass='SimdFloatReduceAdd', opLat=49, cyclesPerOp=7),
               #OpDesc(opClass='SimdFloatReduceCmp', opLat=34, cyclesPerOp=7),
               #OpDesc(opClass='SimdFloatReduceAddA',opLat=114,cyclesPerOp=15),

               OpDesc(opClass='SimdShift',opLat=4),
               OpDesc(opClass='SimdShiftAcc', opLat=4),
               OpDesc(opClass='SimdSqrt', opLat=4),
               OpDesc(opClass='SimdFloatAdd',opLat=9),
               OpDesc(opClass='SimdFloatAlu',opLat=4),
               OpDesc(opClass='SimdFloatCmp', opLat=4),
               OpDesc(opClass='SimdFloatCvt', opLat=9),
               OpDesc(opClass='SimdFloatMisc', opLat=4),
               OpDesc(opClass='SimdFloatMult', opLat=9),
               OpDesc(opClass='SimdFloatMultAcc',opLat=9),
               #OpDesc(opClass='SimdFloatSqrtS', opLat=98, pipelined=False),
               OpDesc(opClass='SimdFloatSqrt', opLat=154, pipelined=False),

               #OpDesc(opClass='SimdAluA', opLat=4),
               #OpDesc(opClass='SimdMiscA', opLat=6),
               #OpDesc(opClass='SimdMiscA2', opLat=10, cyclesPerOp=2),
               #OpDesc(opClass='SimdFloatA', opLat=9),
               #OpDesc(opClass='SimdIndexA', opLat=15, cyclesPerOp=2),
               #OpDesc(opClass='SimdGpr', opLat=25),
               #OpDesc(opClass='SimdFloatP', opLat=9), # FLOP=1
               #OpDesc(opClass='SimdFloatF', opLat=15, cyclesPerOp=2),# FLOP=1
               #OpDesc(opClass='SimdFIDX', opLat=15, cyclesPerOp=2), # FLOP=2
               #OpDesc(opClass='SimdFCMLA', opLat=16, cyclesPerOp=3),# FLOP=2

               OpDesc(opClass='FloatAdd', opLat=9),
               OpDesc(opClass='FloatCmp', opLat=4),
               OpDesc(opClass='FloatCvt', opLat=9),
               OpDesc(opClass='FloatMult', opLat=9),
               OpDesc(opClass='FloatMultAcc', opLat=9),
               OpDesc(opClass='FloatDiv', opLat=29, pipelined=False),
               #OpDesc(opClass='FloatDivd', opLat=43, pipelined=False),
               OpDesc(opClass='FloatMisc', opLat=4),
               OpDesc(opClass='FloatSqrt', opLat=29, pipelined=False),
               #OpDesc(opClass='FloatSqrtd', opLat=43, pipelined=False)
    ]
    count = 1

class O3_ARM_PostK_FLB(FUDesc):
    opList = [ OpDesc(opClass='SimdAdd', opLat=4),
               OpDesc(opClass='SimdAddAcc', opLat=8),
               OpDesc(opClass='SimdAlu', opLat=4),
               OpDesc(opClass='SimdMisc', opLat=4),
               #OpDesc(opClass='SimdMisc2', opLat=8, cyclesPerOp=2),
               OpDesc(opClass='SimdCvt', opLat=9),
               OpDesc(opClass='SimdMult',opLat=9),
               OpDesc(opClass='SimdMultAcc',opLat=9),
               OpDesc(opClass='SimdShift',opLat=4),
               OpDesc(opClass='SimdShiftAcc', opLat=4),
               OpDesc(opClass='SimdFloatAdd',opLat=9),
               OpDesc(opClass='SimdFloatAlu',opLat=4),
               OpDesc(opClass='SimdFloatCvt', opLat=9),
               OpDesc(opClass='SimdFloatMisc', opLat=4),
               OpDesc(opClass='SimdFloatMult', opLat=9),
               OpDesc(opClass='SimdFloatMultAcc',opLat=9),
               #OpDesc(opClass='SimdAluB', opLat=4),
               #OpDesc(opClass='SimdMiscB', opLat=6),
               #OpDesc(opClass='SimdFloatB', opLat=10, cyclesPerOp=2),
               #OpDesc(opClass='SimdIndexB', opLat=15, cyclesPerOp=3),

               OpDesc(opClass='FloatAdd', opLat=9),
               OpDesc(opClass='FloatCmp', opLat=4),
               OpDesc(opClass='FloatCvt', opLat=9),
               OpDesc(opClass='FloatMult', opLat=9),
               OpDesc(opClass='FloatMultAcc', opLat=9),
               OpDesc(opClass='FloatMisc', opLat=4)
    ]
    count = 1

# Load/Store Units
class O3_ARM_PostK_LoadStore(FUDesc):
    opList = [ OpDesc(opClass='MemRead',opLat=2),
               OpDesc(opClass='FloatMemRead',opLat=5),
               #OpDesc(opClass='SveMemRead', opLat=8),
               OpDesc(opClass='MemWrite',opLat=1),
               OpDesc(opClass='FloatMemWrite',opLat=1),
               #OpDesc(opClass='SveMemWrite', opLat=1)
    ]
    count = 1

# Functional Units for this CPU
class O3_ARM_PostK_FUP(FUPool):
    FUList = [O3_ARM_PostK_Int_A(), O3_ARM_PostK_Int_B(),
              O3_ARM_PostK_FLA(), O3_ARM_PostK_FLB(),
              O3_ARM_PostK_LoadStore(), O3_ARM_PostK_LoadStore()]

# Bi-Mode Branch Predictor
class O3_ARM_PostK_BP(BiModeBP):
    globalPredictorSize = 16384
    globalCtrBits = 2
    choicePredictorSize = 16384
    choiceCtrBits = 2
    BTBEntries = 4096
    BTBTagSize = 18
    RASSize = 8
    instShiftAmt = 2

class O3_ARM_PostK_3(DerivO3CPU):
    LQEntries = 40 # 80
    SQEntries = 24
    LSQDepCheckShift = 0
    LFSTSize = 2048
    SSITSize = 2048
    decodeToFetchDelay = 1
    renameToFetchDelay = 1
    iewToFetchDelay = 1
    commitToFetchDelay = 1
    renameToDecodeDelay = 1
    iewToDecodeDelay = 1
    commitToDecodeDelay = 1
    iewToRenameDelay = 1
    commitToRenameDelay = 1
    commitToIEWDelay = 1
    fetchWidth = 8
    #fetchBufferSize = 128 # 192 but should be 256/n
    fetchBufferSize = 64
    fetchToDecodeDelay = 2 # 1
    decodeWidth = 4
    decodeToRenameDelay = 2 # 1
    renameWidth = 4
    renameToIEWDelay = 2 # 1
    issueToExecuteDelay = 1
    dispatchWidth = 4
    issueWidth = 4
    wbWidth = 4
    fuPool = O3_ARM_PostK_FUP()
    iewToCommitDelay = 1
    renameToROBDelay = 1
    commitWidth = 4
    squashWidth = 40
    trapLatency = 13
    backComSize = 25 # 5
    forwardComSize = 20 # 4
    numPhysIntRegs = 96
    numPhysFloatRegs = 512
    numPhysVecRegs = 128
    #numPhysPredRegs = 48
    numIQEntries = 48 # 64
    numROBEntries = 128
    cacheLoadPorts=2
    cacheStorePorts=1
    #storePortUsageRatio = 2
    #splitUnalignedAccess = False
    switched_out = False
    #requestLineWidth=2048
    #commitStopOnBranch=True
    branchPred = O3_ARM_PostK_BP()

# Instruction Cache
class O3_ARM_PostK_ICache(Cache):
    tag_latency = 2
    data_latency = 3
    response_latency = 3
    mshrs = 8
    tgts_per_mshr = 8
    size = '64kB'
    assoc = 4
    is_read_only = True
    writeback_clean = False

# Data Cache
class O3_ARM_PostK_DCache(Cache):
    tag_latency = 2
    data_latency = 3
    response_latency = 3
    mshrs = 21
    tgts_per_mshr = 32
    size = '64kB'
    assoc = 4
    write_buffers = 21
    writeback_clean = False
    prefetch_on_access = True
    #downgrade_on_shared_req = False
    #forward_clean_evict = False
    #one_port = True
    #evict_latency = 3
    #writeback_latency = 4
    prefetcher = StridePrefetcher(degree=8, latency = 1)
    #prefetcher = KPrefetcher(l1degree=2, latency=1, queue_size=80,
    #                         l1maxprfofs=1536, on_inst=False,
    #                         l2maxprfofs=10240, writeprefetch=True)

# TLB Cache
# Use a cache as a L2 TLB
class O3_ARM_PostK_WalkCache(Cache):
    tag_latency = 4
    data_latency = 4
    response_latency = 4
    mshrs = 6
    tgts_per_mshr = 8
    size = '1kB'
    assoc = 4
    write_buffers = 16
    is_read_only = True
    writeback_clean = False

# L2 Cache
class O3_ARM_PostK_L2(Cache):
    tag_latency = 37
    data_latency = 37
    response_latency = 37
    mshrs = 64
    tgts_per_mshr = 12
    size = '8MB'
    assoc = 16
    write_buffers = 64
    #prefetch_on_access = True
    clusivity = 'mostly_incl'
    #downgrade_on_shared_req = False
    #forward_clean_evict = False
    # Simple stride prefetcher
    #prefetcher = KPrefetcher(degree=8, latency = 1)
    #tags = LRUhash()
    tags = BaseSetAssoc()
    replacement_policy = LRURP()
