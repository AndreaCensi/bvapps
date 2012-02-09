sets=wallpapers1 wallpapers2 wallpapers3
subdirs=

include ../boot_targets.mk

joined: $(foreach set,$(sets),joined-$(set).mp4)

joined-%.mp4: $(shell find sets/$*/ -type f -name '*.mp4')
	# XXX: not sure what's going on
	# echo ----	# 
		# find sets/$* -type f -name '*.mp4'
		# echo ----
		# echo $(shell find sets/$*/ -type f -name '*.mp4')
	python ../join.py $@ $(shell find sets/$*/ -type f -name '*.mp4')
	
	
# experimental
sets/joined.gif: joined.mp4
	# note: joined-huge is huge!
	ffmpeg -y -i $< -pix_fmt rgb24 sets/joined-huge.gif
	convert -delay 5 -loop 0 sets/joined-huge.gif $@
	-rm -f sets/joined-huge.gif

%-opt.gif: %.gif
	convert $< -layers optimize $@
