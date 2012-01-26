sets=wallpapers1
subdirs=

include ../boot_targets.mk


files=$(shell find sets -type f -name '*.mp4')

join: joined-redo.mp4

joined-redo.mp4: joined.mp4
	ffmpeg -i $<  -y -sameq $@

joined.mp4:
	MP4Box $(foreach var,$(files),-cat $(var)) $@