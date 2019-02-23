
__author__      =   'Matt Wilson'
__copyright__   =   'Copyright 2019, Synesis Software'
__credits__     =   [
        'Garth Lancaster',
        'Matt Wilson',
 ]
__email__       =   'matthew@synesis.com.au'
__license__     =   'BSD-3-Clause'
__maintainer__  =   'Matt Wilson'
__status__      =   'Alpha'
__version__     =   '0.0.2'

from .alias import Alias, alias
from .flag_alias import FlagAlias, flag
from .option_alias import OptionAlias, option

from .arguments import Arguments
from .flag_argument import FlagArgument as Flag
from .option_argument import OptionArgument as Option

import sys

def parse(argv = None, aliases = None):

    argv    =   argv if None != type(argv) else sys.argv

    return Arguments(argv, aliases)


