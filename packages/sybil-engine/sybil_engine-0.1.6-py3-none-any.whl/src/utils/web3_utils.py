from typing import Optional, Any

from web3 import Web3
from web3.middleware import geth_poa_middleware


def from_wei_to_eth(wei):
    return Web3().from_wei(wei, 'ether')


def from_wei_to_gwei(wei):
    return Web3().from_wei(wei, 'gwei')


def from_eth_to_wei(eth):
    return Web3().to_wei(eth, 'ether')


def init_web3(chain_instance, proxy: Optional[Any]):
    if proxy is not None:
        provider = Web3.HTTPProvider(chain_instance['rpc'], request_kwargs={"proxies": {'https': proxy, 'http': proxy}})
    else:
        provider = Web3.HTTPProvider(endpoint_uri=chain_instance['rpc'])

    web3 = Web3(provider=provider)

    if chain_instance['poa']:
        web3.middleware_onion.inject(geth_poa_middleware, layer=0)

    return web3

