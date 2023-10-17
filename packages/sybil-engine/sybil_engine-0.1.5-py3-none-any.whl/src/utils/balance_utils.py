from _decimal import Decimal, ROUND_DOWN

from loguru import logger

from core.contract.erc20contract import Erc20Contract
from core.contract.stargate_token_pool import StargateTokenPool
from core.contract.weth import WETH
from core.engine.data.tokens import get_tokens_for_chain
from core.engine.utils.utils import AccountException, interval_to_round
from core.engine.utils.web3_utils import from_eth_to_wei, from_wei_to_eth


def verify_balance(min_native_balance, chain_instance, account, web3):
    native_balance = get_native_balance(account, web3, chain_instance)

    logger.info(f"Native balance: {native_balance.log_line()}")

    if min_native_balance.wei >= native_balance.wei:
        raise NotEnoughNativeBalance(f"Min native balance {min_native_balance.log_line()} > native balance",
                                     chain_instance['chain'])

    return native_balance


def amount_to_swap_for_pair(account, chain, min_native_balance, native_balance, pair, swap_amount_interval, swap_token,
                            web3):
    if swap_amount_interval == '':
        swap_amount_interval = pair['amount']

    if swap_token == 'ETH':
        amount_to_swap = interval_to_eth_balance(swap_amount_interval, account, chain, web3)

        if swap_amount_interval == 'all_balance':
            amount_to_swap = amount_to_swap.minus(min_native_balance)

        if amount_to_swap.wei > native_balance.wei:
            raise NotEnoughNativeBalance(
                f"Account balance {native_balance.log_line()} < {amount_to_swap.log_line()} amount to swap.")
    else:
        amount_to_swap = interval_to_erc20_balance(swap_amount_interval, account, swap_token, chain, web3)

    return amount_to_swap


def interval_to_erc20_balance(erc20_interval, account, token, chain, web3):
    if erc20_interval == 'all_balance':
        return Erc20Token(chain, token, web3).balance(account)
    else:
        return Erc20Balance(int(interval_to_round(erc20_interval) * 10 ** 6), chain, token)


def interval_to_weth_balance(erc20_interval, account, chain, web3):
    if erc20_interval == 'all_balance':
        return WETHToken(chain, web3).balance(account)
    else:
        return WETHBalance(int(interval_to_round(erc20_interval) * 10 ** 6), chain)


