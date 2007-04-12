Summary:	BindGraph gathers bind9 statistics
Name:		bindgraph
Version:	0.2
Release:	%mkrel 4
License:	GPL
Group:		Networking/WWW
URL:		http://www.linux.it/~md/software/
Source0:	http://www.linux.it/~md/software/bindgraph-0.2.tar.bz2
Source1:	bindgraph.init.bz2
Source2:	bindgraph.sysconfig.bz2
Source3:	bindgraph.logrotate.bz2
Patch0:		bindgraph-0.2-mdk_config.diff
Patch1:		bindgraph-0.2-silly_typo.diff
Requires(post): rpm-helper
Requires(preun): rpm-helper
Requires:	rrdtool
#Requires:	perl-File-Tail
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-root

%description
DNS statistics RRDtool frontend for BIND9 BindGraph is a very
simple DNS statistics RRDtool frontend for BIND9 that produces
daily, weekly, monthly and yearly graphs of the DNS server's
activity (queries, errors, etc.).

%prep

%setup -q
%patch0 -p1
%patch1 -p0

bzcat %{SOURCE1} > bindgraph.init
bzcat %{SOURCE2} > bindgraph.sysconfig
bzcat %{SOURCE3} > bindgraph.logrotate

%build

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

# don't fiddle with the initscript!
export DONT_GPRINTIFY=1

install -d %{buildroot}%{_initrddir}
install -d %{buildroot}%{_sysconfdir}/sysconfig
install -d %{buildroot}%{_sysconfdir}/logrotate.d
install -d %{buildroot}%{_sbindir}
install -d %{buildroot}%{_localstatedir}/bindgraph
install -d %{buildroot}/var/run/bindgraph
install -d %{buildroot}/var/log/bindgraph
install -d %{buildroot}/var/cache/bindgraph
install -d %{buildroot}/var/www/cgi-bin

install -m0755 bindgraph.pl %{buildroot}%{_sbindir}/bindgraph
install -m0755 bindgraph.cgi %{buildroot}/var/www/cgi-bin/
install -m0755 bindgraph.init %{buildroot}%{_initrddir}/bindgraph
install -m0644 bindgraph.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/bindgraph
install -m0644 bindgraph.logrotate %{buildroot}%{_sysconfdir}/logrotate.d/bindgraph

%post
%_post_service bindgraph

%preun
%_preun_service bindgraph

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files 
%defattr(-,root,root)
%doc ChangeLog COPYING rbldnsd.diff README
%attr(0755,root,root) %{_initrddir}/bindgraph
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/sysconfig/bindgraph
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/logrotate.d/bindgraph
%attr(0755,root,root) %{_sbindir}/bindgraph
%attr(0755,root,root) /var/www/cgi-bin/bindgraph.cgi
%dir %attr(0755,root,root) /var/run/bindgraph
%dir %attr(0755,root,root) /var/log/bindgraph
%dir %attr(0755,root,root) /var/cache/bindgraph
%dir %attr(0755,root,root) %{_localstatedir}/bindgraph


