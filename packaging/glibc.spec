#
# spec file for package glibc
#
# Copyright (c) 2012 SUSE LINUX Products GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# This will avoid building some parts of glibc
%bcond_with    fast_build

Name:           glibc
Summary:        Standard Shared Libraries (from the GNU C Library)
License:        LGPL-2.1+ and LGPL-2.1+-with-GCC-exception and GPL-2.0+
Group:          Base/Libraries
BuildRequires:  fdupes
BuildRequires:  makeinfo
BuildRequires:  xz
BuildRequires:  gcc-c++
BuildRequires:  gettext-tools
BuildRequires:  libstdc++-devel
#BuildRequires:  pkgconfig(systemd)

%define _filter_GLIBC_PRIVATE 1
%if %_target_cpu == "i686"
# For i686 let's only build what's different from i586, so
# no need to build documentation
%define build_profile 1
%define build_locales 1
%define build_html 0
%else
%if %{with fast_build}
%define build_profile 0
%define build_locales 0
%define build_html 0
%else
# Default:
%define build_profile 1
%define build_locales 1
%define build_html 1
%endif
%endif

%define disable_assert 0
%define enable_stackguard_randomization 1


%ifarch x86_64
%define enablekernel 2.6.16
%else
%define enablekernel 2.6.16
%endif
Conflicts:      kernel < %{enablekernel}
%ifarch armv7l armv7hl
# The old runtime linker link gets not provided by rpm find.provides, but it exists
Provides:       ld-linux.so.3
Provides:       ld-linux.so.3(GLIBC_2.4)
%endif
Version:        2.20
Release:        0
%define glibc_major_version 2.20
%define git_id 9a869d822025
Url:            http://www.gnu.org/software/libc/libc.html
Source:         glibc-%{version}.tar.xz
Source5:        nsswitch.conf
Source7:        bindresvport.blacklist
Source8:        glibc_post_upgrade.c
Source9:        glibc.rpmlintrc
Source10:       baselibs.conf
# For systemd 
Source20:       nscd.conf
Source21:       nscd.service
Source1001: 	glibc.manifest

Requires(pre):  filesystem
Provides:       rtld(GNU_HASH)

%description
The GNU C Library provides the most important standard libraries used
by nearly all programs: the standard C library, the standard math
library, and the POSIX thread library. A system is not functional
without these libraries.

%package info
Summary:        Info Files for the GNU C Library
License:        GFDL-1.1
Group:          Documentation
BuildArch:      noarch

%description info
This package contains the documentation for the GNU C library stored as
info files. Due to a lack of resources, this documentation is not
complete and is partially out of date.

%package html
Summary:        HTML Documentation for the GNU C Library
License:        GFDL-1.1
Group:          Documentation
BuildArch:      noarch

%description html
This package contains the HTML documentation for the GNU C library. Due
to a lack of resources, this documentation is not complete and is
partially out of date.

%package i18ndata
Summary:        Database Sources for 'locale'
License:        GPL-2.0+ and MIT
Group:          Base/Libraries
BuildArch:      noarch

%description i18ndata
This package contains the data needed to build the locale data files to
use the internationalization features of the GNU libc. It is normally
not necessary to install this packages, the data files are already
created.

%package locale
Summary:        Locale Data for Localized Programs
License:        GPL-2.0+ and MIT and LGPL-2.1+
Requires(post): /usr/bin/cat
Requires:       glibc = %{version}

%description locale
Locale data for the internationalisation features of the GNU C library.

%package -n nscd
Summary:        Name Service Caching Daemon
License:        GPL-2.0+
Group:          System/Service
Provides:       glibc:/usr/sbin/nscd
Requires:       glibc = %{version}

%description -n nscd
Nscd caches name service lookups and can dramatically improve
performance with NIS, NIS+, and LDAP.

%package profile
Summary:        Libc Profiling and Debugging Versions
License:        LGPL-2.1+ and LGPL-2.1+-with-GCC-exception and GPL-2.0+
Group:          Base/Utilities
Requires:       glibc = %{version}

%description profile
This package contains special versions of the GNU C library which are
necessary for profiling and debugging.

%package devel
Summary:        Include Files and Libraries Mandatory for Development
License:        BSD-3-Clause and LGPL-2.1+ and LGPL-2.1+-with-GCC-exception and GPL-2.0+
Requires:       glibc = %{version}
Requires:       linux-kernel-headers

%description devel
These libraries are needed to develop programs which use the standard C
library.

