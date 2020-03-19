import os
data_dir = '.'

def filepath(kind, filename):
    '''Determine the path to a file in the data directory.'''
    fp = os.path.join(data_dir, kind, filename)
    if not os.path.exists(fp):
        print('WARNING: Resource not available "%s"' % fp)
        return None
    return fp

def load(kind, filename, mode='rb'):
    '''Open a file in the data directory.'''
    return open(filepath(filename,kind), mode)
