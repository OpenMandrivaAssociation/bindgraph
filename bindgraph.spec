Summary:	Gathers bind9 statistics
Name:		bindgraph
Version:	0.2
Release:	17
License:	GPL
Group:		Networking/WWW
URL:		http://www.linux.it/~md/software/
Source0:	http://ftp.debian.org/debian/pool/main/b/bindgraph/bindgraph_0.2a.orig.tar.gz
Source1:	bindgraph.service
Source2:	bindgraph.sysconfig
Source3:	bindgraph.logrotate
Patch0:		bindgraph-0.2-mdk_config.diff
Requires:       webserver
Requires(post):   rpm-helper
Requires(preun):   rpm-helper
Requires:	bind
Requires:	rrdtool
#Requires:	perl-File-Tail
BuildArch:	noarch

Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units

%description
DNS statistics RRDtool frontend for BIND9 BindGraph is a very simple DNS
statistics RRDtool frontend for BIND9 that produces daily, weekly, monthly and
yearly graphs of the DNS server's activity (queries, errors, etc.).

%prep

%setup -q
%patch0 -p0

%build

%install
install -d %{buildroot}%{_sysconfdir}/sysconfig
install -d %{buildroot}%{_sysconfdir}/logrotate.d
install -d %{buildroot}%{_sbindir}
install -d %{buildroot}%{_localstatedir}/lib/bindgraph
install -d %{buildroot}/var/run/bindgraph
install -d %{buildroot}/var/log/bindgraph
install -d %{buildroot}/var/cache/bindgraph
install -d %{buildroot}/var/www/cgi-bin

install -m0755 bindgraph.pl %{buildroot}%{_sbindir}/bindgraph
install -m0755 bindgraph.cgi %{buildroot}/var/www/cgi-bin/
install -D -m0644 %{SOURCE1} %{buildroot}%{_unitdir}/bindgraph.service
install -m0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/bindgraph
install -m0644 %{SOURCE3} %{buildroot}%{_sysconfdir}/logrotate.d/bindgraph

install -d %{buildroot}%{_webappconfdir}
cat > %{buildroot}%{_webappconfdir}/%{name}.conf << EOF
<Location /cgi-bin/bindgraph.cgi>
    Require all granted
</Location>
EOF

%post
%systemd_post bindgraph.service

%preun
%systemd_preun bindgraph.service

%postun
%systemd_postun_with_restart bindgraph.service

%clean

%files 
%doc ChangeLog COPYING rbldnsd.diff README
%{_unitdir}/bindgraph.service
%config(noreplace) %{_webappconfdir}/%{name}.conf
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/sysconfig/bindgraph
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/logrotate.d/bindgraph
%attr(0755,root,root) %{_sbindir}/bindgraph
%attr(0755,root,root) /var/www/cgi-bin/bindgraph.cgi
%dir %attr(0755,root,root) /var/run/bindgraph
%dir %attr(0755,root,root) /var/log/bindgraph
%dir %attr(0755,apache,root) /var/cache/bindgraph
%dir %attr(0755,root,root) %{_localstatedir}/lib/bindgraph
