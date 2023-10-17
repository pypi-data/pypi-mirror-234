# This file is placed in the Public Domain
#
# pylint: disable=C0116


"""NAME

::

    SBN - Skull, Bones and Number (OTP-CR-117/19)


SYNOPSIS

::

    sbn <cmd> [key=val] 
    sbn <cmd> [key==val]
    sbn [-c] [-d] [-v]


DESCRIPTION

::


    SBN is a python3 IRC bot is intended to be programmable  in a
    static, only code, no popen, no user imports and no reading modules from
    a directory, way. It can show genocide and suicide stats of king netherlands
    his genocide into a IRC channel, display rss feeds and log simple text
    messages.

    SBN contains correspondence <writings> with the International Criminal Court, 
    asking for arrest of the king of the  netherlands, for the genocide he is
    committing with his new treatement laws. Current status is "no basis to
    proceed" judgement of the prosecutor which requires a basis to prosecute
    <reconsider> to have the king actually arrested.


INSTALL


::

    $ pipx install sbn


USAGE

::

    use the following alias for easier typing

    $ alias sbn="python3 -m sbn"


    without any argument the bot does nothing

    $ sbn
    $

    giving an argument makes the bot check for a command

    see list of commands

    $ sbn cmd
    cfg,cmd,dlt,dne,dpl,log,man,met,mod,mre,nme,now,pwd
    rem,req,rss,sts,tdo,thr

    start a console

    $ sbn -c
    >

    list of modules

    $ sbn mod
    cmd,err,flt,fnd,irc,log,mdl,mod,
    req, rss,slg,sts,tdo,thr,upt,ver

    start as daemon

    $ sbn -d
    $ 


CONFIGURATION


::

 irc

    $ sbn cfg server=<server>
    $ sbn cfg channel=<channel>
    $ sbn cfg nick=<nick>

 sasl

    $ sbn pwd <nsvnick> <nspass>
    $ sbn cfg password=<frompwd>

 rss

    $ sbn rss <url>
    $ sbn dpl <url> <item1,item2>
    $ sbn rem <url>
    $ sbn nme <url< <name>


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
    mdl - genocide model
    met - add a user
    mre - displays cached output
    nck - changes nick on irc
    now - genocide stats
    pwd - sasl nickserv name/pass
    rem - removes a rss feed
    req - reconsider
    rss - add a feed
    slg - slogan
    thr - show the running threads
    tpc - genocide stats into topic


SYSTEMD


::

    using the pipx installation, replace "<user>" with the user running pipx

    [Unit]
    Description=Skull, Bones and Number (OTP-CR-117/19)
    Requires=network.target
    After=network.target

    [Service]
    DynamicUser=True
    Type=fork
    User=<user>
    Group=<user>
    PIDFile=sbn.pid
    WorkingDirectory=/home/<user>/.sbn
    ExecStart=/home/<user>/.local/pipx/venvs/sbn/bin/python3 -m sbn -d
    RemainAfterExit=yes

    [Install]
    WantedBy=multi-user.target



FILES

::

    ~/.local/bin/sbn
    ~/.local/pipx/venvs/sbn/


AUTHOR


::

    Bart Thate <bthate@dds.nl>


COPYRIGHT

::

    SBN is Public Domain.


"""


def man(event):
    event.reply(__doc__)
