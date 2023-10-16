from caos._internal.console.ansi_colors import ColorCode

_LOGO_CAOS_ASCII_SIMPLE = r'''
   ___     _     ___    ___ 
  / __|   / \   /   \  / __|
 | (__   /   \ |     | \__ \
  \___| /_____\ \___/  |___/
'''

_LOGO_CAOS_ASCII_ANSI_COLORS = r'''
   {cyan}___{x}     {green}_{x}     {gray}___{x}    {magenta}___{x} 
  {cyan}/ __|{x}   {green}/ \{x}   {gray}/   \{x}  {magenta}/ __|{x}
 {cyan}| (__{x}   {green}/   \{x} {gray}|     |{x} {magenta}\__ \{x}
  {cyan}\___|{x} {green}/_____\{x} {gray}\___/{x}  {magenta}|___/{x}
'''.format(
    cyan=ColorCode.CYAN, green=ColorCode.GREEN, gray=ColorCode.GRAY, magenta=ColorCode.MAGENTA,x=ColorCode.END
)

_PROMPT_CAOS_SIMPLE = "[caos] {command} --> {message}"
_CAOS_COLORS_TEXT = "[{cyan}c{x}{green}a{x}{gray}o{x}{magenta}s{x}] ".format(
    cyan=ColorCode.CYAN, green=ColorCode.GREEN,
    gray=ColorCode.GRAY, magenta=ColorCode.MAGENTA,
    x=ColorCode.END
)

_PROMPT_CAOS_ANSI_COLORS = _CAOS_COLORS_TEXT + "{command} --> {message}"




