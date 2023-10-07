.. _manual:


.. raw:: html

    <br><br>


.. title:: Manual

    
**NAME**

 | ``GENOCIDE`` - Reconsider OTP-CR-117/19


**SYNOPSIS**

 ::

  genocide <cmd> [key=val] 
  genocide <cmd> [key==val]
  genocide [-c] [-d] [-v]


**DESCRIPTION**


 ``GENOCIDE`` is a python3 IRC bot is intended to be programmable  in a
 static, only code, no popen, no user imports and no reading modules from
 a directory, way. It can show genocide and suicide stats of king netherlands
 his genocide into a IRC channel, display rss feeds and log simple text
 messages, source is `here <source.html>`_.

 ``GENOCIDE`` holds evidence that king netherlands is doing a genocide, a 
 written :ref:`response <king>` where king netherlands confirmed taking note
 of “what i have written”, namely :ref:`proof <evidence>` that medicine he
 uses in treatement laws like zyprexa, haldol, abilify and clozapine are poison
 that make impotent, is both physical (contracted muscles) and mental (let 
 people hallucinate) torture and kills members of the victim groups. 

 ``GENOCIDE`` contains `correspondence <writings.html>`_ with the
 International Criminal Court, asking for arrest of the king of the 
 netherlands, for the genocide he is committing with his new treatement laws.
 Current status is "no basis to proceed" judgement of the prosecutor 
 which requires a :ref:`basis to prosecute <reconsider>` to have the king actually
 arrested.


**INSTALL**

 with sudo::

  $ python3 -m pip install genocide

 as user::

  $ pipx install genocide

 or download the tar, see::

  https://pypi.org/project/genocide

**USAGE**


 list of commands::

    $ genocide cmd
    cmd,err,flt,sts,thr,upt

 start a console::

    $ genocide -c
    >

 start additional modules::

    $ genocide mod=<mod1,mod2> -c
    >

 list of modules::

    $ genocide mod
    cmd,err,flt,fnd,irc,log,mdl,mod,
    req, rss,slg,sts,tdo,thr,upt,ver

 to start irc, add mod=irc when
 starting::

     $ genocide mod=irc -c

 to start rss, also add mod=rss
 when starting::

     $ genocide mod=irc,rss -c

 start as daemon::

    $ genocide mod=irc,rss -d
    $ 


**CONFIGURATION**


 *irc*

 ::

    $ genocide cfg server=<server>
    $ genocide cfg channel=<channel>
    $ genocide cfg nick=<nick>

 *sasl*

 ::

    $ genocide pwd <nsvnick> <nspass>
    $ genocide cfg password=<frompwd>

 *rss*

 ::

    $ genocide rss <url>
    $ genocide dpl <url> <item1,item2>
    $ genocide rem <url>
    $ genocide nme <url< <name>


**COMMANDS**


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


**FILES**

 ::

    ~/.local/bin/genocide
    ~/.local/pipx/venvs/genocide/
    /usr/local/bin/genocide
    /usr/local/share/doc/genocide

**AUTHOR**


 ::
 
    Bart Thate <bthate@dds.nl>


**COPYRIGHT**

 ::

    GENOCIDE is Public Domain.
