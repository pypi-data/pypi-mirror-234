"""Format data."""

import eth_utils.address

# GENERIC #####################################################################

def strip_hex_prefix(data: str) -> str:
    return data.replace('0x', '')

# ADDRESS #####################################################################

def format_address_with_checksum(address: str) -> str:
    __address = '0x{0:0>40x}'.format(int(address if address else '0', 16))
    return eth_utils.address.to_checksum_address(__address)
