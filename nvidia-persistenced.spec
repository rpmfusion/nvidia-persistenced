Name:           nvidia-persistenced
Version:        390.42
Release:        1%{?dist}
Summary:        Daemon for maintaining persistent driver state

License:        MIT and GPLv2+
URL:            https://download.nvidia.com/XFree86/%{name}/
Source0:        %{url}/%{name}-%{version}.tar.bz2
ExclusiveArch:  x86_64 i686 armv7hl

BuildRequires:  m4
# https://fedoraproject.org/wiki/Changes/SunRPCRemoval
BuildRequires:  libtirpc-devel

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
export CFLAGS="%{optflags} -I%{_includedir}/tirpc"
export LDFLAGS="%{?__global_ldflags} -ltirpc"
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
* Tue Mar 13 2018 Leigh Scott <leigh123linux@googlemail.com> - 390.42-1
- Update to 390.42

* Fri Mar 02 2018 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 390.25-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Jan 29 2018 Leigh Scott <leigh123linux@googlemail.com> - 390.25-1
- Update to 390.25

* Thu Jan 11 2018 Leigh Scott <leigh123linux@googlemail.com> - 390.12-1
- Update to 390.12
- Switch to libtirpc-devel for rpc

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

