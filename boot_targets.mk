max_processes=8
bom=boot_olympics_manager 
bom_params=--contracts --seterr=raise

all: sets-all subdirs-all

%-set-status:
	@echo "----------------------- Status for $* -----------------------"
	compmake --slave --path sets/$*/storage/compmake default stats

boottests:
	#BO_TEST_CONFIG=${PROJ_ROOT} nosetests -w $BO_DIR $*
	BO_TEST_CONFIG=$(PWD)/config/ VEHICLES_TEST_CONFIG=$(PWD)/config/ nosetests bootstrapping_olympics $*

%-set-all:
	$(bom) $(bom_params) batch $* --command "parmake n=$(max_processes)"

%-set-learn:
	$(bom) $(bom_params) batch $* --command "parmake n=$(max_processes)"

%-set-clean-compmake:
	-rm -rf sets/$*/storage/compmake

%-set-distclean:
	-rm -rf sets/$*

### 

sets-all: $(addsuffix -set-all,$(sets))
subdirs-all: $(addsuffix -subdir-all,$(sets))

sets-learn: $(addsuffix -set-learn,$(sets))
subdirs-learn: $(addsuffix -subdir-learn,$(sets))

sets-status: $(addsuffix -set-status,$(sets)) 
subdirs-status: $(addsuffix -subdir-status,$(subdirs))

sets-clean-compmake: $(addsuffix -set-clean-compmake,$(sets))
subdirs-clean-compmake: $(addsuffix -subdir-clean-compmake,$(sets))

sets-distclean: $(addsuffix -set-distclean,$(sets))
subdirs-distclean: $(addsuffix -subdir-distclean,$(sets))

### 

%-subdir-all:
	make -C $* all
%-subdir-status:
	make -C $* status
%-subdir-learn:
	make -C $* learn
%-subdir-clean-compmake:
	make -C $* clean-compmake
%-subdir-distclean:
	make -C $* distclean

###

status: sets-status subdirs-status
learn: sets-learn subdirs-learn
clean-compmake: sets-clean-compmake subdirs-clean-compmake
distclean: sets-distclean subdirs-distclean