%package devel-static
Summary:        C library static libraries for -static linking
License:        BSD-3-Clause and LGPL-2.1+ and LGPL-2.1+-with-GCC-exception and GPL-2.0+
Requires:       %{name}-devel = %{version}
# Provide Fedora name for package to make packaging easier
Provides:       %{name}-static = %version

%description devel-static
The glibc-devel-static package contains the C library static libraries
for -static linking.  You don't need these, unless you link statically,
which is highly discouraged.

%package devel-utils
Summary:        Development utilities from GNU C library
License:        LGPL-2.1+
Requires:       glibc = %{version}

%description devel-utils
The glibc-devel-utils package contains various binaries which can be helpful during program
debugging.

If you are unsure if you need this, don't install this package.

%package extra
Summary:        Extra binaries from GNU C Library
License:        LGPL-2.1+
Requires:       glibc = %{version}

%description extra
The glibc-extra package contains some extra binaries for glibc that
are not essential but recommend to use.

makedb: A program to create a database for nss

%package obsolete
Summary:        Obsolete Shared Libraries from the GNU C Library
License:        LGPL-2.0+
Requires:       glibc = %{version}

%description obsolete
This package provides some old libraries from the GNU C Library which
are no longer supported. Additional it provides a compatibility library
for old binaries linked against glibc 2.0.

Install this package if you need one of this libraries to get old
binaries working, but since this libraries are not supported and there
is no gurantee that they work for you, you should try to get newer
versions of your software.

%prep
%setup -n glibc-%{version} -q 
cp %{SOURCE1001} .

%build
if [ -x /bin/uname.bin ]; then
	/bin/uname.bin -a
else
	uname -a
fi
uptime || :
ulimit -a
nice
# We do not want configure to figure out the system its building one
# to support a common ground and thus set build and host to the
# target_cpu.
%ifarch %arm
%define target %{_target_cpu}-tizen-linux-gnueabi
%else
%define target %{_target_cpu}-tizen-linux
%endif
# Don't use as-needed, it breaks glibc assumptions
# Before enabling it, run the testsuite and verify that it
# passes completely
export LD_AS_NEEDED=0
# Adjust glibc version.h
echo "#define CONFHOST \"%{target}\"" >> version.h
echo "#define GITID \"%{git_id}\"" >> version.h
#
# Default CFLAGS and Compiler
#
BuildFlags=$(echo %{optflags} | sed -e "s/-Wp,-D_FORTIFY_SOURCE=2//g" | sed -e "s/-ffast-math//" | sed -e "s/atom/i686/g" |  sed -e "s/-fexceptions//" )
BuildFlags="$BuildFlags -O2 -g -U_FORTIFY_SOURCE"
BuildFlags="$(echo $BuildFlags | sed -e 's#-fstack-protector##' -e 's#-ffortify=[0-9]*##')"
BuildCC="%__cc"
BuildCCplus="%__cxx"
add_ons=",libidn"


BuildFlags="$BuildFlags -g"
%if %{disable_assert}
	BuildFlags="$BuildFlags -DNDEBUG=1"
%endif
%ifarch %ix86
	add_ons=$add_ons
%endif
%ifarch %arm aarch64
	add_ons=$add_ons,ports
%endif
%ifarch mipsel
	# fails to build otherwise - need to recheck and fix
	%define enable_stackguard_randomization 0
%endif

configure_and_build_glibc() {
	local dirname="$1"; shift
	local cflags="$1"; shift
	local addons="$1"; shift
	mkdir "cc-$dirname"
	cd "cc-$dirname"
%ifarch %arm aarch64
	# remove asynchronous-unwind-tables during configure as it causes
	# some checks to fail spuriously on arm
	conf_cflags="${cflags/-fasynchronous-unwind-tables/}"
	conf_cflags="${conf_cflags/-funwind-tables/}"
%else
	conf_cflags="$cflags"
%endif

	profile="--disable-profile"
%if %{build_profile}
        if [ "$dirname" = "base" ] ; then
	    profile="--enable-profile"
	fi
%endif
	CFLAGS="$conf_cflags" BUILD_CFLAGS="$conf_cflags" \
        CC="$BuildCC" CXX="$BuildCCplus"  ../configure \
		--prefix=%{_prefix} \
		--libexecdir=%{_libexecdir} --infodir=%{_infodir} \
		--enable-add-ons=nptl$addons \
	        $profile \
		"$@" \
%if %{enable_stackguard_randomization}
		--enable-stackguard-randomization \
%endif
		--build=%{target} --host=%{target} \
%ifarch %{ix86} x86_64 
		--enable-multi-arch \
%endif
		--enable-kernel=%{enablekernel} \
		--enable-bind-now  --enable-obsolete-rpc
	# explicitly set CFLAGS to use the full CFLAGS (not the reduced one for configure)
	make %{?_smp_mflags} #CFLAGS="$cflags" BUILD_CFLAGS="$cflags"
	cd ..
}

	#
	# Build base glibc
	#
	configure_and_build_glibc base "$BuildFlags" "$add_ons"

