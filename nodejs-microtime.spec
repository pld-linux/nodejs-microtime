%define		pkg	microtime
Summary:	Get the current time in microseconds
Name:		nodejs-%{pkg}
Version:	0.2.0
Release:	3
License:	MIT
Group:		Development/Libraries
URL:		https://github.com/wadey/node-microtime
Source0:	http://registry.npmjs.org/microtime/-/%{pkg}-%{version}.tgz
# Source0-md5:	9bc25aebc64b0c7370727013098dd6c3
Patch0:		library-path.patch
BuildRequires:	nodejs-devel
BuildRequires:	rpmbuild(macros) >= 1.634
BuildRequires:	sed >= 4.0
Requires:	nodejs
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
%patch0 -p1

# make it noop for npm link
%{__sed} -i -e 's,node-waf configure build,/bin/true,' package.json

%build
NODE_PATH=%{nodejs_libdir}/%{pkg} \
node-waf configure build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{nodejs_libdir}/%{pkg}
cp -pr index.js package.json $RPM_BUILD_ROOT%{nodejs_libdir}/%{pkg}

node-waf install \
	--destdir=$RPM_BUILD_ROOT

chmod a+x $RPM_BUILD_ROOT%{nodejs_libdir}/%{pkg}/microtime.node

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md LICENSE
%dir %{nodejs_libdir}/%{pkg}
%{nodejs_libdir}/%{pkg}/package.json
%{nodejs_libdir}/%{pkg}/index.js
%attr(755,root,root) %{nodejs_libdir}/%{pkg}/microtime.node
