|pypi| |actions| |codecov| |downloads|


edc-label
---------

Print labels from for clinic/edc projects

To add print servers update settings.CUPS_SERVERS::

	# settings.py
	...

	CUPS_SERVERS = ["localhost", "prn.sample.org"]

	...

If not set, the default print server is "localhost".

Note: it is fine to just configure the local CUPS server (localhost) with remote printers as per below.


CUPS and printer Installation
+++++++++++++++++++++++++++++


Install CUPS Print Server::

	sudo apt-get install cups

	sudo cp /etc/cups/cupsd.conf /etc/cups/cupsd.conf.original

	sudo chmod a-w /etc/cups/cupsd.conf.original

Edit ``/etc/cups/cupsd.conf`` to listen on your public IP::

	sudo  nano /etc/cups/cupsd.conf

Add the last line with your public IP::

	    Listen 127.0.0.1:631           # existing loopback Listen
	    Listen /var/run/cups/cups.sock # existing socket Listen
	--> Listen PUBLIC_IP:631      # Listen on the LAN interface, Port 631 (IPP)

Restart CUPS::

	sudo systemctl restart cups.service

Add a remote printer by name to your CUPS server
++++++++++++++++++++++++++++++++++++++++++++++++

``LOCAL_PRINTER_NAME``: printer as named on the EDC, your server

``REMOTE_CUPS_IP_ADDRESS``: IP of remote CUPS server

``REMOTE_PRINTER_NAME``: printer name installed on remote CUPS server

	lpadmin -p LOCAL_PRINTER_NAME -E -v ipp://REMOTE_CUPS_IP_ADDRESS/printers/REMOTE_PRINTER_NAME

For example::

	lpadmin -p ambition_clinic_label_printer -E -v ipp://154.70.150.42/printers/ambition_clinic_label_printer
	lpadmin -p ambition_lab_label_printer -E -v ipp://154.70.150.42/printers/ambition_lab_label_printer
	lpadmin -p specimen_reception_label_printer -E -v ipp://154.70.150.42/printers/specimen_reception_label_printer


Add an IP addressable remote printer
++++++++++++++++++++++++++++++++++++

``REMOTE_CUPS_IP_ADDRESS``: printer IP installed on remote CUPS server

	lpadmin -p LOCAL_PRINTER_NAME -E -v ipp://REMOTE_CUPS_IP_ADDRESS/ipp/print -m everywhere

For example::

	lpadmin -p PRINTER_NAME -E -v ipp://REMOTE_IP_ADDRESS/ipp/print -m everywhere


See also http://labelary.com/viewer.html


.. |pypi| image:: https://img.shields.io/pypi/v/edc-label.svg
    :target: https://pypi.python.org/pypi/edc-label

.. |actions| image:: https://github.com/clinicedc/edc-label/workflows/build/badge.svg?branch=develop
  :target: https://github.com/clinicedc/edc-label/actions?query=workflow:build

.. |codecov| image:: https://codecov.io/gh/clinicedc/edc-label/branch/develop/graph/badge.svg
  :target: https://codecov.io/gh/clinicedc/edc-label

.. |downloads| image:: https://pepy.tech/badge/edc-label
   :target: https://pepy.tech/project/edc-label
