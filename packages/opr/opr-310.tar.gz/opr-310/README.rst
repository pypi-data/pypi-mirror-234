NAME

::

   OPR - Object Programming Runtime


DESCRIPTION


::

    OPR is a python3 runtime is intended to be programmable  in a
    static, only code, no popen, no user imports and no reading
    modules from a directory, way. 

    OPR provides some functionality, it can connect to IRC, fetch
    and display RSS feeds, take todo notes, keep a shopping list and
    log text.


SYNOPSIS


::

    opr <cmd> [key=val] 
    opr <cmd> [key==val]
    opr [-c] [-d] [-v]


INSTALL


::

    $ pipx install opr

USAGE


::

    for ease of use, use an alias

    $ alias opr="python3 -m opr"

    list of commands

    $ opr cmd
    cmd,err,flt,sts,thr,upt

    start a console

    $ opr -c
    >

    start additional modules

    $ opr mod=<mod1,mod2> -c
    >

    list of modules

    $ opr mod
    bsc,err,flt,irc,log,mod,rss,shp,
    sts,tdo,thr,udp

    to start irc, add mod=irc when
    starting

    $ opr mod=irc -c

    to start rss, also add mod=rss
    when starting

    $ opr mod=irc,rss -c

    start as daemon

    $ opr mod=irc,rss -d
    $ 


CONFIGURATION


::

    irc

    $ opr cfg server=<server>
    $ opr cfg channel=<channel>
    $ opr cfg nick=<nick>

    sasl

    $ opr pwd <nsvnick> <nspass>
    $ opr cfg password=<frompwd>

    rss

    $ opr rss <url>
    $ opr dpl <url> <item1,item2>
    $ opr rem <url>
    $ opr nme <url< <name>


COMMANDS


::

    cmd - commands
    cfg - irc configuration
    dlt - remove a user
    dpl - sets display items
    ftc - runs a fetching batch
    fnd - find objects 
    flt - instances registered
    log - log some text
    met - add a user
    mre - displays cached output
    nck - changes nick on irc
    pwd - sasl nickserv name/pass
    rem - removes a rss feed
    rss - add a feed
    slg - slogan
    thr - show the running threads


SYSTEMD

::

    [Unit]
    Description=Object Programming Runtime
    Requires=network.target
    After=network.target

    [Service]
    DynamicUser=True
    Type=fork
    User=bart
    Group=bart
    PIDFile=opr.pid
    WorkingDirectory=/home/bart/.opr
    ExecStart=/home/bart/.local/pipx/venvs/opr/bin/opr mod=irc,rss,mdl -d
    RemainAfterExit=yes

    [Install]
    WantedBy=multi-user.target


FILES

::

    ~/.local/bin/opr
    ~/.local/pipx/venvs/opr/


AUTHOR

::

    Bart Thate <bthate@dds.nl>


COPYRIGHT

::

    OPR is placed in the Public Domain.
