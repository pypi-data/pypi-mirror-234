# do not import all endpoints into this module because that uses a lot of memory and stack frames
# if you need the ability to import all endpoints from this module, import them with
# from automation_test_with_submodule.paths.hello import Api

from automation_test_with_submodule.paths import PathValues

path = PathValues.HELLO