def interval_to_eth_balance(eth_interval, account, chain, web3):
    if eth_interval == 'all_balance':
        balance = get_native_balance_for_params(account, web3, chain, 'ETH')
    else:
        balance = NativeBalance(from_eth_to_wei(interval_to_round(eth_interval)), chain, 'ETH')

    return NativeBalance(int(balance.wei // 10000) * 10000, chain, balance.token)


def get_native_balance(account, web3, chain_instance):
    return NativeBalance(web3.eth.get_balance(account.address), chain_instance['chain'], chain_instance['gas_token'])


def get_native_balance_for_params(account, web3, chain, token):
    return NativeBalance(web3.eth.get_balance(account.address), chain, token)


def get_max_balance_data(token_type, chains, account):
    from core.modules.stargate.web3_utils import get_all_account_data
    data = get_all_account_data(account, chains)
    from core.modules.stargate.web3_utils import print_account_data
    print_account_data(data)

    if token_type == 'USDC':
        return find_chain_with_max_usdc(data)
    else:
        return find_chain_with_max_native(data)


def find_chain_with_max_usdc(account_data):
    max_usdc_balance = max(account_data, key=lambda x: x[1].wei_compare())

    if max_usdc_balance[1] == 0:
        raise Exception("Can't bridge tokens, all chain USDC balances are zero")

    return max_usdc_balance


def find_chain_with_max_native(account_data):
    max_native_balance = max(account_data, key=lambda x: x[2].wei_compare())

    if max_native_balance[2] == 0:
        raise Exception("Can't bridge tokens, all chain ETH balances are zero")

    return max_native_balance


class Balance:
    max_number = 1000000000000000000000

    def __init__(self, wei_balance, chain, token):
        self.wei = wei_balance
        self.chain = chain
        self.token = token

    def readable(self):
        raise Exception("not supported")

    def log_line(self):
        if self.readable() < Balance.max_number:
            factor = Decimal('1e{}'.format(-6))
            return str(self.readable().quantize(factor, rounding=ROUND_DOWN)) + ' ' + self.token
        else:
            return self.readable()

    def wei_compare(self):
        pass

    def minus(self, balance):
        if self.chain != balance.chain and balance.chain is not None:
            raise BalanceException(f'Trying to minus wrong chain {self.chain} - {balance.chain}')

        if self.token != balance.token and self.token is not None:
            raise BalanceException(f'Trying to minus wrong token {self.token} - {balance.token}')

        if self.wei <= balance.wei:
            raise BalanceException(f'Result of minus cant be less than 0 {self.wei} - {balance.wei}')

        return self.__class__(
            self.wei - balance.wei,
            self.chain,
            self.token
        )


class NativeBalance(Balance):
    def __init__(self, wei_balance, chain, token):
        super().__init__(wei_balance, chain, token)

    def wei_compare(self):
        return self.wei

    def readable(self):
        return Decimal(from_wei_to_eth(self.wei))


class Erc20Balance(Balance):
    def __init__(self, wei_balance, chain, token):
        super().__init__(wei_balance, chain, token)

    def wei_compare(self):
        if self.chain == 'BSC':
            return self.wei / 10 ** 12
        else:
            return self.wei

    def readable(self):
        if self.chain == 'BSC':
            return Decimal(self.wei / 10 ** 18)
        else:
            return Decimal(self.wei / 10 ** 6)


class WETHBalance(Balance):
    def __init__(self, wei_balance, chain):
        super().__init__(wei_balance, chain, 'WETH')

    def wei_compare(self):
        return self.wei

    def readable(self):
        return Decimal(self.wei / 10 ** 18)


class BalanceException(AccountException):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class NotEnoughERC20Balance(AccountException):
    def __init__(self, message, chain=None):
        self.message = message
        self.chain = chain
        super().__init__(self.message)


class NotEnoughNativeBalance(AccountException):
    def __init__(self, message, chain=None):
        self.message = message
        self.chain = chain
        super().__init__(self.message)


class StargatePoolToken:
    def __init__(self, chain, token, web3):
        self.chain = chain
        self.token = token
        self.web3 = web3
        self.token_pool_contract = StargateTokenPool(get_tokens_for_chain(self.chain)[self.token], self.web3)

    def balance(self, account):
        if self.token == 'STARGATE_USDC_POOL':
            return Erc20Balance(self.token_pool_contract.balance_of(account), self.chain, self.token)
        else:
            return NativeBalance(self.token_pool_contract.balance_of(account), self.chain, self.token)

    def approve(self, account, contract_on_approve):
        return self.token_pool_contract.approve(account, contract_on_approve)

    def allowance(self, account, allowance_contract):
        return self.token_pool_contract.allowance(account, allowance_contract)


class Erc20Token:
    def __init__(self, chain, token, web3):
        self.chain = chain
        self.token = token
        self.web3 = web3
        self.erc20_contract = Erc20Contract(get_tokens_for_chain(self.chain)[self.token], self.web3)

    def balance(self, account):
        return Erc20Balance(self.erc20_contract.balance_of(account), self.chain, self.token)

    def approve(self, account, contract_on_approve):
        return self.erc20_contract.approve(account, contract_on_approve)

    def allowance(self, account, allowance_contract):
        return self.erc20_contract.allowance(account, allowance_contract)


class WETHToken:
    def __init__(self, chain, web3):
        self.chain = chain
        self.web3 = web3
        self.weth_contract = WETH(get_tokens_for_chain(self.chain)['WETH'], self.web3)

    def balance(self, account):
        return WETHBalance(self.weth_contract.balance_of(account), self.chain)
