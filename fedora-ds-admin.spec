%define shortname fedora-ds
%define pkgname   dirsrv

Summary:	Fedora Administration Server (admin)
Name:		fedora-ds-admin
Version:	1.1.4
Release:	1
License:	GPL v2
Group:		Daemons
Source0:	http://directory.fedoraproject.org/sources/%{name}-%{version}.tar.bz2
# Source0-md5:	02d3da65fbb4901c7abf6f3c1dad78f9
URL:		http://directory.fedoraproject.org/
BuildRequires:	apache-devel
BuildRequires:	apache-mod_nss
BuildRequires:	apr-devel
BuildRequires:	cyrus-sasl-devel >= 2.1.19
BuildRequires:	fedora-adminutil-devel >= 1.1.5
BuildRequires:	icu >= 3.4
BuildRequires:	libicu-devel >= 3.4
BuildRequires:	mozldap-devel >= 6.0.4
BuildRequires:	nspr-devel >= 4.6.4
BuildRequires:	nss-devel >= 3.11.4
BuildRequires:	svrcore-devel >= 4.0.3
Requires:	fedora-ds-base
Requires:	apache-mod_nss
Requires:	nss-tools
Requires:	perl-Mozilla-LDAP
Requires(post):	/sbin/chkconfig
Requires(preun):	/sbin/chkconfig
Requires(preun):	/sbin/service
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Fedora Administration Server is an HTTP agent that provides management
features for Fedora Directory Server. It provides some management web
apps that can be used through a web browser. It provides the
authentication, access control, and CGI utilities used by the console.

%prep
%setup -q

%build
%configure \
	--with-adminutil=%{_prefix}

%ifarch x86_64 ppc64 ia64 s390x sparc64
export USE_64=1
%endif

%{__make} \
	CFLAGS="%{rpmcflags} $(pkg-config --cflags apr-util-1)"

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# make console jars directory
install -d $RPM_BUILD_ROOT%{_datadir}/%{pkgname}/html/java

#remove libtool and static libs
rm -f $RPM_BUILD_ROOT%{_libdir}/*.a
rm -f $RPM_BUILD_ROOT%{_libdir}/*.so
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/%{pkgname}/modules/*.a
rm -f $RPM_BUILD_ROOT%{_libdir}/%{pkgname}/modules/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add %{pkgname}-admin
/sbin/ldconfig


%preun
if [ $1 = 0 ]; then
        %service %{pkgname}-admin stop >/dev/null 2>&1 || :
        /sbin/chkconfig --del %{pkgname}-admin
fi

%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc LICENSE
%dir %{_sysconfdir}/%{pkgname}/admin-serv
%config(noreplace)%{_sysconfdir}/%{pkgname}/admin-serv/*.conf
%{_datadir}/%{pkgname}
%{_initrddir}/%{pkgname}-admin
%config(noreplace)%verify(not md5 mtime size) /etc/sysconfig/%{pkgname}-admin
%attr(755,root,root) %{_sbindir}/*
%attr(755,root,root) %{_libdir}/*.so.*
%{_libdir}/%{pkgname}/modules
%{_libdir}/%{pkgname}/perl
%dir %{_libdir}/%{pkgname}/cgi-bin
%attr(755,root,root) %{_libdir}/%{pkgname}/cgi-bin/*
