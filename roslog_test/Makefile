bom=boot_olympics_manager -d .


learn:
	$(bom) learn-log -a BDSAgent_C1 -r LDR13
	$(bom) learn-log -a EstStats -r LDR13
	
all: learn
	$(bom) learn-log -a EstStats -r LDR13 --once
	$(bom) learn-log -a BDSAgent_C1 -r LDR13 --once

status:
	true
	
test:
	true

clean:
	true
	
distclean:
	rm -rf states