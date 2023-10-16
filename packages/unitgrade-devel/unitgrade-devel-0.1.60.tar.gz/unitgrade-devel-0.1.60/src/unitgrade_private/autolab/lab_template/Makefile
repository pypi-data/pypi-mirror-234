#
# Makefile to manage the example Hello Lab
#

# Get the name of the lab directory
# LAB = $(notdir $(PWD)) # Fail on windows for some reason...

all: handout handout-tarfile

handout: 
	# Rebuild the handout directory that students download
	(rm -rf {{ base_name }}-handout; mkdir {{ base_name }}-handout)
	cp -p src/Makefile-handout {{ base_name }}-handout/Makefile
	cp -p src/README-handout {{ base_name }}-handout/README
{%- for f in src_files_to_handout %}
	cp -p src/{{f}} {{ base_name }}-handout
{% endfor %}

handout-tarfile: handout
	# Build *-handout.tar and autograde.tar
	# tar cvf {{ base_name }}-handout.tar {{ base_name }}-handout
	# cp -p {{ base_name }}-handout.tar autograde.tar
	tar cvf autograde.tar {{ base_name }}-handout
	# cp -p {{ base_name }}-handout.tar autograde.tar

clean:
	# Clean the entire lab directory tree.  Note that you can run
	# "make clean; make" at any time while the lab is live with no
	# adverse effects.
	rm -f *~ *.tar
	(cd src; make clean)
	(cd test-autograder; make clean)
	rm -rf {{ base_name }}-handout
	rm -f autograde.tar
#
# CAREFULL!!! This will delete all student records in the logfile and
# in the handin directory. Don't run this once the lab has started.
# Use it to clean the directory when you are starting a new version
# of the lab from scratch, or when you are debugging the lab prior
# to releasing it to the students.
#
cleanallfiles:
	# Reset the lab from scratch.
	make clean
	rm -f log.txt
	rm -rf handin/*

