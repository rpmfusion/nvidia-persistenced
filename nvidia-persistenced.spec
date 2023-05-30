%undefine _ld_as_needed

Name:           nvidia-persistenced
Epoch:          3
Version:        535.43.02
Release:        2%{?dist}
Summary:        Daemon for maintaining persistent driver state

License:        MIT and GPLv2+
URL:            https://github.com/NVIDIA/%{name}
Source0:        %url/archive/%{version}/%{name}-%{version}.tar.gz
# This package is also available for 390xx/340xx
# So enable i686 and armv7hl
ExclusiveArch:  x86_64 i686 armv7hl aarch64

BuildRequires:  gcc
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
  %{_smp_mflags} \
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
* Tue May 30 2023 Leigh Scott <leigh123linux@gmail.com> - 3:535.43.02-2
- Update to 535.43.02 beta

* Fri Mar 24 2023 Leigh Scott <leigh123linux@gmail.com> - 3:530.41.03-1
- Update to 530.41.03

* Sun Mar 05 2023 Leigh Scott <leigh123linux@gmail.com> - 3:530.30.02-1
- Update to 530.30.02 beta

* Fri Feb 10 2023 Leigh Scott <leigh123linux@gmail.com> - 3:525.89.02-1
- Update to 525.89.02

* Thu Jan 19 2023 Leigh Scott <leigh123linux@gmail.com> - 3:525.85.05-1
- Update to 525.85.05

* Thu Jan 05 2023 Leigh Scott <leigh123linux@gmail.com> - 3:525.78.01-1
- Update to 525.78.01

* Mon Nov 28 2022 Leigh Scott <leigh123linux@gmail.com> - 3:525.60.11-1
- Update to 525.60.11

* Thu Nov 10 2022 Leigh Scott <leigh123linux@gmail.com> - 3:525.53-1
- Update to 525.53 beta

* Thu Oct 13 2022 Leigh Scott <leigh123linux@gmail.com> - 3:520.56.06-1
- Update to 520.56.06

* Sun Sep 25 2022 Dennnis Gilmore <dennis@ausil.us> - 3:515.76-2
- add aarch64 support

* Wed Sep 21 2022 Leigh Scott <leigh123linux@gmail.com> - 3:515.76-1
- Update to 515.76

* Mon Aug 08 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 3:515.65.01-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild and ffmpeg
  5.1

* Thu Aug 04 2022 Leigh Scott <leigh123linux@gmail.com> - 3:515.65.01-1
- Update to 515.65.01

* Tue Jun 28 2022 Leigh Scott <leigh123linux@gmail.com> - 3:515.57-1
- Update to 515.57

* Wed Jun 01 2022 Leigh Scott <leigh123linux@gmail.com> - 3:515.48.07-1
- Update to 515.48.07

* Thu May 12 2022 Leigh Scott <leigh123linux@gmail.com> - 3:515.43.04-1
- Update to 515.43.04 beta

* Tue Apr 26 2022 Nicolas Chauvet <kwizart@gmail.com> - 3:510.68.02-1
- Update to 510.68.02

* Wed Mar 23 2022 Leigh Scott <leigh123linux@gmail.com> - 3:510.60.02-1
- Update to 510.60.02 release

* Tue Feb 15 2022 Nicolas Chauvet <kwizart@gmail.com> - 3:510.54-1
- Update to 510.54

* Thu Feb 10 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 3:510.47.03-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Feb 01 2022 Leigh Scott <leigh123linux@gmail.com> - 3:510.47.03-1
- Update to 510.47.03 release

* Wed Jan 12 2022 Leigh Scott <leigh123linux@gmail.com> - 3:510.39.01-1
- Update to 510.39.01 beta

* Tue Dec 14 2021 Leigh Scott <leigh123linux@gmail.com> - 3:495.46-1
- Update to 495.46 release

* Tue Oct 26 2021 Leigh Scott <leigh123linux@gmail.com> - 3:495.44-1
- Update to 495.44 release

