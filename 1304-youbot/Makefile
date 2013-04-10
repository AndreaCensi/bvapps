logs=out-boot_root/logs/experiments
bom="bom -d out-boot_root"

# First phase: converting ROS logs to bootstrapping logs

convert1: 
	rs2b-convert --jobs uA_b1_tw_hlhr_nominal -c parmake

convert2:
	rs2b-convert --jobs uA_b1_tw_cf_nominal  -c parmake


# Make variations using nuisances
nuisance1:
	bom -d out-boot_root  nuislog -e uA_b1_tw_hlhr_sane -r uA_b1_tw_hlhr

nuisance2:
	bom -d out-boot_root  nuislog -e uA_b1_tw_hlhr_sane_s4 -r uA_b1_tw_hlhr



list_logs:	
	bom -d out-boot_root list-logs 

list_agents:	
	bom -d out-boot_root list-agents

list_states:	
	bom -d out-boot_root list-states -v

simple_stats:
	bom -d out-boot_root learn-log -a stats1 -r uA_b1_tw_hlhr_sane_s4
	bom -d out-boot_root learn-log -a stats1 -r uA_b1_tw_hlhr_sane_s4 --once

simple_stats_camera_clean:
	bom -d out-boot_root clean-states -a stats2 -r uA_b1_tw_cf

simple_stats_camera:
	bom -d out-boot_root learn-log -a stats2 -r uA_b1_tw_cf
	bom -d out-boot_root learn-log -a stats2 -r uA_b1_tw_cf --once


# Learning dynamics

learn_bds_hlh3:
	bom -d out-boot_root learn-log -a bdse1 -r uA_b1_tw_hlhr_sane_s4 -p 2000
	bom -d out-boot_root learn-log -a bdse1 -r uA_b1_tw_hlhr_sane_s4 --once




### With the santitized

convert3:
	rs2b-convert --jobs uA_b1_tw_hlhr_s4_nominal --console
stats3:
	bom -d out-boot_root learn-log -a stats1 -r uA_b1_tw_hlhr_s4
	bom -d out-boot_root learn-log -a stats1 -r uA_b1_tw_hlhr_s4 --once
bds3:
	bom -d out-boot_root learn-log -a bdse1 -r uA_b1_tw_hlhr_s4 -p 5000


