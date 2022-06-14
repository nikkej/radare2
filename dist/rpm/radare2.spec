%global         _hardened_build 1
%global         gituser         radareorg
%global         gitname         radare2
%global         commit          e45c08acbff838eef559e2177a37266ad79e5c46
%global         latest          %(/usr/bin/git ls-remote https://github.com/radareorg/radare2.git HEAD | /usr/bin/cut -f1)
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})
%global         commitdate      20220613
%global         gitversion      .git%{shortcommit}
%if "%{commit}" != "%{latest}"
%global         commit          %(/usr/bin/git ls-remote https://github.com/radareorg/radare2.git HEAD | /usr/bin/cut -f1)
%global         archive         %(c=%{commit}; /usr/bin/curl -L https://api.github.com/repos/radareorg/radare2/tarball/$c > "SOURCES/radare2-${c:0:7}.tar.gz")
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})
%global         commitdate      %(/usr/bin/date '+%Y%m%d')
%global         gitversion      .git%{shortcommit}
%endif

Name:           %{gitname}
Version:        %{commitdate}
Release:        1%{gitversion}
Summary:        The %{name} reverse engineering framework
Group:          Applications/Engineering
License:        LGPLv3
URL:            https://www.radare.org/
Source0:        https://api.github.com/repos/%{gituser}/%{name}/tarball/%{commit}/%{name}-%{shortcommit}.tar.gz


BuildRequires:  git-core
BuildRequires:  coreutils
BuildRequires:  curl
BuildRequires:  file-devel
BuildRequires:  libzip-devel
#BuildRequires:  capstone-devel >= 3.0.4

#Assume more versions installed in paraller side-by-side
%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}

%description
The %{name} is a reverse-engineering framework that is multi-architecture,
multi-platform, and highly scriptable.  %{name} provides a hexadecimal
editor, wrapped I/O, file system support, debugger support, diffing
between two functions or binaries, and code analysis at opcode,
basic block, and function levels.


%package devel
Summary:        Development files for the %{name} package
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description devel
Development files for the %{name} package. See %{name} package for more
information.


%prep
%setup -q -n %{gituser}-%{name}-%{shortcommit}

%build
%configure --with-sysmagic --with-syszip #--with-syscapstone
CFLAGS="%{optflags} -fPIC -I../include" make %{?_smp_mflags} LIBDIR=%{_libdir} PREFIX=%{_prefix} DATADIR=%{DATADIR}

# Do not run the testsuite yet
# %check
# make tests


%install
rm -rf %{buildroot}
NOSUDO=1 make install DESTDIR=%{buildroot} LIBDIR=%{_libdir} PREFIX=%{_prefix}
cp shlr/sdb/src/libsdb.a %{buildroot}/%{_libdir}/libsdb.a

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%files
%doc COMMUNITY.md CONTRIBUTING.md DEVELOPERS.md INSTALL.md README.md SECURITY.md USAGE.md
%license COPYING
%{_bindir}/r*
%{_libdir}/libr*
%{_libdir}/*.a
%{_libdir}/%{name}/*
%{_mandir}/*
%{_datadir}/%{name}/*
%{_docdir}/%{name}/*


%files devel
%{_includedir}/libr
%{_libdir}/libsdb.a
%{_libdir}/pkgconfig/*.pc

%post -n %{name}-devel -p /sbin/ldconfig
%postun -n %{name}-devel -p /sbin/ldconfig


%changelog
* Tue Jun 14 2022 Juha Nikkanen <nikkej@gmail.com> - gitcc6c574
- Made a pure git src rpm spec, i.e. no static references to any version

* Mon Jun 13 2022 Juha Nikkanen <nikkej@gmail.com> - 5.7.1
- Updated.

* Mon Sep 20 2021 pancake <pancake@nopcode.org> 5.4.2
- update for latest centos8 and r2 codebase

* Sat Oct 10 2020 pancake <pancake@nopcode.org> 5.1.0
- update for latest centos8 and r2 codebase

* Sat Oct 10 2015 Michal Ambroz <rebus at, seznam.cz> 0.10.0-1
- build for Fedora for alpha of 0.10.0

* Sun Nov 09 2014 Pavel Odvody <podvody@redhat.com> 0.9.8rc3-0
- Initial tito package
