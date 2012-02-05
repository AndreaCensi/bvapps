# TODO: add nuisances for DD

sets=anims2c
subdirs=

include ../boot_targets.mk

set=anims2c

%-trace.mp4:
	./compose_frame.pg --video trace    --set $(set) --robot $* --out $@

%-tracesb.mp4:
	./compose_frame.pg --video tracesb  --set $(set) --robot $* --out $@
	
	

robots2c=r-d_SE2_dd_v2-cam360 r-d_SE2_car_v_w-cam360 rn-d_SE2_dd_v2-cam360

animations-trace:  $(addsuffix -trace.mp4,$(robots2c))
animations-tracesb:  $(addsuffix -tracesb.mp4,$(robots2c))
animations:   animations-tracesb animations-trace
	
	
demo: 
	make all && make -j8 animations