Name:           libgcrypt
Version:        1.5.0
Release:        0
License:        GPL-2.0+ ; LGPL-2.1+
Summary:        The GNU Crypto Library
%define libsoname %{name}
Url:            http://directory.fsf.org/wiki/Libgcrypt
Group:          System/Libraries
Source:         %{name}-%{version}.tar.bz2
Source2:        baselibs.conf
BuildRequires:  libgpg-error-devel >= 1.8
BuildRequires:  libtool

%description
Libgcrypt is a general purpose crypto library based on the code used in
GnuPG (alpha version).

%package devel
License:        GFDL-1.1 ; GPL-2.0+ ; LGPL-2.1+ ; MIT
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
%defattr(-,root,root)
%license COPYING COPYING.LIB
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
