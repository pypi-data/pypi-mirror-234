.PHONY: all
all: debian pip

.PHONY: debian
debian: pducontrol.1 pducontrol.5
	debuild -uc -us

.PHONY: pip
pip:
	python setup.py sdist

pducontrol.1: pducontrol/__cli.py
	PYTHONPATH=. argparse-manpage \
		--pyfile $< \
		--function get_parser \
		--author "Pol Bodet" \
		--author-email pol.bodet@nav-timing.safrangroup.com \
		--project-name pdu-control \
		--url https://bitbucket.org/spectracom/pdu-control/ | \
			sed 's/argparse-manpage/pducontrol/g' | \
			sed 's/^\(pducontrol\)/\1 - Utility for controlling power delivery units./g' \
				> $@

pducontrol.5: pducontrol.5.md
	ronn $< -r --pipe > $@

.PHONY: test
test:
	PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -v

.PHONY: clean
clean:
	@rm -rf pducontrol.1 pducontrol.5 dist
