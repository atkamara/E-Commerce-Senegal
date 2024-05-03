from .Model import Config
from functools import cached_property
from .utils import dir

class MainCss(Config):
    _conf_file:str = dir('css.ini')
    @cached_property
    def _val_conf_attr(self):
        return self.css