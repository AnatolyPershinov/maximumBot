# модуль ищет статью в википедии

import wikipedia


class WikiProcessor:
    def __init__(self, article, *args):
        self.article = article
        self.message : str

    def _get_summary(self):
        wikipedia.set_lang("ru")
        if not self.article:
            return "Запрос пуст"
        
        try:
            return wikipedia.summary(self.article)
        except wikipedia.exceptions.PageError: # в случае если не нашли статью
            return "Не удалось найти информацию по запросу"
        
    def run(self):
        self.message = self._get_summary()
        
