%define major 0
%define libname	%mklibname rlottie %{major}
%define devname	%mklibname -d rlottie

%global commit0 cebc6c12811d28e4ee9c1e114474b714deb052ef
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global date 20190720

Name: rlottie
Version: 0
Release: 1.%{date}git%{shortcommit0}%{?dist}

# Main source: LGPLv2+
# rapidjson (base) - MIT
# rapidjson (msinttypes) - BSD
# freetype rasterizer - FTL
# vector (vinterpolator) - MPLv1.1
License: LGPLv2+ and MIT and FTL and BSD and MPLv1.1
Summary: Platform independent standalone library that plays Lottie Animation

URL: https://github.com/Samsung/%{name}
Source0: %{url}/archive/%{commit0}.tar.gz#/%{name}-%{shortcommit0}.tar.gz

BuildRequires: gtest-devel
BuildRequires: meson

%description
rlottie is a platform independent standalone C++ library for rendering
vector based animations and art in realtime.

Lottie loads and renders animations and vectors exported in the bodymovin
JSON format. Bodymovin JSON can be created and exported from After Effects
with bodymovin, Sketch with Lottie Sketch Export, and from Haiku.

For the first time, designers can create and ship beautiful animations
without an engineer painstakingly recreating it by hand. Since the animation
is backed by JSON they are extremely small in size but can be large in
complexity.

%package -n	%{libname}
Summary:	Platform independent standalone library that plays Lottie Animation
Group:		System/Libraries

%description -n	%{libname}
rlottie is a platform independent standalone C++ library for rendering
vector based animations and art in realtime.

Lottie loads and renders animations and vectors exported in the bodymovin
JSON format. Bodymovin JSON can be created and exported from After Effects
with bodymovin, Sketch with Lottie Sketch Export, and from Haiku.

For the first time, designers can create and ship beautiful animations
without an engineer painstakingly recreating it by hand. Since the animation
is backed by JSON they are extremely small in size but can be large in
complexity.

%package -n %{devname}
Summary: Development files for %{name}
Provides: %{name}-devel
Requires: %{libname} = %{EVRD}

%description -n %{devname}
%{summary}.

%prep
%autosetup -n %{name}-%{commit0}
sed -e "s/, 'werror=true'//" -e "s/, 'optimization=s'//" -i meson.build
export CXXFLAGS="%{optflags} -stdlib=libc++"
rm -rf test

%build
%meson \
    -Dtest=true \
    -Dthread=true \
    -Dexample=false \
    -Dtest=false \
    -Dcache=false \
    -Dlog=false \
    -Dmodule=false
%meson_build

%install
%meson_install

%check
%meson_test

%files -n %{libname}
%{_libdir}/lib%{name}.so.0*

%files -n %{devname}
%doc AUTHORS README.md
%license COPYING licenses/*
%{_includedir}/%{name}*.h
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/%{name}.pc
