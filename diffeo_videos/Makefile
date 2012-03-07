
sources=video0 video1
diffeos=twirl10 zoom1 zoom2 rot90 twirl20
variants=
variants+=-smooth
some=$(foreach source,$(sources), $(foreach diffeo, $(diffeos), $(foreach variant, $(variants), out/$(source)-$(diffeo)$(variant).mp4 out/$(source)$(variant)-$(diffeo).mp4)))

comparisons=$(foreach source,$(sources), $(foreach diffeo, $(diffeos),out/$(source)-diff-$(diffeo).mp4))

all: $(some) $(comparisons) out/video0.mp4  out/video1.mp4 
	
comparisons: $(comparisons)
	
clean: 
	rm -f $(some)
	
download:
	rsync -av  ender@nessa:/home/ender/BIGDATA/er1-logs_compact_better/conf2/*234934/video\?.avi .

width=200

diff=pg -m boot_agents.diffeo.pg diffeo_movie --width $(width) --every 1

%-pow3.mp4: %.mp4
	$(diff) --f pow3    --file $< --out $@

%-rot90.mp4: %.mp4
	$(diff) --f rot90   --file $< --out $@

%-twirl10.mp4: %.mp4
	$(diff) --f twirl10 --file $< --out $@

%-twirl20.mp4: %.mp4
	$(diff) --f twirl20 --file $< --out $@

%-zoom1.mp4: %.mp4
	$(diff) --f zoom1   --file $< --out $@

%-zoom2.mp4: %.mp4
	$(diff) --f zoom2   --file $< --out $@

%-smooth.mp4: %.mp4
	./movie_smooth.pg --every 1 --file $< --out $@

out/%.mp4: %.avi
	./movie_subframe.pg --every 10 --file $< --out $@
	#pg-video-tomp4 $< -o $@

out/video0-diff-%.mp4: out/video0-smooth-%.mp4 out/video0-%-smooth.mp4
	./movie_diff.pg --file1  $(word 1,$^) --file2 $(word 2,$^) --out $@

out/video1-diff-%.mp4: out/video1-smooth-%.mp4 out/video1-%-smooth.mp4
	./movie_diff.pg --file1  $(word 1,$^) --file2 $(word 2,$^) --out $@
	


# don't delete intermediate files
.SECONDARY:
	