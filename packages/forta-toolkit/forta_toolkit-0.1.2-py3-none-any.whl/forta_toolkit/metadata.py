"""Load the bot metadata."""

import json
import logging
import os

import web3

# BOT VERSION #################################################################

def get_bot_version() -> str:
    """Read the bot version from the package metadata."""
    __version = ''
    try:
        with open('package.json', 'r') as __f:
            __metadata = json.load(__f)
            __version = __metadata.get('version', '')
    except Exception as e:
        logging.error('could not find the file "package.json"')
    finally:
        return __version

# CHAIN ID ####################################################################

def load_chain_id(provider: web3.Web3) -> int:
    """Load the chain id into the execution environment."""
    __chain_id = 1
    try:
        __chain_id = int(os.environ.get('FORTA_CHAIN_ID', '') or provider.eth.chain_id)
        os.environ['FORTA_CHAIN_ID'] = str(__chain_id)
        logging.info(f'set chain id to {__chain_id}')
    except Exception as e:
        logging.error(f'error getting the chain id (kept to {__chain_id})')
    finally:
        return __chain_id

# SECRETS #####################################################################

def load_secrets(filepath: str='secrets.json') -> dict:
    """Load the secrets into the execution environment."""
    __secrets = {}
    try:
        with open(filepath, 'r') as __f:
            __secrets = json.load(__f)
            for __k, __v in __secrets.items():
                os.environ[__k] = __v
    except Exception as e:
        logging.info(f'could not find the file "{filepath}"')
    finally:
        return __secrets
