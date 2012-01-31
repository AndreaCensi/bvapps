subdirs=
sets=bo_hidden1_light bo_hidden1

include ../boot_targets.mk

bomt=bom -d sets/bo_hidden1 
agent=BDSAgent_C1
robot=r_turret
set=bo_hidden1
test-servonav:
	-rm -f sets/$(set)/logs/simulations/$(robot)/$(agent)/$(robot)-$(agent)-*-servo*
	$(bomt) servonav -a $(agent) -r $(robot) --num_episodes=1 --max_episode_len=4
	$(bomt) video -a  $(agent)_C1_servo -r $(robot) -m boot_log2movie_servonav