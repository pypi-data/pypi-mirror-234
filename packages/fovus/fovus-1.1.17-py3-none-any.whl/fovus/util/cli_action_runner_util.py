from fovus.constants.cli_constants import CLI_ARGUMENTS


class CliActionRunnerUtil:  # pylint: disable=too-few-public-methods
    @staticmethod
    def get_argument_string_list_from_keys(keys):
        argument_list = []
        for key in keys:
            argument_list.append(str(CLI_ARGUMENTS[key]))
        return argument_list
