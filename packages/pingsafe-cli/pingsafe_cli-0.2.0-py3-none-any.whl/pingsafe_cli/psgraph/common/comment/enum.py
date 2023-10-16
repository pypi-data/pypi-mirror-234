import re

COMMENT_REGEX = re.compile(r'(pingsafe:skip=) *([A-Za-z_\d]+)(:[^\n]+)?')
