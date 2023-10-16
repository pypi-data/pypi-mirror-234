GNU Health - All modules
========================

This package aims to install GNU Health, all of its ~40 modules, underlying
trytond modules and dependencies.
In order to install GNU Health and all modules this way you need:

* Python > 3.6
* Some system packages, e.g. on Debian based systems: python3-pip python3-dev python3-virtualenv libpq-dev gcc
* PostgreSQL backend and a database
* Configuration file(s) for trytond

You might also want to add:

* Certificates & TLS
* Systemd .service file
* uWSGI
* Reverse Proxy

You can find configuration templates in gnuhealth-all-modules/etc. They will be shipped during installation as well.
After installation the folder can be located by running 'pip3 show gnuhealth-all-modules'.

Check 'HOWTO' for informations on packaging, using testpypi, signatures and hashes.

This content is available both on PyPI and on GitLab in case you want to double check the integrity:

https://pypi.org/project/gnuhealth-all-modules/

https://gitlab.com/geraldwiese/gnu-health-all-modules-pypi

Further reading:

GNU Health core package
https://pypi.org/project/gnuhealth/

GNU Health documentation
https://www.gnuhealth.org/docs/

GNU Health vanilla installation
https://en.wikibooks.org/wiki/GNU_Health/Installation

Tryton documentation
https://docs.tryton.org/en/latest/

GNU Health bug tracker
https://savannah.gnu.org/bugs/?group=health

GNU Health homepage
https://www.gnuhealth.org/index.html
