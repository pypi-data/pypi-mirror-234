import questionary


class CheckboxWizard:
    """
    Class load options and create choice
    """

    def __init__(self, options):
        self.options = options
        self.selected_options = []

    def select_options(self, sub_options):
        """
        Create a sub options for spring dependencies
        :param sub_options: Sub Options from dependencies.json
        :return: Selected choice
        """
        choice = questionary.checkbox(
            "Select dependencies:",
            choices=sub_options
        ).ask()
        if choice:
            self.selected_options.extend(choice)

    def process_options(self, options):
        """
        Create dependencies from dependencies.json
        :param options: Options read from dependencies.json
        :return: Selected dependencies.
        """
        if isinstance(options, list):
            for option in options:
                self.process_options(option)
        elif isinstance(options, dict):
            for category, items in options.items():
                self.select_options(items)

    def run(self):
        """
        Run selected options.
        :return:
        """
        self.process_options(self.options)
        return self.selected_options
