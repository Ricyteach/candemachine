from dataclasses import asdict

from .. import cande
from ..exceptions import CandeDeserializationError
from ..candemain import CandeMain


def cande_obj(cande_main):
    cande_obj = cande(**asdict(cande_main))
    # TODO: continue .cid input file processing
    return cande_obj


PREAMBLE_END = 27
CID_CONSTRUCTORS = {CandeMain:cande_obj, }


def preamble_test(line):
    return line[PREAMBLE_END - 2:PREAMBLE_END] == "!!"


def remove_preambles(lines):
    # remove preamble from each line if it is there
    for i,line in enumerate(lines):
        if preamble_test(line):
            lines[i] = line[PREAMBLE_END:]


def check_preamble(lines):
    if all(line[PREAMBLE_END-2:PREAMBLE_END]=="!!" for line in lines if line.strip() and line.strip()!="STOP") and \
            any(line[PREAMBLE_END-2:PREAMBLE_END]=="!!" for line in lines):
        return True


def process(ilines):
    lines = list(ilines)
    if check_preamble(lines):
        remove_preambles(lines)
    for cls in CID_CONSTRUCTORS:
        try:
            obj = cls.from_cid(lines[0])
        except CandeDeserializationError:
            continue
        else:
            break
    else:
        raise CandeDeserializationError(f"Failed to identify type of first .cid file line:\n{lines[0]!r}")

    return CID_CONSTRUCTORS[type(cande_obj)](cande_obj)
