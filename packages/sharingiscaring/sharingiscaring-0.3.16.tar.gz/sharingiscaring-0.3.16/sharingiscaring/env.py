import os


# Does a path exist?
# This is false for dangling symbolic links on systems that support them.
def exists(path):
    """Test whether a path exists.  Returns False for broken symbolic links"""
    try:
        os.stat(path)
    except (OSError, ValueError):
        return False
    return True


file_exists = exists("envdonotcommit.py")
if file_exists:
    from envdonotcommit import MONGODB_PASSWORD_LOCAL
else:
    MONGODB_PASSWORD_LOCAL = None
MONGODB_PASSWORD = os.environ.get("MONGODB_PASSWORD", MONGODB_PASSWORD_LOCAL)
BRANCH = os.environ.get("BRANCH", "dev")
ENVIRONMENT = os.environ.get("ENVIRONMENT", "prod")
NOTIFIER_API_TOKEN = os.environ.get(
    "NOTIFIER_API_TOKEN", "5940257423:AAHqd5kqm0NZsYCyJDK20GSAk0MHitEDfpU"
)
API_TOKEN = os.environ.get(
    "API_TOKEN", "5456222180:AAF6RYi_zNziRi4DrE_GCffqHMrP5EHVR-A"
)
FASTMAIL_TOKEN = os.environ.get("FASTMAIL_TOKEN", "3y9k8csgylkeh9hm")
