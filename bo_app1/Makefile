subdirs=
sets=bo_app1a bo_app1_stats 
sets+=bo_app1b
# bgds_test servo_test embed_test 

include ../boot_targets.mk



agent=BDSAgent_C1
robot=r_rf_A
# robot=r_cam_A
set=bo_app1a
bomt=bom -d sets/$(set) 
test-servonav:
	-rm -f sets/$(set)/logs/simulations/$(robot)/$(agent)/$(robot)-$(agent)-*-servo*
	$(bomt) servonav -a $(agent) -r $(robot) --num_episodes=1 --max_episode_len=600
	$(bomt) video -a  $(agent)_servo -r $(robot) -m boot_log2movie_servonav
