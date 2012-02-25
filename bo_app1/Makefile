subdirs=
sets=bo_app1a bo_app1_stats 
sets+=bo_app1b
sets+=bo_app1c
sets+=bo_app1d
# bgds_test servo_test embed_test 

include ../boot_targets.mk 

robots=r_cam_A r_rf_A r_fs_A_nn
robots+=r_fs_A r_fs_B_f r_fs_A_nn r_fs_B_f_nn r_fs_A_mn r_fs_B_f_mn
robots+=rsim-d_SE2_dd_v-cam360 rsim-d_SE2_dd_v-rf360 rsim-d_SE2_dd_v-fs_05_rand144 rsim-d_SE2_dd_v-fs_05_12x12 rsim-d_SE2_car_v-cam360 rsim-d_SE2_car_v-rf360 rsim-d_SE2_car_v-fs_05_rand144 rsim-d_SE2_car_v-fs_05_12x12

extra-videos: $(foreach robot, $(robots), videos/join-exz1no-$(robot).mp4)  $(foreach robot, $(robots), videos/join-exz1sb-$(robot).mp4) 
	
extra-html: videos/videos-exz1no.html videos/videos-exz1sb.html

join=../join.py

videos/join-exz1no-%.mp4: extra-videos
	mkdir -p videos
	$(join) $@ $(shell find sets/ -type f -name '*$**exz1no.mp4')

videos/join-exz1sb-%.mp4: extra-videos
	mkdir -p videos
	$(join) $@ $(shell find sets/ -type f -name '*$**exz1sb.mp4')

videos/videos-%.html:	
	./create-video-webpage.py videos/join-$*-*.mp4 > $@
