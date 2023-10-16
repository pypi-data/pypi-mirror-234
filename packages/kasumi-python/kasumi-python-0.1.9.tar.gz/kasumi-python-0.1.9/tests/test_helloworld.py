from typing import List, Dict
from kasumi import Kasumi,KasumiConfigration,DefaultActionStrategy
from examples.helloworld.helloworld import PopipaSpider,popipa_search_desc

def test_helloworld():
    app = Kasumi(
        KasumiConfigration(app_id=0, token=0, search_key="",search_desc=popipa_search_desc, search_strategy=DefaultActionStrategy)
    )
    app.add_action(PopipaSpider(app))
    app.run_forever()