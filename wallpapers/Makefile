sets=wallpapers1 wallpapers2 wallpapers3
subdirs=

include ../boot_targets.mk


files=$(shell find sets/wallpapers1 -type f -name '*.mp4')

join: joined.mp4 sets/joined-opt.gif

sets/joined.gif: joined.mp4
	# note: joined-huge is huge!
	ffmpeg -y -i $< -pix_fmt rgb24 sets/joined-huge.gif
	convert -delay 5 -loop 0 sets/joined-huge.gif $@
	-rm -f sets/joined-huge.gif

%-opt.gif: %.gif
	convert $< -layers optimize $@

joined.mp4:
	MP4Box $(foreach var,$(files),-cat $(var)) $@