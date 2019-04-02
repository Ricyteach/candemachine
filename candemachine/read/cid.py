from dataclasses import asdict

from .. import cande
from candemachine.candemain import CandeMain


def process(ilines):
    cande_main = CandeMain.from_cid(next(ilines))
    cande_obj = cande(**asdict(cande_main))
    # TODO: continue .cid input file processing
    return cande_obj
