Name:		zabbix
Version:	6.0.38
Release:	%{?alphatag:%{?alphatag}.}release2%{?dist}
Summary:	The Enterprise-class open source monitoring solution
Group:		Applications/Internet
License:	GPLv2+
URL:		http://www.zabbix.com/
Source0:	https://cdn.zabbix.com/zabbix/sources/development/6.0/%{name}-%{version}%{?alphatag}.tar.gz
Source1:	zabbix-web22.conf
Source2:	zabbix-web24.conf
Source3:	zabbix-logrotate.in
Source4:	zabbix-java-gateway.init
Source5:	zabbix-agent.init
Source6:	zabbix-server.init
Source7:	zabbix-proxy.init
Source10:	zabbix-agent.service
Source11:	zabbix-server.service
Source12:	zabbix-proxy.service
Source13:	zabbix-java-gateway.service
Source15:	zabbix-tmpfiles.conf
Source16:	zabbix-php-fpm.conf
Source17:	zabbix-web-fcgi.conf
Source18:	zabbix-nginx.conf
Source19:	zabbix-agent2.service
Source20:	zabbix-agent.sysconfig
Source21:	zabbix-agent2.init
Source22:	zabbix-agent2.sysconfig
Source23:	zabbix-web-service.service
Source24:	zabbix_policy.te
Patch0:		frontend.patch
Patch1:		fping3-sourceip-option.patch
Patch2:		java-gateway.patch
Patch3:		conf.patch
Patch4:		agent2.conf.patch
Patch5:		rhel6-go11.6.patch
Patch6:		conf.var.run.patch
Patch7:		agent2.conf.var.run.patch
Patch8:		agent2.conf.socket.patch


Buildroot:	%{_tmppath}/zabbix-%{version}-%{release}-root-%(%{__id_u} -n)

%{!?rhel: %global rhel 0}
%{!?amzn: %global amzn 0}

%{!?build_agent: %global build_agent 1}

%ifarch x86_64 aarch64
%if 0%{?rhel} >= 6 || %{amzn} >= 2023
%{!?build_agent2: %global build_agent2 1}
%endif
%if 0%{?rhel} >= 8 || %{amzn} >= 2023
%{!?build_web_service: %global build_web_service 1}
%endif
%endif

%if 0%{?rhel} >= 7 || %{amzn} >= 2023
%{!?build_proxy: %global build_proxy 1}
%{!?build_java_gateway: %global build_java_gateway 1}
%endif

%if 0%{?rhel} >= 8 || %{amzn} >= 2023
%{!?build_server: %global build_server 1}
%{!?build_frontend: %global build_frontend 1}
%endif

%{!?build_with_mysql: %global build_with_mysql 1}
%{!?build_with_pgsql: %global build_with_pgsql 1}
%{!?build_with_sqlite: %global build_with_sqlite 1}

%{!?zabbix_script_dir: %global zabbix_script_dir /usr/lib/zabbix}

%if 0%{build_with_mysql} == 0 && 0%{build_with_pgsql} == 0
%global build_server 0
%if 0%{build_with_sqlite} == 0
%global build_proxy 0
%endif
%endif

%if 0%{?rhel} >= 7 || %{amzn} >= 2023
%{!?build_selinux_policy: %global build_selinux_policy 1}
%endif

# FIXME: Building debuginfo is broken on RHEL 5 & 8. Disabled for now.
%if 0%{?rhel} <= 5 || 0%{?rhel} >= 8
%define debug_package %{nil}
%endif

# Enable hardening
%if 0%{?rhel} >= 8 || %{amzn} >= 2023
%global _hardened_build 1
%endif

BuildRequires:	make
%if 0%{?rhel} >= 8 || %{amzn} >= 2023
BuildRequires:	mariadb-connector-c-devel
BuildRequires:	postgresql-devel >= 12.0
BuildRequires:	sqlite-devel
BuildRequires:	net-snmp-devel
BuildRequires:	openldap-devel
BuildRequires:	unixODBC-devel
BuildRequires:	curl-devel >= 7.13.1
%if %{amzn} == 0
BuildRequires:	OpenIPMI-devel >= 2
%endif
BuildRequires:	libssh-devel >= 0.9.0
BuildRequires:	java-devel >= 1.6.0
BuildRequires:	libxml2-devel
BuildRequires:	libevent-devel
%endif
%if 0%{?rhel} >= 7 || %{amzn} >= 2023
BuildRequires:	pcre2-devel
%else
BuildRequires:	pcre-devel
%endif
%if 0%{?rhel} >= 6 || %{amzn} >= 2023
BuildRequires:	openssl-devel >= 1.0.1
%endif
%if 0%{?rhel} >= 7 || %{amzn} >= 2023
BuildRequires:	systemd
%endif
%if 0%{?build_selinux_policy}
BuildRequires: policycoreutils-devel
%if 0%{?rhel} >= 9 || %{amzn} >= 2023
BuildRequires: selinux-policy-devel
%endif
%endif

%description
Zabbix is the ultimate enterprise-level software designed for
real-time monitoring of millions of metrics collected from tens of
thousands of servers, virtual machines and network devices.

%if 0%{?build_agent}
%package agent
Summary:		Zabbix agent
Group:			Applications/Internet
Requires:		logrotate
Requires(pre):		/usr/sbin/useradd
%if 0%{?rhel} >= 7 || %{amzn} >= 2023
Requires(post):		systemd
Requires(preun):	systemd
Requires(preun):	systemd
%else
Requires(post):		/sbin/chkconfig
Requires(preun):	/sbin/chkconfig
Requires(preun):	/sbin/service
Requires(postun):	/sbin/service
%endif
%endif

%if 0%{?build_agent2} != 1
%if 0%{?build_agent}
%description agent
Zabbix agent to be installed on monitored systems.
%endif

%else
%if 0%{?build_agent}
%description agent
Old implementation of zabbix agent.
To be installed on monitored systems.
%endif

%package agent2
Summary:		Zabbix agent 2
Group:			Applications/Internet
Requires:		logrotate
%if 0%{?rhel} >= 7 || %{amzn} >= 2023
Requires(post):		systemd
Requires(preun):	systemd
Requires(preun):	systemd
%else
Requires(post):		/sbin/chkconfig
Requires(preun):	/sbin/chkconfig
Requires(preun):	/sbin/service
Requires(postun):	/sbin/service
%endif
Requires:		zabbix-agent2-plugin-mongodb
Requires:		zabbix-agent2-plugin-postgresql

%description agent2
New implementation of zabbix agent.
To be installed on monitored systems.
%endif

%if 0%{?build_web_service}
%package web-service
Summary:		Zabbix web service
Group:			Applications/Internet
Requires:		logrotate
Requires(post):		systemd
Requires(preun):	systemd
Requires(preun):	systemd

%description web-service
Zabbix web servce for performing various tasks using headless web browser.
%endif

%if 0%{?build_agent}
%package get
Summary:		Zabbix get
Group:			Applications/Internet

%description get
Zabbix get command line utility.

%package sender
Summary:		Zabbix sender
Group:			Applications/Internet

%description sender
Zabbix sender command line utility.
%endif

%if 0%{?build_server} || 0%{?build_proxy}
%package js
Summary:		Zabbix js
Group:			Applications/Internet

%description js
Zabbix js command line utility.

%package sql-scripts
Summary:		Zabbix database sql scripts
Group:			Applications/Internet
BuildArch:		noarch

%description sql-scripts
SQL files needed to setup Zabbix server or proxy databases
%endif

%if 0%{?build_proxy}
%package proxy-mysql
Summary:		Zabbix proxy for MySQL or MariaDB database
Group:			Applications/Internet
Requires:		fping
Requires(post):		systemd
Requires(preun):	systemd
Requires(postun):	systemd
Provides:		zabbix-proxy = %{version}-%{release}
Provides:		zabbix-proxy-implementation = %{version}-%{release}

%description proxy-mysql
Zabbix proxy with MySQL or MariaDB database support.

%package proxy-pgsql
Summary:		Zabbix proxy for PostgreSQL database
Group:			Applications/Internet
Requires:		fping
Requires(post):		systemd
Requires(preun):	systemd
Requires(postun):	systemd
Provides:		zabbix-proxy = %{version}-%{release}
Provides:		zabbix-proxy-implementation = %{version}-%{release}

%description proxy-pgsql
Zabbix proxy with PostgreSQL database support.

%package proxy-sqlite3
Summary:		Zabbix proxy for SQLite3 database
Group:			Applications/Internet
Requires:		fping
Requires(post):		systemd
Requires(preun):	systemd
Requires(postun):	systemd
Provides:		zabbix-proxy = %{version}-%{release}
Provides:		zabbix-proxy-implementation = %{version}-%{release}

%description proxy-sqlite3
Zabbix proxy with SQLite3 database support.
%endif

%if 0%{?build_server}
%package server-mysql
Summary:		Zabbix server for MySQL or MariaDB database
Group:			Applications/Internet
Requires:		fping
Requires(post):		systemd
Requires(preun):	systemd
Requires(postun):	systemd
Provides:		zabbix-server = %{version}-%{release}
Provides:		zabbix-server-implementation = %{version}-%{release}

%description server-mysql
Zabbix server with MySQL or MariaDB database support.

%package server-pgsql
Summary:		Zabbix server for PostgresSQL database
Group:			Applications/Internet
Requires:		fping
Requires(post):		systemd
Requires(preun):	systemd
Requires(postun):	systemd
Provides:		zabbix-server = %{version}-%{release}
Provides:		zabbix-server-implementation = %{version}-%{release}
%description server-pgsql
Zabbix server with PostgresSQL database support.
%endif

%if 0%{?build_frontend}
%package web
Summary:		Zabbix web frontend common package
Group:			Application/Internet
BuildArch:		noarch
Requires:		dejavu-sans-fonts
Requires(post):		%{_sbindir}/update-alternatives
Requires(preun):	%{_sbindir}/update-alternatives

%description web
Zabbix web frontend common package

%package web-deps
Summary:		PHP dependencies metapackage for frontend
Group:			Application/Internet
BuildArch:		noarch
Requires:		zabbix-web = %{version}-%{release}
Requires:		php-gd >= 7.2
Requires:		php-bcmath >= 7.2
Requires:		php-mbstring >= 7.2
Requires:		php-xml >= 7.2
Requires:		php-ldap >= 7.2
Requires:		php-json >= 7.2
Requires:		php-fpm >= 7.2
Requires:		zabbix-web = %{version}-%{release}
Requires:		zabbix-web-database = %{version}-%{release}

%description web-deps
PHP dependencies metapackage for frontend

%package web-mysql
Summary:		Zabbix web frontend for MySQL
Group:			Applications/Internet
BuildArch:		noarch
Requires:		zabbix-web = %{version}-%{release}
Requires:		zabbix-web-deps = %{version}-%{release}
Requires:		php-mysqlnd
Provides:		zabbix-web-database = %{version}-%{release}

%description web-mysql
Zabbix web frontend for MySQL

%package web-pgsql
Summary:		Zabbix web frontend for PostgreSQL
Group:			Applications/Internet
BuildArch:		noarch
Requires:		zabbix-web = %{version}-%{release}
Requires:		zabbix-web-deps = %{version}-%{release}
Requires:		php-pgsql
Provides:		zabbix-web-database = %{version}-%{release}

