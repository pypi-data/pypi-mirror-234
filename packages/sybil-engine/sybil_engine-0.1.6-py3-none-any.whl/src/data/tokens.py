from core.engine.config.app_config import get_network
from core.engine.data.networks import NetworkNotFoundException
from core.engine.utils.file_loader import load_json_resource


def get_tokens_for_chain(chain):
    network = get_network()

    if network == 'MAIN':
        return load_json_resource("../../../resources/main/tokens.json")[chain]
    elif network == 'LOCAL':
        return load_json_resource("../../../resources/local/tokens.json")[chain]
    elif network == 'GOERLI':
        return load_json_resource("../../../resources/goerli/tokens.json")[chain]
    else:
        raise NetworkNotFoundException(f"{chain} not found")
