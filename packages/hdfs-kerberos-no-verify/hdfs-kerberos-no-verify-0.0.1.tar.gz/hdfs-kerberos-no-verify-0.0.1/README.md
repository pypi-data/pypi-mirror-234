# HDFS Kerberos but no SSL verify 

A custom of `from hdfs.ext.kerberos import KerberosClient` from [hdfs](https://github.com/mtth/hdfs) package that allow you to use with self-signed https url. 

# Usage 

Use as you use KerberosClient

```python
from hdfs_kerberos_no_verify import NoVerifyKerberosClient as KerberosClient 

# use as you would use KerberosClient

def create_keberos_hdfs_client():
    """
    require kinit
    please kinit from terminal to get ticket first
    """
    import os
    os.environ["KRB5_CONFIG"]="/where/did/you/put-krb5/etc/krb5.conf" 
    hostport = "https://master1975.me.meowingful.com:8999"  # your self-signed https 
    client = KerberosClient(hostport, mutual_auth='DISABLED')
    return client

client = create_keberos_hdfs_client()

client.list("/home/myfile")


```

# To build from source

```
pip install build
python -m build
```