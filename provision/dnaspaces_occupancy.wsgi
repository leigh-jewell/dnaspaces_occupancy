activate_this = '/home/ubuntu/.local/share/virtualenvs/dnaspaces_occupancy-yXIlRPkF/bin/activate_this.py'

with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

import sys

sys.path.insert(0, "/var/www/dnaspaces_occupancy")

from app import app as application
