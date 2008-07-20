Summary:	BindGraph gathers bind9 statistics
Name:		bindgraph
Version:	0.2
Release:	%mkrel 7
License:	GPL
Group:		Networking/WWW
URL:		http://www.linux.it/~md/software/
Source0:	http://ftp.debian.org/debian/pool/main/b/bindgraph/bindgraph_0.2a.orig.tar.gz
Source1:	bindgraph.init
Source2:	bindgraph.sysconfig
Source3:	bindgraph.logrotate
Patch0:		bindgraph-0.2-mdk_config.diff
Requires(pre):  apache-mpm-prefork
Requires:       apache-mpm-prefork
Requires(post): rpm-helper
Requires(preun): rpm-helper
Requires(postun): rpm-helper
BuildRequires:  apache-base >= 2.0.54
Requires:	bind
Requires:	rrdtool
#Requires:	perl-File-Tail
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
DNS statistics RRDtool frontend for BIND9 BindGraph is a very simple DNS
statistics RRDtool frontend for BIND9 that produces daily, weekly, monthly and
yearly graphs of the DNS server's activity (queries, errors, etc.).

%prep

%setup -q
%patch0 -p0

cp %{SOURCE1} bindgraph.init
cp %{SOURCE2} bindgraph.sysconfig
cp %{SOURCE3} bindgraph.logrotate

%build

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

# don't fiddle with the initscript!
export DONT_GPRINTIFY=1

install -d %{buildroot}%{_initrddir}
install -d %{buildroot}%{_sysconfdir}/sysconfig
install -d %{buildroot}%{_sysconfdir}/logrotate.d
install -d %{buildroot}%{_sysconfdir}/httpd/conf/webapps.d
install -d %{buildroot}%{_sbindir}
install -d %{buildroot}%{_localstatedir}/lib/bindgraph
install -d %{buildroot}/var/run/bindgraph
install -d %{buildroot}/var/log/bindgraph
install -d %{buildroot}/var/cache/bindgraph
install -d %{buildroot}/var/www/cgi-bin

install -m0755 bindgraph.pl %{buildroot}%{_sbindir}/bindgraph
install -m0755 bindgraph.cgi %{buildroot}/var/www/cgi-bin/
install -m0755 bindgraph.init %{buildroot}%{_initrddir}/bindgraph
install -m0644 bindgraph.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/bindgraph
install -m0644 bindgraph.logrotate %{buildroot}%{_sysconfdir}/logrotate.d/bindgraph

cat > %{buildroot}%{_sysconfdir}/httpd/conf/webapps.d/%{name}.conf << EOF
<Location /cgi-bin/bindgraph.cgi>
    Order Deny,Allow
    Deny from All
    Allow from 127.0.0.1
    ErrorDocument 403 "Access denied per %{_sysconfdir}/httpd/conf/webapps.d/%{name}.conf"
</Location>
EOF

%post
%_post_service bindgraph
%_post_webapp

%preun
%_preun_service bindgraph

%postun
%_postun_webapp

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files 
%defattr(-,root,root)
%doc ChangeLog COPYING rbldnsd.diff README
%attr(0755,root,root) %{_initrddir}/bindgraph
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/conf/webapps.d/%{name}.conf
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/sysconfig/bindgraph
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/logrotate.d/bindgraph
%attr(0755,root,root) %{_sbindir}/bindgraph
%attr(0755,root,root) /var/www/cgi-bin/bindgraph.cgi
%dir %attr(0755,root,root) /var/run/bindgraph
%dir %attr(0755,root,root) /var/log/bindgraph
%dir %attr(0755,apache,root) /var/cache/bindgraph
%dir %attr(0755,root,root) %{_localstatedir}/lib/bindgraph
