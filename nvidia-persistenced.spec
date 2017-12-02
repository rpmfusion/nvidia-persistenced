Name:           nvidia-persistenced
Version:        387.34
Release:        1%{?dist}
Summary:        Daemon for maintaining persistent driver state

License:        MIT and GPLv2+
URL:            https://github.com/NVIDIA/nvidia-persistenced
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz
ExclusiveArch:  x86_64 i686 armv7hl aarch64 ppc64le

BuildRequires:  m4

Buildrequires: systemd
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description
A daemon for maintaining persistent driver state,
specifically for use by the NVIDIA Linux driver.


%prep
%setup -q


%build
export CFLAGS="%{optflags}"
export LDFLAGS="%{?__global_ldflags}"
%make_build \
  NVDEBUG=1 \
  NV_VERBOSE=1 \
  STRIP_CMD=true NV_KEEP_UNSTRIPPED_BINARIES=1 \
  X_LDFLAGS="-L%{_libdir}" \
  CC_ONLY_CFLAGS="%{optflags}"
(cd _out/Linux_*/ ; cp %{name}.unstripped %{name} ; cd -)


%install
%make_install NV_VERBOSE=1 PREFIX=%{_prefix}

#Install the initscript
mkdir -p %{buildroot}%{_unitdir}
install -pm 0644 init/systemd/%{name}.service.template \
  %{buildroot}%{_unitdir}/%{name}.service
#Change the daemon running owner
sed -i -e "s/__USER__/root/" %{buildroot}%{_unitdir}/%{name}.service

#Fix perm
chmod -x %{buildroot}%{_mandir}/man1/%{name}.1.*


%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun %{name}.service


%files
%doc README
%license COPYING
%{_unitdir}/%{name}.service
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1.*


%changelog
* Sat Dec 02 2017 Leigh Scott <leigh123linux@googlemail.com> - 387.34-1
- Update to 387.34

* Mon Oct 30 2017 Nicolas Chauvet <kwizart@gmail.com> - 387.22-1
- Update to 387.22

* Tue Sep 26 2017 Leigh Scott <leigh123linux@googlemail.com> - 384.90-1
- Update to 384.90

* Thu Aug 03 2017 Nicolas Chauvet <kwizart@gmail.com> - 384.59-1
- Update to 384.59

* Thu Jun 27 2013 Nicolas Chauvet <kwizart@gmail.com> - 319.32-1
- Initial version

