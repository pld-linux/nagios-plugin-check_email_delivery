%define		plugin	check_email_delivery
%include	/usr/lib/rpm/macros.perl
Summary:	Nagios plugins to check email delivery
Name:		nagios-plugin-%{plugin}
Version:	0.6.3
Release:	0.2
License:	GPL v2
Group:		Networking
Source0:	http://www.buhacoff.net/2008/projects/nagios/check_email_delivery-%{version}.tar.gz
# Source0-md5:	b977887d281f998e67251bef4e9c295f
URL:		http://apricoti.pbwiki.com/NagiosCheckEmailDelivery
BuildRequires:	perl-tools-pod
BuildRequires:	rpm-perlprov >= 4.1-13
BuildRequires:	sed >= 4.0
Requires:	nagios-core
Requires:	perl-Mail-IMAPClient
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		plugindir	%{_prefix}/lib/nagios/plugins
%define		_sysconfdir	/etc/nagios/plugins

%description
Nagios plugin which sends e-mail to server and then checks if the
email arrived by login into IMAP server.

%description -l et.UTF-8
Nagiose plugin, mis saadab emaili serverile ning seejärel logib
IMAPiga kasutajaga mailikontole ning kontrollib kas email on saabunud.

%prep
%setup -q -n check_email_delivery-%{version}

# The ePN scripts are same as base, just without pod docs,
# which we package as man pages anyway.
mv check_email_delivery_epn check_email_delivery
mv check_imap_receive_epn check_imap_receive
mv check_smtp_send_epn check_smtp_send

%{__sed} -i -e 's,/usr/local/nagios/libexec,%{plugindir},' check_*

cat > nagios.cfg <<'EOF'
define command {
	command_name check_email_delivery
	command_line %{plugindir}/check_email_delivery -H $HOSTADDRESS$ --mailfrom $ARG3$ --mailto $ARG4$ --username $ARG5$ --password $ARG6$ --libexec %{plugindir} -w $ARG1$ -c $ARG2$
}
EOF

%build
for a in docs/*.pod; do
	pod2man $a > docs/$(basename $a .pod).1
done

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{plugindir},%{_mandir}/man1}
install check_* $RPM_BUILD_ROOT%{plugindir}
cp -a nagios.cfg $RPM_BUILD_ROOT%{_sysconfdir}/%{plugin}.cfg
cp -a docs/*.1 $RPM_BUILD_ROOT%{_mandir}/man1

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES.txt README.txt docs/*.txt
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{plugin}.cfg
%attr(755,root,root) %{plugindir}/check_email_delivery
%attr(755,root,root) %{plugindir}/check_imap_receive
%attr(755,root,root) %{plugindir}/check_smtp_send
%{_mandir}/man1/check_email_delivery.1*
%{_mandir}/man1/check_imap_receive.1*
%{_mandir}/man1/check_smtp_send.1*
