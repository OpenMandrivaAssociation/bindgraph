Summary:	Gathers bind9 statistics
Name:		bindgraph
Version:	0.2
Release:	13
License:	GPL
Group:		Networking/WWW
URL:		http://www.linux.it/~md/software/
Source0:	http://ftp.debian.org/debian/pool/main/b/bindgraph/bindgraph_0.2a.orig.tar.gz
Source1:	bindgraph.init
Source2:	bindgraph.sysconfig
Source3:	bindgraph.logrotate
Patch0:		bindgraph-0.2-mdk_config.diff
Requires:       webserver
%if %mdkversion < 201010
Requires(postun):   rpm-helper
%endif
Requires(post):   rpm-helper
Requires(preun):   rpm-helper
Requires:	bind
Requires:	rrdtool
#Requires:	perl-File-Tail
BuildArch:	noarch

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

install -d %{buildroot}%{_initrddir}
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
install -m0755 bindgraph.init %{buildroot}%{_initrddir}/bindgraph
install -m0644 bindgraph.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/bindgraph
install -m0644 bindgraph.logrotate %{buildroot}%{_sysconfdir}/logrotate.d/bindgraph

install -d %{buildroot}%{_webappconfdir}
cat > %{buildroot}%{_webappconfdir}/%{name}.conf << EOF
<Location /cgi-bin/bindgraph.cgi>
    Require all granted
</Location>
EOF

%post
%_post_service bindgraph
%if %mdkversion < 201010
%_post_webapp
%endif

%preun
%_preun_service bindgraph


%clean

%files 
%doc ChangeLog COPYING rbldnsd.diff README
%attr(0755,root,root) %{_initrddir}/bindgraph
%config(noreplace) %{_webappconfdir}/%{name}.conf
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/sysconfig/bindgraph
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/logrotate.d/bindgraph
%attr(0755,root,root) %{_sbindir}/bindgraph
%attr(0755,root,root) /var/www/cgi-bin/bindgraph.cgi
%dir %attr(0755,root,root) /var/run/bindgraph
%dir %attr(0755,root,root) /var/log/bindgraph
%dir %attr(0755,apache,root) /var/cache/bindgraph
%dir %attr(0755,root,root) %{_localstatedir}/lib/bindgraph


%changelog
* Sun Dec 05 2010 Oden Eriksson <oeriksson@mandriva.com> 0.2-10mdv2011.0
+ Revision: 610071
- rebuild

* Mon Mar 01 2010 Guillaume Rousse <guillomovitch@mandriva.org> 0.2-9mdv2010.1
+ Revision: 513189
- rely on filetrigger for reloading apache configuration begining with 2010.1, rpm-helper macros otherwise
- switch to "open to all" default access policy
- no need to prevent initscript translation

* Wed Sep 02 2009 Thierry Vignaud <tv@mandriva.org> 0.2-8mdv2010.0
+ Revision: 424621
- rebuild

* Sun Jul 20 2008 Oden Eriksson <oeriksson@mandriva.com> 0.2-7mdv2009.0
+ Revision: 238958
- rebuild

  + Pixel <pixel@mandriva.com>
    - adapt to %%_localstatedir now being /var instead of /var/lib (#22312)

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Thu May 10 2007 Oden Eriksson <oeriksson@mandriva.com> 0.2-6mdv2008.0
+ Revision: 26127
- use the source from debian that actually works (duh!)
- added some apache config as well...

* Thu May 10 2007 Oden Eriksson <oeriksson@mandriva.com> 0.2-5mdv2008.0
+ Revision: 25915
- fix the path to the query.log
- bunzip the sources


* Fri Dec 22 2006 Oden Eriksson <oeriksson@mandriva.com> 0.2-4mdv2007.0
+ Revision: 101620
- Import bindgraph

* Sun Jan 08 2006 Oden Eriksson <oeriksson@mandriva.com> 0.2-4mdk
- rebuild

* Sun Dec 19 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 0.2-3mdk
- fix a silly typo

* Sun Dec 19 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 0.2-2mdk
- ahh, i forgot the %%post, %%preun and logrotate stuff...

* Sun Dec 19 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 0.2-1mdk
- initial debian import but with a twist
- partly rediffed the debian patch (P0)
- added S1 & S2

