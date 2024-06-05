from aiogram import types
from fluentogram import TranslatorHub


class TranslatorRunnerMiddleware:
    def __init__(self, translator_hub: TranslatorHub):
        self.translator_hub = translator_hub

    async def __call__(self, handler, event: types.Message, data: dict):
        user = event.from_user
        if user is None:
            translator = self.translator_hub.get_translator_by_locale('en')
        else:
            language_code = user.language_code or 'en'
            translator = self.translator_hub.get_translator_by_locale(language_code)
            if translator is None:
                translator = self.translator_hub.get_translator_by_locale('en')
        data['i18n'] = translator

        return await handler(event, data)
