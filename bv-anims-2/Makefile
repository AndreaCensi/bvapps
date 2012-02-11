sets=bv-anims-2a  bv-anims-2c bv-anims-2d bv-anims-2b
subdirs=
videos=close_onlydata_no close_data_sb close_data_no close_nodata_sbu


include ../boot_targets.mk
 

remake-videos:
	nice -n 10 bom batch bv-anims-2a --command 'clean video*; parmake'		
	nice -n 10 bom batch bv-anims-2b --command 'clean video*; parmake'		
	nice -n 10 	bom batch bv-anims-2c --command 'clean video*; parmake'		
	nice -n 10 	bom batch bv-anims-2d --command 'clean video*; parmake'	


join=python ../join.py

	