#
# Build html documentation
#
%if %{build_html}
make -C cc-base html
%endif

#
# Build glibc_post_upgrade binary
#
$BuildCC -static %{optflags} -Os $RPM_SOURCE_DIR/glibc_post_upgrade.c -o glibc_post_upgrade \
     -Lcc-base -Bcc-base/csu \
    '-DREMOVE_TLS_DIRS' '-DREMOVE_PPC_OPTIMIZE_POWER5' \
    '-DLIBDIR="/%{_lib}"' '-DGCONV_MODULES_DIR="%{_libdir}/gconv"'


#######################################################################
###
### CHECK
###
#######################################################################

%check
# The testsuite will fail if asneeded is used
export LD_AS_NEEDED=0
# This has to pass on all platforms!
# Exceptions:
# None!
make %{?_smp_mflags} -C cc-base check-abi

#######################################################################
###
### INSTALL
###
#######################################################################

%install
# We don't want to strip the .symtab from our libraries in find-debuginfo.sh,
# certainly not from libpthread.so.* because it is used by libthread_db to find
# some non-exported symbols in order to detect if threading support
# should be enabled.  These symbols are _not_ exported, and we can't easily
# export them retroactively without changing the ABI.  So we have to
# continue to "export" them via .symtab, instead of .dynsym :-(
# But we also want to keep .symtab and .strtab of other libraries since some
# debugging tools currently require these sections directly inside the main
# files - specifically valgrind and PurifyPlus.
export STRIP_KEEP_SYMTAB=*.so*

# Make sure we will create the gconv-modules.cache
mkdir -p %{buildroot}%{_libdir}/gconv
touch %{buildroot}%{_libdir}/gconv/gconv-modules.cache

# Install base glibc
make %{?_smp_mflags} install_root=%{buildroot} install -C cc-base

