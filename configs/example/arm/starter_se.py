# Copyright (c) 2016-2017, 2022-2023 Arm Limited
# All rights reserved.
#
# The license below extends only to copyright in the software and shall
# not be construed as granting a license to any other intellectual
# property including but not limited to intellectual property relating
# to a hardware implementation of the functionality of the software
# licensed hereunder.  You may use the software subject to the license
# terms below provided that you ensure that this notice is replicated
# unmodified and in its entirety in all distributions of the software,
# modified or unmodified, in source code or in binary form.
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

"""This script is the syscall emulation example script from the ARM
Research Starter Kit on System Modeling. More information can be found
at: http://www.arm.com/ResearchEnablement/SystemModeling
"""

import argparse
import os
import shlex

import m5
from m5.objects import *
from m5.util import addToPath

m5.util.addToPath('../..')

from common import ObjectList
from common import MemConfig
from common.cores.arm import HPI
from common.cores.arm.O3_ARM_v7a import *
import common.cores.arm.O3_PostK as PostK
import common.cores.arm.ex5_big as ex5_big
import common.cores.arm.ex5_LITTLE as ex5_LITTLE

import devices
from cfg_generater import generate_configs



# Pre-defined CPU configurations. Each tuple must be ordered as : (cpu_class,
# l1_icache_class, l1_dcache_class, l2_Cache_class). Any of
# the cache class may be 'None' if the particular cache is not present.
cpu_types = {
    "atomic" : ( AtomicSimpleCPU, None, None, None),
    "minor" : (MinorCPU,
               devices.L1I, devices.L1D,
               devices.L2),
    "hpi" : ( HPI.HPI,
              HPI.HPI_ICache, HPI.HPI_DCache,
              HPI.HPI_L2),
    "ac" : (AtomicSimpleCPU,
            devices.L1I, devices.L1D, devices.L2),
    "o3" : (O3CPU,
            devices.L1I, devices.L1D, devices.L2),
    "timing" : (ObjectList.cpu_list.get("O3_ARM_v7a_3"),
            devices.L1I, devices.L1D, devices.L2),
    "ex5" : (ObjectList.cpu_list.get("ex5_big"),
            ex5_big.L1I, ex5_big.L1D, ex5_big.L2),
    "ex5l" : (ObjectList.cpu_list.get("ex5_LITTLE"),
            ex5_LITTLE.L1I, ex5_LITTLE.L1D, ex5_LITTLE.L2),
    "pk" : (ObjectList.cpu_list.get("O3_ARM_PostK_3"),
            PostK.O3_ARM_PostK_ICache, PostK.O3_ARM_PostK_DCache,
            PostK.O3_ARM_PostK_L2)
}


class SimpleSeSystem(System):
    '''
    Example system class for syscall emulation mode
    '''

    # Use a fixed cache line size of 64 bytes
    cache_line_size = 64

    def __init__(self, args, **kwargs):
        super(SimpleSeSystem, self).__init__(**kwargs)

        # Setup book keeping to be able to use CpuClusters from the
        # devices module.
        self._clusters = []
        self._num_cpus = 0

        # Create a voltage and clock domain for system components
        self.voltage_domain = VoltageDomain(voltage="3.3V")
        self.clk_domain = SrcClockDomain(clock="1GHz",
                                         voltage_domain=self.voltage_domain)

        # Create the off-chip memory bus.
        self.membus = SystemXBar()

        # Wire up the system port that gem5 uses to load the kernel
        # and to perform debug accesses.
        self.system_port = self.membus.cpu_side_ports


        # Add CPUs to the system. A cluster of CPUs typically have
        # private L1 caches and a shared L2 cache.
        self.cpu_cluster = devices.CpuCluster(self,
                                              args.num_cores,
                                              args.cpu_freq, "1.2V",
                                              *cpu_types[args.cpu])

        # Create a cache hierarchy (unless we are simulating a
        # functional CPU in atomic memory mode) for the CPU cluster
        # and connect it to the shared memory bus.
        if self.cpu_cluster.memoryMode() == "timing":
            self.cpu_cluster.addL1()
            self.cpu_cluster.addL2(self.cpu_cluster.clk_domain)
        elif args.cpu == "ac":
            self.cpu_cluster.addL1()
            self.cpu_cluster.addL2(self.cpu_cluster.clk_domain)
            for i in range(args.num_cores):
                self.cpu_cluster.cpus[i].branchPred = O3_ARM_v7a_BP()
        self.cpu_cluster.connectMemSide(self.membus)

        if args.maxinsts:
            for i in range(args.num_cores):
                self.cpu_cluster.cpus[i].max_insts_all_threads = \
                    args.maxinsts

        if args.simpoint_profile:
            for i in range(args.num_cores):
                self.cpu_cluster.cpus[i].addSimPointProbe(
                    args.simpoint_interval)

        # Tell gem5 about the memory mode used by the CPUs we are
        # simulating.
        self.mem_mode = self.cpu_cluster.memoryMode()

    def numCpuClusters(self):
        return len(self._clusters)

    def addCpuCluster(self, cpu_cluster, num_cpus):
        assert cpu_cluster not in self._clusters
        assert num_cpus > 0
        self._clusters.append(cpu_cluster)
        self._num_cpus += num_cpus

    def numCpus(self):
        return self._num_cpus