%description web-pgsql
Zabbix web frontend for PostgreSQL

%package apache-conf
Summary:		Automatic zabbix frontend configuration with apache
Group:			Applications/Internet
BuildArch:		noarch
Requires:		zabbix-web-deps = %{version}-%{release}
Requires:		httpd

%description apache-conf
Zabbix frontend configuration for apache

%package nginx-conf
Summary:		Zabbix frontend configuration for nginx and php-fpm
Group:			Applications/Internet
BuildArch:		noarch
Requires:		zabbix-web-deps = %{version}-%{release}
Requires:		nginx

%description nginx-conf
Zabbix frontend configuration for nginx and php-fpm

%package web-japanese
Summary:		Japanese font settings for Zabbix frontend
Group:			Applications/Internet
BuildArch:		noarch
Requires:		google-noto-sans-cjk-ttc-fonts
Requires:		glibc-langpack-ja
Requires:		zabbix-web = %{version}-%{release}
Requires(post):		%{_sbindir}/update-alternatives
Requires(preun):	%{_sbindir}/update-alternatives

%description web-japanese
Japanese font configuration for Zabbix web frontend
%endif

%if 0%{?build_java_gateway}
%package java-gateway
Summary:		Zabbix java gateway
Group:			Applications/Internet
Requires:		java-headless >= 1.6.0
Requires(post):		systemd
Requires(preun):	systemd
Requires(postun):	systemd

%description java-gateway
Zabbix java gateway
%endif

%if 0%{?build_selinux_policy}
%package selinux-policy
Summary:		Zabbix SELinux policy
Group:			Applications/Internet
Requires(post):		%{_sbindir}/semodule
Requires(preun):	%{_sbindir}/semodule

%description selinux-policy
Zabbix SELinux policy
%endif



#
# prep
#

%prep
%setup0 -q -n %{name}-%{version}%{?alphatag}

%if 0%{?build_frontend}
%patch0 -p1

## remove font file
rm -f ui/assets/fonts/DejaVuSans.ttf

# replace font in defines.inc.php
sed -i -r "s/(define\(.*_FONT_NAME.*)DejaVuSans/\1graphfont/" \
	ui/include/defines.inc.php

# remove .htaccess files
rm -f ui/app/.htaccess
rm -f ui/conf/.htaccess
rm -f ui/include/.htaccess
rm -f ui/local/.htaccess

# remove translation source files and scripts
find ui/locale -name '*.po' | xargs rm -f
find ui/locale -name '*.sh' | xargs rm -f
%endif

%if 0%{?build_server} || 0%{?build_proxy} || 0%{?build_agent} || 0%{?build_agent2}
%patch1 -p1
%endif

%if 0%{?build_server} || 0%{?build_proxy}
# traceroute command path for global script
sed -i -e 's|/usr/bin/traceroute|/bin/traceroute|' database/mysql/data.sql
sed -i -e 's|/usr/bin/traceroute|/bin/traceroute|' database/postgresql/data.sql
%endif

%if 0%{?build_server}
# sql files for servers
cat database/mysql/schema.sql > database/mysql/server.sql
cat database/mysql/images.sql >> database/mysql/server.sql
cat database/mysql/data.sql >> database/mysql/server.sql
gzip database/mysql/server.sql

cat database/postgresql/schema.sql > database/postgresql/server.sql
cat database/postgresql/images.sql >> database/postgresql/server.sql
cat database/postgresql/data.sql >> database/postgresql/server.sql
gzip database/postgresql/server.sql
%endif

%if 0%{?build_proxy}
# sql files for proxies
mv database/mysql/schema.sql database/mysql/proxy.sql
mv database/postgresql/schema.sql database/postgresql/proxy.sql
mv database/sqlite3/schema.sql database/sqlite3/proxy.sql
%endif

%if 0%{?build_java_gateway}
%patch2 -p1
%endif

# update config files
%patch3 -p1

%if 0%{?build_agent2}
%patch4 -p1
%if 0%{?rhel} == 6
%patch5 -p1
%endif
%endif

%if 0%{?rhel} <= 6
%patch6 -p1
%if 0%{?build_agent2}
%patch7 -p1
%endif
%endif

%if 0%{?build_agent2}
%patch8 -p1
%endif

%build
# Build consists of 1-3 configure/make passes, one for each database.
# pass 1: is sqlite proxy, may be omitted.
# pass 2: is pqsql server/proxy, may be omitted.
# pass 3: If only one database is enabled, then it must occur with pass 3.

build_conf_common="
	--enable-dependency-tracking
	--sysconfdir=/etc/zabbix
	--libdir=%{_libdir}/zabbix
	--enable-ipv6
	--with-net-snmp
	--with-ldap
	--with-libcurl
%if %{amzn} == 0
	--with-openipmi
%endif
	--with-unixodbc
%if 0%{?rhel} >= 8 || %{amzn} >= 2023
	--with-ssh
%else
	--with-ssh2
%endif
	--with-libxml2
	--with-libevent
%if 0%{?rhel} >= 7 || %{amzn} >= 2023
	--with-libpcre2
%else
	--with-libpcre
%endif
%if 0%{?rhel} >= 6 || %{amzn} >= 2023
	--with-openssl
%endif
"

# setup pass 3
%if 0%{?build_with_mysql} && ( 0%{?build_server} || 0%{?build_proxy} )
build_conf_3="
%if 0%{?build_server}
	--enable-server
%endif
%if 0%{?build_proxy}
	--enable-proxy
%endif
	--with-mysql
"

build_db_3=mysql
%endif


# setup pass 2
%if 0%{?build_with_pgsql} && ( 0%{?build_server} || 0%{?build_proxy} )
build_conf_2="
%if 0%{?build_server}
	--enable-server
%endif
%if 0%{?build_proxy}
	--enable-proxy
%endif
	--with-postgresql
"

if [ -z "$build_conf_3" ]; then
	build_conf_3="$build_conf_2"
	build_conf_2=""
	build_db_3="pgsql"
fi
%endif


# setup pass 1
%if 0%{?build_with_sqlite} && 0%{?build_proxy}
build_conf_1="--enable-proxy --with-sqlite3"

if [ -z "$build_conf_3" ]; then
	build_conf_3="$build_conf_1"
	build_conf_1=""
	build_db_3=sqlite3
fi
%endif


# add agents, web-service and java-gateway to pass 3
build_conf_3="
%if 0%{?build_agent}
	--enable-agent
%endif
%if 0%{?build_agent2}
	--enable-agent2
%endif
%if 0%{?build_java_gateway}
	--enable-java
%endif
%if 0%{?build_web_service}
	--enable-webservice
%endif
	$build_conf_3
"


%if 0%{?build_server} || 0%{?build_proxy}
make_flags="EXTERNAL_SCRIPTS_PATH=/usr/lib/zabbix/externalscripts"
%endif

%if 0%{?build_server}
make_flags="$make_flags ALERT_SCRIPTS_PATH=/usr/lib/zabbix/alertscripts"
%endif

# pass 1
if [ -n "$build_conf_1" ]; then
	%configure $build_conf_common $build_conf_1
	make -j16 $make_flags
	mv src/zabbix_proxy/zabbix_proxy src/zabbix_proxy/zabbix_proxy_sqlite3
fi


# pass 2
if [ -n "$build_conf_2" ]; then
	%configure $build_conf_common $build_conf_2
	make -j16 $make_flags
%if 0%{?build_server}
	mv src/zabbix_server/zabbix_server src/zabbix_server/zabbix_server_pgsql
%endif
%if 0%{?build_proxy}
	mv src/zabbix_proxy/zabbix_proxy src/zabbix_proxy/zabbix_proxy_pgsql
%endif
fi


# pass 3
if [ -n "$build_conf_3" ]; then
	%configure $build_conf_common $build_conf_3
	make -j16 $make_flags
%if 0%{?build_server}
	mv src/zabbix_server/zabbix_server "src/zabbix_server/zabbix_server_$build_db_3"
%endif
%if 0%{?build_proxy}
	mv src/zabbix_proxy/zabbix_proxy "src/zabbix_proxy/zabbix_proxy_$build_db_3"
%endif
fi


# build selinux policy
%if 0%{?build_selinux_policy}
cp %{SOURCE24} .
make -f /usr/share/selinux/devel/Makefile zabbix_policy.pp
%endif


#
# install
#

%install

rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/log/zabbix
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/run/zabbix
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/zabbix
mkdir -p $RPM_BUILD_ROOT%{_datadir}
mkdir -p $RPM_BUILD_ROOT%{_datadir}/man/man8
mkdir -p $RPM_BUILD_ROOT%{_datadir}/zabbix
mkdir -p $RPM_BUILD_ROOT%{_sbindir}


%if 0%{?build_agent2} || 0%{?build_web_service}
make DESTDIR=$RPM_BUILD_ROOT GOBIN=$RPM_BUILD_ROOT%{_sbindir} install
%else
make DESTDIR=$RPM_BUILD_ROOT install
%endif


%if 0%{?build_agent}
mv $RPM_BUILD_ROOT%{_sysconfdir}/zabbix/zabbix_agentd.conf.d $RPM_BUILD_ROOT%{_sysconfdir}/zabbix/zabbix_agentd.d
install -dm 755 $RPM_BUILD_ROOT%{_docdir}/zabbix-agent-%{version}
cat %{SOURCE3} | sed \
	-e 's|COMPONENT|agentd|g' \
	> $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/zabbix-agent
%if 0%{?rhel} >= 7 || %{amzn} >= 2023
install -Dm 0644 -p %{SOURCE10} $RPM_BUILD_ROOT%{_unitdir}/zabbix-agent.service
install -Dm 0644 -p %{SOURCE15} $RPM_BUILD_ROOT%{_tmpfilesdir}/zabbix-agent.conf
%else
install -Dm 0755 -p %{SOURCE5} $RPM_BUILD_ROOT%{_sysconfdir}/init.d/zabbix-agent
install -Dm 0644 -p %{SOURCE20} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/zabbix-agent
%endif
%else
%if 0%{?build_agent2}
rm $RPM_BUILD_ROOT%{_sbindir}/zabbix_agentd
rm $RPM_BUILD_ROOT%{_sysconfdir}/zabbix/zabbix_agentd.conf
%endif
%endif


%if 0%{?build_agent2}
cat %{SOURCE3} | sed \
	-e 's|COMPONENT|agent2|g' \
	> $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/zabbix-agent2
cp man/zabbix_agent2.man $RPM_BUILD_ROOT%{_mandir}/man8/zabbix_agent2.8
%if 0%{?rhel} >= 7 || %{amzn} >= 2023
install -Dm 0644 -p %{SOURCE19} $RPM_BUILD_ROOT%{_unitdir}/zabbix-agent2.service
install -Dm 0644 -p %{SOURCE15} $RPM_BUILD_ROOT%{_tmpfilesdir}/zabbix_agent2.conf
%else
install -Dm 0755 -p %{SOURCE21} $RPM_BUILD_ROOT%{_sysconfdir}/init.d/zabbix-agent2
install -Dm 0644 -p %{SOURCE22} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/zabbix-agent2
%endif
%endif


