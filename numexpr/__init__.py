###################################################################
#  Numexpr - Fast numerical array expression evaluator for NumPy.
#
#      License: MIT
#      Author:  See AUTHORS.txt
#
#  See LICENSE.txt and LICENSES/*.txt for details about copyright and
#  rights to use.
####################################################################

"""
Numexpr is a fast numerical expression evaluator for NumPy.  With it,
expressions that operate on arrays (like "3*a+4*b") are accelerated
and use less memory than doing the same calculation in Python.

See:

https://github.com/pydata/numexpr

for more info about it.

"""

from .__config__ import show as show_config, get_info

if get_info('mkl'):
    use_vml = True
else:
    use_vml = False

is_cpu_amd_intel = False # DEPRECATION WARNING: WILL BE REMOVED IN FUTURE RELEASE

# cpuinfo imports were moved into the test submodule function that calls them 
# to improve import times.

import os, os.path
import platform
from numexpr.expressions import E
from numexpr.necompiler import NumExpr, disassemble, evaluate, re_evaluate
# from numexpr.tests import test, print_versions
from numexpr.interpreter import MAX_THREADS
from numexpr.utils import (
    get_vml_version, set_vml_accuracy_mode, set_vml_num_threads,
    set_num_threads, detect_number_of_cores, detect_number_of_threads)

# Detect the number of cores
ncores = detect_number_of_cores()
nthreads = detect_number_of_threads()

# Initialize the number of threads to be used
if 'sparc' in platform.machine():
    import warnings

    warnings.warn('The number of threads have been set to 1 because problems related '
                  'to threading have been reported on some sparc machine. '
                  'The number of threads can be changed using the "set_num_threads" '
                  'function.')
    set_num_threads(1)
else:
    set_num_threads(nthreads)

# The default for VML is 1 thread (see #39)
set_vml_num_threads(1)

from . import version

dirname = os.path.dirname(__file__)

__version__ = version.version

def print_versions():
    """Print the versions of software that numexpr relies on."""
    try:
        import numexpr.tests
        return numexpr.tests.print_versions()
    except ImportError:
        # To maintain Python 2.6 compatibility we have simple error handling
        raise ImportError('`numexpr.tests` could not be imported, likely it was excluded from the distribution.')

def test(verbosity=1):
    """Run all the tests in the test suite."""
    try:
        import numexpr.tests
        return numexpr.tests.test(verbosity=verbosity)
    except ImportError:
        # To maintain Python 2.6 compatibility we have simple error handling
        raise ImportError('`numexpr.tests` could not be imported, likely it was excluded from the distribution.')