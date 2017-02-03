from google.appengine.ext import vendor

import sys

if 'lib' not in sys.path:
    sys.path[0:0] = ['lib']

# Add any libraries installed in the "lib" folder.
vendor.add('lib')