%if 0%{?build_web_service}
cat %{SOURCE3} | sed \
	-e 's|COMPONENT|web_service|g' \
	> $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/zabbix-web-service
cp man/zabbix_web_service.man $RPM_BUILD_ROOT%{_mandir}/man8/zabbix_web_service.8
install -Dm 0644 -p %{SOURCE23} $RPM_BUILD_ROOT%{_unitdir}/zabbix-web-service.service
install -Dm 0644 -p %{SOURCE15} $RPM_BUILD_ROOT%{_tmpfilesdir}/zabbix_web_service.conf
%endif


%if 0%{?build_server} || 0%{?build_proxy}
mkdir -p $RPM_BUILD_ROOT%{zabbix_script_dir}
mv $RPM_BUILD_ROOT%{_datadir}/zabbix/externalscripts $RPM_BUILD_ROOT%{zabbix_script_dir}


#
# install sql files
#
%if 0%{?build_with_mysql}
mkdir -p $RPM_BUILD_ROOT%{_datadir}/zabbix-sql-scripts/mysql
%if 0%{?build_proxy}
cp database/mysql/proxy.sql $RPM_BUILD_ROOT%{_datadir}/zabbix-sql-scripts/mysql
%endif
%if 0%{?build_server}
cp database/mysql/server.sql.gz $RPM_BUILD_ROOT%{_datadir}/zabbix-sql-scripts/mysql
cp database/mysql/option-patches/double.sql $RPM_BUILD_ROOT%{_datadir}/zabbix-sql-scripts/mysql
cp database/mysql/option-patches/history_pk_prepare.sql $RPM_BUILD_ROOT%{_datadir}/zabbix-sql-scripts/mysql
%endif
%endif

