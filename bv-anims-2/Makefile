sets=bv-anims-2a bv-anims-2b bv-anims-2c
subdirs=

include ../boot_targets.mk

# other: video-set-bv-anims-2a.mp4

allofthem:
	bom batch bv-anims-2a --command 'parmake'		
	bom batch bv-anims-2b --command 'parmake'	
	bom batch bv-anims-2c --command 'parmake'	
	

clean-videos:
	bom batch bv-anims-2a --command 'clean video*'		
	bom batch bv-anims-2b --command 'clean video*'	
	bom batch bv-anims-2c --command 'clean video*'		


join=python ../join.py

other: kind-close_data_sb.mp4  kind-close_data_no.mp4 kind-close_nodata_no.mp4 kind-close_nodata_sbu.mp4



kind-%.mp4: 
	echo prefix: $*
	$(join) $@ $(shell find sets/ -type f -name '*$*.mp4')
	
	
all: allofthem other
	
.PHONY: other all
