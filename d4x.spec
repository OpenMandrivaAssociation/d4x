%define name	d4x
%define version	2.5.7.1
%define release	%mkrel 7
%define group	Networking/File transfer

%define	section	Internet/File Transfer
%define	title	Downloader for X

%define Summary	Web Downloader for X

Summary: 	%{Summary}
Name: 		%{name}
Version: 	%{version}
Release:	%{release}
License: 	Artistic
Group: 		%{group}
Source: 	%{name}-%{version}.tar.bz2
Source1:	d4x-zh_TW.po.bz2
Source2:	d4x-pt_BR.po.bz2
Patch0:		d4x-2.5.7.1-fix-deprecated-gtk.patch
Patch1:		d4x-2.5.7.1-fix-str-fmt.patch
Patch2:		d4x-2.5.7.1-gcc4.4.patch
URL: 		https://www.krasu.ru/soft/chuchelo/
BuildRoot: 	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
Buildrequires:	libao-devel
Buildrequires:  gtk+2-devel 
Buildrequires:  imagemagick
Buildrequires:  openssl-devel
BuildRequires:	gettext-devel 
Buildrequires:  desktop-file-utils
BuildRequires:	esound-devel
BuildRequires:	boost-devel
Obsoletes:	nt
Provides:	nt

%description
This program lets you download files from internet/intranet using
ftp, http or https protocol.
Main features:
    * multithreaded design
    * convient user-friendly interface
    * automatic resuming after connection breaks
    * multiple simultaneous downloads
    * recursive ftp and http downloading
    * wildcards support for ftp recursing
    * proxy support (ftp and http)
    * supports for traffic limitation
    * mass downloading function
    * and other ...

%prep
%setup -q -n %{name}-%{version}
%patch0 -p0
%patch1 -p0
%patch2 -p0
bzcat %{SOURCE2} > po/pt_BR.po

%build
autoreconf -fi
%configure2_5x \
	--enable-release \
	--disable-esd \
	--disable-oss \
	--enable-libao

# force gmo file regeneration
rm -f po/stamp-po
%make 

%install
rm -rf %{buildroot}
%makeinstall_std

mkdir -p %{buildroot}%{_datadir}/pixmaps
install -m 644 share/d4x_aqua.png %{buildroot}%{_datadir}/pixmaps/
install -m 644 share/nt-gray.png %{buildroot}%{_datadir}/pixmaps/
install -m 644 share/nt.png %{buildroot}%{_datadir}/pixmaps/

install -m 644 -D share/nt.desktop %{buildroot}%{_datadir}/gnome/apps/Internet/nt.desktop

mkdir -p %{buildroot}%{_miconsdir} \
         %{buildroot}%{_liconsdir} \
         %{buildroot}%{_iconsdir}

install -m 644      share/nt.png %{buildroot}%{_iconsdir}/nt.png
convert -size 16x16 share/nt.png %{buildroot}%{_miconsdir}/nt.png
convert -size 48x48 share/nt.png %{buildroot}%{_liconsdir}/nt.png

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
mv %{buildroot}%{_datadir}/gnome/apps/Internet/nt.desktop %{buildroot}%{_datadir}/applications/nt.desktop

# menu

desktop-file-install --vendor="" \
  --remove-category="Application" \
  --add-category="P2P" \
  --add-category="FileTransfer" \
  --add-category="Network" \
  --add-category="X-MandrivaLinux-Internet-FileTransfer" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications $RPM_BUILD_ROOT%{_datadir}/applications/*


# traditional Chinese translation
if test ! -d %{buildroot}%{_datadir}/locale/zh_TW/LC_MESSAGES; then
  mkdir -p %{buildroot}%{_datadir}/locale/zh_TW/LC_MESSAGES
  bzcat %{SOURCE1} | msgfmt -o %{buildroot}%{_datadir}/locale/zh_TW/LC_MESSAGES/d4x.mo -
fi

%find_lang %{name}

%if %mdkversion < 200900
%post
%{update_menus}
%endif

%if %mdkversion < 200900
%postun
%{clean_menus}
%endif

%clean
rm -fr %{buildroot}

%files -f %{name}.lang
%defattr(-, root, root)
%doc ChangeLog INSTALL* README* PLANS TODO 
%{_bindir}/*
%{_datadir}/applications/nt.desktop
%{_miconsdir}/nt.png
%{_iconsdir}/nt.png
%{_liconsdir}/nt.png
#%{_datadir}/gnome/apps/Internet/nt.desktop
%{_datadir}/pixmaps/*
%dir %{_datadir}/d4x
%{_datadir}/d4x/*
%{_mandir}/man1/nt.1*



