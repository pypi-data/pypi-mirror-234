from raft.collection import Collection
from .subscription_tasks import subscriptions
from .resource_group_tasks import resource_groups
from .resource_group_tasks import providers
from .ldap_tasks import update_ldaps_cert


azure_tasks = Collection()
azure_tasks.add_task(subscriptions)
azure_tasks.add_task(resource_groups)
azure_tasks.add_task(providers)
azure_tasks.add_task(update_ldaps_cert)

