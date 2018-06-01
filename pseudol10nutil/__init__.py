try:
    from pseudol10nutil import POFileUtil, PseudoL10nUtil
except ImportError:
    from .pseudol10nutil import POFileUtil, PseudoL10nUtil

__all__ = ["POFileUtil", "PseudoL10nUtil"]
