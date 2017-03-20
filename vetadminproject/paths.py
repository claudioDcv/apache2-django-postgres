import os
import sys

# ------------------------------------------------------------------------------
# Calculation of directories relative to the module location
# ------------------------------------------------------------------------------
def project_dir_and_name():
    this_path = os.path.realpath(__file__)
    conf_path = os.path.dirname(this_path)
    django_project_path = os.path.dirname(conf_path)
    return os.path.split(django_project_path)

PROJECT_DIR, PROJECT_NAME = project_dir_and_name()
TMP_FOLDER = '/tmp'
PYTHON_BIN = os.path.dirname(sys.executable)
VAR_ROOT = os.path.join(PROJECT_DIR, PROJECT_NAME, 'var')
