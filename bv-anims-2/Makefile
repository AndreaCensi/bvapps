sets=bv-anims-2a  bv-anims-2c bv-anims-2d # bv-anims-2b
subdirs=
videos=close_onlydata_no close_data_sb close_data_no close_nodata_sbu


include ../boot_targets.mk
 

allofthem:
	bom batch bv-anims-2a --command 'parmake'		
	bom batch bv-anims-2c --command 'parmake'	
	bom batch bv-anims-2d --command 'parmake'	
	

remake-videos:
	bom batch bv-anims-2a --command 'clean video*; parmake'		
	bom batch bv-anims-2d --command 'clean video*; parmake'	
	bom batch bv-anims-2c --command 'clean video*; parmake'		


join=python ../join.py


video_summaries: $(foreach video,$(videos),videos/video-summary-$(video).mp4) 
	
videos/video-summary-%.mp4: 
	mkdir -p videos
	$(join) $@ $(shell find sets/ -type f -name '*$*.mp4')
	
	
all: allofthem other
	
.PHONY: other all