* Fri Oct 15 2021 Leigh Scott <leigh123linux@gmail.com> - 3:495.29.05-1
- Update to 495.29.05 beta

* Tue Sep 21 2021 Leigh Scott <leigh123linux@gmail.com> - 3:470.74-1
- Update to 470.74 release

* Wed Aug 11 2021 Leigh Scott <leigh123linux@gmail.com> - 3:470.63.01-1
- Update to 470.63.01 release

* Wed Aug 04 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 3:470.57.02-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Jul 19 2021 Leigh Scott <leigh123linux@gmail.com> - 3:470.57.02-1
- Update to 470.57.02 release

* Wed Jun 23 2021 Leigh Scott <leigh123linux@gmail.com> - 3:470.42.01-1
- Update to 470.42.01 beta

* Sat May 22 2021 Leigh Scott <leigh123linux@gmail.com> - 3:465.31-1
- Update to 465.31 release

* Fri Apr 30 2021 Leigh Scott <leigh123linux@gmail.com> - 3:465.27-1
- Update to 465.27 release

* Thu Apr 15 2021 Leigh Scott <leigh123linux@gmail.com> - 3:465.24.02-1
- Update to 465.24.02 release

* Wed Mar 31 2021 Leigh Scott <leigh123linux@gmail.com> - 3:465.19.01-1
- Update to 465.19.01 beta

* Fri Mar 19 2021 Leigh Scott <leigh123linux@gmail.com> - 3:460.67-1
- Update to 460.67 release

* Thu Feb 25 2021 Leigh Scott <leigh123linux@gmail.com> - 3:460.56-1
- Update to 460.56 release

* Thu Feb 04 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 3:460.39-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jan 27 2021 Leigh Scott <leigh123linux@gmail.com> - 3:460.39-1
- Update to 460.39 release

* Thu Jan  7 2021 Leigh Scott <leigh123linux@gmail.com> - 3:460.32.03-1
- Update to 460.32.03 release

* Wed Dec 16 2020 Leigh Scott <leigh123linux@gmail.com> - 3:460.27.04-1
- Update to 460.27.04 beta

* Wed Nov 18 2020 Leigh Scott <leigh123linux@gmail.com> - 3:455.45.01-1
- Update to 455.45.01 release

* Thu Oct 29 2020 Leigh Scott <leigh123linux@gmail.com> - 3:455.38-1
- Update to 455.38 release

* Wed Oct 14 2020 Nicolas Chauvet <kwizart@gmail.com> - 3:455.28-2
- Enable arches for legacy 390x/340xx

* Wed Oct  7 2020 Leigh Scott <leigh123linux@gmail.com> - 3:455.28-1
- Update to 455.28 release

* Fri Sep 18 2020 Leigh Scott <leigh123linux@gmail.com> - 3:455.23.04-1
- Update to 455.23.04 beta

* Wed Aug 19 2020 Leigh Scott <leigh123linux@gmail.com> - 3:450.66-1
- Update to 450.66 release

* Thu Jul 09 2020 Leigh Scott <leigh123linux@gmail.com> - 3:450.57-1
- Update to 450.57 release

* Wed Jun 24 2020 Leigh Scott <leigh123linux@gmail.com> - 3:450.51-1
- Update to 450.51 beta

* Tue Apr 07 2020 leigh123linux <leigh123linux@googlemail.com> - 3:440.82-1
- Update to 440.82 release

* Fri Feb 28 2020 leigh123linux <leigh123linux@googlemail.com> - 3:440.64-1
- Update to 440.64 release

* Mon Feb 03 2020 Leigh Scott <leigh123linux@gmail.com> - 3:440.59-1
- Update to 440.59 release

* Wed Dec 11 2019 Leigh Scott <leigh123linux@googlemail.com> - 3:440.44-1
- Update to 440.44 release

* Fri Nov 22 2019 Leigh Scott <leigh123linux@googlemail.com> - 3:440.36-1
- Update to 440.36 release

* Mon Nov 04 2019 Leigh Scott <leigh123linux@gmail.com> - 3:440.31-1
- Update to 440.31 release

