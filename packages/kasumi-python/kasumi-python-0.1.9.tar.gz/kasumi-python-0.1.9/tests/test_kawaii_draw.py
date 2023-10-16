from examples.stable_diffussion.main import *

def test_stable_diffussion():
    kasumi = Kasumi(
        KasumiConfigration(
            kasumi_url='http://127.0.0.1:8192',
            app_id=58,
            token='',
            search_key=SEARCH_KEY,
        )
    )
    kasumi.add_action(KawaiiDrawAction())
    kasumi.run_forever(5984)