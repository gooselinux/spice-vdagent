Name:           spice-vdagent
Version:        0.6.3
Release:        8%{?dist}
Summary:        Agent for Spice guests
Group:          Applications/System
License:        GPLv3+
URL:            http://spice-space.org/
Source0:        http://spice-space.org/download/releases/%{name}-%{version}.tar.bz2
# Some small fixes from upstream git
Patch0:         0001-Install-spice-vdagentd-in-usr-sbin-not-sbin.patch
Patch1:         0002-Only-start-spice-vdagentd-in-runlevel-5.patch
Patch2:         0003-sysv-initscript-fix-lsb-header-multi-line-descriptio.patch
Patch3:         0004-Put-the-pid-and-log-files-into-their-own-subdir.patch
Patch4:         0005-sysv-initscript-exit-cleanly-when-not-running-under-.patch
# For: 680227 - automatically align guest res with multiple monitors broken
Patch5:         0006-Allow-changing-the-resolution-through-the-agent-on-m.patch
# For: 688257 - mouse click does not work
Patch6:         0007-vdagentd-Modprobe-uinput-from-spice-vdagentd.sh-init.patch
Patch7:         0008-vdagentd-Don-t-open-virtio-port-if-creating-uinput-f.patch
# For: 681797 - spice-vdagent does not auto restart
Patch8:         0009-vdagent-Add-daemonizing-support-daemonize-by-default.patch
# These fix chunk demultiplexing when chunks from messages for different
# ports get intermixed.
Patch9:         0010-vdagentd-fix-potentially-copying-more-data-then-a-ch.patch
Patch10:        0011-vdagent-virtio-port-rename-port-parameter-to-vport.patch
Patch11:        0012-vdagent-virtio-port-don-t-pass-the-chunk-header-only.patch
Patch12:        0013-vdagent-virtio-port-properly-demultiplex-vdagent-mes.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  dbus-devel spice-protocol libXrandr-devel libXfixes-devel
BuildRequires:  desktop-file-utils
ExclusiveArch:  i686 x86_64
Requires:       ConsoleKit
Requires(post):   chkconfig
Requires(postun): initscripts
Requires(preun):  chkconfig
Requires(preun):  initscripts

%description
Spice agent for Linux guests offering the following features:

Features:
* Client mouse mode (no need to grab mouse by client, no mouse lag)
  this is handled by the daemon by feeding mouse events into the kernel
  via uinput. This will only work if the active X-session is running a
  spice-vdagent process so that its resolution can be determined.
* Automatic adjustment of the X-session resolution to the client resolution
* Support of copy and paste (text and images) between the active X-session
  and the client


%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1


%build
make %{?_smp_mflags} CFLAGS="$RPM_OPT_FLAGS"


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT


%clean
rm -rf $RPM_BUILD_ROOT


%post
/sbin/chkconfig --add spice-vdagentd

%preun
if [ $1 = 0 ] ; then
    /sbin/service spice-vdagentd stop >/dev/null 2>&1
    /sbin/chkconfig --del spice-vdagentd
fi

%postun
if [ "$1" -ge "1" ] ; then
    /sbin/service spice-vdagentd condrestart >/dev/null 2>&1 || :
fi


%files
%defattr(-,root,root,-)
%doc COPYING ChangeLog README TODO
%{_initddir}/spice-vdagentd
%{_bindir}/spice-vdagent
%{_sbindir}/spice-vdagentd
%{_var}/log/spice-vdagentd
%{_var}/run/spice-vdagentd
%{_sysconfdir}/xdg/autostart/spice-vdagent.desktop
# For /usr/share/gdm/autostart/LoginWindow/spice-vdagent.desktop
# We own the dir too, otherwise we must Require gdm
%{_datadir}/gdm


%changelog
* Thu Mar 24 2011 Hans de Goede <hdegoede@redhat.com> 0.6.3-8
- Fix chunk demultiplexing when chunks from messages for different ports
  get intermixed
  Related: rhbz#658464

* Thu Mar 17 2011 Hans de Goede <hdegoede@redhat.com> 0.6.3-7
- Daemonize per user session vdagent process on startup, this avoids a long
  delay after logging in
- Fix mouse not working with the agent installed
  Resolves: rhbz#688257

* Mon Mar 07 2011 Hans de Goede <hdegoede@redhat.com> 0.6.3-6
- Fix setting of the guest resolution from a multi monitor client
  Resolves: rhbz#680227
- Limit build archs to i686 and x86_64
  Related: rhbz#658464

* Mon Jan 10 2011 Hans de Goede <hdegoede@redhat.com> 0.6.3-5
- Make sysvinit script exit cleanly when not running on a spice enabled vm
  Related: rhbz#658464

* Tue Dec 14 2010 Hans de Goede <hdegoede@redhat.com> 0.6.3-4
- Build for RHEL-6
  Resolves: rhbz#658464

* Fri Nov 19 2010 Hans de Goede <hdegoede@redhat.com> 0.6.3-3
- Put the pid and log files into their own subdir (#648553)

* Mon Nov  8 2010 Hans de Goede <hdegoede@redhat.com> 0.6.3-2
- Fix broken multiline description in initscript lsb header (#648549)

* Sat Oct 30 2010 Hans de Goede <hdegoede@redhat.com> 0.6.3-1
- Initial Fedora package
