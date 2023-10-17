import os
import site

# Environment variable specific(?) to this plugin. Expects this to be set
# in modulefiles
for path in os.environ.get("PYTHON_SITE_PACKAGES", "").split(":"):
    site.addsitedir(path)
