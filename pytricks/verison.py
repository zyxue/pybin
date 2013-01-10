#: Package version; this is the only place where it is set.
VERSION = 0,3,0
#: Set to ``True`` for a release. If set to ``False`` then the patch level
#: will have the suffix "-dev".
RELEASE = True
if not RELEASE:
    VERSION = VERSION[:2] + (str(VERSION[2]) + '-dev',)

def get_version():
    """Return current package version as a string."""
    return ".".join(map(str,VERSION))
