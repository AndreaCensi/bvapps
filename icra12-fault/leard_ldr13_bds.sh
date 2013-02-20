#!/bin/bash
set -e
set -x
#boot_learn -l $LOGSM/logs-normalized_sensel_values_all_sensels  learn-log -a diffeo_agent_2d_ldr13 -r LDR13 -p 300 #--reset

cmd="boot_learn -l $LOGSM/logs-normalized_sensel_values_all_sensels"

$cmd learn-log -a bds_agent_dev -r LDR13 -p 1000  --interval_save 800