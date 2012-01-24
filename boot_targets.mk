max_processes=8
bom=boot_olympics_manager 
#bom_params=--seterr=raise
bom_params=--contracts --seterr=raise

all: sets-all subdirs-all

%-set-status:
	@echo "----------------------- Status for $* -----------------------"
	@compmake --slave --path sets/$*/storage/compmake default stats

boottests:
	#BO_TEST_CONFIG=${PROJ_ROOT} nosetests -w $BO_DIR $*
	BO_TEST_CONFIG=default:$(PWD)/config/ VEHICLES_TEST_CONFIG=default:$(PWD)/config/ nosetests bootstrapping_olympics $(NOSE_PARAMS) $*

%-set-all:
	$(bom) $(bom_params) batch $* --command "parmake n=$(max_processes)"

%-set-try:
	-$(bom) $(bom_params) batch $* --command "parmake n=$(max_processes)"

%-set-clean-videos:
	-rm -rf sets/$*/videos/
	-$(bom) $(bom_params) batch $* --command "clean video*"	

%-set-clean-compmake:
	-rm -rf sets/$*/storage/compmake

%-set-distclean:
	-rm -rf sets/$*

### 

sets-clean-videos: $(addsuffix -set-clean-videos,$(sets))
subdirs-clean-videos: $(addsuffix -subdir-clean-videos,$(subdirs))



sets-all: $(addsuffix -set-all,$(sets))
subdirs-all: $(addsuffix -subdir-all,$(subdirs))

sets-try: $(addsuffix -set-try,$(sets))
subdirs-try: $(addsuffix -subdir-try,$(subdirs))

sets-status: $(addsuffix -set-status,$(sets)) 
subdirs-status: $(addsuffix -subdir-status,$(subdirs))

sets-clean-compmake: $(addsuffix -set-clean-compmake,$(sets))
subdirs-clean-compmake: $(addsuffix -subdir-clean-compmake,$(subdirs))

sets-distclean: $(addsuffix -set-distclean,$(sets))
subdirs-distclean: $(addsuffix -subdir-distclean,$(subdirs))
	true
### 

%-subdir-all:
	$(MAKE) -C $* all
%-subdir-status:
	$(MAKE) -C $* status
%-subdir-try:
	$(MAKE) -C $* try
%-subdir-clean-compmake:
	$(MAKE) -C $* clean-compmake
%-subdir-distclean:
	$(MAKE) -C $* distclean

###

status: sets-status subdirs-status
try: sets-try subdirs-try
clean-compmake: sets-clean-compmake subdirs-clean-compmake
distclean: sets-distclean subdirs-distclean
