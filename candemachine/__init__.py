from candemachine.cande import cande
from candemachine.level3.candeparts import Node, Element, Boundary

# Set default logging handler to avoid "No handler found" warnings.
import logging
from logging import NullHandler

logging.getLogger(__name__).addHandler(NullHandler())
