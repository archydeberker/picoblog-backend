import actions
import models

def test_hashtag_detection():
    text = '#title our new title'
    tags = models.find_hashtags(text)
    assert '#title' in tags

    text = '#publish'
    tags = models.find_hashtags(text)
    assert '#publish' in tags