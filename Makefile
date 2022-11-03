DEST=~/.local/bin

install: uninstall
	@cp -vr bookmarks_lib ${DEST}/bookmarks_lib
	@cp -v bookmarks.py ${DEST}/bookmarks

uninstall:
	@rm -vrf ${DEST}/bookmarks_lib
	@rm -v ${DEST}/bookmarks

reqs:
	@pip install -r requirements.txt
