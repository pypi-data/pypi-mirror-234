import pyfiglet


class SpringBootBannerGenerator:
    def __init__(self, banner_text, output_dir="."):
        self.banner_text = banner_text
        self.output_dir = output_dir

    def generate_banner(self):
        banner_text = self.generate_banner_text()
        banner_file_path = f"{self.output_dir}/banner.txt"
        with open(banner_file_path, "w") as file:
            file.write(banner_text)

    def generate_banner_text(self):
        banner_text = pyfiglet.figlet_format(self.banner_text, font="big")
        banner_lines = banner_text.splitlines()

        for i in range(len(banner_lines)):
            banner_lines[i] = "${Ansi.GREEN} " + banner_lines[i]

        spring_boot_text = "\n${Ansi.GREEN}\n${Ansi.RED} :: ${spring.application.name} - v${spring.application.version} :: Powered By: Spring Boot${spring-boot.formatted-version} :: \o/\n${Ansi.DEFAULT}"
        banner_text = "\n".join(banner_lines) + spring_boot_text + "\n"
        return banner_text

