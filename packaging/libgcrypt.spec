#
# spec file for package libgcrypt
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

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#


Name:           libgcrypt
Version:        1.5.0
Release:        0
License:        GPL-2.0+ ; LGPL-2.1+
Summary:        The GNU Crypto Library
%define libsoname %{name}
Url:            http://directory.fsf.org/wiki/Libgcrypt
Group:          Development/Libraries/C and C++
Source:         %{name}-%{version}.tar.bz2
Source2:        baselibs.conf
Source3:        idea.c.gz
Patch0:         %{name}-ppc64.patch
Patch1:         %{name}-strict-aliasing.patch
Patch3:         %{name}-1.4.1-rijndael_no_strict_aliasing.patch
Patch4:         %{name}-sparcv9.diff
Patch5:         %{name}-1.5.0-idea.patch
Patch6:         %{name}-1.5.0-idea_codecleanup.patch
BuildRequires:  libgpg-error-devel >= 1.8
BuildRequires:  libtool
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
Libgcrypt is a general purpose crypto library based on the code used in
GnuPG (alpha version).

%package devel
License:        GFDL-1.1 ; GPL-2.0+ ; LGPL-2.1+ ; MIT
Summary:        The GNU Crypto Library
Group:          Development/Libraries/C and C++
Requires:       %{libsoname} = %{version}
Requires:       glibc-devel
Requires:       libgpg-error-devel >= 1.8

%description devel
Libgcrypt is a general purpose crypto library based on the code used in
GnuPG (alpha version).

This package contains needed files to compile and link against the
library.

%prep
%setup -q
gzip -dc < %{SOURCE3} > cipher/idea.c
%patch0 -p1
%patch1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1

%build
# define ciphers to build
ENABLE_CIPHER="arcfour blowfish cast5 des aes twofish serpent rfc2268 seed camellia idea"
ENABLE_PUBKEY="dsa elgamal rsa ecc"
ENABLE_DIGEST="crc md4 md5 rmd160 sha1 sha256 sha512 tiger whirlpool"
#
autoreconf -fi
%configure --with-pic \
		--enable-noexecstack \
		--disable-static \
		--enable-ciphers="$ENABLE_CIPHER" \
		--enable-pubkey-ciphers="$ENABLE_PUBKEY" \
		--enable-digests="$ENABLE_DIGEST"
make %{?_smp_mflags}

%check
# Nice idea. however this uses /dev/random, which hangs
# on hardware without random feeds.
#make check

%install
%make_install
#
rm %{buildroot}%{_libdir}/%{name}.la

%post  -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/%{name}.so.11*

%files devel
%defattr(-,root,root)
%{_infodir}/gcrypt.info.gz
%{_infodir}/gcrypt.info-1.gz
%{_bindir}/dumpsexp
%{_bindir}/hmac256
%{_bindir}/%{name}-config
%{_libdir}/%{name}.so
%{_includedir}/gcrypt*.h
%{_datadir}/aclocal/%{name}.m4

%changelog
