version=1.0

all:

install:
	mkdir -p /usr/local/share/fconconfig/doc
	cp README COPYING /usr/local/share/fconconfig/doc
	cp fconconfig.py /usr/local/bin/fconconfig
	chmod +x /usr/local/bin/fconconfig

uninstall:
	rm -rf /usr/local/share/fconconfig
	rm -f /usr/local/bin/fconconfig

package:
	rm -rf fconconfig*.tar.gz fconconfig/
	rsync -av --progress ./ fconconfig --exclude fconconfig --exclude .git --exclude xboxdrv.sh
	tar zczf fconconfig-$(version).tar.gz fconconfig

clean:
	rm -f fconconfig*.tar.gz
