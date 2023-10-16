import os
import pathlib

import i18n
from fastapi_exception import BaseTranslatorService


class I18nService(BaseTranslatorService):
    def __init__(self):
        i18n.set('file_format', 'json')
        i18n.set('filename_format', '{namespace}.{format}')
        i18n.set('fallback', 'en')
        i18n.set('enable_memoization', True)

        i18r_dir = f'{pathlib.Path(os.path.abspath(os.path.dirname(__file__))).parent}/i18n'
        i18n.load_path.append(i18r_dir)

    def translate(self, key: str, **kwargs):
        return i18n.t(key, **kwargs)


i18n_service = I18nService()
