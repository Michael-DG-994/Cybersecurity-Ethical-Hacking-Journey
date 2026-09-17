Gruppi:
Sudo Administrator: administrator but has super user
Administrators (can read logs in other group's directories that the other two can't access) | main dir: /home/shared/administrator_dir
Marketing (can write in marketing_data.txt in /home/shared/marketing_docs, can't read/write anywhere else) | main dir: /home/shared/marketing_docs
Accounting (can write in accoutning_report.txt in /home/shared/accounting_docs, CAN READ marketing_data.txt but can't write on it) | main dir: /home/shared/accounting_docs

Users added:
Adminigildo - Sudo Administrator 
Moderichael - Administrator
Quadrulio - Accounting
Gerubardo - Marketing

directories:

/home/shared/administrator_dir : null (admins can write on it)
/home/shared/marketing_docs : 
	/home/shared/marketing_docs/marketing_data.txt ( marketing:rw- , Others:r-- )
	/home/shared/marketing_docs/marketing.log ( administrators:rw- , Others:r-- )
/home/shared/accounting_docs :
	/home/shared/marketing_docs/marketind_data.txt ( accounting:rw- , Others:--- )
	/home/shared/marketing_docs/marketing.log ( administrators:rw- , Others:--- )