install_optimized_variant() {
	local dirname="$1"; shift
	local subdir="$1"; shift
	local subdir_up="$1"; shift

cd "cc-$dirname"
destdir=$RPM_BUILD_ROOT/%{_lib}/$subdir
mkdir -p $destdir
# Don't run a complete make install, we know which libraries
# we want
for lib in libc math/libm nptl/libpthread rt/librt nptl_db/libthread_db
do
  libbase=${lib#*/}
  libbaseso=$(basename $RPM_BUILD_ROOT/%{_lib}/${libbase}-*.so)
  # Only install if different from base lib
  if cmp -s ${lib}.so ../cc-base/${lib}.so; then
    ln -sf $subdir_up/$libbaseso $destdir/$libbaseso
  else
    cp -a ${lib}.so $destdir/$libbaseso
  fi
  # Emulate ldconfig
  ln -sf $libbaseso $destdir/$(basename $RPM_BUILD_ROOT/%{_lib}/${libbase}.so.*)
done
cd ..
}


# Install locales
%if %{build_locales}
	# XXX Do not install locales in parallel!
	cd cc-base
	# localedef creates hardlinks to other locales if possible
	# this will not work if we generate them in parallel.
	# thus we need to run fdupes on  /usr/lib/locale/
	# Still, on my system this is a speed advantage:
	# non-parallel build for install-locales: 9:34mins
	# parallel build with fdupes: 7:08mins
	make %{?_smp_mflags} install_root=%{buildroot} localedata/install-locales
	%fdupes %{buildroot}/usr/lib/locale
	cd ..
%endif
# Create file list for glibc-locale package
%{find_lang} libc

# Prepare obsolete/, used only on some architectures:
export RPM_BUILD_ROOT
%ifarch %ix86
mkdir -p %{buildroot}/%{_lib}/obsolete
%endif

# NPTL <bits/stdio-lock.h> is not usable outside of glibc, so include
# the generic one (RH#162634)
cp -av bits/stdio-lock.h %{buildroot}%{_includedir}/bits/stdio-lock.h


# Miscelanna:

install -m 0700 glibc_post_upgrade %{buildroot}%{_sbindir}

install -m 644 %{SOURCE7} %{buildroot}/etc
install -m 644 %{SOURCE5} %{buildroot}/etc
install -m 644 posix/gai.conf %{buildroot}/etc

mkdir -p %{buildroot}/etc/default
install -m 644 nis/nss %{buildroot}/etc/default/

mkdir -p %{buildroot}%{_includedir}/resolv
install -m 0644 resolv/mapv4v6addr.h %{buildroot}%{_includedir}/resolv/
install -m 0644 resolv/mapv4v6hostent.h %{buildroot}%{_includedir}/resolv/

%if %{build_html}
mkdir -p %{buildroot}%{_datadir}/doc/glibc
cp -p cc-base/manual/libc/*.html %{buildroot}%{_datadir}/doc/glibc
%endif


# nscd tools:

cp nscd/nscd.conf %{buildroot}/etc
mkdir -p %{buildroot}/etc/init.d
ln -sf /sbin/service %{buildroot}/usr/sbin/rcnscd
mkdir -p %{buildroot}/var/run/nscd
touch %{buildroot}/var/run/nscd/{passwd,group,hosts}
touch %{buildroot}/var/run/nscd/{socket,nscd.pid}

#
# Create ld.so.conf
#
cat > %{buildroot}/etc/ld.so.conf <<EOF
%if "%{_lib}" == "lib64"
/usr/local/lib64
%endif
/usr/local/lib
include /etc/ld.so.conf.d/*.conf
# /lib64, /lib, /usr/lib64 and /usr/lib gets added
# automatically by ldconfig after parsing this file.
# So, they do not need to be listed.
EOF
# Add ldconfig cache directory for directory ownership
mkdir -p %{buildroot}/var/cache/ldconfig
# Empty the ld.so.cache:
rm -f %{buildroot}/etc/ld.so.cache
touch %{buildroot}/etc/ld.so.cache

# Don't look at ldd! We don't wish a /bin/sh requires
chmod 644 %{buildroot}%{_bindir}/ldd

# Remove timezone data, now coming in standalone package:
for i in sbin/sln usr/bin/tzselect usr/sbin/zic usr/sbin/zdump etc/localtime; do
	rm -f %{buildroot}/$i
done
rm -rf %{buildroot}%{_datadir}/zoneinfo

mkdir -p %{buildroot}/usr/lib/tmpfiles.d/
install -m 644 %{SOURCE20} %{buildroot}/usr/lib/tmpfiles.d/
mkdir -p %{buildroot}/usr/lib/systemd/system
install -m 644 %{SOURCE21} %{buildroot}/usr/lib/systemd/system

%ifarch armv7hl
# Provide compatibility link
ln -s ld-%{glibc_major_version}.so %{buildroot}/lib/ld-linux.so.3
%endif

%ifarch aarch64
# We don't need a symlink as our filesystem already solves this issue
rm -f %{buildroot}/lib/ld-linux-aarch64.so.1
%endif

# Move getconf to %{_libexecdir}/getconf/ to avoid cross device link
mv %{buildroot}%{_bindir}/getconf %{buildroot}%{_libexecdir}/getconf/getconf
ln -s %{_libexecdir}/getconf/getconf %{buildroot}%{_bindir}/getconf

#######################################################################
###
### ...
###
#######################################################################

%post -p %{_sbindir}/glibc_post_upgrade

%postun -p /sbin/ldconfig

%post locale
for l in /usr/share/locale/locale.alias %{_libdir}/gconv/gconv-modules; do
	[ -d "$l.d" ] || continue
	echo "###X# The following is autogenerated from extra files in the .d directory:" >>"$l"
	cat "$l.d"/* >>"$l"
done
/usr/sbin/iconvconfig

%post info
%install_info --info-dir=%{_infodir} %{_infodir}/libc.info.gz

%postun info
%install_info_delete --info-dir=%{_infodir} %{_infodir}/libc.info.gz

%post -n nscd
mkdir -p /var/run/nscd
exit 0


%files
%manifest %{name}.manifest
# glibc
%defattr(-,root,root)
%license LICENSES
%config(noreplace) /etc/bindresvport.blacklist
%config /etc/ld.so.conf
%attr(0644,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /etc/ld.so.cache
%config(noreplace) /etc/rpc
%verify(not md5 size mtime) %config(noreplace) /etc/nsswitch.conf
%verify(not md5 size mtime) %config(noreplace) /etc/gai.conf
%config(noreplace) /etc/default/nss
/%{_lib}/ld-%{glibc_major_version}.so

# Each architecture has a different name for the dynamic linker:
%ifarch %arm
%ifarch armv7hl
/%{_lib}/ld-linux-armhf.so.3
# Keep compatibility link
/%{_lib}/ld-linux.so.3
%else
/%{_lib}/ld-linux.so.3
%endif
%endif
%ifarch x86_64
/%{_lib}/ld-linux-x86-64.so.2
%endif
%ifarch %ix86 %sparc
/%{_lib}/ld-linux.so.2
%endif
%ifarch aarch64
/%{_lib}/ld-linux-aarch64.so.1
%endif

/%{_lib}/libanl-%{glibc_major_version}.so
/%{_lib}/libanl.so.1
/%{_lib}/libc-%{glibc_major_version}.so
/%{_lib}/libc.so.6*
/%{_lib}/libcidn-%{glibc_major_version}.so
/%{_lib}/libcidn.so.1
/%{_lib}/libcrypt-%{glibc_major_version}.so
/%{_lib}/libcrypt.so.1
/%{_lib}/libdl-%{glibc_major_version}.so
/%{_lib}/libdl.so.2*
/%{_lib}/libm-%{glibc_major_version}.so
/%{_lib}/libm.so.6*
/%{_lib}/libnsl-%{glibc_major_version}.so
/%{_lib}/libnsl.so.1
/%{_lib}/libnss_compat-%{glibc_major_version}.so
/%{_lib}/libnss_compat.so.2
/%{_lib}/libnss_db-%{glibc_major_version}.so
/%{_lib}/libnss_db.so.2
/%{_lib}/libnss_dns-%{glibc_major_version}.so
/%{_lib}/libnss_dns.so.2
/%{_lib}/libnss_files-%{glibc_major_version}.so
/%{_lib}/libnss_files.so.2
/%{_lib}/libnss_hesiod-%{glibc_major_version}.so
/%{_lib}/libnss_hesiod.so.2
/%{_lib}/libnss_nis-%{glibc_major_version}.so
/%{_lib}/libnss_nis.so.2
/%{_lib}/libnss_nisplus-%{glibc_major_version}.so
/%{_lib}/libnss_nisplus.so.2
/%{_lib}/libpthread-%{glibc_major_version}.so
/%{_lib}/libpthread.so.0
/%{_lib}/libresolv-%{glibc_major_version}.so
/%{_lib}/libresolv.so.2
/%{_lib}/librt-%{glibc_major_version}.so
/%{_lib}/librt.so.1
/%{_lib}/libutil-%{glibc_major_version}.so
/%{_lib}/libutil.so.1
%define optimized_libs() \
	%dir %attr(0755,root,root) /%{_lib}/%1\
	/%{_lib}/%1/libc-%{glibc_major_version}.so\
	/%{_lib}/%1/libc.so.6*\
	/%{_lib}/%1/libm-%{glibc_major_version}.so\
	/%{_lib}/%1/libm.so.6*\
	/%{_lib}/%1/libpthread-%{glibc_major_version}.so\
	/%{_lib}/%1/libpthread.so.0\
	/%{_lib}/%1/librt-%{glibc_major_version}.so\
	/%{_lib}/%1/librt.so.1\
	/%{_lib}/%1/libthread_db-1.0.so\
	/%{_lib}/%1/libthread_db.so.1

%dir %attr(0700,root,root) /var/cache/ldconfig
/sbin/ldconfig
%{_bindir}/gencat
%{_bindir}/getconf
%{_bindir}/getent
%{_bindir}/iconv
%attr(755,root,root) %{_bindir}/ldd
%ifarch %ix86 sparc sparcv9
	%{_bindir}/lddlibc4
%endif
%{_bindir}/locale
%{_bindir}/localedef
%dir %attr(0755,root,root) %{_libexecdir}/getconf
%{_libexecdir}/getconf/*
%{_sbindir}/glibc_post_upgrade
%{_sbindir}/iconvconfig

%ifarch %ix86

%files obsolete
%manifest %{name}.manifest
%defattr (755,root,root,755)
%dir /%{_lib}/obsolete/
	#%dir /%{_lib}/obsolete/noversion
	#/%{_lib}/obsolete/noversion/libNoVersion-%{glibc_major_version}.so
	#/%{_lib}/obsolete/noversion/libNoVersion.so.1
%endif

%files locale -f libc.lang
%manifest %{name}.manifest
%defattr(-,root,root)
%{_datadir}/locale/locale.alias
%if %{build_locales}
/usr/lib/locale/*
%endif
%{_libdir}/gconv

%files devel
%manifest %{name}.manifest
%defattr(-,root,root)
%license COPYING COPYING.LIB 
%doc NEWS README BUGS CONFORMANCE
%{_bindir}/rpcgen
%{_includedir}/*
%{_libdir}/*.o
%{_libdir}/*.so
# These static libraries are needed even for shared builds
%{_libdir}/libc_nonshared.a
%{_libdir}/libg.a
%{_libdir}/libieee.a
%ifarch ppc ppc64 s390 s390x sparc sparcv8 sparcv9 sparcv9v
# This is not built on sparc64.
	%{_libdir}/libnldbl_nonshared.a
%endif
%{_libdir}/libmcheck.a
%{_libdir}/libpthread_nonshared.a
%{_libdir}/librpcsvc.a

%files devel-static
%manifest %{name}.manifest
%defattr(-,root,root)
%{_libdir}/libBrokenLocale.a
%{_libdir}/libanl.a
%{_libdir}/libc.a
%{_libdir}/libcrypt.a
%{_libdir}/libdl.a
%{_libdir}/libm.a
%{_libdir}/libnsl.a
%{_libdir}/libpthread.a
%{_libdir}/libresolv.a
%{_libdir}/librt.a
%{_libdir}/libutil.a

%files info
%manifest %{name}.manifest
%defattr(-,root,root)
%doc %{_infodir}/libc.info.gz
%doc %{_infodir}/libc.info-?.gz
%doc %{_infodir}/libc.info-??.gz

%if %{build_html}
%files html
%manifest %{name}.manifest
%defattr(-,root,root)
%doc %{_prefix}/share/doc/glibc
%endif

%files i18ndata
%manifest %{name}.manifest
%defattr(-,root,root)
%{_prefix}/share/i18n

%files -n nscd
%manifest %{name}.manifest
%defattr(-,root,root)
%config(noreplace) /etc/nscd.conf
%{_sbindir}/nscd
%{_sbindir}/rcnscd
/usr/lib/systemd/system/nscd.service
%dir /usr/lib/tmpfiles.d
/usr/lib/tmpfiles.d/nscd.conf
%dir %attr(0755,root,root) %ghost /var/run/nscd
%attr(0644,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /var/run/nscd/nscd.pid
%attr(0666,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /var/run/nscd/socket
%attr(0600,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /var/run/nscd/passwd
%attr(0600,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /var/run/nscd/group
%attr(0600,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /var/run/nscd/hosts

%if %{build_profile}
%files profile
%manifest %{name}.manifest
%defattr(-,root,root)
%{_libdir}/libc_p.a
%{_libdir}/libBrokenLocale_p.a
%{_libdir}/libanl_p.a
%{_libdir}/libm_p.a
%{_libdir}/libcrypt_p.a
%{_libdir}/libpthread_p.a
%{_libdir}/libresolv_p.a
%{_libdir}/libnsl_p.a
%{_libdir}/librt_p.a
%{_libdir}/librpcsvc_p.a
%{_libdir}/libutil_p.a
%{_libdir}/libdl_p.a
%endif

%files devel-utils
%manifest %{name}.manifest
%defattr(-,root,root)
/%{_lib}/libmemusage.so
/%{_lib}/libpcprofile.so
/%{_lib}/libBrokenLocale-%{glibc_major_version}.so
/%{_lib}/libBrokenLocale.so.1
/%{_libdir}/libBrokenLocale.so
/%{_lib}/libSegFault.so
/%{_lib}/libthread_db-1.0.so
/%{_lib}/libthread_db.so.1
/%{_libdir}/libthread_db.so
%dir /%{_libdir}/audit
/%{_libdir}/audit/sotruss-lib.so
# These need gd-devel for building
# %%{_bindir}/memusage
# %%{_bindir}/memusagestat
%{_bindir}/mtrace
%{_bindir}/pcprofiledump
%{_bindir}/sotruss
%{_bindir}/xtrace
%{_bindir}/pldd
%{_bindir}/catchsegv
%{_bindir}/sprof

%files extra
%manifest %{name}.manifest
%defattr(-,root,root)
%{_bindir}/makedb
/var/lib/misc/Makefile


%docs_package
