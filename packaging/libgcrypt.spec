Name:           libgcrypt
Version:        1.6.2
Release:        0
License:        LGPL-2.1+ and GPL-2.0+
Summary:        The GNU Crypto Library
%define libsoname %{name}
Url:            http://directory.fsf.org/wiki/Libgcrypt
Group:          Security/Crypto Libraries
Source:         %{name}-%{version}.tar.bz2
Source2:        baselibs.conf
Source1001: 	libgcrypt.manifest
BuildRequires:  libgpg-error-devel >= 1.8
BuildRequires:  libtool

%description
Libgcrypt is a general purpose crypto library based on the code used in
GnuPG (alpha version).

%package devel
License:        GPL-2.0+ and LGPL-2.1+ and X11 and BSD-2.0 and IETF
Summary:        The GNU Crypto Library
Group:          Development/Libraries
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
cp %{SOURCE1001} .

%build
# define ciphers to build
ENABLE_CIPHER="arcfour blowfish cast5 des aes twofish serpent rfc2268 seed camellia"
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

%post  -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%defattr(-,root,root)
%license COPYING COPYING.LIB
%{_libdir}/%{name}.so.20*

%files devel
%manifest %{name}.manifest
%defattr(-,root,root)
%{_infodir}/gcrypt.info.gz
%{_infodir}/gcrypt.info-1.gz
%{_infodir}/gcrypt.info-2.gz
%{_mandir}/man1/hmac256.1.gz
%{_bindir}/dumpsexp
%{_bindir}/hmac256
%{_bindir}/mpicalc
%{_bindir}/%{name}-config
%{_libdir}/%{name}.so
%{_includedir}/gcrypt*.h
%{_datadir}/aclocal/%{name}.m4

%changelog
