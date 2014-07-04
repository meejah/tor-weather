# Kind thanks to Damian Johnson and his great work on the existing weather
# Most of this code has been taken from https://gitweb.torproject.org/user/atagar/weather.git
# and adapted accordingly.

import logging
import string
import re

LOG_FMT = '%(asctime)s %(message)s'
LOG_LVL = logging.DEBUG
logging.basicConfig(format=LOG_FMT)
logger = logging.getLogger(__name__)
logger.setLevel(LOG_LVL)

## CONSTANTS ##
UNPARSABLE = 'unparsable-mail.log'


def deobfuscate_mail(relay):
    """
    Parse the email address from a RelayDetails object of Details document.

    @type relay: RelayDetails
    @param relay: Consists of relay-specific details.
    @rtype: str
    @return: The email address of relay specified in the contact field.
    If the email address cannot be parsed, the empty string.
    """

    contact = relay.contact
    if contact is None:
        return ""
    punct = string.punctuation
    clean_line = contact.replace('<', '').replace('>', '')

    email = re.search('[^\s]+'
                      '(?:@|[' + punct + '\s]+at[' + punct + '\s]+).+'
                      '(?:\.|[' + punct + '\s]+dot[' + punct + '\s]+)[^\n\s\)\(]+',
                      clean_line, re.IGNORECASE)

    if email is None or email == "":
        unparsable = open(UNPARSABLE, 'a')
        unparsable.write(contact.encode('utf-8') + '\n')
        unparsable.close()
        email = ""
    else:
        email = email.group()
        email = email.lower()
        email = re.sub('[' + punct + '\s]+(at|ta)[' + punct + '\s]+', '@', email)
        email = re.sub('[' + punct + '\s]+(dot|tod|d0t)[' + punct + '\s]+', '.', email)
        email = re.sub('[' + punct + '\s]+hyphen[' + punct + '\s]+', '-', email)

    return email
