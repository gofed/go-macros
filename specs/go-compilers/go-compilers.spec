Name:           go-compilers
Version:        1
Release:        1%{?dist}
Summary:        Go language compilers for various architectures
Group:          Development/Tools
License:        GPLv3+
Source0:        macros.go-compilers-golang
Source1:        macros.go-compilers-gcc
Source2:        macros.go-rpm
Source3:        gobundled.prov
Source4:        gosymlink.deps
Source5:        go.attr
Source6:        gobundled.attr
Source7:        gosymlink.attr
Source8:        go-rpm-integration
Source9:        golist


ExclusiveArch:  %{go_arches}

# for install, cut and rm commands
BuildRequires:  coreutils
# for go specific macros
BuildRequires:  go-srpm-macros

%description
The package provides correct golang language compiler
base on an architectures.

%ifarch %{golang_arches}
%package golang-compiler
Summary:       compiler for golang

BuildRequires: golang

Requires:      golang

Provides:      compiler(go-compiler) = 2
Provides:      compiler(golang)

%description golang-compiler
Compiler for golang.
%endif

%ifarch %{gccgo_arches}
%package gcc-go-compiler
Summary:       compiler for gcc-go

# GCC>=5 holds in Fedora now
Requires:      gcc-go

Provides:      compiler(go-compiler) = 1
Provides:      compiler(gcc-go)

%description gcc-go-compiler
Compiler for gcc-go.
%endif

%prep

%build

%install
%ifarch %{golang_arches}
# executables
install -m 755 -D %{SOURCE8} %{buildroot}%{_bindir}/go-rpm-integration
install -m 755 -D %{SOURCE3} %{buildroot}%{_rpmconfigdir}/gobundled.prov
install -m 755 -D %{SOURCE4} %{buildroot}%{_rpmconfigdir}/gosymlink.deps
# macros
install -m 644 -D %{SOURCE0} %{buildroot}%{_rpmconfigdir}/macros.d/macros.go-compilers-golang
install -m 644 -D %{SOURCE2} %{buildroot}%{_rpmconfigdir}/macros.d/macros.go-rpm
# attrs
install -m 644 -D %{SOURCE5} %{buildroot}%{_rpmconfigdir}/fileattrs/go.attr
install -m 644 -D %{SOURCE6} %{buildroot}%{_rpmconfigdir}/fileattrs/gobundled.attr
install -m 644 -D %{SOURCE7} %{buildroot}%{_rpmconfigdir}/fileattrs/gosymlink.attr

install -D -p -m 0755 %{SOURCE9} %{buildroot}%{_bindir}/golist
%endif

%ifarch %{gccgo_arches}
install -m 644 -D %{SOURCE1} %{buildroot}%{_rpmconfigdir}/macros.d/macros.go-compilers-gcc
%endif

%ifarch %{golang_arches}
%files golang-compiler
%{_rpmconfigdir}/macros.d/macros.go-compilers-golang
%{_rpmconfigdir}/macros.d/macros.go-rpm
%{_rpmconfigdir}/gobundled.prov
%{_rpmconfigdir}/gosymlink.deps
%{_rpmconfigdir}/fileattrs/go.attr
%{_rpmconfigdir}/fileattrs/gobundled.attr
%{_rpmconfigdir}/fileattrs/gosymlink.attr
%{_bindir}/golist
%{_bindir}/go-rpm-integration
%endif

%ifarch %{gccgo_arches}
%files gcc-go-compiler
%{_rpmconfigdir}/macros.d/macros.go-compilers-gcc
%endif

%changelog
* Wed Mar 28 2018 Jakub Čajka <jcajka@fedoraproject.org> - 1-1
- initial sample package
