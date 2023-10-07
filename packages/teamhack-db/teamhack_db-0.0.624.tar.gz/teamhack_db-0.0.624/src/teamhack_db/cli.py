from dnslib          import QTYPE
from psycopg2 import connect

from .sql     import create_table, insert, select_hostname_recordtype
from .util    import get_name, get_record_type

def start_cli(conn):
  while True: # User interface to add and lookup DNS records
    choice = input('\n \n \n - "1" to add a DNS record, \n \n - "2" to add a name server record, \n \n - "3" to lookup a DNS record: \n \n \n')

    if choice == '0': break

    if choice == '1':
        name        = input('Enter the name of the DNS record: \n ')
        name        = get_name(name)
        record_type = input('Enter the type of the DNS record (A, AAAA, MX, etc.): \n')
        rt          = get_record_type(record_type)
        if rt is None:
          print(f'invalid record type: {record_type}\n')
          continue
        value       = input('Enter the value of the DNS record: \n')
        insert(conn, name, rt, value)
        conn.commit()
        print(f'DNS record added: {name} {record_type} {value} \n')

    elif choice == '2':
        name     = input('Enter the name of the domain: \n')
        name     = get_name(name)
        ns_value = input('Enter the name server value: \n')
        insert(conn, name, QTYPE.NS, ns_value)
        conn.commit()
        print(f'NS record added for {name}: {ns_value} \n')

    elif choice == '3':
        name        = input('Enter the name of the DNS record: \n')
        name        = get_name(name)
        record_type = input('Enter the type of the DNS record (A, AAAA, MX, NS, etc.):\n ')
        rt          = get_record_type(record_type)
        if rt is None:
          print(f'invalid record type: {record_type}\n')
          continue
        ip          = select_hostname_recordtype(conn, name, rt)
        #if name in dns_records and record_type in dns_records[name]:
        print(f'{name} {record_type} {ip}')
        #else:
        #    print(f'DNS record not found: {name} {record_type} \n')

    else:
        print('Invalid choice. Please enter "1", "2", or "3". \n \n try again... \n \n')

