"""This module contains the CtlUtil class. CtlUtil objects set up a connection
to Stem and handle communication concerning consensus documents and 
descriptor files.

@var unparsable_email_file: A log file for contacts with unparsable emails.
"""

import socket
from config import config
import logging
import re
import string
import stem.version
from stem.control import Controller, EventType

#for unparsable emails
unparsable_email_file = 'log/unparsable_emails.txt'

# Match fingerprint regex
# Fingerprint lines in the descriptors can be
# a) opt fingerprint ABCD ABCD ABCD ABCD ABCD ABCD ABCD ABCD ABCD ABCD
# b) fingerprint ABCD ABCD ABCD ABCD ABCD ABCD ABCD ABCD ABCD ABCD
match_fingerprint = "^(opt\ )?fingerprint ([0-9A-F]{4}\ [0-9A-F]{4}\ [0-9A-F]{4}\ [0-9A-F]{4}\ [0-9A-F]{4}\ [0-9A-F]{4}\ [0-9A-F]{4}\ [0-9A-F]{4}\ [0-9A-F]{4}\ [0-9A-F]{4})$"

# Match router regex
# Router names can be between 1 and 19 alphanumeric characters ([A-Za-z0-9])
match_router = "^router\ ([A-Za-z0-9]{0,19})\ .*$"

# Match hibernating regex
# Hibernating indicator lines can be
# a) opt hibernating 1
# b) hibernating 1
match_hibernating = "^(opt\ )?hibernating 1$"

