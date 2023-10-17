from core.engine.config.app_config import get_network
from core.engine.data.networks import NetworkNotFoundException
from core.engine.utils.file_loader import load_json_resource


def get_contracts_for_chain(chain):
    network = get_network()

    if network == 'MAIN':
        return load_json_resource("../../../resources/main/contracts.json")[chain]
    elif network == 'LOCAL':
        return load_json_resource("../../../resources/local/contracts.json")[chain]
    elif network == 'GOERLI':
        return load_json_resource("../../../resources/goerli/contracts.json")[chain]
    else:
        raise NetworkNotFoundException(f"{chain} not found")
