import questionary


class SampleChoiceWizard:
    """
    Select Sample Files or not choice

    :param options: Read from array ['Yes', 'No']
    """

    def __init__(self, options):
        self.options = options
        self.selected = ""

    def select_options(self, options):
        choice = questionary.select(
            "Generate Samples:",
            default="yes",
            choices=options
        ).ask()
        if choice:
            self.selected = choice

    def run(self):
        self.select_options(self.options)
        return self.selected
