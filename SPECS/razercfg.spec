Name:           razercfg
Version:        0.42
Release:        4%{?dist}
Summary:        A Razer device configuration tool
# Icons are http://creativecommons.org/licenses/by/4.0/
License:        GPLv2
Group:          Applications/System
URL:            http://bues.ch/cms/hacking/razercfg.html
Source0:        http://bues.ch/razercfg/%{name}-%{version}.tar.xz
# Upstream provides none of the following files
Source1:        razercfg.appdata.xml

BuildRequires:  cmake >= 2.4
BuildRequires:  gcc
BuildRequires:  help2man
BuildRequires:  hicolor-icon-theme
BuildRequires:  libappstream-glib
BuildRequires:  python3-qt5
BuildRequires:  pkgconfig(libusb-1.0)
BuildRequires:  python3-devel
BuildRequires:  desktop-file-utils
%{?systemd_requires}
BuildRequires:  systemd

Requires:       python3-pyside2

%description
Razercfg is the next generation Razer device configuration
tool bringing the Razer gaming experience to the free Open Source world.
Including commandline tool (razercfg) and QT GUI qrazercfg.

%prep
%setup -q
sed -i 's|DESTINATION lib|DESTINATION lib${LIB_SUFFIX}|' librazer/CMakeLists.txt

%build
%cmake .
%cmake_build %{?_smp_mflags}

%install
%cmake_install
rm %{buildroot}%{_libdir}/librazer.so
# install man pages
mkdir -p %{buildroot}%{_mandir}/man1
PYTHONPATH=%{buildroot}/usr/lib/python3.9/site-packages/ \
help2man -N --no-discard-stderr %{buildroot}%{_bindir}/razercfg > \
%{buildroot}%{_mandir}/man1/razercfg.1
# Note that the following line breaks if razercfg is actually installed
help2man -N -n "Use specific profiles per game" %{buildroot}%{_bindir}/razer-gamewrapper > \
%{buildroot}%{_mandir}/man1/razer-gamewrapper.1
LD_LIBRARY_PATH=%{buildroot}%{_libdir} help2man -N %{buildroot}%{_bindir}/razerd > \
%{buildroot}%{_mandir}/man1/razerd.1
# install appdata file
install -Dpm 0644 %{SOURCE1} \
%{buildroot}%{_datadir}/appdata/razercfg.appdata.xml
appstream-util validate-relax --nonet \
%{buildroot}%{_datadir}/appdata/razercfg.appdata.xml
# Set icon for desktop file
desktop-file-edit --set-icon=razercfg \
%{buildroot}%{_datadir}/applications/razercfg.desktop

%check
ctest -V %{?_smp_mflags}

%post
# By default, Fedora services are not enabled and started
# Policy is to configure services with  Presets. But razerd
# is quite useless for the user if not started...
#%systemd_post razerd.service
systemctl enable razerd.service
systemctl start razerd.service
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
udevadm control --reload-rules 2>&1 > /dev/null || :
ldconfig

%preun
%systemd_preun razerd.service

%postun
%systemd_postun_with_restart razerd.service
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi
udevadm control --reload-rules 2>&1 > /dev/null || :
ldconfig

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files
%defattr(-,root,root)
%doc HACKING.md README.md COPYING
%{_bindir}/*
%{_datadir}/applications/razercfg.desktop
%{_datadir}/appdata/razercfg.appdata.xml
%{_datadir}/icons/hicolor/scalable/apps/razercfg*.svg
%{_unitdir}/razerd.service
%{_libdir}/librazer.so.1
%{_tmpfilesdir}/razerd.conf
%{_sysconfdir}/pm/sleep.d/50-razer
%{_udevrulesdir}/*.rules
%{_mandir}/man1/razer*
%{python3_sitelib}/*

%changelog
* Sat Nov 12 2022 Johan Heikkilä <johan.heikkila@gmail.com> 0.42:4
- Updated spec for Fedora 37

* Thu Nov 25 2021 Johan Heikkilä <johan.heikkila@gmail.com> 0.42:3
- Updated spec due to Fedora 35

* Sat Oct 31 2020 Johan Heikkilä <johan.heikkila@gmail.com> 0.42:2
- Updated spec due to changes in Fedora 33

* Fri Jun 5 2020 Johan Heikkilä <johan.heikkila@gmail.com> 0.42:1
- Update to 0.42

* Wed May 06 2020 Johan Heikkilä <johan.heikkila@gmail.com> 0.41:1.1
- Fedora 32 has python3-pyside2

* Sun Nov 03 2019 Johan Heikkilä <johan.heikkila@gmail.com> 0.41:1.0
- Updated to 0.41

* Fri Nov 23 2018 Johan Heikkilä <johan.heikkila@gmail.com> 0.40:1.0
- Updated to 0.40

* Tue May 1 2018 Johan Heikkilä <johan.heikkila@gmail.com> 0.39:1.1
- Fedora 28 supports python3-pyside

* Thu May 18 2017 Johan Heikkilä <johan.heikkila@gmail.com> 0.38
- Updated to 0.39

* Sun Nov 20 2016 Johan Heikkilä <johan.heikkila@gmail.com> 0.38
- Updated for latest version and Fedora 24

* Sun Oct 16 2016 Johan Heikkilä <johan.heikkila@gmail.com> 0.37
- Updated for latest version and Fedora 24

* Tue May 17 2016 Huaren Zhong <huaren.zhong@gmail.com> 0.32
- Rebuild for Fedora

* Wed Oct 15 2014 umeabot <umeabot> 0.22-3.mga5
+ Revision: 747083
- Second Mageia 5 Mass Rebuild

* Tue Sep 16 2014 umeabot <umeabot> 0.22-2.mga5
+ Revision: 688620
- Mageia 5 Mass Rebuild

* Sun Feb 16 2014 dams <dams> 0.22-1.mga5
+ Revision: 592569
- new version 0.22

* Fri Oct 18 2013 umeabot <umeabot> 0.19-5.mga4
+ Revision: 521578
- Mageia 4 Mass Rebuild

* Wed Jan 23 2013 fwang <fwang> 0.19-4.mga3
+ Revision: 391313
- update rpm group

* Wed Jan 16 2013 fwang <fwang> 0.19-3.mga3
+ Revision: 388470
- correct udev rules dir
+ umeabot <umeabot>
- Mass Rebuild - https://wiki.mageia.org/en/Feature:Mageia3MassRebuild

* Wed Oct 17 2012 shlomif <shlomif> 0.19-1.mga3
+ Revision: 307632
- New version 0.19

* Mon Aug 27 2012 fedya <fedya> 0.18-1.mga3
+ Revision: 284614
- mkrel 1 added
- OpenSource it's mispelling
- rpmlint fixes
- imported package razercfg
