from system.config import default
from system import framework
from system.engine import loader,log,registry
class run:
    def __init__(self):
        registry_ = registry.registry()
        config = default.default_config()
        framework.framework(config)
        registry_.set("config", config)
        registry_.set("log", log.handler(config))
        registry_.set("loader", loader.loader(registry_))
        registry_.run()
        pass