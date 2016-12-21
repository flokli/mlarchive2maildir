import re

import six


def _deobfuscate_addr(addr):
    """replaces some obfuscaded mail addresses to their real ones"""
    p = re.compile(r"(?P<user>[\w\s\-\.\+]+) at (?P<domain>[\w\.-]+) \((?P<name>.*)\)")
    out = re.sub(p, r"\g<name> <\g<user>@\g<domain>>", addr)
    return out


def deobfuscate(message):
    for header in ('To', 'From', 'Cc', 'Reply-To'):
        if message[header] and isinstance(message[header], six.string_types):
            deobf_addr = _deobfuscate_addr(message[header])
            del message[header]
            message[header] = deobf_addr
