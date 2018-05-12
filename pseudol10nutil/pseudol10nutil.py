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
        if not self.transforms:
            return s
        result = s
        for munge in self.transforms:
            result = munge(result)
        return result
