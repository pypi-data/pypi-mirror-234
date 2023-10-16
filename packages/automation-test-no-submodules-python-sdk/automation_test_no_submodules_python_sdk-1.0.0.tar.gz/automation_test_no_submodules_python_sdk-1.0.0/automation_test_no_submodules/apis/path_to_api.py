import typing_extensions

from automation_test_no_submodules.paths import PathValues
from automation_test_no_submodules.apis.paths.hello import Hello

PathToApi = typing_extensions.TypedDict(
    'PathToApi',
    {
        PathValues.HELLO: Hello,
    }
)

path_to_api = PathToApi(
    {
        PathValues.HELLO: Hello,
    }
)
