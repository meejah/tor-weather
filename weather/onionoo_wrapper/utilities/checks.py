"""
Regular checks made on the data received from Onionoo
"""

DEFAULT_THRESHOLD = 20 * 1024

def is_stable(relay):
    """ Parse the RelayDetails object to check if the relay is stable """
    return 'Stable' in relay.flags


def is_hibernating(relay):
    """ Return True if hibernating field set to True, false otherwise """
    return relay.hibernating == True


def is_bandwidth_low(relay, sub=None):
    """ Returns True if relay bandwidth is lower than threshold """
    threshold = DEFAULT_THRESHOLD
    if sub:
        threshold = sub.threshold
    return (relay.observed_bandwidth < threshold)


def check_in_ports(ports):
    """ Checks if port 80 is present in the ports list """
    for entry in ports:
        if entry == '80':
            return True
        if '-' in entry:
            [x, y] = entry.split('-')
            if 80 in range(int(x), int(y)):
                return True
    return False


def check_exitport(relay):
    """ Return True if relay allows traffic to exit through port 80 """
    exit_policy = relay.exit_policy_summary
    if 'accept' in exit_policy:
        return check_in_ports(exit_policy['accept'])
    elif 'reject' in exit_policy:
        return not check_in_ports(exit_policy['reject'])
    return False
