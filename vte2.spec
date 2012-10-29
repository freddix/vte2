Summary:	VTE terminal widget library
Name:		vte2
Version:	0.28.2
Release:	2
License:	LGPL
Group:		X11/Libraries
Source0:	http://ftp.gnome.org/pub/gnome/sources/vte/0.28/vte-%{version}.tar.xz
# Source0-md5:	497f26e457308649e6ece32b3bb142ff
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gettext-devel
BuildRequires:	gtk+-devel
BuildRequires:	libtool
BuildRequires:	ncurses-devel
BuildRequires:	pkg-config
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libexecdir	%{_libdir}/%{name}

%description
The vte package contains a terminal widget for GTK+. It's used by
gnome-terminal among other programs.

%package devel
Summary:	Headers for VTE
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
The vte package contains a terminal widget for GTK+. It's used by
gnome-terminal among other programs.

You should install the vte-devel package if you would like to
compile applications that use the vte terminal widget. You do not need
to install vte-devel if you just want to use precompiled
applications.

%package apidocs
Summary:	VTE API documentation
Group:		Documentation
Requires:	gtk-doc-common

%description apidocs
VTE API documentation.

%package terminal
Summary:	Basic VTE terminal
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}

%description terminal
Basic VTE terminal.

%prep
%setup -qn vte-%{version}

# kill gnome common deps
sed -i -e 's/GNOME_COMPILE_WARNINGS.*//g'	\
-i -e 's/GNOME_MAINTAINER_MODE_DEFINES//g'	\
    -i -e 's/GNOME_COMMON_INIT//g'		\
    -i -e 's/GNOME_CXX_WARNINGS.*//g'		\
    -i -e 's/GNOME_DEBUG_CHECK//g' configure.in

%build
%{__gtkdocize}
%{__intltoolize}
%{__libtoolize}
%{__aclocal}
%{__autoheader}
%{__automake}
%{__autoconf}
cd gnome-pty-helper
%{__libtoolize}
%{__aclocal}
%{__autoheader}
%{__automake}
%{__autoconf}
%configure \
	--disable-silent-rules		\
	--disable-static		\
	--with-html-dir=%{_gtkdocdir}
%{__make}
cd ..
%configure \
	--disable-introspection		\
	--disable-silent-rules		\
	--disable-static		\
	--with-default-emulation=rxvt	\
	--with-html-dir=%{_gtkdocdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

rm -rf $RPM_BUILD_ROOT%{_datadir}/locale/{ca@valencia,en@shaw}

%find_lang vte-0.0

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /usr/sbin/ldconfig
%postun	-p /usr/sbin/ldconfig

%files -f vte-0.0.lang
%defattr(644,root,root,755)
%doc NEWS README AUTHORS
%attr(755,root,root) %ghost %{_libdir}/libvte.so.?
%attr(755,root,root) %{_libdir}/libvte.so.*.*.*
%dir %{_libexecdir}
%attr(2755,root,utmp) %{_libexecdir}/gnome-pty-helper
%{_datadir}/vte

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libvte.so
%{_includedir}/vte-0.0
%{_pkgconfigdir}/vte.pc

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/vte-0.0

%files terminal
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/vte

