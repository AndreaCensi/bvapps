max_processes=16
bom=boot_olympics_manager 
bom_params=--seterr=raise
#command=parmake n=$(max_processes) 
command=parmake
#bom_params=--contracts --seterr=raise
# Default targets for compmake
targets_all=not video*
targets_complete=all

# targets=
nice=nice -n 20
nose=nosetests --with-id #--processes=16 --process-timeout=30 --process-restartworker

#--processes=8


all: sets-all subdirs-all

%-set-status:
	@echo "----------------------- Status for $* -----------------------"
	-compmake sets/$*/storage/compmake -c stats

test: subdirs-test boot-tests vehicles-tests local-tests

local-tests:
	$(nose) $(NOSE_PARAMS) 
	
boot-tests:
	BO_TEST_CONFIG=default:$(PWD)/config/ VEHICLES_TEST_CONFIG=default:$(PWD)/config/ $(nose) bootstrapping_olympics $(NOSE_PARAMS) 


	
vehicles-tests:
	VEHICLES_TEST_CONFIG=default:$(PWD)/config/ $(nose) vehicles  $(NOSE_PARAMS) 

%-set-all: sets/display_vehicles
	$(nice) $(bom) $(bom_params) batch $* --command "$(command) $(targets_all)"

%-set-console: 
	$(nice) $(bom) $(bom_params) batch $*  --command "exit"

%-set-complete: sets/display_vehicles
		$(nice) $(bom) $(bom_params) batch $* --command "$(command) $(targets_complete)"


sets/display_vehicles:
	vehicles_display_demo_vehicles -g 0 -d default:. -o $@


%-set-try:
	-$(bom) $(bom_params) batch $* --command "$(command) $(targets_all)"

%-set-clean-videos:
	-rm -rf sets/$*/videos/
	-$(bom) $(bom_params) batch $* --command "clean video*; parmake videos"	

%-set-clean-compmake:
	-rm -rf sets/$*/storage/compmake

%-set-distclean:
	-rm -rf sets/$*

### 

sets-clean-videos: $(addsuffix -set-clean-videos,$(sets))
subdirs-clean-videos: $(addsuffix -subdir-clean-videos,$(subdirs))


sets-complete: $(addsuffix -set-complete,$(sets))
subdirs-complete: $(addsuffix -subdir-complete,$(subdirs))

sets-all: $(addsuffix -set-all,$(sets))
subdirs-all: $(addsuffix -subdir-all,$(subdirs))

#sets-test: $(addsuffix -set-test,$(sets))
subdirs-test: $(addsuffix -subdir-test,$(subdirs))

sets-try: $(addsuffix -set-try,$(sets))
subdirs-try: $(addsuffix -subdir-try,$(subdirs))

sets-status: $(addsuffix -set-status,$(sets)) 
subdirs-status: $(addsuffix -subdir-status,$(subdirs))

sets-clean-compmake: $(addsuffix -set-clean-compmake,$(sets))
subdirs-clean-compmake: $(addsuffix -subdir-clean-compmake,$(subdirs))

sets-distclean: $(addsuffix -set-distclean,$(sets))
subdirs-distclean: $(addsuffix -subdir-distclean,$(subdirs))

### 

%-subdir-all:
	$(MAKE) -C $* all
%-subdir-complete:
	$(MAKE) -C $* all
%-subdir-test:
	$(MAKE) -C $* test
%-subdir-status:
	$(MAKE) -C $* status
%-subdir-try:
	$(MAKE) -C $* try
%-subdir-clean-compmake:
	$(MAKE) -C $* clean-compmake
%-subdir-distclean:
	$(MAKE) -C $* distclean

###
complete: sets-complete subdirs-complete
status: sets-status subdirs-status
try: sets-try subdirs-try
clean-compmake: sets-clean-compmake subdirs-clean-compmake
distclean: sets-distclean subdirs-distclean


videos/video-set-%.mp4: $(shell find sets/$*/ -type f -name '*.mp4')
	@python ../join.py $@ $^

videos/video-all.mp4: $(shell find sets/ -type f -name '*.mp4')
	@python ../join.py $@ $^

# Summary by type
video-summaries: $(foreach video,$(videos),videos/video-summary-$(video).mp4) 
	
videos/video-summary-%.mp4: 
	mkdir -p videos
	$(join) $@ $(shell find sets/ -type f -name '*$*.mp4')
	
