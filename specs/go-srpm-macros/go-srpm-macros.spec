Name:           go-srpm-macros
Version:        1
Release:        1%{?dist}
Summary:        RPM macros for building Golang packages for various architectures
Group:          Development/Libraries
License:        GPLv3+
Source0:        macros.go-srpm
BuildArch:      noarch
# for install command
BuildRequires:  coreutils

%description
The package provides macros for building projects in Go
on various architectures.

%prep
# nothing to prep, just for hooks

%build
# nothing to build, just for hooks

%install
install -m 644 -D "%{SOURCE0}" \
    '%{buildroot}%{_rpmconfigdir}/macros.d/macros.go-srpm'

%files
%{_rpmconfigdir}/macros.d/macros.go-srpm

%changelog
* Wed Mar 28 2018 Jakub Čajka <jcajka@fedoraproject.org>
- initial sample package
