subdirs=bo_app1 bv-anims-1 bo_hidden roslog_test

all:
	make -C bo_app1
	make -C bv-anims-1
	make -C bo_hidden
	make -C roslog_test


include boot_targets.mk