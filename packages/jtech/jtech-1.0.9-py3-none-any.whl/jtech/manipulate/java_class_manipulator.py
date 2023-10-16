class JavaFileManipulator:
    def __init__(self, file_path):
        self.file_path = file_path

    def add_imports(self, import_statements):
        """
        Adiciona uma lista de imports ao arquivo Java.
        :param import_statements: Lista de declarações de import a serem adicionadas.
        """
        with open(self.file_path, 'r') as file:
            lines = file.readlines()

        updated_lines = []

        # Verifica se os imports já existem no arquivo
        for line in lines:
            if line.strip().startswith('import '):
                existing_import = line.strip().replace('import ', '')
                if existing_import in import_statements:
                    import_statements.remove(existing_import)
            updated_lines.append(line)

        # Adiciona os imports restantes abaixo das outras importações
        if import_statements:
            last_import_index = len(updated_lines) - 1
            while last_import_index > 0 and not updated_lines[last_import_index].startswith('import '):
                last_import_index -= 1
            updated_lines.insert(last_import_index + 1, '\n')  # Adiciona uma nova linha antes dos imports

            for import_statement in import_statements:
                updated_lines.insert(last_import_index + 2, f'import {import_statement};\n')
                last_import_index += 1

        with open(self.file_path, 'w') as file:
            file.writelines(updated_lines)

    def add_import_to_class(self, import_statement):
        """
        Add import annotation in java class.
        :param import_statement: imports.
        """
        with open(self.file_path, 'r') as file:
            lines = file.readlines()

        updated_lines = []

        found_class = False
        import_added = False

        for line in lines:
            if not found_class and line.strip().startswith('public class'):
                if isinstance(import_statement, list):
                    updated_lines.append(f'@Import({{ {", ".join(import_statement)} }})\n')
                else:
                    updated_lines.append(f'@Import({import_statement})\n')
                found_class = True

            updated_lines.append(line)

            if not import_added and found_class and line.strip() == '{':
                if isinstance(import_statement, list):
                    for import_item in import_statement:
                        updated_lines.append(f'import {import_item};\n')
                else:
                    updated_lines.append(f'import {import_statement};\n')
                import_added = True

        with open(self.file_path, 'w') as file:
            file.writelines(updated_lines)

    def manipulate_clean_arch(self, param):
        if param.redis & param.kafka:
            imports = [
                param.package + ".config.infra.kafka.KafkaConfiguration",
                param.package + ".config.infra.redis.RedisConfiguration",
                "org.springframework.context.annotation.Import"
            ]
            self.add_import_to_class(["RedisConfiguration.class", "KafkaConfiguration.class"])
            self.add_imports(imports)
        elif param.redis:
            imports = [
                param.package + ".config.infra.redis.RedisConfiguration",
                "org.springframework.context.annotation.Import"
            ]
            self.add_import_to_class("RedisConfiguration.class")
            self.add_imports(imports)
        elif param.kafka:
            imports = [
                param.package + ".config.infra.kafka.KafkaConfiguration",
                "org.springframework.context.annotation.Import"
            ]
            self.add_import_to_class("KafkaConfiguration.class")
            self.add_imports(imports)

    def manipulate_cqrs_arch(self, param):
        if param.redis & param.kafka:
            imports = [
                param.package + ".infra.KafkaConfiguration",
                param.package + ".infra.RedisConfiguration",
                "org.springframework.context.annotation.Import"
            ]
            self.add_import_to_class(["RedisConfiguration.class", "KafkaConfiguration.class"])
            self.add_imports(imports)
        elif param.redis:
            imports = [
                param.package + ".infra.RedisConfiguration",
                "org.springframework.context.annotation.Import"
            ]
            self.add_import_to_class("RedisConfiguration.class")
            self.add_imports(imports)
        elif param.kafka:
            imports = [
                param.package + ".infra.KafkaConfiguration",
                "org.springframework.context.annotation.Import"
            ]
            self.add_import_to_class("KafkaConfiguration.class")
            self.add_imports(imports)

