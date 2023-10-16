import questionary


class ArchitectureChoiceWizard:
    """
    Select Architecture type from choice

    :param options: Read from array ['Default', 'Clean', 'Cqrs']
    """

    def __init__(self, options):
        self.options = options
        self.selected = ""

    def select_options(self, options):
        choice = questionary.select(
            "Select Architecture Type:",
            choices=options
        ).ask()
        if choice:
            self.selected = choice

    def run(self):
        self.select_options(self.options)
        return self.selected
