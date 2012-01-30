subdirs=
sets=bo_app1a  bgds_test servo_test embed_test
# heavy: bo_app1b


include ../boot_targets.mk



agent=BDSAgent_C1
# robot=r_rf_A
robot=r_cam_A
set=bo_app1a
bomt=bom -d sets/$(set) 
test-servonav:
	-rm -f sets/$(set)/logs/simulations/$(robot)/$(agent)/$(robot)-$(agent)-*-servo*
	$(bomt) servonav -a $(agent) -r $(robot) --num_episodes=1 --max_episode_len=600
	$(bomt) video -a  $(agent)_servo -r $(robot) -m boot_log2movie_servonav
