import typing_extensions

from automation_test_with_submodule.apis.tags import TagValues
from automation_test_with_submodule.apis.tags.greetings_api import GreetingsApi

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
