%define		pkg	microtime
Summary:	Get the current time in microseconds
Name:		nodejs-%{pkg}
Version:	0.3.3
Release:	2
License:	MIT
Group:		Development/Libraries
URL:		https://github.com/wadey/node-microtime
Source0:	http://registry.npmjs.org/microtime/-/%{pkg}-%{version}.tgz
# Source0-md5:	0235c2c7e670706dd9ad0d05c773706e
BuildRequires:	nodejs-devel >= 0.8
BuildRequires:	rpmbuild(macros) >= 1.657
BuildRequires:	nodejs-gyp
BuildRequires:	sed >= 4.0
Requires:	nodejs >= 0.6
Requires:	nodejs-bindings >= 1.0.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# redefine for arch specific
%define		nodejs_libdir	%{_libdir}/node

%description
Date.now() will only give you accuracy in milliseconds. This module
calls gettimeofday(2) to get the time in microseconds and provides it
in a few different formats.

The same warning from that function applies: The resolution of the
system clock is hardware dependent, and the time may be updated
continuously or in `ticks'.

%prep
%setup -qc
mv package/* .

%build
node-gyp configure --nodedir=/usr/src/nodejs --gyp=/usr/bin/gyp
node-gyp build --jobs=%{?__jobs} --verbose

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{nodejs_libdir}/%{pkg}
cp -pr index.js package.json $RPM_BUILD_ROOT%{nodejs_libdir}/%{pkg}
install -p build/Release/%{pkg}.node $RPM_BUILD_ROOT%{nodejs_libdir}/%{pkg}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md LICENSE
%dir %{nodejs_libdir}/%{pkg}
%{nodejs_libdir}/%{pkg}/package.json
%{nodejs_libdir}/%{pkg}/index.js
%attr(755,root,root) %{nodejs_libdir}/%{pkg}/%{pkg}.node
