try:
    __import__('pkg_resources').declare_namespace(__name__)
except ImportError:
    __path__ = __import__('pkgutil').extend_path(__path__, __name__)

from .persistence import *


class NaverDB():

    def __init__(self, app, config):
        self.persistence = Persistence(app, config)


if __name__ == '__main__':
    pass
