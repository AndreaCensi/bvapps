
logs=/mnt/bootrepo1/BIGDATA/201302-ldr/logs
bom="bom -d . -l $(logs)"

list_logs:	
	bom -d . -l $(logs) list-logs

list_agents:	
	bom -d . -l $(logs) list-agents

simple_stats:
	bom -d . -l $(logs) learn-log -a stats1 -r LDR13
	bom -d . -l $(logs) learn-log -a stats1 -r LDR13 --once

simple_stats2:
	bom -d . -l $(logs) learn-log -a stats2 -r Ypc2LDR13
	bom -d . -l $(logs) learn-log -a stats2 -r Ypc2LDR13 --once

nuislog:
	bom -d . -l $(logs) nuislog -e Ypc2LDR13 -r LDR13

testnuis:
	bom -d . -l $(logs) learn-log -a stats1 -r Ypc2LDR13

testlearndiff:
	bom -d . -l $(logs) learn-log -r Ypc2LDR13 -a icra12-diffeo-ldr13

convert_to_dp_log:
	# Here we convert the boot logs to the DP rosbag logs
	pg bootol2dp bag=logs/Ypc2LDR13.processed.bag logdir=logs/ delta=1

learn:
	dp plearn -s Ypc2LDR13 -l n35s -c make

nuislog128:
	bom -d . -l $(logs) nuislog -e Y128LDR13 -r LDR13

nuislog64:
	bom -d . -l $(logs) nuislog -e Y64LDR13 -r LDR13


make_processed:
	# Here we convert the boot logs to the DP rosbag logs
	pg bootol2dp logdir=logs/ id_robot=Y128LDR13 delta=1   bag=logs/T10Y128LDR13.processed.bag &
	pg bootol2dp logdir=logs/ id_robot=Y128LDR13 delta=0.5 bag=logs/T05Y128LDR13.processed.bag &
	pg bootol2dp logdir=logs/ id_robot=Y128LDR13 delta=0.3 bag=logs/T03Y128LDR13.processed.bag &
	pg bootol2dp logdir=logs/  id_robot=Y64LDR13 delta=1   bag=logs/T10Y64LDR13.processed.bag &
	pg bootol2dp logdir=logs/  id_robot=Y64LDR13 delta=0.5 bag=logs/T05Y64LDR13.processed.bag &
	pg bootol2dp logdir=logs/  id_robot=Y64LDR13 delta=0.3 bag=logs/T03Y64LDR13.processed.bag &
	

subdirs=
sets=

include ../boot_targets.mk 

 
clean-report: $(addprefix clean-report-, $(sets))

clean-report-%:
	bom batch $* --command='clean report-*'
