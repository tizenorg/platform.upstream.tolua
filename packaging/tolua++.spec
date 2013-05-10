Name:       tolua++
Summary:    tolua++ package
Version:    1.0.93
Release:    1
Group:      TO_BE/FILLED_IN
License:    TO BE FILLED IN
Source0:    %{name}-%{version}.tar.gz
BuildRequires:  liblua-devel
BuildRequires:  cmake

%description
tolua++ package

%package devel
Summary:    tolua++ package (devel)
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description devel
tolua++ package (devel)

%prep
%setup -q

%build
MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`
%ifarch %{ix86}
CXXFLAGS="$CXXFLAGS -D_OSP_DEBUG_ -D_OSP_X86_ -D_OSP_EMUL_" cmake . -DCMAKE_INSTALL_PREFIX=%{_prefix} -DOBS=1 -DFULLVER=%{version} -DMAJORVER=${MAJORVER} -DARCH=x86
%else
CXXFLAGS="$CXXFLAGS -mthumb -Wa,-mimplicit-it=thumb -D_OSP_DEBUG_ -D_OSP_ARMEL_" cmake . -DCMAKE_INSTALL_PREFIX=%{_prefix} -DOBS=1 -DFULLVER=%{version} -DMAJORVER=${MAJORVER} -DARCH=arm
%endif


# Call make instruction with smp support
make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/usr/share/license
cp %{_builddir}/%{name}-%{version}/COPYRIGHT  %{buildroot}/usr/share/license/%{name}

%{__make} DESTDIR=%{?buildroot:%{buildroot}} INSTALL_ROOT=%{?buildroot:%{buildroot}} install
rm -f %{?buildroot:%{buildroot}}%{_infodir}/dir
find %{?buildroot:%{buildroot}} -regex ".*\\.la$" | xargs rm -f --

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%manifest tolua++.manifest
%defattr(-,root,root,-)
/usr/share/license/%{name}

%files devel
%defattr(-,root,root,-)
%{_includedir}/tolua++.h
%{_libdir}/libtolua++.a
