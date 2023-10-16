class PropertiesCreator:
    def __init__(self, file_path):
        self.file_path = file_path

    def create_gradle_properties(self):
        content = "APP_VERSION=1.0.0-SNAPSHOT\n"

        with open(self.file_path, "w") as file:
            file.write(content)

    def create_test_properties(self):
        content = """# Configuração do banco de dados H2 em memória
spring.datasource.url=jdbc:h2:mem:testdb;DB_CLOSE_DELAY=-1;DATABASE_TO_UPPER=false
spring.datasource.driver-class-name=org.h2.Driver
spring.datasource.username=sa
spring.datasource.password=
spring.jpa.database-platform=org.hibernate.dialect.H2Dialect
spring.jpa.show-sql=true
# Criação automática de tabelas pelo Hibernate
spring.jpa.hibernate.ddl-auto=create
    """
        with open(self.file_path, "w") as file:
            file.write(content.strip())
