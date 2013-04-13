config_raw_log := ../00-collect/config

logs:= out-boot_root/logs/experiments

bom := bom -d out-boot_root
bom_learn_log := $(bom) learn-log
# First phase: converting ROS logs to bootstrapping logs

rs2b := rs2b --contracts --config ./config $(config_raw_log) --dummy 

convert := $(rs2b) convert   
compmake_mode ?= --console

convert:
	$(convert) --jobs uA_b1_tw_hlhr_s4_nominal $(compmake_mode)

stats:
	$(bom_learn_log) -a stats1 -r uA_b1_tw_hlhr_s4
	$(bom_learn_log) -a stats1 -r uA_b1_tw_hlhr_s4 --once

# bds3:
# 	bom -d out-boot_root learn-log -a bdse1 -r uA_b1_tw_hlhr_s4 -p 5000



# convert1: 
# 	$(convert) --jobs uA_b1_tw_hlhr_nominal 

# convert2:
# 	$(convert) --jobs uA_b1_tw_cf_nominal 


# # Make variations using nuisances
# nuisance1:
# 	bom -d out-boot_root  nuislog -e uA_b1_tw_hlhr_sane -r uA_b1_tw_hlhr

# nuisance2:
# 	bom -d out-boot_root  nuislog -e uA_b1_tw_hlhr_sane_s4 -r uA_b1_tw_hlhr

list-logs:	
	$(bom) list-logs 

list-agents:	
	$(bom) list-agents

list-states:	
	$(bom) list-states -v

# simple_stats:
# 	$(bom_learn_log)  -a stats1 -r uA_b1_tw_hlhr_sane_s4
	
# 	$(bom_learn_log)  -a stats1 -r uA_b1_tw_hlhr_sane_s4 --once

# simple_stats_camera_clean:
# 	$(bom) clean-states -a stats2 -r uA_b1_tw_cf

# simple_stats_camera:
# 	bom -d out-boot_root learn-log -a stats2 -r uA_b1_tw_cf
# 	bom -d out-boot_root learn-log -a stats2 -r uA_b1_tw_cf --once


# # Learning dynamics

# learn_bds_hlh3:
# 	bom -d out-boot_root learn-log -a bdse1 -r uA_b1_tw_hlhr_sane_s4 -p 2000
# 	bom -d out-boot_root learn-log -a bdse1 -r uA_b1_tw_hlhr_sane_s4 --once



### With the santitized
