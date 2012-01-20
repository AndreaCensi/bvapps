#!/usr/bin/env python
from bootstrapping_olympics import logger
from bootstrapping_olympics.programs.manager.experiments_utils import (
    experiment_explore_learn_main)
from bootstrapping_olympics.utils import wrap_script_entry_point
from os.path import dirname
from vehicles import VehiclesConfig
import os

cwd = os.path.dirname(os.path.realpath(__file__))
proj_root = dirname(dirname(cwd))


robots = ['r_turret', 'r_turret_C2']
agents = ['BDSAgent_C1', 'EstStats']
explorer = 'expswitch_t1'

def go(args):
    # load vehicles config
    VehiclesConfig.load()
    VehiclesConfig.load(proj_root)

    # FIXME make this robust
    experiment_explore_learn_main(proj_root,
                                  explorer, agents, robots, args)

def main():
    wrap_script_entry_point(go, logger)

if __name__ == '__main__': 
    main()

