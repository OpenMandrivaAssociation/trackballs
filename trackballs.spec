%define name trackballs
%define version 1.1.4
%define release %mkrel 1
%define title Trackballs
%define longtitle A Marble Madness-like game

Name: %{name}
Version: %{version}
Release: %{release}
Summary: A Marble Madness-like game
Summary(fr): Un jeu inspiré de Marble Madness
Group: Games/Arcade
License: GPL
URL: http://trackballs.sourceforge.net/
Source0: http://prdownloads.sourceforge.net/trackballs/%{name}-%{version}.tar.bz2
Source1: %{name}-16.png
Source2: %{name}-32.png
Source3: %{name}-48.png
Patch: trackballs-1.1.4-desktop.patch
BuildRequires: guile-devel >= 1.6
BuildRequires: SDL_ttf-devel
BuildRequires: SDL_mixer-devel
BuildRequires: SDL_image-devel
BuildRequires: mesaglu-devel

%description
Trackballs is a simple game similar to the
classical game Marble Madness, on the Amiga,
in the 80's. By steering a marble ball through
a labyrinth filled with vicious hammers, pools
of acid and other obstacles the player collects
points.

When the ball reaches the destination you continue
on the next, more difficult, level - unless, of
course, the time runs out.

You steer the ball using the mouse and by pressing
>spacebar< you can jump a short distance.

When all levels are finished, an editor mode permits
to create new ones ("trackballs -e").
All is explained in the docs.

%prep
%setup -q
%patch -p1

%build
export LDFLAGS=-L%{_prefix}/X11R6/%_lib
%configure2_5x --bindir=%{_gamesbindir} \
  --datadir=%{_gamesdatadir} \
  --with-highscores=%{_localstatedir}/%{name}/highScores
%make

%install
rm -rf %{buildroot}
%makeinstall_std MKINSTALLDIRS=`pwd`/mkinstalldirs iconsdir=%buildroot%_datadir/icons/hicolor

# icons
install -D -m 644 %{SOURCE1} %{buildroot}%{_miconsdir}/%{name}.png
install -D -m 644 %{SOURCE2} %{buildroot}%{_iconsdir}/%{name}.png 
install -D -m 644 %{SOURCE3} %{buildroot}%{_liconsdir}/%{name}.png 

# menu
install -d -m 755 %{buildroot}%{_menudir}
cat >%{buildroot}%{_menudir}/%{name} <<EOF
?package(%{name}): \
command="%{_gamesbindir}/%{name}" \
needs="X11" \
section="More Applications/Games/Arcade" \
icon="%{name}.png" \
title="%{title}" \
longtitle="%{longtitle}" \
xdg="true"
EOF

mv %buildroot%_datadir/games/{locale,applications} %buildroot%_datadir

%find_lang  %name

%files -f %name.lang
%defattr(-,root,root)
%doc AUTHORS ChangeLog COPYING FAQ INSTALL README TODO
%doc docs/*html
%attr(2755,root,games) %{_gamesbindir}/%{name}
%{_gamesdatadir}/%{name}
%{_mandir}/man6/%{name}.*
%{_menudir}/%{name}
%_datadir/icons/hicolor/*/apps/*.*
%{_datadir}/applications/%{name}.desktop
%{_iconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_liconsdir}/%{name}.png

%clean
rm -rf %{buildroot}

%post
%{update_menus}
%update_icon_cache hicolor

%postun
%{clean_menus}
%clean_icon_cache hicolor


