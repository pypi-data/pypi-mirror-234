from requests.structures import CaseInsensitiveDict
import re

UNSET = object()
DFLT_DATA_COLUMN = 'data'
DFLT_NAME_COLUMN = 'name'
DFLT_PNAME_COLUMN = 'parent_name'
SHAREDMEMBER = 'sharedmember'
VIEW = "View"
VIEW_DICT = CaseInsensitiveDict(view=VIEW)
HIERARCHY = CaseInsensitiveDict(
    Base="Base",
    IBase="IBase",
    Children="Children",
    IChildren="IChildren",
    Descendant="Descendant",
    IDescendant="IDescendant",
)
ROOT = "#root"
ACCEPT_LANS = [
    'zh-cn',
    'en'
]
RE_DIMNAME_PARSER = re.compile('(?P<name>.*){(?P<body>.*)}')
RE_SERVER_NAME_PARSER = re.compile('^[a-z-]+(?P<ver>[0-9-]+)$', re.IGNORECASE)
RE_MODULEID_PARSER = re.compile('^[A-Z]+(?P<ver>[0-9_]+)$', re.IGNORECASE)
RE_SYS_SERVER_PARSER = re.compile('^(?:https?://)?([a-z-]+-server)$', re.IGNORECASE)
DECIMAL_COL = 'decimal_val'
STRING_COL = 'string_val'
INDEX_FIELD = 'index'
