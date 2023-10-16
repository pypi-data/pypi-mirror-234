import typing_extensions

from automation_test_no_submodules.apis.tags import TagValues
from automation_test_no_submodules.apis.tags.greetings_api import GreetingsApi

TagToApi = typing_extensions.TypedDict(
    'TagToApi',
    {
        TagValues.GREETINGS: GreetingsApi,
    }
)

tag_to_api = TagToApi(
    {
        TagValues.GREETINGS: GreetingsApi,
    }
)
