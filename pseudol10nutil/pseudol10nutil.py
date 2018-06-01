import codecs
import os.path
import re

import six

from . import transforms


class PseudoL10nUtil:
    """
    Class for performing pseudo-localization on strings.
    """

    def __init__(self, init_transforms=None):
        """
        Initializer for class.

        :param init_transforms: Optional list of initial transforms.  If not
                                specified, the default list of transforms is
                                transliterate_diacritic, pad_length and
                                square_brackets.
        """
        if init_transforms is not None:
            self.transforms = init_transforms
        else:
            self.transforms = [
                transforms.transliterate_diacritic,
                transforms.pad_length,
                transforms.square_brackets
                ]

    def pseudolocalize(self, s):
        """
        Performs pseudo-localization on a string.  The specific transforms to be
        applied to the string is defined in the transforms field of the object.

        :param s: String to pseudo-localize.
        :returns: Copy of the string s with the transforms applied.  If the input
                  string is an empty string or None, an empty string is returned.
        """
        if not s:  # If the string is empty or None
            return u""
        if not isinstance(s, six.text_type):
            raise TypeError("String to pseudo-localize must be of type '{0}'.".format(six.text_type.__name__))
        # If no transforms are defined, return the string as-is.
        if not self.transforms:
            return s
        fmt_spec = re.compile(
            r"""(
            {.*?}  # https://docs.python.org/3/library/string.html#formatstrings
            |
            %(?:\(\w+?\))?.*?[acdeEfFgGiorsuxX%]  # https://docs.python.org/3/library/stdtypes.html#printf-style-string-formatting
            )""", re.VERBOSE)
        # If we don't find any format specifiers in the input string, just munge the entire string at once.
        if not fmt_spec.search(s):
            result = s
            for munge in self.transforms:
                result = munge(result)
        # If there are format specifiers, we do transliterations on the sections of the string that are not format
        # specifiers, then do any other munging (padding the length, adding brackets) on the entire string.
        else:
            substrings = fmt_spec.split(s)
            for munge in self.transforms:
                if munge in transforms._transliterations:
                    for idx in range(len(substrings)):
                        if not fmt_spec.match(substrings[idx]):
                            substrings[idx] = munge(substrings[idx])
                    else:
                        continue
                else:
                    continue
            result = u"".join(substrings)
            for munge in self.transforms:
                if munge not in transforms._transliterations:
                    result = munge(result)
        return result


class POFileUtil:
    """
    Class for performing pseudo-localization on gettext PO (Portable Object) message catalogs.
    """

    def __init__(self, l10nutil=None):
        """
        Initializer for class.

        :param l10nutil: Optional instance of PseudoL10nUtil object.  This can be used to pass in an instance of the
                         PseudoL10nUtil class with the transforms already configured.  Otherwise, an instance of the
                         PseudoL10nUtil class will be created with the default transforms.
        """
        if not l10nutil:
            self.l10nutil = PseudoL10nUtil()
        else:
            self.l10nutil = l10nutil

    def pseudolocalizefile(self, input_filename, output_filename, input_encoding='UTF-8', output_encoding='UTF-8',
                           overwrite_existing=True):
        """
        Method for pseudo-localizing the message catalog file.

        :param input_filename: Filename of the source (input) message catalog file.
        :param output_filename: Filename of the target (output) message catalog file.
        :param input_encoding: String indicating the encoding of the input file.  Optional, defaults to 'UTF-8'.
        :param output_encoding: String indicating the encoding of the output file.  Optional, defaults to 'UTF-8'.
        :param overwrite_existing: Boolean indicating if an existing output message catalog file should be overwritten.
                                   True by default. If False, an IOError will be raised.
        """
        leading_trailing_double_quotes = re.compile(r'^"|"$')
        output_encoding='UTF-8'
        if not os.path.isfile(input_filename):
            raise IOError("Input message catalog not found: {0}".format(os.path.abspath(input_filename)))
        if os.path.isfile(output_filename) and not overwrite_existing:
            raise IOError("Error, output message catalog already exists: {0}".format(os.path.abspath(output_filename)))
        with codecs.open(input_filename, mode="r", encoding=input_encoding) as in_fileobj:
            with codecs.open(output_filename, mode="w", encoding=output_encoding) as out_fileobj:
                for current_line in in_fileobj:
                    out_fileobj.write(current_line)
                    if current_line.startswith("msgid"):
                        msgid = current_line.split(maxsplit=1)[1].strip()
                        msgid = leading_trailing_double_quotes.sub('', msgid)
                        msgstr = self.l10nutil.pseudolocalize(msgid)
                        out_fileobj.write("msgstr \"{0}\"\n".format(msgstr))
                        next(in_fileobj)