def get_processes(cmd):
    """Interprets commands to run and returns a list of processes"""

    cwd = os.getcwd()
    multiprocesses = []
    for idx, c in enumerate(cmd):
        argv = shlex.split(c)

        process = Process(pid=100 + idx, cwd=cwd, cmd=argv, executable=argv[0])
        process.gid = os.getgid()

        print("info: %d. command and arguments: %s" % (idx + 1, process.cmd))
        multiprocesses.append(process)

    return multiprocesses


def create(args):
    ''' Create and configure the system object. '''

    if args.l1d_size != "":
        devices.L1D.size = args.l1d_size
    if args.l1i_size != "":
        devices.L1I.size = args.l1i_size
    if args.l2_size != "":
        if args.l2_size == "0":
            cpu_types[args.cpu] = (cpu_types[args.cpu][0],
                                   cpu_types[args.cpu][1],
                                   cpu_types[args.cpu][2], None)
        else:
            devices.L2.size = args.l2_size
    if args.random > 0:
        args, branchPred = generate_configs(args, args.random - 1)

    system = SimpleSeSystem(args)

    if args.random > 0:
        for i in range(args.num_cores):
            system.cpu_cluster.cpus[i].branchPred = branchPred()

    # Tell components about the expected physical memory ranges. This
    # is, for example, used by the MemConfig helper to determine where
    # to map DRAMs in the physical address space.
    system.mem_ranges = [AddrRange(start=0, size=args.mem_size)]

    # Configure the off-chip memory system.
    MemConfig.config_mem(args, system)

    # Wire up the system's memory system
    system.connect()

    # Parse the command line and get a list of Processes instances
    # that we can pass to gem5.
    processes = get_processes(args.commands_to_run)
    if len(processes) != args.num_cores:
        print(
            "Error: Cannot map %d command(s) onto %d CPU(s)"
            % (len(processes), args.num_cores)
        )
        sys.exit(1)

    system.workload = SEWorkload.init_compatible(processes[0].executable)

    # Assign one workload to each CPU
    for cpu, workload in zip(system.cpu_cluster.cpus, processes):
        cpu.workload = workload

    return system


def main():
    parser = argparse.ArgumentParser(epilog=__doc__)

    parser.add_argument("commands_to_run", metavar="command(s)", nargs='*',
                        help="Command(s) to run")
    parser.add_argument("--cpu", type=str, choices=list(cpu_types.keys()),
                        default="atomic",
                        help="CPU model to use")
    parser.add_argument("--cpu-freq", type=str, default="2GHz")
    parser.add_argument("--num-cores", type=int, default=1,
                        help="Number of CPU cores")
    parser.add_argument("--mem-type", default="DDR4_2400_16x4",
                        choices=ObjectList.mem_list.get_names(),
                        help = "type of memory to use")
    parser.add_argument("--mem-channels", type=int, default=2,
                        help = "number of memory channels")
    parser.add_argument("--mem-ranks", type=int, default=None,
                        help = "number of memory ranks per channel")
    parser.add_argument("--mem-size", action="store", type=str,
                        default="2GB",
                        help="Specify the physical memory size")
    parser.add_argument("--l1d_size", type=str, default="")
    parser.add_argument("--l1i_size", type=str, default="")
    parser.add_argument("--l2_size", type=str, default="")
    parser.add_argument("--maxinsts", type=int, default=0, help="Total " \
                        "number of instructions to simulate")
    parser.add_argument("--simpoint-profile", action="store_true",
                        help="Enable basic block profiling for SimPoints")
    parser.add_argument("--simpoint-interval", type=int, default=10000000,
                        help="SimPoint interval in num of instructions")
    parser.add_argument("--checkpoint-at-end", action="store_true",
                        help="take a checkpoint at end of run")
    parser.add_argument("--restore", type=str, default=None)
    parser.add_argument("--random", "-r", type=int, default=0,
                        help="Random number for configurations")

    args = parser.parse_args()

    # Create a single root node for gem5's object hierarchy. There can
    # only exist one root node in the simulator at any given
    # time. Tell gem5 that we want to use syscall emulation mode
    # instead of full system mode.
    root = Root(full_system=False)

    # Populate the root node with a system. A system corresponds to a
    # single node with shared memory.
    root.system = create(args)

    # Instantiate the C++ object hierarchy. After this point,
    # SimObjects can't be instantiated anymore.
    if args.restore is not None:
        m5.instantiate(args.restore)
    else:
        m5.instantiate()

    # Start the simulator. This gives control to the C++ world and
    # starts the simulator. The returned event tells the simulation
    # script why the simulator exited.
    event = m5.simulate()

    if args.checkpoint_at_end:
        m5.checkpoint(os.path.join(m5.options.outdir, "cpt.%d" % m5.curTick()))

    # Print the reason for the simulation exit. Some exit codes are
    # requests for service (e.g., checkpoints) from the simulation
    # script. We'll just ignore them here and exit.
    print(f"{event.getCause()} ({event.getCode()}) @ {m5.curTick()}")


if __name__ == "__m5_main__":
    main()