class CtlUtil:
    """A class that handles communication with the local Tor process via
    Stem.

    @type _CONTROL_HOST: str
    @cvar _CONTROL_HOST: Constant for the control host of the Stem connection.
    @type _CONTROL_PORT: int
    @cvar _CONTROL_PORT: Constant for the control port of the Stem connection.
    @type _AUTHENTICATOR: str
    @cvar _AUTHENTICATOR: Constant for the authenticator string of the Stem
        connection.
    @type control_host: str
    @ivar control_host: Control host of the Stem connection.
    @type control_port: int
    @ivar control_port: Control port of the Stem connection.
    @type sock: socket._socketobject
    @ivar sock: Socket of the Stem connection.
    @type authenticator: str
    @ivar authenticator: Authenticator string of the Stem connection.
    @type control: Stem Connection
    @ivar control: Connection to Stem.
    """
    _CONTROL_HOST = '127.0.0.1'
    _CONTROL_PORT = config.control_port 
    _AUTHENTICATOR = config.authenticator
    
    def __init__(self, control_host = _CONTROL_HOST, 
                control_port = _CONTROL_PORT, sock = None, 
                authenticator = _AUTHENTICATOR):
        """Initialize the CtlUtil object, connect to Stem."""

        self.sock = sock

        if not sock:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.control_host = control_host
        self.control_port = control_port
        self.authenticator = authenticator

        # Try to connect 
        try:
            self.sock.connect((self.control_host, self.control_port))
        except:
            errormsg = "Could not connect to Tor control port.\n" + \
            "Is Tor running on %s with its control port opened on %s?" %\
            (control_host, control_port)

            logging.error(errormsg)
            raise

        
        self.control = Controller.from_port(port = self.control_port)

        # Authenticate connection
        self.control.authenticate(config.authenticator)


    def __del__(self):
        """Closes the connection when the CtlUtil object is garbage collected.
        (From original Tor Weather)
        """
        
        self.sock.close()
        del self.sock
        self.sock = None

        try:
            self.control.close()
        except:
            pass
        
        del self.control
        self.control = None

    def get_single_consensus(self, node_id):
        """Get a consensus document for a specific router with fingerprint
        C{node_id}.

        @type node_id: str
        @param node_id: Fingerprint of the node requested with no spaces.
        @rtype: str
        @return: String representation of the single consensus entry or the
                 empty string if the consensus entry cannot be retrieved.
        """
        cons = ''
        try:
            cons = self.control.get_info("ns/id/" + node_id)

        except stem.ControllerError, e:
            logging.error("ControllerError: %s" % str(e))
        except stem.ProtocolError, e:
            logging.error("ProtocolError: %s" % str(e))
        except:
            logging.error("Unknown exception in "+\
                    "ctlutil.CtlUtil.get_single_consensus()")

        return cons

        
    def get_full_consensus(self):
        """Get the entire consensus document for every router currently up.

        @rtype: str
        @return: String representation of entire consensus document.
        """
        return self.control.get_info("ns/all")

    def get_single_descriptor(self, node_id):
        """Get a descriptor file for a specific router with fingerprint 
        C{node_id}. If a descriptor cannot be retrieved, returns the 
        empty string.

        @type node_id: str
        @param node_id: Fingerprint of the node requested with no spaces.
        @rtype: str
        @return: String representation of the single descirptor file or
        the empty string if no such descriptor file exists.
        """
        desc = ''
        try:
            desc = self.control.get_info("desc/id/" + node_id)
        except stem.ControllerError, e:
            logging.error("ControllerError: %s" % str(e))
        except stem.ProtocolError, e:
            logging.error("ProtocolError: %s" % str(e))
        except:
            logging.error("Unknown exception in CtlUtil" +
                          "get_single_descriptor()")
        return desc

    def get_full_descriptor(self):
        """Get all current descriptor files for every router currently up.

        @rtype: str
        @return: String representation of all descriptor files.
        """
        return self.control.get_info("desc/all-recent")

    def get_descriptor_list(self):
        """Get a list of strings of all descriptor files for every router
        currently up.

        @rtype: list[str]
        @return: List of strings representing all individual descriptor files.
        """
        # Individual descriptors are delimited by -----END SIGNATURE-----
        return self.get_full_descriptor().split("-----END SIGNATURE-----")

    def get_rec_version_list(self):
        """Get a list of currently recommended versions sorted in ascending
        order."""
        return self.control.get_info("status/version/recommended").split(',')

    def get_stable_version_list(self):
        """Get a list of stable, recommended versions of client software.

        @rtype: list[str]
        @return: A list of stable, recommended versions of client software
        sorted in ascending order.
        """
        version_list = self.get_rec_version_list()
        for version in version_list:
            if 'alpha' in version or 'beta' in version:
                index = version_list.index(version)
                version_list = version_list[:index]
                break

        return version_list

    def get_version(self, fingerprint):
        """Get the version of the Tor software that the relay with fingerprint
        C{fingerprint} is running

        @type fingerprint: str
        @param fingerprint: The fingerprint of the Tor relay to check.

        @rtype: str
        @return: The version of the Tor software that this relay is running or
                 '' if the version cannot be retrieved.
        """
        desc = self.get_single_descriptor(fingerprint)
        search = re.search('\nplatform\sTor\s.*\s', desc)

        if search != None:
            return search.group().split()[2].replace(' ', '')
        else:
            return ''

    def get_highest_version(self, versionlist):
        """Return the highest Tor version from a list of versions.
        """
        if len(versionlist) is 0:
            return ""

        highest = stem.version.Version("0.0.0.0")
        for v in versionlist:
            cur = stem.version.Version(v)
            if cur > highest:
                highest = cur

        return str(highest)
        
    def get_version_type(self, fingerprint):
        """Get the type of version the relay with fingerprint C{fingerprint}
        is running. 
        
        @type fingerprint: str
        @param fingerprint: The fingerprint of the Tor relay to check.

        @rtype: str
        @return: The type of version of Tor the client is running, where the
        types are RECOMMENDED or OBSOLETE. 

        Returns RECOMMENDED if the relay is running a version that is found 
        in the `recommended' versions list or if the version is a more recent 
        dev version than the most recent recommended dev version. (Basically, 
        we don't want to bother people for being nice and testing new versions 
        for us) 
        There is one more special case where we return RECOMMENDED and that is 
        when there is *no* recommended version currently known.

        We return OBSOLETE if neither of the above criteria matches.
        If the version cannot be determined, return ERROR.
        """
        version_list = self.get_rec_version_list()
        client_version = self.get_version(fingerprint)

        if client_version == '':
            return 'ERROR'

        # Special case when the dirauth can't agree on recommended versions,
        # the list is empty. In that case we play along as if everything was 
        # fine
        if len(version_list) == 0:
            return 'RECOMMENDED'

        if client_version in version_list:
            return 'RECOMMENDED'

        # Check if the user is running a more recent dev version than is found
        # in the `recommended' list
        if client_version.endswith("-dev"):
            version_list.append(client_version)
            if self.get_highest_version(version_list) == client_version:
                return 'RECOMMENDED'
            # If 0.2.1.34 is stable, that means 0.2.1.34-dev is fine, too.
            nondev_name = client_version.replace("-dev", "")
            if nondev_name in version_list:
                return 'RECOMMENDED'

        return 'OBSOLETE'

    def has_rec_version(self, fingerprint):
        """Check if a Tor relay is running a recommended version of the Tor
        software.
        
        @type fingerprint: str
        @param fingerprint: The router's fingerprint
        
        @rtype: bool
        @return: C{True} if the router is running a recommended version, 
            C{False} if not.
        """
        rec_version_list = self.get_rec_version_list()
        node_version = self.get_version(fingerprint) 
        rec_version = False
        for version in rec_version_list:
            if version == node_version:
                rec_version = True
                break

        return rec_version

    def is_up(self, fingerprint):
        """Check if this node is up (actively running) by requesting a
        consensus document for node C{fingerprint}. If a document is received
        successfully, then the node is up; if a document is not received, then 
        the router is down. If a node is hiberanating, it will return C{False}.

        @type fingerprint: str
        @param fingerprint: Fingerprint of the node in question.
        @rtype: bool
        @return: C{True} if the node is up, C{False} if it's down.
        """
        cons = self.get_single_consensus(fingerprint)
        if cons == '':
            return False
        else:
            return True

    def is_exit(self, node_id):
        """Check if this node is an exit node (accepts exits to port 80).
        
        @type node_id: str
        @param node_id: The router's fingerprint
        @rtype: bool
        @return: True if this router accepts exits to port 80, false if not
            or if the descriptor file can't be accessed for this router.
        """
        try:
            descriptor = self.get_single_descriptor(node_id)
            desc_lines = descriptor.split('\n')
            for line in desc_lines:
                if (line.startswith('accept') and (line.endswith(':80') 
                                                   or line.endswith('*:*'))):
                    return True
            return False
        except stem.ControllerError, e:
            logging.error("ControllerError: %s" % str(e))
            return False
        except stem.ProtocolError, e:
            logging.error("ProtocolError: %s" % str(e))
            return False
        except:
            # some other error with the function
            logging.error("Unknown exception in ctlutil.Ctlutil.is_exit()")
           return False

    def get_finger_name_list(self):
        """Get a list of fingerprint and name pairs for all routers in the
        current descriptor file.

        @rtype: list[(str,str)]
        @return: List of fingerprint and name pairs for all routers in the 
                 current descriptor file.
        """
        # Make a list of tuples of all router fingerprints in descriptor
        # with whitespace removed and router names.
        router_list= []
            
        # Loop through each individual descriptor file.
        for desc in self.get_descriptor_list():
            finger = ""

            # Split each descriptor into lines.
            desc_lines = desc.split("\n")
                
            # Loop through each line in the descriptor.
            for line in desc_lines:
                match = re.match(match_fingerprint, line)
                if match:
                    finger = match.group(2)
                    finger = finger.replace(' ', '')
                match = re.match(match_router, line)
                if match:
                    name = match.group(1)

            # We ignore routers that don't publish their fingerprints
            if not finger == "":
                router_list.append((finger, name))
        
        return router_list

    def get_finger_list(self):
        """Get a list of fingerprints for all routers in the current
        descriptor file.

        @rtype: list[str]
        @return: List of fingerprints for all routers in the current 
                 descriptor file.
        """
        # Use get_finger_name_list and take out name fields.
        finger_name_list = self.get_finger_name_list()

        finger_list = []
        # Append the first element of each pair.
        for pair in finger_name_list:
            finger_list.append(pair[0])
        
        return finger_list

    def get_new_avg_bandwidth(self, avg_bandwidth, hours_up, obs_bandwidth):
        """Calculates the new average bandwidth for a router in kB/s. The 
        average is calculated by rounding rather than truncating.
         
        @type avg_bandwidth: int
        @param avg_bandwidth: The current average bandwidth for the router in
            kB/s.
        @type hours_up: int
        @param hours_up: The number of hours this router has been up 
        @type obs_bandwidth: int
        @param obs_bandwidth: The observed bandwidth in KB/s taken from the 
            most recent descriptor file for this router
        @rtype: int
        @return: The average bandwidth for this router in KB/s
        """
        new_avg = float((hours_up*avg_bandwidth) + obs_bandwidth)/(hours_up + 1)
        new_avg = int(round(new_avg))
        return new_avg

    def get_email(self, fingerprint):
        """Get the contact email address for a router operator.

        @type fingerprint: str
        @param fingerprint: The fingerprint of the router whose email will be
                            returned.
        @rtype: str
        @return: The router operator's email address or the empty string if
                the email address is unable to be parsed.
        """
        
        desc = self.get_single_descriptor(fingerprint)
        email = self._parse_email(desc)
        return email

    def is_stable(self, fingerprint):
        """Check if a Tor node has the stable flag.
        @type fingerprint: str
        @param fingerprint: The fingerprint of the router to check

        @rtype: bool
        @return: True if this router has a valid consensus with the stable
        flag, false otherwise.
        """

        try:
            info = self.get_single_consensus(fingerprint)
            if re.search('\ns.* Stable ', info):
                return True
            else:
                return False
        except stem.ControllerError, e:
            logging.error("ControllerError: %s" % str(e))
            return False
        except stem.ProtocolError, e:
            logging.error("ProtocolError: %s" % str(e))
            return False
        except:
            logging.error("Unknown exception in ctlutil.Ctlutil.is_stable()")
            return False

    def is_hibernating(self, fingerprint):
        """Check if the Tor relay with fingerprint C{fingerprint} is
        hibernating.
        @type fingerprint: str
        @param fingerprint: The fingerprint of the Tor relay to check.

        @rtype: bool
        @return: True if the Tor relay has a current descriptor file with
        the hibernating flag, False otherwise."""

        desc = self.get_single_descriptor(fingerprint)
        if not desc == "":
            match = re.match(match_hibernating, desc)
            if match:
                return True
            else:
                return False

    def is_up_or_hibernating(self, fingerprint):
        """Check if the Tor relay with fingerprint C{fingerprint} is up or 
        hibernating.

        @type fingerprint: str
        @param fingerprint: The fingerprint of the Tor relay to check.

        @rtype: bool
        @return: True if self.is_up(fingerprint or 
        self.is_hibernating(fingerprint)."""
        
        return (self.is_up(fingerprint) or self.is_hibernating(fingerprint))
    
    def get_bandwidth(self, fingerprint):
        """Get the observed bandwidth in KB/s from the most recent descriptor
        for the Tor relay with fingerprint C{fingerprint}.

        @type fingerprint: str
        @param fingerprint: The fingerprint of the Tor relay to check
        @rtype: float
        @return: The observed bandwidth for this Tor relay.
        """
        desc = self.get_single_descriptor(fingerprint)
        bandwidth = 0	  	
        desc_lines = desc.split('\n')
        for line in desc_lines:
            if line.startswith('bandwidth'):
                word_list = line.split()
                # the 4th word in the line is the bandwidth-observed in B/s
                bandwidth = int(word_list[3]) / 1000
        return bandwidth
        
    def _parse_email(self, desc):
        """Parse the email address from an individual router descriptor 
        string.

        @type desc: str
        @param desc: The string representation of the descriptor file for a
                    Tor router.
        @rtype: str
        @return: The email address in desc. If the email address cannot be
                parsed, the empty string.
        """
        split_desc = desc.split('\n')
        punct = string.punctuation
        contact = ""

        for line in split_desc:
            if line.startswith('contact '):
                contact = contact + line

        clean_line = contact.replace('<', ' ').replace('>', ' ') 

        email = re.search('[^\s]+(?:@|['+punct+'\s]+at['+punct+'\s]+).+(?:\.'+
                          '|['+punct+'\s]+dot['+punct+'\s]+)[^\n\s\)\(]+', 
                          clean_line, re.IGNORECASE)
    
        if email == None:
            logging.info("Couldn't parse an email address from line:\n%s" %
                         contact)
            unparsable = open(unparsable_email_file, 'w')
            unparsable.write(contact + '\n')
            unparsable.close()
            email = ""

        else:
            email = email.group()
            email = email.lower()
            email = re.sub('['+punct+'\s]+at['+punct+'\s]+', '@', email)
            email = re.sub('['+punct+'\s]+dot['+punct+'\s]+', '.', email)
            email = email.replace(' d0t ', '.').replace(' hyphen ', '-').\
                    replace(' ', '')

        return email
