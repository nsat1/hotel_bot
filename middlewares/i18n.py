from fluentogram import TranslatorHub


class TranslatorRunnerMiddleware:
    def __init__(self, translator_hub: TranslatorHub):
        self.translator_hub = translator_hub

    async def __call__(self, handler, event, data):
        user = data.get('event_from_user')
        translator = self.translator_hub.get_translator_by_locale(user.language_code)
        if translator is None:
            translator = self.translator_hub.get_translator_by_locale('en')
        data['i18n'] = translator

        return await handler(event, data)
