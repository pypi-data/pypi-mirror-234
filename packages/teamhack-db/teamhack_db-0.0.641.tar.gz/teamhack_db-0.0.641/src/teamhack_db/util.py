from dnslib import QTYPE

def get_name(name):
  if not name.endswith('.'): name = f'{name}.'
  return name

def get_record_type(record_type):
  if   record_type == 'A':  return QTYPE.A
  elif record_type == 'NS': return QTYPE.NS
  elif record_type == 'MX': return QTYPE.MX
  return None

