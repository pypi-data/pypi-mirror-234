import questionary


class BannerTextWizard:
    def __init__(self, banner_text):
        self.banner_text = banner_text

    def prompt_banner_text(self):
        self.banner_text = questionary.text("Banner Text: ", default=self.banner_text).ask()

    def run(self):
        self.prompt_banner_text()
