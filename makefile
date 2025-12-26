dumpdata:
	python manage.py dumpdata \
	--exclude auth.permission \
	--exclude auth.group \
	--exclude contenttypes \
	--exclude admin.logentry \
	--exclude sessions \
	--indent 2 > db.json