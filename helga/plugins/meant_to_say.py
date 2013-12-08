import re

from helga.plugins import match


@match(r'^s/(.*?)/(.*?)/?$')
def meant_to_say(client, channel, nick, message, matches):
    try:
        last = client.last_message[channel][nick]
    except KeyError:
        return None

    old, new = matches[0]
    modified = re.sub(old, new, last)

    # Don't respond if we don't replace anything ... it's annoying
    if modified != last:
        return '{0} meant to say: {1}'.format(nick, modified)
