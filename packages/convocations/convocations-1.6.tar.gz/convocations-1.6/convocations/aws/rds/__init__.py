import time

from raft import task
from ...base.utils import print_table
from ...base.utils import notice, notice_end
from ..base import AwsTask, yielder


@task(klass=AwsTask)
def rds_instances(ctx, name='', cluster=None, session=None, profile=None, **kwargs):
    """
    shows all rds instances and their endpoints
    """
    from ..base import name_tag
    from ..ec2 import yield_instances
    notice('getting instances')
    rds = session.client('rds')
    if cluster:
        instances = rds.describe_db_instances(Filters=[{
            'Name': 'db-cluster-id',
            'Values': [ cluster ],
        }])
    else:
        instances = rds.describe_db_instances()
    instances = instances['DBInstances']
    notice_end()
    name = name.lower()
    any_custom = False
    for x in instances:
        st_id = x['DBInstanceIdentifier']
        if name not in st_id.lower():
            continue
        if 'custom' in x['Engine']:
            any_custom = True
            break
    ec2_instances = {}
    if any_custom:
        notice('getting ec2 instance info')
        ec2_instances = {
            name_tag(x): x
            for x in yield_instances(name='db-', session=session)
        }
        notice_end()
    header = [ 'name', 'engine', 'endpoint', 'status', ]
    rows = []
    for x in instances:
        st_id = x['DBInstanceIdentifier']
        engine = x['Engine']
        endpoint = x.get('Endpoint')
        if name not in st_id.lower():
            continue
        rows.append([
            st_id,
            f"{engine} {x['EngineVersion']}",
            f"{endpoint['Address']}:{endpoint['Port']}" if endpoint else '',
            x['DBInstanceStatus'],
        ])
    rows.sort(key=lambda lx: lx[0])
    print_table(header, rows)
    print()
    if not any_custom:
        return
    header = [ 'name', 'id', 'ip', ]
    rows = []
    for x in instances:
        st_id = x['DBInstanceIdentifier']
        engine = x['Engine']
        if name not in st_id.lower():
            continue
        if 'custom' in engine:
            resource_id = x.get('DbiResourceId')
            if not resource_id:
                continue
            key = resource_id.lower()
            y = ec2_instances.get(key)
            if y:
                rows.append([
                    st_id,
                    y['InstanceId'],
                    y['PrivateIpAddress'],
                ])
    rows.sort(key=lambda lx: lx[0])
    print_table(header, rows)


@task(klass=AwsTask)
def rds_clusters(ctx, name='', session=None, profile=None, **kwargs):
    """
    shows all rds instances and their endpoints
    """
    rds = session.client('rds')
    clusters = rds.describe_db_clusters()
    name = name.lower()
    clusters = clusters['DBClusters']
    header = [ 'name', 'endpoint', ]
    rows = []
    for x in clusters:
        cluster_name = x['DBClusterIdentifier']
        cluster_name = cluster_name.lower()
        if name in cluster_name:
            rows.append([
                x['DBClusterIdentifier'],
                x['Endpoint'],
            ])
    rows.sort(key=lambda lx: lx[0])
    print_table(header, rows)


@task(klass=AwsTask)
def sys_password(ctx, cluster_name, session=None, profile=None, **kwargs):
    """
    shows the sys password for an custom rds for oracle rac database
    """
    notice('connecting to rds')
    rds = session.client('rds')
    clusters = rds.describe_db_clusters()
    clusters = clusters['DBClusters']
    notice_end()
    notice(cluster_name)
    cluster_name = cluster_name.lower()
    resource_id = None
    for x in clusters:
        st = x['DBClusterIdentifier'].lower()
        if cluster_name == st:
            resource_id = x['DbClusterResourceId']
            notice_end(resource_id)
            break
    if not resource_id:
        return
    notice('looking up sys password')
    secret_name = f'do-not-delete-rds-custom-{resource_id}-sys-'
    sm = session.client('secretsmanager')
    fn = yielder(sm, 'list_secrets', session, Filters=[{
        'Key': 'name',
        'Values': [ secret_name ],
    }])
    notice_end()
    for x in fn:
        name = x['Name']
        response = sm.get_secret_value(SecretId=name)
        print(response['SecretString'])


@task(klass=AwsTask)
def rds_ssh(ctx, name, session=None, profile=None, **kwargs):
    """
    sshes to a custom rds for oracle rac database
    """
    notice('connecting to rds')
    rds = session.client('rds')
    instances = rds.describe_db_instances(Filters=[{
        'Name': 'db-instance-id',
        'Values': [ name ],
    }])
    instances = instances['DBInstances']
    if instances:
        resource_id = instances[0]['DbiResourceId']
        notice_end(resource_id)
    else:
        notice_end('not found')
        return
    from convocations.aws.ec2 import instance_by_name
    from convocations.aws.ec2.ssh import download_secret
    x = instance_by_name(ctx, resource_id, session=session)
    key_name = x.key_name
    username = 'ec2-user'
    ip_address = x.private_ip_address
    notice('key name')
    notice_end(key_name)
    notice('ip address')
    notice_end(ip_address)
    with download_secret(session, x.key_name) as f:
        ssh_cmd = f'ssh -i {f.name} {username}@{ip_address}'
        notice_end(ssh_cmd)
        ctx.run(ssh_cmd, pty=True)
        return


@task(klass=AwsTask)
def download_rds_ssh_key(ctx, name, filename, session=None, **kwargs):
    """
    saves the ssh private key file to a specified filename
    """
    notice('connecting to rds')
    rds = session.client('rds')
    instances = rds.describe_db_instances(Filters=[{
        'Name': 'db-instance-id',
        'Values': [ name ],
    }])
    instances = instances['DBInstances']
    if instances:
        resource_id = instances[0]['DbiResourceId']
        notice_end(resource_id)
    else:
        notice_end('not found')
        return
    from convocations.aws.ec2 import instance_by_name
    from convocations.aws.ec2.ssh import download_secret
    x = instance_by_name(ctx, resource_id, session=session)
    key_name = x.key_name
    notice('key name')
    notice_end(key_name)
    with download_secret(session, x.key_name) as f:
        ctx.run(f'cp -f {f.name} {filename}')


@task(klass=AwsTask)
def delete_rac_cluster(ctx, name, session=None, **kwargs):
    """
    creates the staging oroms rds cluster and database instances
    """
    notice('connecting to rds')
    rds = session.client('rds')
    notice_end()
    notice('getting instances')
    instances = rds.describe_db_instances(Filters=[{
        'Name': 'db-cluster-id',
        'Values': [ name ]
    }])
    instances = instances['DBInstances']
    notice_end()
    for x in instances[1:]:
        st = x['DBInstanceIdentifier']
        notice(f'deleting {st}')
        rds.delete_db_instance(
            DBInstanceIdentifier=st,
            SkipFinalSnapshot=True,
            DeleteAutomatedBackups=True,
        )
        time.sleep(5)
        notice_end()
    notice('deleting cluster')
    rds.delete_db_cluster(
        DBClusterIdentifier=name,
        SkipFinalSnapshot=True,
    )
    notice_end()
