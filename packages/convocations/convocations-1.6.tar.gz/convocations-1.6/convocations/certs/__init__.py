from raft import Collection
from .validator import validate_chain
from .ed25519 import ed25519_self_signed_cert


cert_tasks = Collection(
    validate_chain,
    ed25519_self_signed_cert,
)
