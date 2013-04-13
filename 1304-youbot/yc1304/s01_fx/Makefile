
bg_dir=bgs
video_dir=/data/work/1303-youbot-videos/src/src-videos
out=depth

video1=$(video_dir)/unicornA_base1_2013-04-03-16-36-03.mp4
bg1=$(bg_dir)/unicornA_base1_2013-04-03-16-36-03.bg.png

video2=$(video_dir)/unicornA_base1_2013-04-02-20-37-43.mp4
bg2=$(bg_dir)/unicornA_base1_2013-04-02-20-37-43.bg.png


video3=$(video_dir)/unicornA_base1_2013-04-03-12-58-11.mp4
bg3=$(bg_dir)/unicornA_base1_2013-04-03-12-58-11.bg.png

log1=unicornA_base1_2013-04-03-16-36-03
log2=unicornA_base1_2013-04-02-20-37-43
log3=unicornA_base1_2013-04-03-12-58-11
log4=unicornA_base1_2013-04-03-13-16-53
log5=unicornA_base1_2013-04-03-13-30-28

video4=$(video_dir)/unicornA_base1_2013-04-03-13-16-53.mp4
bg4=$(bg_dir)/unicornA_base1_2013-04-03-13-16-53.bg.png



video5=$(video_dir)/unicornA_base1_2013-04-03-13-30-28.mp4
bg5=$(bg_dir)/unicornA_base1_2013-04-03-13-30-28.bg.png

$(bg1):
	pg-video-background -i $(video1) -o $(bg1) -f 400,20,100,150

$(bg2):
	pg-video-background -i $(video2) -o $(bg2) -f 20,80,150

$(bg3):
	pg-video-background -i $(video3) -o $(bg3) -f 20,80,150

$(bg4):
	pg-video-background -i $(video4) -o $(bg4) -f 300,80,150

$(bg5):
	pg-video-background -i $(video5) -o $(bg5) -f 300,80,150


composite1: $(bg1)
	mkdir -p $(out)
	pg video_bg_depth video=$(video1) bg=$(bg1) out=$(out)/unicornA_base1_2013-04-03-16-36-03.300 perc=98.75 every=300

composite2: $(bg2)
	mkdir -p $(out)
	pg video_bg_depth video=$(video2) bg=$(bg2) out=$(out)/unicornA_base1_2013-04-02-20-37-43.300 perc=97 every=600

composite3:
	mkdir -p $(out)
	pg video_bg_depth video=$(video_dir)/$(log3).mp4 bg=$(bg_dir)/$(log3).bg.png out=$(out)/$(log3).600 perc=96.5 every=600

composite4:
	mkdir -p $(out)
	pg video_bg_depth video=$(video_dir)/$(log4).mp4 bg=$(bg_dir)/$(log4).bg.png out=$(out)/$(log4).600 perc=96.5 every=600

composite5:
	mkdir -p $(out)
	pg video_bg_depth video=$(video_dir)/$(log5).mp4 bg=$(bg_dir)/$(log5).bg.png out=$(out)/$(log5).600 perc=96.5 every=600
