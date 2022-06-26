%global         gituser         radareorg
%global         gitname         radare2
%global         commit          0360057781ee3f3b37af04409eac570a969deca6
%global         latest          %(curl -s https://api.github.com/repos/radareorg/radare2/commits/HEAD | grep -E '^  "sha"' | cut -d '"' -f4)
%global         commitdate      %(date '+%Y%m%d')
%if "%{commit}" != "%{latest}"
# It is radical to modify spec file but this seems to work on user installed rpmbuild and
# Fedora fc35 mock. How about other distros?
%global         modifyspec      %(c=%{commit}; l=%{latest}; wd=%{_specdir}; while IFS='' read -r line; do echo "${line//$c/$l}"; done < "$wd/radare2.spec" > "$wd/radare2.spec.tmp"; rm -f %{SOURCE0}; mv -f "$wd/radare2.spec.tmp" "$wd/radare2.spec";)
%global         commit          %{latest}
%global         archive         %(c=%{commit}; wd=%{_topdir}; curl -s -L https://api.github.com/repos/radareorg/radare2/tarball/$c > "$wd/SOURCES/radare2-${c:0:7}.tar.gz")
%endif
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})
%global         gitversion      .git%{shortcommit}

Name:           %{gitname}
Version:        %{commitdate}
Release:        1%{gitversion}
Summary:        The %{name} reverse engineering framework
Group:          Applications/Engineering
License:        LGPLv3
URL:            https://www.radare.org/
Source0:        https://api.github.com/repos/%{gituser}/%{gitname}/tarball/%{commit}/%{gitname}-%{shortcommit}.tar.gz


BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  git-core
BuildRequires:  coreutils
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
* Mon Jun 20 2022 Juha Nikkanen <nikkej@gmail.com> - git43eb022
- Introduced macro modifyspec where commit hash of HEAD is changed if needed

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
