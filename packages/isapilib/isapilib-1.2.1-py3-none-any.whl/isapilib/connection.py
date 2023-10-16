from django.db import connections

from isapilib.exceptions import SepaException
from isapilib.models import SepaBranch, UserAPI, SepaBranchUsers


def add_conn(username, gwmbac):
    try:
        user = UserAPI.objects.get(usuario=username)
        branch = SepaBranch.objects.get(gwmbac=gwmbac)
        permission = SepaBranchUsers.objects.get(iduser_id=user.id, idbranch_id=branch.id)

        conn = f'external-{branch.id}'
        connections.databases[conn] = {
            'ENGINE': 'mssql',
            'NAME': branch.conf_db if branch.conf_db else '',
            'USER': branch.conf_user if branch.conf_user else '',
            'PASSWORD': branch.conf_pass if branch.conf_pass else '',
            'HOST': branch.conf_ip_ext if branch.conf_ip_ext else '',
            'PORT': branch.conf_port if branch.conf_port else '',
            'TIME_ZONE': None,
            'CONN_HEALTH_CHECKS': None,
            'CONN_MAX_AGE': None,
            'ATOMIC_REQUESTS': None,
            'AUTOCOMMIT': True,
            'OPTIONS': {
                'driver': 'ODBC Driver 17 for SQL Server',
            }
        }
        return conn
    except UserAPI.DoesNotExist:
        raise SepaException('The user does not exist')
    except SepaBranch.DoesNotExist:
        raise SepaException('The agency does not exist')
    except SepaBranchUsers.DoesNotExist:
        raise SepaException('You do not have permissions on the agency')
