import json
from random import choice
from typing import Dict, List
from melobot import Plugin, session
from melobot import ArgFormatter as Format
from melobot import send, this_dir, clear_cq

from ..env import COMMON_CHECKER, PASER_GEN


be_ill = Plugin.on_message(checker=COMMON_CHECKER,
                           parser=PASER_GEN.gen(["发病", "ill"],
                                                formatters=[
                                                    Format(verify=lambda x: len(x) <= 20,
                                                           src_desc="发病对象",
                                                           src_expect="字符数 <= 20")
                                                ]))


data_path = this_dir("data.json")

class AsoulIllness(Plugin):
    def __init__(self) -> None:
        super().__init__()
        with open(data_path, encoding='utf-8') as fp:
            self.data: List[Dict[str, str]] = json.load(fp)

    @be_ill
    async def be_ill(self) -> None:
        target = session.args.vals.pop(0)
        target = clear_cq(target)
        text_pair = choice(self.data)
        text, person = text_pair["text"], text_pair["person"]
        text = text.replace(person, target)
        await send(text, enable_cq=True)