%if 0%{?build_with_pgsql}
mkdir -p $RPM_BUILD_ROOT%{_datadir}/zabbix-sql-scripts/postgresql
mkdir $RPM_BUILD_ROOT%{_datadir}/zabbix-sql-scripts/postgresql/tsdb_history_pk_upgrade_no_compression
mkdir $RPM_BUILD_ROOT%{_datadir}/zabbix-sql-scripts/postgresql/tsdb_history_pk_upgrade_with_compression
%if 0%{?build_proxy}
cp database/postgresql/proxy.sql $RPM_BUILD_ROOT%{_datadir}/zabbix-sql-scripts/postgresql
%endif
%if 0%{?build_server}
cp database/postgresql/server.sql.gz $RPM_BUILD_ROOT%{_datadir}/zabbix-sql-scripts/postgresql
cp database/postgresql/timescaledb/schema.sql $RPM_BUILD_ROOT%{_datadir}/zabbix-sql-scripts/postgresql/timescaledb.sql
cp database/postgresql/option-patches/double.sql $RPM_BUILD_ROOT%{_datadir}/zabbix-sql-scripts/postgresql
cp database/postgresql/option-patches/history_pk_prepare.sql $RPM_BUILD_ROOT%{_datadir}/zabbix-sql-scripts/postgresql
%endif
cp -R database/postgresql/timescaledb/option-patches/without-compression/*.sql $RPM_BUILD_ROOT%{_datadir}/zabbix-sql-scripts/postgresql/tsdb_history_pk_upgrade_no_compression
cp -R database/postgresql/timescaledb/option-patches/with-compression/*.sql $RPM_BUILD_ROOT%{_datadir}/zabbix-sql-scripts/postgresql/tsdb_history_pk_upgrade_with_compression
%endif

%if 0%{?build_with_sqlite} && 0%{?build_proxy}
mkdir -p $RPM_BUILD_ROOT%{_datadir}/zabbix-sql-scripts/sqlite3
cp database/sqlite3/proxy.sql $RPM_BUILD_ROOT%{_datadir}/zabbix-sql-scripts/sqlite3
%endif
%endif


%if 0%{?build_proxy}
mv $RPM_BUILD_ROOT%{_sysconfdir}/zabbix/zabbix_proxy.conf.d $RPM_BUILD_ROOT%{_sysconfdir}/zabbix/zabbix_proxy.d
install -m 0755 -p src/zabbix_proxy/zabbix_proxy_* $RPM_BUILD_ROOT%{_sbindir}/
rm $RPM_BUILD_ROOT%{_sbindir}/zabbix_proxy
cat %{SOURCE3} | sed \
	-e 's|COMPONENT|proxy|g' \
	> $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/zabbix-proxy
install -Dm 0644 -p %{SOURCE12} $RPM_BUILD_ROOT%{_unitdir}/zabbix-proxy.service
install -Dm 0644 -p %{SOURCE15} $RPM_BUILD_ROOT%{_tmpfilesdir}/zabbix-proxy.conf
%endif


%if 0%{?build_server}
mv $RPM_BUILD_ROOT%{_sysconfdir}/zabbix/zabbix_server.conf.d $RPM_BUILD_ROOT%{_sysconfdir}/zabbix/zabbix_server.d
install -m 0755 -p src/zabbix_server/zabbix_server_* $RPM_BUILD_ROOT%{_sbindir}/
rm $RPM_BUILD_ROOT%{_sbindir}/zabbix_server
mv $RPM_BUILD_ROOT%{_datadir}/zabbix/alertscripts $RPM_BUILD_ROOT%{zabbix_script_dir}
cat %{SOURCE3} | sed \
	-e 's|COMPONENT|server|g' \
	> $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/zabbix-server
install -Dm 0644 -p %{SOURCE11} $RPM_BUILD_ROOT%{_unitdir}/zabbix-server.service
install -Dm 0644 -p %{SOURCE15} $RPM_BUILD_ROOT%{_tmpfilesdir}/zabbix-server.conf
%endif


%if 0%{?build_frontend}
find ui -name '*.orig' | xargs rm -f
cp -a ui/* $RPM_BUILD_ROOT%{_datadir}/zabbix
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/zabbix/web
touch $RPM_BUILD_ROOT%{_sysconfdir}/zabbix/web/zabbix.conf.php
mv $RPM_BUILD_ROOT%{_datadir}/zabbix/conf/maintenance.inc.php $RPM_BUILD_ROOT%{_sysconfdir}/zabbix/web/
install -Dm 0644 -p %{SOURCE16} $RPM_BUILD_ROOT%{_sysconfdir}/php-fpm.d/zabbix.conf
install -Dm 0644 -p %{SOURCE17} $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d/zabbix.conf
install -Dm 0644 -p %{SOURCE18} $RPM_BUILD_ROOT%{_sysconfdir}/nginx/conf.d/zabbix.conf
%endif


%if 0%{?build_java_gateway}
mv $RPM_BUILD_ROOT%{_sbindir}/zabbix_java/startup.sh $RPM_BUILD_ROOT%{_sbindir}/zabbix_java_gateway_startup
mv $RPM_BUILD_ROOT%{_sbindir}/zabbix_java/shutdown.sh $RPM_BUILD_ROOT%{_sbindir}/zabbix_java_gateway_shutdown
mv $RPM_BUILD_ROOT%{_sbindir}/zabbix_java/settings.sh $RPM_BUILD_ROOT%{_sysconfdir}/zabbix/zabbix_java_gateway.conf
mv $RPM_BUILD_ROOT%{_sbindir}/zabbix_java/lib/logback.xml $RPM_BUILD_ROOT%{_sysconfdir}/zabbix/zabbix_java_gateway_logback.xml
rm $RPM_BUILD_ROOT%{_sbindir}/zabbix_java/lib/logback-console.xml
mv $RPM_BUILD_ROOT%{_sbindir}/zabbix_java $RPM_BUILD_ROOT%{_datadir}/zabbix-java-gateway
install -Dm 0644 -p %{SOURCE13} $RPM_BUILD_ROOT%{_unitdir}/zabbix-java-gateway.service
install -Dm 0644 -p %{SOURCE15} $RPM_BUILD_ROOT%{_tmpfilesdir}/zabbix-java-gateway.conf
%endif


%if 0%{?build_selinux_policy}
mkdir -p $RPM_BUILD_ROOT%{_datadir}/selinux/packages/zabbix
mv zabbix_policy.pp $RPM_BUILD_ROOT%{_datadir}/selinux/packages/zabbix
%endif


%clean
rm -rf $RPM_BUILD_ROOT


#
# files & scriptlets
#


%if 0%{?build_agent}

%files agent
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README conf/zabbix_agentd/userparameter_mysql.conf
%config(noreplace) %{_sysconfdir}/zabbix/zabbix_agentd.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/zabbix-agent
%dir %{_sysconfdir}/zabbix/zabbix_agentd.d
%attr(0755,zabbix,zabbix) %dir %{_localstatedir}/log/zabbix
%attr(0755,zabbix,zabbix) %dir %{_localstatedir}/run/zabbix
%{_sbindir}/zabbix_agentd
%{_mandir}/man8/zabbix_agentd.8*
%if 0%{?rhel} >= 7 || %{amzn} >= 2023
%{_unitdir}/zabbix-agent.service
%{_tmpfilesdir}/zabbix-agent.conf
%else
%{_sysconfdir}/init.d/zabbix-agent
%config(noreplace) %{_sysconfdir}/sysconfig/zabbix-agent
%endif

%files get
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README
%{_bindir}/zabbix_get
%{_mandir}/man1/zabbix_get.1*

%files sender
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README
%{_bindir}/zabbix_sender
%{_mandir}/man1/zabbix_sender.1*

%pre agent
getent group zabbix > /dev/null || groupadd -r zabbix
getent passwd zabbix > /dev/null || \
	useradd -r -g zabbix -d %{_localstatedir}/lib/zabbix -s /sbin/nologin \
	-c "Zabbix Monitoring System" zabbix
:

%post agent
%if 0%{?rhel} >= 7 || %{amzn} >= 2023
%systemd_post zabbix-agent.service
%else
/sbin/chkconfig --add zabbix-agent || :
%endif

%preun agent
if [ "$1" = 0 ]; then
%if 0%{?rhel} >= 7 || %{amzn} >= 2023
%systemd_preun zabbix-agent.service
%else
/sbin/service zabbix-agent stop >/dev/null 2>&1
/sbin/chkconfig --del zabbix-agent
%endif
fi
:

%postun agent
%if 0%{?rhel} >= 7 || %{amzn} >= 2023
%systemd_postun_with_restart zabbix-agent.service
%else
if [ $1 -ge 1 ]; then
/sbin/service zabbix-agent try-restart >/dev/null 2>&1 || :
fi
%endif

%posttrans agent
# preserve old userparameter_mysql.conf file during upgrade
if [ -f %{_sysconfdir}/zabbix/zabbix_agentd.d/userparameter_mysql.conf.rpmsave ] && [ ! -f %{_sysconfdir}/zabbix/zabbix_agentd.d/userparameter_mysql.conf ]; then
       cp -vn %{_sysconfdir}/zabbix/zabbix_agentd.d/userparameter_mysql.conf.rpmsave %{_sysconfdir}/zabbix/zabbix_agentd.d/userparameter_mysql.conf
fi
:
%endif



%if 0%{?build_agent2}
%files agent2
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README
%config(noreplace) %{_sysconfdir}/zabbix/zabbix_agent2.conf
%dir %{_sysconfdir}/zabbix/zabbix_agent2.d
%config(noreplace) %{_sysconfdir}/zabbix/zabbix_agent2.d/plugins.d/ceph.conf
%config(noreplace) %{_sysconfdir}/zabbix/zabbix_agent2.d/plugins.d/docker.conf
%config(noreplace) %{_sysconfdir}/zabbix/zabbix_agent2.d/plugins.d/memcached.conf
%config(noreplace) %{_sysconfdir}/zabbix/zabbix_agent2.d/plugins.d/mysql.conf
%config(noreplace) %{_sysconfdir}/zabbix/zabbix_agent2.d/plugins.d/oracle.conf
%config(noreplace) %{_sysconfdir}/zabbix/zabbix_agent2.d/plugins.d/redis.conf
%config(noreplace) %{_sysconfdir}/zabbix/zabbix_agent2.d/plugins.d/smart.conf
%config(noreplace) %{_sysconfdir}/zabbix/zabbix_agent2.d/plugins.d/modbus.conf
%config(noreplace) %{_sysconfdir}/zabbix/zabbix_agent2.d/plugins.d/mqtt.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/zabbix-agent2
%attr(0755,zabbix,zabbix) %dir %{_localstatedir}/log/zabbix
%attr(0755,zabbix,zabbix) %dir %{_localstatedir}/run/zabbix
%{_sbindir}/zabbix_agent2
%{_mandir}/man8/zabbix_agent2.8*
%if 0%{?rhel} >= 7 || %{amzn} >= 2023
%{_unitdir}/zabbix-agent2.service
%{_tmpfilesdir}/zabbix_agent2.conf
%else
%{_sysconfdir}/init.d/zabbix-agent2
%config(noreplace) %{_sysconfdir}/sysconfig/zabbix-agent2
%endif

%pre agent2
getent group zabbix > /dev/null || groupadd -r zabbix
getent passwd zabbix > /dev/null || \
	useradd -r -g zabbix -d %{_localstatedir}/lib/zabbix -s /sbin/nologin \
	-c "Zabbix Monitoring System" zabbix
:

%post agent2
%if 0%{?rhel} >= 7 || %{amzn} >= 2023
%systemd_post zabbix-agent2.service
%endif
# make sure that agent2 log file is create with proper attributes (ZBX-18243)
if [ $1 == 1 ] && [ ! -f %{_localstatedir}/log/zabbix/zabbix_agent2.log ]; then
	touch %{_localstatedir}/log/zabbix/zabbix_agent2.log
	chown zabbix:zabbix %{_localstatedir}/log/zabbix/zabbix_agent2.log
fi
:

%if 0%{?rhel} >= 7 || %{amzn} >= 2023
%preun agent2
%systemd_preun zabbix-agent2.service
:

%postun agent2
%systemd_postun_with_restart zabbix-agent2.service
%endif
%endif


%if 0%{?build_web_service}
%files web-service
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README
%{_sbindir}/zabbix_web_service
%config(noreplace) %{_sysconfdir}/zabbix/zabbix_web_service.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/zabbix-web-service
%attr(0755,zabbix,zabbix) %dir %{_localstatedir}/log/zabbix
%attr(0755,zabbix,zabbix) %dir %{_localstatedir}/run/zabbix
%{_unitdir}/zabbix-web-service.service
%{_tmpfilesdir}/zabbix_web_service.conf
%{_mandir}/man8/zabbix_web_service.8*

%pre web-service
getent group zabbix > /dev/null || groupadd -r zabbix
getent passwd zabbix > /dev/null || \
	useradd -r -g zabbix -d %{_localstatedir}/lib/zabbix -s /sbin/nologin \
	-c "Zabbix Monitoring System" zabbix
:

%post web-service
%systemd_post zabbix-web-service.service
:

%preun web-service
%systemd_preun zabbix-web-service.service
:

%postun web-service
%systemd_postun_with_restart zabbix-web-service.service
%endif


%if 0%{?build_server} || 0%{?build_proxy}
%files js
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README
%{_bindir}/zabbix_js

%files sql-scripts
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README
%if 0%{?build_server}
%{_datadir}/zabbix-sql-scripts/mysql/server.sql.gz
%{_datadir}/zabbix-sql-scripts/mysql/double.sql
%{_datadir}/zabbix-sql-scripts/mysql/history_pk_prepare.sql
%{_datadir}/zabbix-sql-scripts/postgresql/server.sql.gz
%{_datadir}/zabbix-sql-scripts/postgresql/timescaledb.sql
%{_datadir}/zabbix-sql-scripts/postgresql/double.sql
%{_datadir}/zabbix-sql-scripts/postgresql/history_pk_prepare.sql
%endif
%if 0%{?build_proxy}
%{_datadir}/zabbix-sql-scripts/mysql/proxy.sql
%{_datadir}/zabbix-sql-scripts/postgresql/proxy.sql
%{_datadir}/zabbix-sql-scripts/sqlite3/proxy.sql
%endif
%if 0%{?build_server} || 0%{?build_proxy}
%{_datadir}/zabbix-sql-scripts/postgresql/tsdb_history_pk_upgrade_no_compression/history_pk_log.sql
%{_datadir}/zabbix-sql-scripts/postgresql/tsdb_history_pk_upgrade_no_compression/history_pk.sql
%{_datadir}/zabbix-sql-scripts/postgresql/tsdb_history_pk_upgrade_no_compression/history_pk_str.sql
%{_datadir}/zabbix-sql-scripts/postgresql/tsdb_history_pk_upgrade_no_compression/history_pk_text.sql
%{_datadir}/zabbix-sql-scripts/postgresql/tsdb_history_pk_upgrade_no_compression/history_pk_uint.sql
%{_datadir}/zabbix-sql-scripts/postgresql/tsdb_history_pk_upgrade_with_compression/history_pk_log.sql
%{_datadir}/zabbix-sql-scripts/postgresql/tsdb_history_pk_upgrade_with_compression/history_pk.sql
%{_datadir}/zabbix-sql-scripts/postgresql/tsdb_history_pk_upgrade_with_compression/history_pk_str.sql
%{_datadir}/zabbix-sql-scripts/postgresql/tsdb_history_pk_upgrade_with_compression/history_pk_text.sql
%{_datadir}/zabbix-sql-scripts/postgresql/tsdb_history_pk_upgrade_with_compression/history_pk_uint.sql
%endif
%endif


%if 0%{?build_proxy}
%if 0%{?build_with_mysql}
%files proxy-mysql
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README
%attr(0600,root,zabbix) %config(noreplace) %{_sysconfdir}/zabbix/zabbix_proxy.conf
%dir %{zabbix_script_dir}/externalscripts
%config(noreplace) %{_sysconfdir}/logrotate.d/zabbix-proxy
%attr(0755,zabbix,zabbix) %dir %{_localstatedir}/log/zabbix
%attr(0755,zabbix,zabbix) %dir %{_localstatedir}/run/zabbix
%{_mandir}/man8/zabbix_proxy.8*
%{_unitdir}/zabbix-proxy.service
%{_tmpfilesdir}/zabbix-proxy.conf
%{_sbindir}/zabbix_proxy_mysql

%pre proxy-mysql
getent group zabbix > /dev/null || groupadd -r zabbix
getent passwd zabbix > /dev/null || \
	useradd -r -g zabbix -d %{_localstatedir}/lib/zabbix -s /sbin/nologin \
	-c "Zabbix Monitoring System" zabbix
:

%post proxy-mysql
%systemd_post zabbix-proxy.service
/usr/sbin/update-alternatives --install %{_sbindir}/zabbix_proxy \
	zabbix-proxy %{_sbindir}/zabbix_proxy_mysql 10
:

%preun proxy-mysql
if [ "$1" = 0 ]; then
%systemd_preun zabbix-proxy.service
/usr/sbin/update-alternatives --remove zabbix-proxy \
%{_sbindir}/zabbix_proxy_mysql
fi
:

%postun proxy-mysql
%systemd_postun_with_restart zabbix-proxy.service
:
%endif


%if 0%{?build_with_pgsql}
%files proxy-pgsql
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README
%attr(0600,root,zabbix) %config(noreplace) %{_sysconfdir}/zabbix/zabbix_proxy.conf
%dir %{zabbix_script_dir}/externalscripts
%config(noreplace) %{_sysconfdir}/logrotate.d/zabbix-proxy
%attr(0755,zabbix,zabbix) %dir %{_localstatedir}/log/zabbix
%attr(0755,zabbix,zabbix) %dir %{_localstatedir}/run/zabbix
%{_mandir}/man8/zabbix_proxy.8*
%{_unitdir}/zabbix-proxy.service
%{_tmpfilesdir}/zabbix-proxy.conf
%{_sbindir}/zabbix_proxy_pgsql

%pre proxy-pgsql
getent group zabbix > /dev/null || groupadd -r zabbix
getent passwd zabbix > /dev/null || \
	useradd -r -g zabbix -d %{_localstatedir}/lib/zabbix -s /sbin/nologin \
	-c "Zabbix Monitoring System" zabbix
:

%post proxy-pgsql
%systemd_post zabbix-proxy.service
/usr/sbin/update-alternatives --install %{_sbindir}/zabbix_proxy \
	zabbix-proxy %{_sbindir}/zabbix_proxy_pgsql 10
:

%preun proxy-pgsql
if [ "$1" = 0 ]; then
%systemd_preun zabbix-proxy.service
/usr/sbin/update-alternatives --remove zabbix-proxy \
	%{_sbindir}/zabbix_proxy_pgsql
fi
:

%postun proxy-pgsql
%systemd_postun_with_restart zabbix-proxy.service
:
%endif


%if 0%{?build_with_sqlite}
%files proxy-sqlite3
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README
%attr(0640,root,zabbix) %config(noreplace) %{_sysconfdir}/zabbix/zabbix_proxy.conf
%dir %{zabbix_script_dir}/externalscripts
%config(noreplace) %{_sysconfdir}/logrotate.d/zabbix-proxy
%attr(0755,zabbix,zabbix) %dir %{_localstatedir}/log/zabbix
%attr(0755,zabbix,zabbix) %dir %{_localstatedir}/run/zabbix
%{_mandir}/man8/zabbix_proxy.8*
%{_unitdir}/zabbix-proxy.service
%{_tmpfilesdir}/zabbix-proxy.conf
%{_sbindir}/zabbix_proxy_sqlite3

%pre proxy-sqlite3
getent group zabbix > /dev/null || groupadd -r zabbix
getent passwd zabbix > /dev/null || \
	useradd -r -g zabbix -d %{_localstatedir}/lib/zabbix -s /sbin/nologin \
	-c "Zabbix Monitoring System" zabbix
:

%post proxy-sqlite3
%systemd_post zabbix-proxy.service
/usr/sbin/update-alternatives --install %{_sbindir}/zabbix_proxy \
	zabbix-proxy %{_sbindir}/zabbix_proxy_sqlite3 10
:

%preun proxy-sqlite3
if [ "$1" = 0 ]; then
%systemd_preun zabbix-proxy.service
/usr/sbin/update-alternatives --remove zabbix-proxy \
	%{_sbindir}/zabbix_proxy_sqlite3
fi
:

%postun proxy-sqlite3
%systemd_postun_with_restart zabbix-proxy.service
:
%endif
%endif


%if 0%{?build_server}
%if 0%{?build_with_mysql}
%files server-mysql
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README
%attr(0600,root,zabbix) %config(noreplace) %{_sysconfdir}/zabbix/zabbix_server.conf
%dir %{zabbix_script_dir}/alertscripts
%dir %{zabbix_script_dir}/externalscripts
%config(noreplace) %{_sysconfdir}/logrotate.d/zabbix-server
%attr(0755,zabbix,zabbix) %dir %{_localstatedir}/log/zabbix
%attr(0755,zabbix,zabbix) %dir %{_localstatedir}/run/zabbix
%{_mandir}/man8/zabbix_server.8*
%{_unitdir}/zabbix-server.service
%{_tmpfilesdir}/zabbix-server.conf
%{_sbindir}/zabbix_server_mysql

%pre server-mysql
getent group zabbix > /dev/null || groupadd -r zabbix
getent passwd zabbix > /dev/null || \
	useradd -r -g zabbix -d %{_localstatedir}/lib/zabbix -s /sbin/nologin \
	-c "Zabbix Monitoring System" zabbix
:

%post server-mysql
%systemd_post zabbix-server.service
/usr/sbin/update-alternatives --install %{_sbindir}/zabbix_server \
	zabbix-server %{_sbindir}/zabbix_server_mysql 10
:

%preun server-mysql
if [ "$1" = 0 ]; then
%systemd_preun zabbix-server.service
/usr/sbin/update-alternatives --remove zabbix-server \
	%{_sbindir}/zabbix_server_mysql
fi
:

%postun server-mysql
%systemd_postun_with_restart zabbix-server.service
:
%endif


%if 0%{?build_with_pgsql}
%files server-pgsql
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README
%attr(0600,root,zabbix) %config(noreplace) %{_sysconfdir}/zabbix/zabbix_server.conf
%dir %{zabbix_script_dir}/alertscripts
%dir %{zabbix_script_dir}/externalscripts
%config(noreplace) %{_sysconfdir}/logrotate.d/zabbix-server
%attr(0755,zabbix,zabbix) %dir %{_localstatedir}/log/zabbix
%attr(0755,zabbix,zabbix) %dir %{_localstatedir}/run/zabbix
%{_mandir}/man8/zabbix_server.8*
%{_unitdir}/zabbix-server.service
%{_tmpfilesdir}/zabbix-server.conf
%{_sbindir}/zabbix_server_pgsql

%pre server-pgsql
getent group zabbix > /dev/null || groupadd -r zabbix
getent passwd zabbix > /dev/null || \
	useradd -r -g zabbix -d %{_localstatedir}/lib/zabbix -s /sbin/nologin \
	-c "Zabbix Monitoring System" zabbix
:

%post server-pgsql
%systemd_post zabbix-server.service
/usr/sbin/update-alternatives --install %{_sbindir}/zabbix_server \
	zabbix-server %{_sbindir}/zabbix_server_pgsql 10
:

%preun server-pgsql
if [ "$1" = 0 ]; then
%systemd_preun zabbix-server.service
/usr/sbin/update-alternatives --remove zabbix-server \
	%{_sbindir}/zabbix_server_pgsql
fi
:

%postun server-pgsql
%systemd_postun_with_restart zabbix-server.service
:
%endif
%endif


%if 0%{?build_frontend}
%files web
%defattr(-,root,root,-)
%dir %{_sysconfdir}/zabbix/web
%ghost %config(noreplace) %{_sysconfdir}/zabbix/web/zabbix.conf.php
%doc AUTHORS ChangeLog COPYING NEWS README
%config(noreplace) %{_sysconfdir}/zabbix/web/maintenance.inc.php
%{_datadir}/zabbix

%files web-deps
%config(noreplace) %{_sysconfdir}/php-fpm.d/zabbix.conf

%files web-japanese
%defattr(-,root,root,-)

%files web-mysql
%defattr(-,root,root,-)

%files web-pgsql
%defattr(-,root,root,-)

%files apache-conf
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/httpd/conf.d/zabbix.conf

%files nginx-conf
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/nginx/conf.d/zabbix.conf

%post web
# The fonts directory was moved into assets subdirectory at one point.
#
# This broke invocation of update-alternatives command below, because the target link for zabbix-web-font changed
# from zabbix/fonts/graphfont.ttf to zabbix/assets/fonts/graphfont.ttf
#
# We handle this movement by deleting /var/lib/alternatives/zabbix-web-font file if it contains the old target link.
# We also remove symlink at zabbix/fonts/graphfont.ttf to have the old fonts directory be deleted during update.
if [ -f /var/lib/alternatives/zabbix-web-font ] && \
	[ -z "$(grep %{_datadir}/zabbix/assets/fonts/graphfont.ttf /var/lib/alternatives/zabbix-web-font)" ]
then
	rm /var/lib/alternatives/zabbix-web-font
	if [ -h %{_datadir}/zabbix/fonts/graphfont.ttf ]; then
		rm %{_datadir}/zabbix/fonts/graphfont.ttf
	fi
fi
%if 0%{?rhel} >= 9 || %{amzn} >= 2023
# remove bad link to fonts/dejavu/DejaVuSans.ttf during upgrade on rhel 9
if [ "$1" = 2 ]; then
	/usr/sbin/update-alternatives --remove zabbix-web-font \
		%{_datadir}/fonts/dejavu/DejaVuSans.ttf
fi
%endif
/usr/sbin/update-alternatives --install %{_datadir}/zabbix/assets/fonts/graphfont.ttf \
%if 0%{?rhel} >= 9 || %{amzn} >= 2023
	zabbix-web-font %{_datadir}/fonts/dejavu-sans-fonts/DejaVuSans.ttf 10
%else
	zabbix-web-font %{_datadir}/fonts/dejavu/DejaVuSans.ttf 10
%endif
:

%post web-japanese
/usr/sbin/update-alternatives --install %{_datadir}/zabbix/assets/fonts/graphfont.ttf zabbix-web-font \
	%{_datadir}/fonts/google-noto-cjk/NotoSansCJK-Regular.ttc 20
:

# The user apache must be available for these to work.
# It is provided by httpd or php-fpm packages.
%post apache-conf
if [ -d /etc/zabbix/web ]; then
	chown apache:apache /etc/zabbix/web/
fi
:

%post nginx-conf
if [ -d /etc/zabbix/web ]; then
	chown apache:apache /etc/zabbix/web/
fi
:

%preun web
if [ "$1" = 0 ]; then
%if 0%{?rhel} >= 9 || %{amzn} >= 2023
/usr/sbin/update-alternatives --remove zabbix-web-font \
	%{_datadir}/fonts/dejavu-sans-fonts/DejaVuSans.ttf
%else
/usr/sbin/update-alternatives --remove zabbix-web-font \
	%{_datadir}/fonts/dejavu/DejaVuSans.ttf
%endif
fi
:

%preun web-japanese
if [ "$1" = 0 ]; then
/usr/sbin/update-alternatives --remove zabbix-web-font \
	%{_datadir}/fonts/google-noto-cjk/NotoSansCJK-Regular.ttc
fi
:
%endif


%if 0%{?build_java_gateway}
%files java-gateway
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README
%config(noreplace) %{_sysconfdir}/zabbix/zabbix_java_gateway.conf
%attr(0755,zabbix,zabbix) %dir %{_localstatedir}/log/zabbix
%attr(0755,zabbix,zabbix) %dir %{_localstatedir}/run/zabbix
%{_datadir}/zabbix-java-gateway
%{_sbindir}/zabbix_java_gateway_startup
%{_sbindir}/zabbix_java_gateway_shutdown
%{_unitdir}/zabbix-java-gateway.service
%{_tmpfilesdir}/zabbix-java-gateway.conf
%config(noreplace) %{_sysconfdir}/zabbix/zabbix_java_gateway_logback.xml

%pre java-gateway
getent group zabbix > /dev/null || groupadd -r zabbix
getent passwd zabbix > /dev/null || \
	useradd -r -g zabbix -d %{_localstatedir}/lib/zabbix -s /sbin/nologin \
	-c "Zabbix Monitoring System" zabbix
:

%post java-gateway
%systemd_post zabbix-java-gateway.service
:

%preun java-gateway
if [ $1 -eq 0 ]; then
%systemd_preun zabbix-java-gateway.service
fi
:

%postun java-gateway
%systemd_postun_with_restart zabbix-java-gateway.service
:
%endif


%if 0%{?build_selinux_policy}
%files selinux-policy
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README
%{_datadir}/selinux/packages/zabbix/zabbix_policy.pp


%post selinux-policy
semodule -i %{_datadir}/selinux/packages/zabbix/zabbix_policy.pp
:

%postun selinux-policy
if [ $1 = 0 ] && semodule -l | grep -q zabbix_policy; then semodule -r zabbix_policy; fi
:
%endif


%changelog
* Mon Jan 31 2025 Zabbix Packager <info@zabbix.com> - 6.0.38-release2
- fixed IPMI pollers

* Mon Jan 27 2025 Zabbix Packager <info@zabbix.com> - 6.0.38-release1
- update to 6.0.38

* Mon Jan 20 2025 Zabbix Packager <info@zabbix.com> - 6.0.38-rc1.release1
- update to 6.0.38rc1
- fixed path to optional database patches

* Tue Dec 17 2024 Zabbix Packager <info@zabbix.com> - 6.0.37-release1
- update to 6.0.37
- added support for amazon linux 2023

* Wed Dec 11 2024 Zabbix Packager <info@zabbix.com> - 6.0.37-rc1.release1
- update to 6.0.37rc1

* Tue Nov 19 2024 Zabbix Packager <info@zabbix.com> - 6.0.36-release1
- update to 6.0.36

* Tue Nov 12 2024 Zabbix Packager <info@zabbix.com> - 6.0.36-rc1.release1
- update to 6.0.36rc1

* Mon Oct 21 2024 Zabbix Packager <info@zabbix.com> - 6.0.35-release1
- update to 6.0.35

* Mon Oct 14 2024 Zabbix Packager <info@zabbix.com> - 6.0.35-rc1.release1
- update to 6.0.35rc1

* Thu Sep 27 2024 Zabbix Packager <info@zabbix.com> - 6.0.34-release2
- added OpenSSL compilation flags

* Thu Sep 26 2024 Zabbix Packager <info@zabbix.com> - 6.0.34-release1
- update to 6.0.34

* Tue Sep 24 2024 Zabbix Packager <info@zabbix.com> - 6.0.34-rc2.release1
- update to 6.0.34rc2

* Mon Sep 16 2024 Zabbix Packager <info@zabbix.com> - 6.0.34-rc1.release1
- update to 6.0.34rc1

* Tue Aug 13 2024 Zabbix Packager <info@zabbix.com> - 6.0.33-release2
- update to 6.0.33

* Tue Aug 06 2024 Zabbix Packager <info@zabbix.com> - 6.0.33-rc1.release2
- second release of 6.0.33rc1

* Tue Aug 06 2024 Zabbix Packager <info@zabbix.com> - 6.0.33-rc1.release1
- update to 6.0.33rc1

* Mon Jul 15 2024 Zabbix Packager <info@zabbix.com> - 6.0.32-release1
- update to 6.0.32

* Tue Jul 09 2024 Zabbix Packager <info@zabbix.com> - 6.0.32-rc1.release1
- update to 6.0.32rc1

* Mon Jun 17 2024 Zabbix Packager <info@zabbix.com> - 6.0.31-release1
- update to 6.0.31

* Mon Jun 10 2024 Zabbix Packager <info@zabbix.com> - 6.0.31-rc1.release1
- update to 6.0.31rc1

* Tue May 21 2024 Zabbix Packager <info@zabbix.com> - 6.0.30-release1
- update to 6.0.30

* Wed May 15 2024 Zabbix Packager <info@zabbix.com> - 6.0.30-rc1.release1
- update to 6.0.30rc1

* Mon Apr 22 2024 Zabbix Packager <info@zabbix.com> - 6.0.29-release1
- update to 6.0.29

* Mon Apr 15 2024 Zabbix Packager <info@zabbix.com> - 6.0.29-rc1.release1
- update to 6.0.29rc1

* Mon Mar 25 2024 Zabbix Packager <info@zabbix.com> - 6.0.28-release1
- update to 6.0.28

* Mon Mar 18 2024 Zabbix Packager <info@zabbix.com> - 6.0.28-rc1.release1
- update to 6.0.28rc1

* Mon Feb 26 2024 Zabbix Packager <info@zabbix.com> - 6.0.27-release1
- update to 6.0.27

* Mon Feb 19 2024 Zabbix Packager <info@zabbix.com> - 6.0.27-rc1.release1
- update to 6.0.27rc1

* Mon Jan 29 2024 Zabbix Packager <info@zabbix.com> - 6.0.26-release1
- update to 6.0.26

* Mon Jan 22 2024 Zabbix Packager <info@zabbix.com> - 6.0.26-rc1.release1
- update to 6.0.26rc1

* Wed Dec 13 2023 Zabbix Packager <info@zabbix.com> - 6.0.25-release1
- update to 6.0.25

* Thu Dec 07 2023 Zabbix Packager <info@zabbix.com> - 6.0.25-rc1.release1
- update to 6.0.25rc1

* Thu Nov 30 2023 Zabbix Packager <info@zabbix.com> - 6.0.24-release1
- update to 6.0.24

* Thu Nov 23 2023 Zabbix Packager <info@zabbix.com> - 6.0.24-rc1.release1
- update to 6.0.24rc1
- added After statements for postgresql 15 and 16 to server and proxy systemd unit files

* Tue Oct 31 2023 Zabbix Packager <info@zabbix.com> - 6.0.23-release1
- update to 6.0.23

* Mon Oct 23 2023 Zabbix Packager <info@zabbix.com> - 6.0.23-rc1.release1
- update to 6.0.23rc1

* Mon Sep 25 2023 Zabbix Packager <info@zabbix.com> - 6.0.22-release1
- update to 6.0.22

* Tue Sep 19 2023 Zabbix Packager <info@zabbix.com> - 6.0.22-rc1.release1
- update to 6.0.22rc1

* Wed Sep 06 2023 Zabbix Packager <info@zabbix.com> - 6.0.21-release2
- added support for aarch64

* Tue Aug 22 2023 Zabbix Packager <info@zabbix.com> - 6.0.21-release1
- update to 6.0.21

* Tue Aug 15 2023 Zabbix Packager <info@zabbix.com> - 6.0.21-rc1.release1
- update to 6.0.21rc1
- fixed web_service logrotate configuration file (ZBX-23169)

* Mon Jul 31 2023 Zabbix Packager <info@zabbix.com> - 6.0.20-release1
- update to 6.0.20

* Mon Jul 24 2023 Zabbix Packager <info@zabbix.com> - 6.0.20-rc1.release1
- update to 6.0.20rc1

* Tue Jun 27 2023 Zabbix Packager <info@zabbix.com> - 6.0.19-release1
- update to 6.0.19

* Mon Jun 19 2023 Zabbix Packager <info@zabbix.com> - 6.0.19-rc1.release1
- update to 6.0.19rc1

* Tue May 30 2023 Zabbix Packager <info@zabbix.com> - 6.0.18-release1
- update to 6.0.18

* Mon May 22 2023 Zabbix Packager <info@zabbix.com> - 6.0.18-rc1.release1
- update to 6.0.18rc1

* Mon Apr 24 2023 Zabbix Packager <info@zabbix.com> - 6.0.17-release1
- update to 6.0.17

* Wed Apr 19 2023 Zabbix Packager <info@zabbix.com> - 6.0.17-rc2.release1
- update to 6.0.17rc2

* Mon Apr 17 2023 Zabbix Packager <info@zabbix.com> - 6.0.17-rc1.release1
- update to 6.0.17rc1

* Tue Apr 11 2023 Zabbix Packager <info@zabbix.com> - 6.0.16-release1
- update to 6.0.16

* Wed Apr 05 2023 Zabbix Packager <info@zabbix.com> - 6.0.16-rc1.release1
- update to 6.0.16rc1

* Fri Mar 31 2023 Zabbix Packager <info@zabbix.com> - 6.0.15-release1
- update to 6.0.15

* Wed Mar 29 2023 Zabbix Packager <info@zabbix.com> - 6.0.15-rc2.release1
- update to 6.0.15rc2

* Wed Mar 22 2023 Zabbix Packager <info@zabbix.com> - 6.0.15-rc1.release1
- update to 6.0.15rc1

* Wed Mar 08 2023 Zabbix Packager <info@zabbix.com> - 6.0.14-release1
- update to 6.0.14

* Mon Feb 27 2023 Zabbix Packager <info@zabbix.com> - 6.0.14-rc2.release1
- update to 6.0.14rc2

* Mon Feb 20 2023 Zabbix Packager <info@zabbix.com> - 6.0.14-rc1.release1
- update to 6.0.14rc1
- removed c99-1.patch; use -std=gnu99 compiler flag instead

* Wed Feb 01 2023 Zabbix Packager <info@zabbix.com> - 6.0.13-release1
- update to 6.0.13

* Fri Jan 27 2023 Zabbix Packager <info@zabbix.com> - 6.0.13-rc1.release1
- update to 6.0.13rc1
- added LimitNOFILE=8192 to agent2 systemd service file (ZBX-22061)
- added agent2.conf.socket.patch (ZBX-22061)
- added c99-1.patch

* Mon Dec 05 2022 Zabbix Packager <info@zabbix.com> - 6.0.12-release1
- update to 6.0.12

* Fri Dec 02 2022 Zabbix Packager <info@zabbix.com> - 6.0.12-rc2.release1
- update to 6.0.12rc2

* Thu Dec 01 2022 Zabbix Packager <info@zabbix.com> - 6.0.12-rc1.release1
- update to 6.0.12rc1

* Mon Nov 28 2022 Zabbix Packager <info@zabbix.com> - 6.0.11-release1
- update to 6.0.11

* Fri Nov 25 2022 Zabbix Packager <info@zabbix.com> - 6.0.11-rc2.release1
- update to 6.0.11rc2

* Mon Nov 21 2022 Zabbix Packager <info@zabbix.com> - 6.0.11-rc1.release1
- update to 6.0.11rc1

* Wed Nov 16 2022 Zabbix Packager <info@zabbix.com> - 6.0.10-release2
- added explicit dependencies on mongodb and postgresql plugins to agent2; to ease upgrade

* Wed Nov 02 2022 Zabbix Packager <info@zabbix.com> - 6.0.10-release1
- update to 6.0.10

* Thu Oct 27 2022 Zabbix Packager <info@zabbix.com> - 6.0.10-rc2.release1
- update to 6.0.10rc2

* Tue Oct 25 2022 Zabbix Packager <info@zabbix.com> - 6.0.10-rc1.release1
- update to 6.0.10rc1
- removed agent2 builtin postgres.conf file; to be replaced with a plugin

* Wed Sep 21 2022 Zabbix Packager <info@zabbix.com> - 6.0.9-release1
- update to 6.0.9

* Mon Sep 19 2022 Zabbix Packager <info@zabbix.com> - 6.0.9-rc2.release1
- update to 6.0.9rc2

* Wed Sep 14 2022 Zabbix Packager <info@zabbix.com> - 6.0.9-rc1.release1
- update to 6.0.9rc1
- moved zabbix-sql-scripts contents out of system documentation and into data directory
- added new postgresql files to sql-scripts package

* Tue Aug 30 2022 Zabbix Packager <info@zabbix.com> - 6.0.8-release2
- second release of 6.0.8 for rhel-9
- fixed path to DejaVuSans font

* Mon Aug 29 2022 Zabbix Packager <info@zabbix.com> - 6.0.8-release1
- update to 6.0.8
- added "release" prefix to package version

* Mon Jul 25 2022 Zabbix Packager <info@zabbix.com> - 6.0.7-1
- update to 6.0.7

* Wed Jun 29 2022 Zabbix Packager <info@zabbix.com> - 6.0.6-2
- fixed postun selinux-policy scriptlet

* Mon Jun 27 2022 Zabbix Packager <info@zabbix.com> - 6.0.6-1
- update to 6.0.6
- removed mongodb from agent2, expecting to use external plugin
- reverted /run to /var/run in conf files using patches 6 & 7 for rhel <= 6
- fixed bogus systemd scriptlet for agent2 on rhel < 7
- silencing agent2 interactive output on rhel 6 (ZBX-20456)

* Mon May 30 2022 Zabbix Packager <info@zabbix.com> - 6.0.5-1
- update to 6.0.5
- added After=postgresql-14.service to server and proxy systemd service files

* Tue May 03 2022 Zabbix Packager <info@zabbix.com> - 6.0.4-1
- update to 6.0.4
- added rhel6-go11.6.patch
- replaced /var/run with /run
- updated selinux-policy to allow web servers connecting to postgres via socket
- fixed selinux-policy postun scriptlet

* Mon Apr 04 2022 Zabbix Packager <info@zabbix.com> - 6.0.3-1
- update to 6.0.3

* Mon Mar 14 2022 Zabbix Packager <info@zabbix.com> - 6.0.2-1
- update to 6.0.2

* Tue Mar 01 2022 Zabbix Packager <info@zabbix.com> - 6.0.1-1
- update to 6.0.1
- fixed EnvironmentFile setting in web-service systemd service file

* Mon Feb 14 2022 Zabbix Packager <info@zabbix.com> - 6.0.0-1
- update to 6.0.0

* Fri Feb 04 2022 Zabbix Packager <info@zabbix.com> - 6.0.0-0.12rc2
- update to 6.0.0rc2

* Tue Feb 01 2022 Zabbix Packager <info@zabbix.com> - 6.0.0-0.11rc1
- update to 6.0.0rc1

* Tue Jan 25 2022 Zabbix Packager <info@zabbix.com> - 6.0.0-0.10beta3
- update to 6.0.0beta3

* Tue Jan 11 2022 Zabbix Packager <info@zabbix.com> - 6.0.0-0.9beta2
- update to 6.0.0beta2
- using pcre2 on rhel >= 7
- added history_pk_prepare.sql to sql-scripts package

* Mon Dec 13 2021 Zabbix Packager <info@zabbix.com> - 6.0.0-0.8beta1
- update to 6.0.0beta1
- removed erronious references to tmpfiles.d on rhel < 7 and fixed _tmpfilesdir macro usage
- removed "Obsoletes: zabbix" for web-servce sub-package
- renamed create.sql.gz to server.sql.gz
- renamed schema.sql to proxy.sql
- compressing only server.sql.gz

* Mon Nov 22 2021 Zabbix Packager <info@zabbix.com> - 6.0.0-0.7alpha7
- update to 6.0.0alpha7

* Tue Nov 09 2021 Zabbix Packager <info@zabbix.com> - 6.0.0-0.6alpha6
- update to 6.0.0alpha6

* Mon Oct 25 2021 Zabbix Packager <info@zabbix.com> - 6.0.0-0.5alpha5
- update to 6.0.0alpha5
- separated agent2 plugin conf files (ZBXNEXT-6428)
- updated php-fpm conf files (ZBX-20106)

* Wed Oct 06 2021 Zabbix Packager <info@zabbix.com> - 6.0.0-0.4alpha4
- update to 6.0.0alpha4

* Mon Sep 20 2021 Zabbix Packager <info@zabbix.com> - 6.0.0-0.3alpha3
- update to 6.0.0alpha3

* Mon Sep 06 2021 Zabbix Packager <info@zabbix.com> - 6.0.0-0.2alpha2
- update to 6.0.0alpha2

* Wed Aug 25 2021 Zabbix Packager <info@zabbix.com> - 6.0.0-0.1alpha1
- update to 6.0.0alpha1
- added selinux-policy package (rhel 7+)

* Wed Jul 21 2021 Zabbix Packager <info@zabbix.com> - 5.4.3-1
- update to 5.4.3

* Mon Jun 28 2021 Zabbix Packager <info@zabbix.com> - 5.4.2-1
- update to 5.4.2

* Mon Jun 07 2021 Zabbix Packager <info@zabbix.com> - 5.4.1-1
- update to 5.4.1
- removed bogus PIDFile from zabbix-web-service.service file
- using conditionals around sub-package definition blocks; fixed wrong arch in rhel-5 package names
- denying web server access to vendor subdir in /usr/share/zabbix
- renamed config.patch to frontend.patch
- replaced conf file sed substitutions with patches

* Thu May 27 2021 Zabbix Packager <info@zabbix.com> - 5.4.0-9
- second build of 5.4.0 agent2
- fixed LogFile path substitution for agent2

* Fri May 14 2021 Zabbix Packager <info@zabbix.com> - 5.4.0-8
- update to 5.4.0
- setting EXTERNAL_SCRIPTS_PATH and ALERT_SCRIPTS_PATH make variables to /usr/lib/zabbix/*

* Thu May 13 2021 Zabbix Packager <info@zabbix.com> - 5.4.0-0.8rc2
- update to 5.4.0rc2

* Tue May 11 2021 Zabbix Packager <info@zabbix.com> - 5.4.0-0.7rc1
- update to 5.4.0rc1

* Mon Apr 26 2021 Zabbix Packager <info@zabbix.com> - 5.4.0-0.6beta3
- update to 5.4.0beta3
- added zabbix-web-service package (ZBXNEXT-6480)

* Thu Mar 11 2021 Zabbix Packager <info@zabbix.com> - 5.4.0-0.5beta2
- update to 5.4.0beta2
- fixed errors and warnings reported by rpmlint
- added ProxyTimeout 300 to apache config, when running with php-fpm
- removed database subdir from sql-scripts package
- added After=postgresql-13.service to server & proxy service files

* Mon Mar 01 2021 Zabbix Packager <info@zabbix.com> - 5.4.0-0.4beta1
- update to 5.4.0beta1

* Thu Feb 18 2021 Zabbix Packager <info@zabbix.com> - 5.4.0-0.3alpha2
- update to 5.4.0alpha2
- updated java-gateway package to use startup and shutdown scripts from zabbix sources

* Thu Jan 28 2021 Zabbix Packager <info@zabbix.com> - 5.4.0-0.2alpha1
- second build of 5.4.0alpha1
- fixed BuildArch and files section for zabbix-sql-scripts package

* Thu Jan 28 2021 Zabbix Packager <info@zabbix.com> - 5.4.0-0.1alpha1
- update to 5.4.0alpha1
- reworked spec file to allow selecting which packages are being built via macros (ZBX-18826)

* Mon Dec 21 2020 Zabbix Packager <info@zabbix.com> - 5.2.3-1
- update to 5.2.3

* Mon Nov 30 2020 Zabbix Packager <info@zabbix.com> - 5.2.2-1
- update to 5.2.2
- added proxy and java-gateway to rhel-7

* Fri Oct 30 2020 Zabbix Packager <info@zabbix.com> - 5.2.1-1
- update to 5.2.1

* Mon Oct 26 2020 Zabbix Packager <info@zabbix.com> - 5.2.0-1
- update to 5.2.0

* Thu Oct 22 2020 Zabbix Packager <info@zabbix.com> - 5.2.0-0.7rc2
- update to 5.2.0rc2

* Tue Oct 20 2020 Zabbix Packager <info@zabbix.com> - 5.2.0-0.6rc1
- update to 5.2.0rc1

* Mon Oct 12 2020 Zabbix Packager <info@zabbix.com> - 5.2.0-0.5beta2
- update to 5.2.0beta2

* Mon Sep 28 2020 Zabbix Packager <info@zabbix.com> - 5.2.0-0.4beta1
- update to 5.2.0beta1
- added User=zabbix & Group=zabbix to all service files

* Mon Sep 14 2020 Zabbix Packager <info@zabbix.com> - 5.2.0-0.3alpha3
- update to 5.2.0alpha3
- added separate zabbix-web-deps package
- doing hardened builds on rhel >= 8
- removed libyaml.patch
- overriding ExternalScripts & AlertScriptsPath in binaries instead of config files (ZBX-17983)

* Mon Aug 31 2020 Zabbix Packager <info@zabbix.com> - 5.2.0-0.2alpha2
- update to 5.2.0alpha2
- building only agent, sender & get packages on rhel <= 7
- creating empty log file for agent2 (ZBX-18243)

* Mon Aug 17 2020 Zabbix Packager <info@zabbix.com> - 5.2.0-0.1alpha1
- update to 5.2.0alpha1
- building server and proxy with mysql 8 & postgresql 12 on rhel/centos 7 (ZBX-18221)
- added various After=postgresql* directives to server & proxy service files (ZBX-17492)

* Mon Jul 13 2020 Zabbix Packager <info@zabbix.com> - 5.0.2-1
- update to 5.0.2
- removed ZBX-17801 patch
- added "if build_agent2" around zabbix_agent2.conf installation (ZBX-17818)

* Thu May 28 2020 Zabbix Packager <info@zabbix.com> - 5.0.1-1
- update to 5.0.1
- changed mysql build dependency on rhel/centos-8 from mysql-devel to mariadb-connector-c-devel (ZBX-17738)
- added patch that fixes (ZBX-17801)

* Mon May 11 2020 Zabbix Packager <info@zabbix.com> - 5.0.0-1
- update to 5.0.0

* Tue May 05 2020 Zabbix Packager <info@zabbix.com> - 5.0.0-0.7rc1
- update to 5.0.0rc1
- moved frontends/php to ui directory

* Mon Apr 27 2020 Zabbix Packager <info@zabbix.com> - 5.0.0-0.6beta2
- update to 5.0.0beta2

* Tue Apr 14 2020 Zabbix Packager <info@zabbix.com> - 5.0.0-0.5beta1
- update to 5.0.0beta1
- added agent2 on rhel/centos 7

* Mon Mar 30 2020 Zabbix Packager <info@zabbix.com> - 5.0.0-0.4alpha4
- update to 5.0.0alpha4
- removed proxy, java-gateway & js packages on rhel 5 & 6 due to minimum supported database version increase

* Mon Mar 16 2020 Zabbix Packager <info@zabbix.com> - 5.0.0-0.3alpha3
- update to 5.0.0alpha3
- using libssh instead of libssh2 (rhel/centos 8)
- removed explicit dependency on php from zabbix-web (rhel/centos 8)
- removed explicit dependency on httpd from zabbix-web (rhel/centos 7)
- added zabbix-apache-conf (rhel/centos 7)
- using zabbix-web-database-scl as zabbix-(apache/nginx)-conf package dependency (rhel/centos 7)

* Mon Feb 17 2020 Zabbix Packager <info@zabbix.com> - 5.0.0-0.2alpha2
- update to 5.0.0alpha2
- fixed font configuration in pre/post scriptlets on rhel-8

* Wed Feb 05 2020 Zabbix Packager <info@zabbix.com> - 5.0.0-0.2alpha1
- added *-scl packages to help with resolving php7.2+ and nginx dependencies of zabbix frontend on rhel/centos 7
- added posttrans script that preserves /etc/zabbix/zabbix_agentd.d/userparameter_mysql.conf file
- added config(noreplace) to /etc/sysconfig/zabbix-agent
- added explicit version to php-module dependencies in zabbix-web package on rhel/centos 8

* Mon Jan 27 2020 Zabbix Packager <info@zabbix.com> - 5.0.0-0.1alpha1
- update to 5.0.0alpha1

* Tue Jan 07 2020 Zabbix Packager <info@zabbix.com> - 4.4.4-2
- build of rhel-5 packages to be resigned with gpg version 3

* Thu Dec 19 2019 Zabbix Packager <info@zabbix.com> - 4.4.4-1
- update to 4.4.4
- added After=<database>.service directives to server and proxy service files

* Wed Nov 27 2019 Zabbix Packager <info@zabbix.com> - 4.4.3-1
- update to 4.4.3
- added User=zabbix and Group=zabbix directives to agent service file

* Mon Nov 25 2019 Zabbix Packager <info@zabbix.com> - 4.4.2-1
- update to 4.4.2

* Mon Oct 28 2019 Zabbix Packager <info@zabbix.com> - 4.4.1-1
- update to 4.4.1

* Mon Oct 07 2019 Zabbix Packager <info@zabbix.com> 4.4.0-1
- update to 4.4.0

* Thu Oct 03 2019 Zabbix Packager <info@zabbix.com> - 4.4.0-0.5rc1
- update to 4.4.0rc1

* Tue Sep 24 2019 Zabbix Packager <info@zabbix.com> - 4.4.0-0.4beta1
- update to 4.4.0beta1
- added zabbix-agent2 package

* Wed Sep 18 2019 Zabbix Packager <info@zabbix.com> - 4.4.0-0.3alpha3
- update to 4.4.0alpha3

* Thu Aug 15 2019 Zabbix Packager <info@zabbix.com> - 4.4.0-0.2alpha2
- update to 4.4.0alpha2
- using google-noto-sans-cjk-ttc-fonts for graphfont in web-japanese package on rhel-8
- added php-fpm as dependency of zabbix-web packages on rhel-8

* Wed Jul 17 2019 Zabbix Packager <info@zabbix.com> - 4.4.0-0.1alpha1
- update to 4.4.0alpha1
- removed apache config from zabbix-web package
- added dedicated zabbix-apache-conf and zabbix-nginx-conf packages

* Fri Mar 29 2019 Zabbix Packager <info@zabbix.com> - 4.2.0-1
- update to 4.2.0
- removed jabber notifications support and dependency on iksemel library

* Tue Mar 26 2019 Zabbix Packager <info@zabbix.com> - 4.2.0-0.6rc2
- update to 4.2.0rc2

* Mon Mar 18 2019 Zabbix Packager <info@zabbix.com> - 4.2.0-0.5rc1
- update to 4.2.0rc1

* Mon Mar 04 2019 Zabbix Packager <info@zabbix.com> - 4.2.0-0.4beta2
- update to 4.2.0beta2

* Mon Feb 18 2019 Zabbix Packager <info@zabbix.com> - 4.2.0-0.1beta1
- update to 4.2.0beta1

* Tue Feb 05 2019 Zabbix Packager <info@zabbix.com> - 4.2.0-0.3alpha3
- build of 4.2.0alpha3 with *.mo files

* Wed Jan 30 2019 Zabbix Packager <info@zabbix.com> - 4.2.0-0.2alpha3
- added timescaledb.sql.gz to zabbix-server-pgsql package

* Mon Jan 28 2019 Zabbix Packager <info@zabbix.com> - 4.2.0-0.1alpha3
- update to 4.2.0alpha3

* Fri Dec 21 2018 Zabbix Packager <info@zabbix.com> - 4.2.0-0.2alpha2
- update to 4.2.0alpha2

* Tue Nov 27 2018 Zabbix Packager <info@zabbix.com> - 4.2.0-0.1alpha1
- update to 4.2.0alpha1

* Mon Oct 29 2018 Zabbix Packager <info@zabbix.com> - 4.0.1-1
- update to 4.0.1

* Mon Oct 01 2018 Zabbix Packager <info@zabbix.com> - 4.0.0-2
- update to 4.0.0

* Fri Sep 28 2018 Zabbix Packager <info@zabbix.com> - 4.0.0-1.1rc3
- update to 4.0.0rc3

* Tue Sep 25 2018 Zabbix Packager <info@zabbix.com> - 4.0.0-1.1rc2
- update to 4.0.0rc2

* Wed Sep 19 2018 Zabbix Packager <info@zabbix.com> - 4.0.0-1.1rc1
- update to 4.0.0rc1

* Mon Sep 10 2018 Zabbix Packager <info@zabbix.com> - 4.0.0-1.1beta2
- update to 4.0.0beta2

* Tue Aug 28 2018 Zabbix Packager <info@zabbix.com> - 4.0.0-1.1beta1
- update to 4.0.0beta1

* Mon Jul 23 2018 Zabbix Packager <info@zabbix.com> - 4.0.0-1.1alpha9
- update to 4.0.0alpha9
- add PHP variable max_input_vars = 10000, overriding default 1000

* Mon Jun 18 2018 Zabbix Packager <info@zabbix.com> - 4.0.0-1.1alpha8
- update to 4.0.0alpha8

* Wed May 30 2018 Zabbix Packager <info@zabbix.com> - 4.0.0-1.1alpha7
- update to 4.0.0alpha7

* Fri Apr 27 2018 Zabbix Packager <info@zabbix.com> - 4.0.0-1.1alpha6
- update to 4.0.0alpha6
- add support for Ubuntu 18.04 (Bionic)
- move enabling JMX interface on Zabbix java gateway to zabbix_java_gateway.conf

* Mon Mar 26 2018 Vladimir Levijev <vladimir.levijev@zabbix.com> - 4.0.0-1.1alpha5
- update to 4.0.0alpha5

* Tue Feb 27 2018 Vladimir Levijev <vladimir.levijev@zabbix.com> - 4.0.0-1.1alpha4
- update to 4.0.0alpha4

* Mon Feb 05 2018 Vladimir Levijev <vladimir.levijev@zabbix.com> - 4.0.0-1.1alpha3
- update to 4.0.0alpha3

* Tue Jan 09 2018 Vladimir Levijev <vladimir.levijev@zabbix.com> - 4.0.0-1.1alpha2
- update to 4.0.0alpha2

* Tue Dec 19 2017 Vladimir Levijev <vladimir.levijev@zabbix.com> - 4.0.0-1alpha1
- update to 4.0.0alpha1

* Thu Nov 09 2017 Vladimir Levijev <vladimir.levijev@zabbix.com> - 3.4.4-2
- add missing translation (.mo) files

* Tue Nov 07 2017 Vladimir Levijev <vladimir.levijev@zabbix.com> - 3.4.4-1
- update to 3.4.4
- fix issue with new line character in pid file that resulted in failure when shutting down daemons on RHEL 5

* Tue Oct 17 2017 Vladimir Levijev <vladimir.levijev@zabbix.com> - 3.4.3-1
- update to 3.4.3

* Mon Sep 25 2017 Vladimir Levijev <vladimir.levijev@zabbix.com> - 3.4.2-1
- update to 3.4.2

* Mon Aug 28 2017 Vladimir Levijev <vladimir.levijev@zabbix.com> - 3.4.1-1
- update to 3.4.1
- change SocketDir to /var/run/zabbix

* Mon Aug 21 2017 Vladimir Levijev <vladimir.levijev@zabbix.com> - 3.4.0-1
- update to 3.4.0

* Wed Apr 26 2017 Kodai Terashima <kodai.terashima@zabbix.com> - 3.4.0-1alpha1
- update to 3.4.0alpla1 r68116
- add libpcre and libevent for compile option

* Sun Apr 23 2017 Kodai Terashima <kodai.terashima@zabbix.com> - 3.2.5-1
- update to 3.2.5
- add TimeoutSec=0 to systemd service file

* Thu Mar 02 2017 Kodai Terashima <kodai.terashima@zabbix.com> - 3.2.4-2
- remove TimeoutSec for systemd

* Mon Feb 27 2017 Kodai Terashima <kodai.terashima@zabbix.com> - 3.2.4-1
- update to 3.2.4
- add TimeoutSec for systemd service file

* Wed Dec 21 2016 Kodai Terashima <kodai.terashima@zabbix.com> - 3.2.3-1
- update to 3.2.3

* Thu Dec 08 2016 Kodai Terashima <kodai.terashima@zabbix.com> - 3.2.2-1
- update to 3.2.2

* Sun Oct 02 2016 Kodai Terashima <kodai.terashima@zabbix.com> - 3.2.1-1
- update to 3.2.1
- use zabbix user and group for Java Gateway
- add SuccessExitStatus=143 for Java Gateway servie file

* Tue Sep 13 2016 Kodai Terashima <kodai.terashima@zabbix.com> - 3.2.0-1
- update to 3.2.0
- add *.conf for Include parameter in agent configuration file

* Mon Sep 12 2016 Kodai Terashima <kodai.terashima@zabbix.com> - 3.2.0rc2-1
- update to 3.2.0rc2

* Fri Sep 09 2016 Kodai Terashima <kodai.terashima@zabbix.com> - 3.2.0rc1-1
- update to 3.2.0rc1

* Thu Sep 01 2016 Kodai Terashima <kodai.terashima@zabbix.com> - 3.2.0beta2-1
- update to 3.2.0beta2

* Fri Aug 26 2016 Kodai Terashima <kodai.terashima@zabbix.com> - 3.2.0beta1-1
- update to 3.2.0beta1

* Fri Aug 12 2016 Kodai Terashima <kodai.terashima@zabbix.com> - 3.2.0alpha1-1
- update to 3.2.0alpha1

* Sun Jul 24 2016 Kodai Terashima <kodai.terashima@zabbix.com> - 3.0.4-1
- update to 3.0.4

* Sun May 22 2016 Kodai Terashima <kodai.terashima@zabbix.com> - 3.0.3-1
- update to 3.0.3
- fix java gateway systemd script to use java options

* Wed Apr 20 2016 Kodai Terashima <kodai.terashima@zabbix.com> - 3.0.2-1
- update to 3.0.2
- remove ZBX-10459.patch

* Sat Apr 02 2016 Kodai Terashima <kodai.terashima@zabbix.com> - 3.0.1-2
- fix proxy packges doesn't have schema.sql.gz
- add server and web packages for RHEL6
- add ZBX-10459.patch

* Sun Feb 28 2016 Kodai Terashima <kodai.terashima@zabbix.com> - 3.0.1-1
- update to 3.0.1
- remove DBSocker parameter

* Sat Feb 20 2016 Kodai Terashima <kodai.terashima@zabbix.com> - 3.0.0-2
- agent, proxy and java-gateway for RHEL 5 and 6

* Mon Feb 15 2016 Kodai Terashima <kodai.terashima@zabbix.com> - 3.0.0-1
- update to 3.0.0

* Thu Feb 11 2016 Kodai Terashima <kodai.terashima@zabbix.com> - 3.0.0rc2
- update to 3.0.0rc2
- add TIMEOUT parameter for java gateway conf

* Thu Feb 04 2016 Kodai Terashima <kodai.terashima@zabbix.com> - 3.0.0rc1
- update to 3.0.0rc1

* Sat Jan 30 2016 Kodai Terashima <kodai.terashima@zabbix.com> - 3.0.0beta2
- update to 3.0.0beta2

* Thu Jan 21 2016 Kodai Terashima <kodai.terashima@zabbix.com> - 3.0.0beta1
- update to 3.0.0beta1

* Thu Jan 14 2016 Kodai Terashima <kodai.terashima@zabbix.com> - 3.0.0alpha6
- update to 3.0.0alpla6
- remove zabbix_agent conf and binary

* Wed Jan 13 2016 Kodai Terashima <kodai.terashima@zabbix.com> - 3.0.0alpha5
- update to 3.0.0alpha5

* Fri Nov 13 2015 Kodai Terashima <kodai.terashima@zabbix.com> - 3.0.0alpha4-1
- update to 3.0.0alpha4

* Thu Oct 29 2015 Kodai Terashima <kodai.terashima@zabbix.com> - 3.0.0alpha3-2
- fix web-pgsql package dependency
- add --with-openssl option

* Mon Oct 19 2015 Kodai Terashima <kodai.terashima@zabbix.com> - 3.0.0alpha3-1
- update to 3.0.0alpha3

* Tue Sep 29 2015 Kodai Terashima <kodai.terashima@zabbix.com> - 3.0.0alpha2-3
- add IfModule for mod_php5 in apache configuration file
- fix missing proxy_mysql alternatives symlink
- chagne snmptrap log filename
- remove include dir from server and proxy conf

* Fri Sep 18 2015 Kodai Terashima <kodai.terashima@zabbix.com> - 3.0.0alpha2-2
- fix create.sql doesn't contain schema.sql & images.sql

* Tue Sep 15 2015 Kodai Terashima <kodai.terashima@zabbix.com> - 3.0.0alpha2-1
- update to 3.0.0alpha2

* Sat Aug 22 2015 Kodai Terashima <kodai.terashima@zabbix.com> - 2.5.0-1
- create spec file from scratch
- update to 2.5.0
