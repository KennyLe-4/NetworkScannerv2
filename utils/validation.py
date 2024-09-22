import re
import ipaddress

def is_valid_target(target):
  # Try to validate as an IP address or subnet
  try:
      # This will validate both IP addresses and subnets
      ipaddress.ip_network(target, strict=False)
      return True
  except ValueError:
      pass

  # Regular expression for validating a domain name
  domain_pattern = re.compile(
      r'^(?=.{1,253}$)(?:(?!-)[A-Za-z0-9-]{1,63}(?<!-)\.)+[A-Za-z]{2,}$'
  )

  # Validate as a domain name
  return domain_pattern.match(target) is not None