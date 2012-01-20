bom=nice -n 15 boot_olympics_manager -d .


all: bv_anims_1_brai_blind

bv_anims_1_brai_blind:
	$(bom) batch bv_anims_1_brai_blind --command 'parmake n=8'


clean-compmake:
	-rm -rf sets/bv_anims_1_brai_blind/storage/compmake
	
test:
	nosetests

status: 
	echo "---- bv_anims_1_brai_blind ---"
	compmake --slave --path sets/bv_anims_1_brai_blind/storage/compmake default stats

