import yaml

from os import listdir
from typing import Any, Dict, List, Union

import fipper


class Language:
    def get_lang(self: 'fipper.Client') -> str:
        langdb = self.mongo_sync.language
        user_id = self.me.id
        mode = self.langm.get(user_id)
        if not mode:
            lang = langdb.find_one({"bot_id": user_id})
            if not lang:
                self.langm[user_id] = "en"
                return "en"
            self.langm[user_id] = lang["lang"]
            return lang["lang"]
        return mode


    def set_lang(self: 'fipper.Client', lang: str):
        langdb = self.mongo_sync.language
        user_id = self.me.id
        self.langm[user_id] = lang
        langdb.update_one(
            {"bot_id": user_id}, {"$set": {"lang": lang}}, upsert=True
        )


    def get_languages(self: 'fipper.Client') -> Dict[str, Union[str, List[str]]]:
        return {
            code: {
                "nama": self.languages[code]["nama"],
                "asli": self.languages[code]["asli"],
                "penulis": self.languages[code]["penulis"],
            }
            for code in self.languages
        }


    def get_string(self: 'fipper.Client'):
        lang = self.get_lang()
        return self.languages[lang]


    async def import_lang(self: 'fipper.Client', file_path):
        for filename in listdir(file_path):
            if filename.endswith(".yml"):
                language_name = filename[:-4]
                self.languages[language_name] = yaml.safe_load(
                    open(file_path + filename, encoding="utf8")
                )
