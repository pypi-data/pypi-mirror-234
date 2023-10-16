"""Moved to :py:mod:`feynml.interface.hepmc`"""
from feynml.interface.hepmc import hepmc_event_to_feynman as _event_to_feynman
from smpl_doc import doc

event_to_feynman = doc.deprecated(
    "2.2.6", "Directly use feynml.interface.hepmc.event_to_feynman()"
)(_event_to_feynman)
