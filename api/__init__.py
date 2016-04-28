from api.app import create_app
from api.settings import DevConfig

app = create_app(config_object=DevConfig)