* Thu Oct 17 2019 Leigh Scott <leigh123linux@googlemail.com> - 3:440.26-1
- Update to 440.26 beta

* Fri Aug 30 2019 Leigh Scott <leigh123linux@googlemail.com> - 3:435.21-1
- Update to 435.21 release

* Tue Aug 13 2019 Leigh Scott <leigh123linux@googlemail.com> - 3:435.17-1
- Update to 435.17 beta

* Sat Aug 10 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 3:430.40-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jul 29 2019 Leigh Scott <leigh123linux@googlemail.com> - 3:430.40-1
- Update to 430.40 release

* Tue Jul 16 2019 Leigh Scott <leigh123linux@googlemail.com> - 3:430.34-1
- Update to 430.34 release

* Mon Jun 17 2019 Nicolas Chauvet <kwizart@gmail.com> - 3:430.26-2
- Add back on armv7hl/aarch64 for 390/l4t

* Tue Jun 11 2019 Leigh Scott <leigh123linux@googlemail.com> - 3:430.26-1
- Update to 430.26 release

* Tue May 14 2019 Leigh Scott <leigh123linux@gmail.com> - 3:430.14-1
- Update to 430.14 release

* Wed Apr 24 2019 Leigh Scott <leigh123linux@googlemail.com> - 3:430.09-1
- Update to 430.09 beta

* Thu Mar 21 2019 Leigh Scott <leigh123linux@googlemail.com> - 3:418.56-1
- Update to 418.56 release

* Tue Mar 05 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 3:418.43-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Feb 22 2019 Leigh Scott <leigh123linux@googlemail.com> - 3:418.43-1
- Update to 418.43 release

* Fri Feb 08 2019 Leigh Scott <leigh123linux@googlemail.com> - 3:418.30-1
- Update to 418.30 beta

* Wed Jan 16 2019 Leigh Scott <leigh123linux@googlemail.com> - 3:415.27-1
- Update to 415.27 release

* Wed Dec 26 2018 Leigh Scott <leigh123linux@googlemail.com> - 3:415.25-1
- Update to 415.25 release

* Fri Dec 14 2018 Leigh Scott <leigh123linux@googlemail.com> - 3:415.23-1
- Update to 415.23 release

* Fri Dec 07 2018 Leigh Scott <leigh123linux@googlemail.com> - 3:415.22-1
- Update to 415.22 release

* Wed Nov 21 2018 Leigh Scott <leigh123linux@googlemail.com> - 3:415.18-1
- Update to 415.18 release

* Fri Nov 16 2018 Leigh Scott <leigh123linux@googlemail.com> - 3:410.78-1
- Update to 410.78 release

* Thu Oct 25 2018 Leigh Scott <leigh123linux@googlemail.com> - 3:410.73-1
- Update to 410.73 release

* Tue Oct 16 2018 Leigh Scott <leigh123linux@googlemail.com> - 3:410.66-1
- Update to 410.66 release

* Thu Sep 20 2018 Leigh Scott <leigh123linux@googlemail.com> - 3:410.57-1
- Update to 410.57 beta

* Wed Aug 22 2018 Leigh Scott <leigh123linux@googlemail.com> - 3:396.54-1
- Update to 396.54

* Wed Aug 15 2018 Nicolas Chauvet <kwizart@gmail.com> - 3:396.51-1
- Bump epoch

* Sat Aug 04 2018 Leigh Scott <leigh123linux@googlemail.com> - 396.51-1
- Update to 396.51

* Fri Jul 27 2018 RPM Fusion Release Engineering <sergio@serjux.com> - 396.45-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jul 20 2018 Leigh Scott <leigh123linux@googlemail.com> - 396.45-1
- Update to 396.45

* Fri May 04 2018 Leigh Scott <leigh123linux@googlemail.com> - 396.24-1
- Update to 396.24

* Thu Mar 29 2018 Leigh Scott <leigh123linux@googlemail.com> - 390.48-1
- Update to 390.48

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

