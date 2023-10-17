from hdfs.ext.kerberos import KerberosClient
from hdfs.client import _Request
 
class NoVerifyKerberosClient(KerberosClient):
    """
    Same with hdfs KerberosClient, but set _Request verify to False. 
    Now you can set url to self-signed https
    """
    _verify = False
    _append = _Request('POST', allow_redirects=False, verify=_verify)  # cf. `read`
    _create = _Request('PUT', allow_redirects=False, verify=_verify)  # cf. `write`
    _delete = _Request('DELETE', verify=_verify)
    _get_acl_status = _Request('GET', verify=_verify)
    _get_content_summary = _Request('GET', verify=_verify)
    _get_file_checksum = _Request('GET', verify=_verify)
    _get_file_status = _Request('GET', verify=_verify)
    _get_home_directory = _Request('GET', verify=_verify)
    _get_trash_root = _Request('GET', verify=_verify)
    _list_status = _Request('GET', verify=_verify)
    _mkdirs = _Request('PUT', verify=_verify)
    _modify_acl_entries = _Request('PUT', verify=_verify)
    _remove_acl_entries = _Request('PUT', verify=_verify)
    _remove_default_acl = _Request('PUT', verify=_verify)
    _remove_acl = _Request('PUT', verify=_verify)
    _open = _Request('GET', stream=True, verify=_verify)
    _rename = _Request('PUT', verify=_verify)
    _set_acl = _Request('PUT', verify=_verify)
    _set_owner = _Request('PUT', verify=_verify)
    _set_permission = _Request('PUT', verify=_verify)
    _set_replication = _Request('PUT', verify=_verify)
    _set_times = _Request('PUT', verify=_verify)
    _allow_snapshot = _Request('PUT', verify=_verify)
    _disallow_snapshot = _Request('PUT', verify=_verify)
    _create_snapshot = _Request('PUT', verify=_verify)
    _delete_snapshot = _Request('DELETE', verify=_verify)
    _rename_snapshot = _Request('PUT', verify=_verify)