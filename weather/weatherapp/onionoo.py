'''utility methods to call OnionPy.

should perhaps be merged to that codebase, but I don't want to
refactor TWO codebases at a time.

'''

from onion_py.manager import Manager

# FIXME fix up onion_py instead, this is just temporary for the most
# part.

class MultipleResultsError(RuntimeError):
    pass

class NoResultsError(RuntimeError):
    pass

def _query_helper(kind, **kw):
    m = Manager()
    if 'limit' not in kw:
        kw['limit'] = 10
    doc = m.query(kind, **kw)
    if len(doc.relays) > 1:
        raise MultipleResultsError('More than one relay found.')
    if len(doc.relays) == 0:
        raise NoResultsError('No relays found.')
    return doc.relays[0]

def _details(**kw):
    return _query_helper('details', **kw)

def _summary(**kw):
    return _query_helper('summary', **kw)


def relay_from_fingerprint(fingerprint):
    '''
    This will return a RelayDetails document for the specified
    fingerprint, or raise an error.
    '''

    return _details(search=fingerprint)

def fingerprint_from_name(name):
    '''
    This will return a RelayDetails document for the specified
    name or raise an error.
    '''
    return _summary(search=name).fingerprint
