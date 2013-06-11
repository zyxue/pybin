# files to prepare for setting up vnc and an productive environment

# ESSENTIALS
# Xvfb               ! X virtual frame buffer, if not already available, download it from 
# http://ftp.xfree86.org/pub/XFree86/4.8.0/binaries/Linux-x86_64-glibc23/
# x11vnc             | vnc server (http://www.karlrunge.com/x11vnc/)
# twm                | window manager (built with imake, imkmf, needs Xorg-macros (e.g. util-macros-1.17)

# customization
# .xinitrc           ! read by xinit
# .Xresources        ! load by xserver, used by x clients
# .Xmodmap           ! for consistent key mapping
# .twmrc             ! configure window manager a bit
# .fonts             ! fonts directory, I copied it from my local desktop, then fc-cache ~/.fonts; fc-list to check

# feh                ! image viewer (depends on other libs (e.g. giblib, imlib2)
# matplotlib
# vmd
# xpdf               ! visualizing pdf
# dilo               ! web browser (may not be very useful)


# echo "use 'killx' to kill vnc"
# echo "killx is aliased to `ps x | grep 'xterm\|twm\|xinit\|Xvfb' | awk '{print $1}' | xargs kill -9'"

running()  { sleep 1; ps -p "$1" >&/dev/null ; }

if [ -n "${DISPLAY}" ]; then
    VNCPORT=$(id -u)					   # ${DISPLAY} without :
else
    VNCPORT=$(id -u)
    DISPLAY=:${VNCPORT}
fi

# the command after -- has to ben full path, see man xinit
xinit -- ${HOME}/zx_local/bin/Xvfb ${DISPLAY} -screen 0 ${VNC_DESKTOP_SCREEN_SIZE} -fp ~/.fonts/X11/misc &

# feels xinit is not that reliable, at least on mp2, so just call Xvfb directly
# and then execute .xinitrc myself
# Xvfb ${DISPLAY} -screen 0 ${VNC_DESKTOP_SCREEN_SIZE} -fp ~/.fonts/X11/misc &

if running $!; then
    # sleep is not the smartest way to wait for Xvfb to initialize properly, but
    # not know any better way at the moment. 5s is just an rough estimate
    sleep 5

    # echo 'executing .xinitrc'
    # . ~/.xinitrc &

    echo 'starting x11vnc'
    x11vnc -display ${DISPLAY} -bg -usepw -rfbport ${VNCPORT} &
fi
