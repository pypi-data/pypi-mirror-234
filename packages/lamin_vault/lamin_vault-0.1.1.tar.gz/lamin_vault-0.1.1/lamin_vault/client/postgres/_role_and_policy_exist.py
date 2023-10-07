from hvac.exceptions import InvalidPath


def role_and_policy_exist(vault_client, instance_id, account_id):
    role_name = f"{instance_id}-{account_id}-db"
    policy_name = f"{role_name}-policy"
    try:
        vault_client.secrets.database.read_role(name=role_name)
        vault_client.sys.read_policy(name=policy_name)
        return True
    except InvalidPath:
        return False
