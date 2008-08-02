%define name trackballs
%define version 1.1.4
%define release %mkrel 5
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
Source4: http://prdownloads.sourceforge.net/trackballs/SixLevels.tar.gz
Patch: trackballs-1.1.4-desktop.patch
BuildRequires: guile-devel >= 1.6
BuildRequires: SDL_ttf-devel
BuildRequires: SDL_mixer-devel
BuildRequires: SDL_image-devel
BuildRequires: mesaglu-devel
BuildRoot: %{_tmppath}/%{name}-%{version}

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
tar -xvzf %{SOURCE4} -C share/levels

%build
export LDFLAGS=-L%{_prefix}/X11R6/%_lib
%configure2_5x --bindir=%{_gamesbindir} \
  --datadir=%{_gamesdatadir} \
  --with-highscores=%{_localstatedir}/lib/games/%{name}/highScores
%make

%install
rm -rf %{buildroot}
%makeinstall_std MKINSTALLDIRS=`pwd`/mkinstalldirs iconsdir=%buildroot%_datadir/icons/hicolor

# icons
install -D -m 644 %{SOURCE1} %{buildroot}%{_miconsdir}/%{name}.png
install -D -m 644 %{SOURCE2} %{buildroot}%{_iconsdir}/%{name}.png 
install -D -m 644 %{SOURCE3} %{buildroot}%{_liconsdir}/%{name}.png 

# menu

mv %buildroot%_datadir/games/{locale,applications} %buildroot%_datadir

%find_lang  %name

%files -f %name.lang
%defattr(-,root,root)
%doc AUTHORS ChangeLog COPYING FAQ INSTALL README TODO
%doc docs/*html
%attr(2755,root,games) %{_gamesbindir}/%{name}
%{_gamesdatadir}/%{name}
%{_mandir}/man6/%{name}.*
%_datadir/icons/hicolor/*/apps/*.*
%{_datadir}/applications/%{name}.desktop
%{_iconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%attr(664, root, games) %ghost %{_localstatedir}/lib/games/%{name}/highScores

%clean
rm -rf %{buildroot}

%post
%if %mdkversion < 200900
%{update_menus}
%update_icon_cache hicolor
%endif
%create_ghostfile %{_localstatedir}/lib/games/%{name}/highScores root games 664

%if %mdkversion < 200900
%postun
%{clean_menus}
%clean_icon_cache hicolor
%endif

