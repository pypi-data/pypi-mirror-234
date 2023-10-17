from tidypath import savedata, savefig, add_arg, modify_arg, delete_arg, SavedataSkippedComputation
from . import script_fmt
from . import np_utils
from . import pd_utils
from . import storage
from . import plots
from . import stats
from . import decomposition
from . import clustering
from .stats import bootstrap, conf_interval
from .stats.rtopy import resample
from .stats.test import permutation
from .storage import delete_stdin_files
from .script_fmt import getopt_printer, incompleted_programs_shell_script
