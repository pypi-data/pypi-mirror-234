#!/usr/bin/env bash

# restart mysqldb
if [ "$1" = "debian11" ] || [ "$1" = "debian12" ]; then
    docker exec --user root ndts service mariadb restart
else
    # workaround for a bug in debian9, i.e. starting mysql hangs
    docker exec --user root ndts service mysql stop
    if [ "$1" = "ubuntu20.04" ] || [ "$1" = "ubuntu20.10" ] || [ "$1" = "ubuntu21.04" ] || [ "$1" = "ubuntu22.04" ] || [ "$1" = "ubuntu23.04" ]; then
	# docker exec --user root ndts /bin/bash -c 'mkdir -p /var/lib/mysql'
	# docker exec --user root ndts /bin/bash -c 'chown mysql:mysql /var/lib/mysql'
	docker exec --user root ndts /bin/bash -c 'usermod -d /var/lib/mysql/ mysql'
    fi
    docker exec --user root ndts service mysql start
    # docker exec  --user root ndts /bin/bash -c '$(service mysql start &) && sleep 30'
fi


echo "install tango db"
docker exec  --user root ndts /bin/sh -c 'apt-get -qq update; apt-get -qq install -y   tango-db tango-common; sleep 10'
if [ "$?" != "0" ]; then exit 255; fi

docker exec --user root ndts /bin/bash -c 'export DEBIAN_FRONTEND=noninteractive; apt-get -qq update; apt-get -qq install -y   tango-db tango-common; sleep 10'
if [ "$?" != "0" ]; then exit 255; fi

if [ "$1" = "ubuntu20.04" ] || [ "$1" = "ubuntu20.10" ] || [ "$1" = "ubuntu21.04" ] || [ "$1" = "ubuntu21.10" ] || [ "$1" = "ubuntu22.04" ] || [ "$1" = "ubuntu23.04" ]; then
    # docker exec  --user tango ndts /bin/bash -c '/usr/lib/tango/DataBaseds 2 -ORBendPoint giop:tcp::10000  &'
    docker exec  --user root ndts /bin/bash -c 'echo -e "[client]\nuser=tango\nhost=127.0.0.1\npassword=rootpw" > /var/lib/tango/.my.cnf'
    docker exec  --user root ndts /bin/bash -c 'echo -e "[client]\nuser=root\npassword=rootpw" > /root/.my.cnf'
fi
docker exec  --user root ndts service tango-db restart

echo "install tango servers"
docker exec  --user root ndts /bin/sh -c 'apt-get -qq update; apt-get -qq install -y  tango-starter tango-test'
if [ "$?" != "0" ]; then exit 255; fi

# restart tango services
docker exec  --user root ndts service tango-starter restart
docker exec  --user root ndts chown -R tango:tango .

if [ "$2" = "2" ]; then
    echo "install python-pytango"
    docker exec  --user root ndts /bin/sh -c 'apt-get -qq update; apt-get -qq install -y   python-pytango nxsconfigserver-db python-nxstools'
else
    echo "install python3-pytango"
    if [ "$1" = "ubuntu20.04" ] || [ "$1" = "ubuntu20.10" ] || [ "$1" = "ubuntu21.04" ] || [ "$1" = "ubuntu23.04" ] || [ "$1" = "ubuntu22.04" ] || [ "$1" = "debian11" ] || [ "$1" = "debian12" ]; then
	docker exec  --user root ndts /bin/sh -c 'apt-get -qq update; apt-get -qq install -y   python3-tango nxsconfigserver-db python3-nxstools'
    else
	docker exec  --user root ndts /bin/sh -c 'apt-get -qq update; apt-get -qq install -y   python3-pytango nxsconfigserver-db python3-nxstools'
    fi
fi
if [ "$?" != "0" ]; then exit 255; fi

if [ "$2" = "2" ]; then
    echo "install python-nxswriter"
    docker exec --user root ndts chown -R tango:tango .
    docker exec  ndts python setup.py build
    docker exec --user root ndts python setup.py  install
else
    echo "install python3-nxswriter"
    docker exec --user root ndts chown -R tango:tango .
    docker exec  ndts python3 setup.py build
    docker exec --user root ndts python3 setup.py  install
fi
if [ "$?" != "0" ]; then exit 255; fi

