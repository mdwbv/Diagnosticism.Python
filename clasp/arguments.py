
from .flag_argument import FlagArgument
from .option_alias import OptionAlias
from .option_argument import OptionArgument

import re

class Arguments:

    def __init__(self, argv, aliases = None):

        if not isinstance(argv, ( list, tuple )):

            raise TypeError("'argv' argument must be an instance of 'list' or 'tuple'")

        if aliases and not isinstance(aliases, ( list, tuple )):

            raise TypeError("'aliases' argument must be None or an instance of 'list' or 'tuple'")


        self.argv       =   argv

        self.aliases    =   aliases if aliases else ()

        flags, options, values  =   Arguments._parse(argv, self.aliases)

        for arg in argv:

            pass

        self.flags      =   tuple(flags)
        """The parsed flags"""

        self.options    =   tuple(options)
        """The parsed options"""

        self.values     =   tuple(values)
        """The parsed values"""


    @staticmethod
    def _parse(argv, aliases):

        flags           =   []
        options         =   []
        values          =   []

        forced_value    =   False
        current_option  =   None

        for index, arg in enumerate(argv):

            if not forced_value:

                if '--' == arg:

                    forced_value = True

                    continue

            if current_option:

                current_option.value    =   arg

                options.append(current_option)

                current_option          =   None

                continue

            if forced_value:

                values.append(arg)

                continue

            m = re.match(r'(-+)([^=]+)', arg)

            if m:

                hyphens         =   m.group(1)
                given_label     =   m.group(2)
                given_name      =   hyphens + given_label
                resolved_name   =   given_name
                argument_alias  =   None
                extras          =   None
                value           =   None
                is_option       =   False

                gr              =   m.group()

                if gr != arg:

                    # The option has an attached value

                    value       =   arg[1 + len(gr):]
                    is_option   =   True

                # Now look through the aliases, for:
                #
                # - the resolved name, and
                # - the default value, if none was attached
                for i, a in enumerate(aliases):

                    if a.name == given_name or given_name in a.aliases:

                        is_option       =   isinstance(a, OptionAlias)

                        resolved_name   =   a.name
                        argument_alias  =   a
                        extras          =   a.extras

                        hyphens_2       =   None
                        given_label_2   =   None
                        value_2         =   None
                        resolved_name_2 =   None

                        alias_has_value =   False

                        m2 = re.match(r'(-+)([^=]+)=(.*)', resolved_name)

                        if m2:

                            alias_has_value =   True

                            hyphens_2       =   m2.group(1)
                            given_label_2   =   m2.group(2)
                            value_2         =   m2.group(3)
                            resolved_name_2 =   hyphens_2 + given_label_2

                            resolved_name   =   resolved_name_2

                        else:

                            pass

                        if is_option:


                            if value != None:

                                if alias_has_value:

                                    sys.stderr.write("\t\talias_has_value\n")

                                    value   =   value_2
                                else:

                                    if a.default_value:

                                        value   =   a.default_value
                        else:

                            if alias_has_value:

                                is_option   =   True
                                value       =   value_2

                        break

                if is_option:

                    option      =   OptionArgument(arg, index, given_name, resolved_name, argument_alias, len(hyphens), given_label, value, extras)

                    if value:

                        options.append(option)
                    else:

                        current_option  =   option
                else:

                    flag        =   FlagArgument(arg, index, given_name, resolved_name, argument_alias, len(hyphens), given_label, extras)

                    flags.append(flag)

            else:

                values.append(arg)

        if current_option:

            value   =   None
            alias   =   current_option.argument_alias

            if alias:

                if alias.default_value:

                    current_option.value = alias.default_value

            options.append(current_option)


        return flags, options, values

