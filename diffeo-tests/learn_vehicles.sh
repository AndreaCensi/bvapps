#!/bin/bash
set -e
set -x
LOGS=/Users/andrea/BIGDATA/landroids-logs/vehicles-bags-canonical/


# logs obtained with
# roslaunch boot_olympics_launch diffeo_rf360_logs.launch

boot_learn -l $LOGS list-logs -v
# boot_learn -l $LOGS list-agents

# boot_learn -l $LOGS learn-log -r d_SE2_dd_v-rf360 -a diffeo_agent_2d_veh -p 300 #--reset

# boot_learn -l $LOGS learn-log -r d_SE2_dd_v-rf360 -a diffeo_agent_2d_veh -p 300 #--reset

boot_learn -l $LOGS learn-log -r d_SE2_dd_v2-rf360 -a diffeo_agent_2d_veh2 -p 100