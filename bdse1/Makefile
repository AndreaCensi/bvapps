subdirs=
sets=bv1bds1 bv1bds2 bv1bds3 bv1servo1 bv1ddstest1 bv1ddstest2

include ../boot_targets.mk 

 
clean-report: $(addprefix clean-report-, $(sets))

clean-report-%:
	bom batch $* --command='clean report-*'
