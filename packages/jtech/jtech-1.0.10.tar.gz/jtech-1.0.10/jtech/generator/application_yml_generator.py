from jtech.manipulate.application_yml_manipulator import ApplicationYmlManipulator


class ApplicationYmlGenerator:
    def __init__(self, param, file, project, package):
        self.param = param
        self.file = file
        self.package = package
        self.project = project

    def generate(self):
        application = ApplicationYmlManipulator(self.file)
        application.generate_header(self.project, self.package)

        if self.param.kafka:
            application.generate_kafka_configuration()

        if self.param.redis:
            application.generate_redis_configuration()

        if self.param.jpa:
            application.generate_jpa_configuration()

        if self.param.mongo:
            application.generate_mongodb_configuration(self.project)

        if self.param.zipkin:
            application.generate_zipkin_configuration()

        if self.param.config_server:
            application.generate_config_server_configuration()

        if self.param.eureka_client:
            application.generate_eureka_client_configuration()
