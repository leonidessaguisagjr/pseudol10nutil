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
        :returns: Copy of the string s with the transforms applied.
        """
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
