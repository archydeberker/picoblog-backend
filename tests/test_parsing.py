import actions
import models


def test_hashtag_detection():
    text = "#title our new title"
    tags = models.find_hashtags(text)
    assert "#title" in tags

    text = "#publish"
    tags = models.find_hashtags(text)
    assert "#publish" in tags


def test_hashtag_removal():
    text = "#title our new title"
    tags = models.remove_hashtags(text)
    assert "#title" not in tags

    text = "#publish"
    tags = models.remove_hashtags(text)
    assert "#publish" not in tags
