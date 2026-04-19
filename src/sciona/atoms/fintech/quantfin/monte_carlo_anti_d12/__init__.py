from sciona.ghost.registry import REGISTRY

from .atoms import *  # noqa: F401,F403

insertcf_recursive = REGISTRY["insertcf_recursive"]["impl"]
insertcf_singleton = REGISTRY["insertcf_singleton"]["impl"]
insertcflist_fold = REGISTRY["insertcflist_fold"]["impl"]
insertcflist_fold_alt = REGISTRY["insertcflist_fold_alt"]["impl"]
process_base_case = REGISTRY["process_base_case"]["impl"]
process_with_cashflows_only = REGISTRY["process_with_cashflows_only"]["impl"]
process_with_observation_only = REGISTRY["process_with_observation_only"]["impl"]
process_with_pending_cashflows = REGISTRY["process_with_pending_cashflows"]["impl"]
