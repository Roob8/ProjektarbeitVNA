import subprocess
import sys
from os.path import join
from os import getenv

assert(sys.platform == 'win32')
VNAKIT_PACKAGE_DIR = join(getenv('ProgramFiles'), 'Vayyar', 'VNAKit', 'python', 'packages')
subprocess.call([sys.executable, "-m", "pip", "install", "--no-index", "--find-links=%s" % VNAKIT_PACKAGE_DIR, "vnakit"])
subprocess.call([sys.executable, "-m", "pip", "install", "--no-index", "--find-links=%s" % VNAKIT_PACKAGE_DIR, "vnakit_ex"])
