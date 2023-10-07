# This file is placed in the Public Domain.
#
# pylint: disable=C0116,W0105,E0402


"status of bots"


from ..runtime import Broker, Errors


def sts(event):
    nmr = 0
    for bot in Broker.objs:
        if 'state' in dir(bot):
            event.reply(str(bot.state))
            nmr += 1
    if not nmr:
        event.reply("no status")
    if not Errors.errors:
        event.reply("no errors")
    for exc in Errors.errors:
        event.reply(Errors.format(exc))
