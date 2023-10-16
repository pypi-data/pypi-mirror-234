from jtech.cqrs_generators.aggregate.cqrs_aggregator_generator import CqrsAggregatorGenerator
from jtech.cqrs_generators.aggregate.cqrs_aggregator_impl_generator import CqrsAggregatorImplGenerator
from jtech.cqrs_generators.commands.cqrs_command_generator import CqrsCommandGenerator
from jtech.cqrs_generators.controllers.cqrs_create_controller_generator import CqrsCreateControllerGenerator
from jtech.cqrs_generators.controllers.cqrs_find_by_id_controller_generator import CqrsFindByIdControllerGenerator
from jtech.cqrs_generators.entities.cqrs_entity_default_generator import CqrsEntityDefaultGenerator
from jtech.cqrs_generators.entities.cqrs_entity_jpa_2_generator import CqrsEntityJpa2Generator
from jtech.cqrs_generators.entities.cqrs_entity_jpa_3_generator import CqrsEntityJpa3Generator
from jtech.cqrs_generators.entities.cqrs_entity_mongo_generator import CqrsEntityMongoGenerator
from jtech.cqrs_generators.infra.cqrs_api_error_generator import CqrsApiErrorGenerator
from jtech.cqrs_generators.infra.cqrs_api_sub_error_generator import CqrsApiSubErrorGenerator
from jtech.cqrs_generators.infra.cqrs_api_validation_error_generator import CqrsApiValidationErrorGenerator
from jtech.cqrs_generators.infra.cqrs_gen_id_generator import CqrsGenIdGenerator
from jtech.cqrs_generators.infra.cqrs_global_handler_generator import CqrsGlobalExceptionHandlerGenerator
from jtech.cqrs_generators.infra.cqrs_http_utils_generator import CqrsHttpUtilsGenerator
from jtech.cqrs_generators.infra.cqrs_jsons_generator import CqrsJsonsGenerator
from jtech.cqrs_generators.infra.cqrs_kafka_generator import CqrsKafkaGenerator
from jtech.cqrs_generators.infra.cqrs_openapi_generator import CqrsOpenApiGenerator
from jtech.cqrs_generators.infra.cqrs_redis_generator import CqrsRedisGenerator
from jtech.cqrs_generators.protocols.cqrs_request_generator import CqrsRequestGenerator
from jtech.cqrs_generators.protocols.cqrs_response_generator import CqrsResponseGenerator
from jtech.cqrs_generators.queries.cqrs_find_by_id_query_generator import CqrsFindByIdQueryGenerator
from jtech.cqrs_generators.repositories.cqrs_repository_default_generator import CqrsRepositoryDefaultGenerator
from jtech.cqrs_generators.repositories.cqrs_repository_jpa_generator import CqrsRepositoryJpaGenerator
from jtech.cqrs_generators.repositories.cqrs_repository_mongo_generator import CqrsRepositoryMongoGenerator
from jtech.cqrs_generators.services.cqrs_create_service_generator import CqrsCreateServiceGenerator
from jtech.cqrs_generators.services.cqrs_create_service_impl_generator import CqrsCreateServiceImplGenerator
from jtech.cqrs_generators.services.cqrs_find_by_id_service_generator import CqrsFindByIdServiceGenerator
from jtech.cqrs_generators.services.cqrs_find_by_id_service_impl_generator import CqrsFindByIdServiceImplGenerator
from jtech.cqrs_generators.tests.cqrs_test_command import CqrsCommandTestGenerator
from jtech.cqrs_generators.tests.cqrs_test_create_controller import CqrsCreateControllerTestGenerator
from jtech.cqrs_generators.tests.cqrs_test_create_service import CqrsCreateServiceTestGenerator
from jtech.cqrs_generators.tests.cqrs_test_entity import CqrsEntityTestGenerator
from jtech.cqrs_generators.tests.cqrs_test_find_by_id_controller import CqrsFindByIdControllerTestGenerator
from jtech.cqrs_generators.tests.cqrs_test_find_by_id_query import CqrsFindByIdQueryTestGenerator
from jtech.cqrs_generators.tests.cqrs_test_find_by_id_service import CqrsFindByIdServiceTestGenerator
from jtech.cqrs_generators.tests.cqrs_test_repository import CqrsRepositoryTestGenerator
from jtech.cqrs_generators.tests.cqrs_test_request import CqrsRequestTestGenerator
from jtech.cqrs_generators.tests.cqrs_test_response import CqrsResponseTestGenerator
from jtech.cqrs_generators.tests.cqrs_test_suite import CqrsSuiteTestGenerator


class CqrsCodeGenerator:
    """
    Class for generate All CQRS Samples
    :param project:
    """

    def __init__(self, param, project, capitalize, path, test_path):
        self.project = project
        self.capitalize = capitalize
        self.path = path
        self.param = param
        self.test_path = test_path

    def gen_aggregate(self):
        if self.param.jpa or self.param.mongo:
            aggregate = CqrsAggregatorGenerator(self.param, self.project, self.capitalize, self.path)
            aggregate.generate()
            aggregate_impl = CqrsAggregatorImplGenerator(self.param, self.project, self.capitalize, self.path)
            aggregate_impl.generate()

    def gen_controllers(self):
        if self.param.jpa or self.param.mongo:
            command = CqrsCreateControllerGenerator(self.param, self.project, self.capitalize, self.path)
            query = CqrsFindByIdControllerGenerator(self.param, self.project, self.capitalize, self.path)
            command.generate()
            query.generate()

    def gen_exceptions(self):
        api_error = CqrsApiErrorGenerator(self.param, self.project, self.capitalize, self.path)
        error_sub = CqrsApiSubErrorGenerator(self.param, self.project, self.capitalize, self.path)
        error_validation = CqrsApiValidationErrorGenerator(self.param, self.project, self.capitalize, self.path)
        error_handler = CqrsGlobalExceptionHandlerGenerator(self.param, self.project, self.capitalize, self.path)
        api_error.generate()
        error_handler.generate()
        error_sub.generate()
        error_validation.generate()

    def gen_kafka_configuration(self):
        kafka = CqrsKafkaGenerator(self.param, self.project, self.capitalize, self.path)
        kafka.generate()

    def gen_redis_configuration(self):
        redis = CqrsRedisGenerator(self.param, self.project, self.capitalize, self.path)
        redis.generate()

    def gen_create_command(self):
        command = CqrsCommandGenerator(self.param, self.project, self.capitalize, self.path)
        command.generate()

    def gen_entity(self):
        if self.param.spring_version.startswith("3") & self.param.jpa:
            entity = CqrsEntityJpa3Generator(self.param, self.project, self.capitalize, self.path)
        elif self.param.spring_version.startswith("2") & self.param.jpa:
            entity = CqrsEntityJpa2Generator(self.param, self.project, self.capitalize, self.path)
        elif self.param.mongo and not self.param.jpa:
            entity = CqrsEntityMongoGenerator(self.param, self.project, self.capitalize, self.path)
        else:
            entity = CqrsEntityDefaultGenerator(self.param, self.project, self.capitalize, self.path)

        entity.generate()

    def gen_find_by_id_query(self):
        query = CqrsFindByIdQueryGenerator(self.param, self.project, self.capitalize, self.path)
        query.generate()

    def gen_genid(self):
        genid = CqrsGenIdGenerator(self.param, self.project, self.capitalize, self.path)
        genid.generate()

    def gen_httputils(self):
        httputils = CqrsHttpUtilsGenerator(self.param, self.project, self.capitalize, self.path)
        httputils.generate()

    def gen_jsons(self):
        jsons = CqrsJsonsGenerator(self.param, self.project, self.capitalize, self.path)
        jsons.generate()

    def gen_openapi(self):
        openapi = CqrsOpenApiGenerator(self.param, self.project, self.capitalize, self.path)
        openapi.generate()

    def gen_repository(self):
        if self.param.jpa:
            repository = CqrsRepositoryJpaGenerator(self.param, self.project, self.capitalize, self.path)
        elif self.param.mongo:
            repository = CqrsRepositoryMongoGenerator(self.param, self.project, self.capitalize, self.path)
        else:
            repository = CqrsRepositoryDefaultGenerator(self.param, self.project, self.capitalize, self.path)

        repository.generate()

    def gen_request(self):
        request = CqrsRequestGenerator(self.param, self.project, self.capitalize, self.path)
        request.generate()

    def gen_response(self):
        response = CqrsResponseGenerator(self.param, self.project, self.capitalize, self.path)
        response.generate()

    def gen_services(self):
        if self.param.jpa or self.param.mongo:
            create_service = CqrsCreateServiceGenerator(self.param, self.project, self.capitalize, self.path)
            create_service_impl = CqrsCreateServiceImplGenerator(self.param, self.project, self.capitalize, self.path)
            find_by_id_service = CqrsFindByIdServiceGenerator(self.param, self.project, self.capitalize, self.path)
            find_by_id_service_impl = CqrsFindByIdServiceImplGenerator(self.param, self.project, self.capitalize,
                                                                       self.path)
            create_service.generate()
            create_service_impl.generate()
            find_by_id_service.generate()
            find_by_id_service_impl.generate()

    def gen_tests(self):
        command = CqrsCommandTestGenerator(self.param, self.project, self.capitalize, self.test_path)
        command.generate()
        if self.param.jpa or self.param.mongo:
            controller = CqrsCreateControllerTestGenerator(self.param, self.project, self.capitalize, self.test_path)
            controller.generate()
            service = CqrsCreateServiceTestGenerator(self.param, self.project, self.capitalize, self.test_path)
            service.generate()
            entity = CqrsEntityTestGenerator(self.param, self.project, self.capitalize, self.test_path)
            entity.generate()
            find_controller = CqrsFindByIdControllerTestGenerator(self.param, self.project, self.capitalize,
                                                                  self.test_path)
            find_controller.generate()
            find_query = CqrsFindByIdQueryTestGenerator(self.param, self.project, self.capitalize, self.test_path)
            find_query.generate()
            find_service = CqrsFindByIdServiceTestGenerator(self.param, self.project, self.capitalize, self.test_path)
            find_service.generate()
            repository = CqrsRepositoryTestGenerator(self.param, self.project, self.capitalize, self.test_path)
            repository.generate()

        request = CqrsRequestTestGenerator(self.param, self.project, self.capitalize, self.test_path)
        request.generate()
        response = CqrsResponseTestGenerator(self.param, self.project, self.capitalize, self.test_path)
        response.generate()
        suite = CqrsSuiteTestGenerator(self.param, self.project, self.capitalize, self.test_path)
        suite.generate()

    def all(self):
        self.gen_aggregate()
        self.gen_controllers()
        self.gen_response()
        self.gen_services()
        self.gen_request()
        self.gen_openapi()
        self.gen_entity()
        self.gen_jsons()
        self.gen_genid()
        self.gen_create_command()
        self.gen_exceptions()
        self.gen_find_by_id_query()
        self.gen_httputils()
        self.gen_repository()
        self.gen_tests()

        if self.param.kafka:
            self.gen_kafka_configuration()

        if self.param.redis:
            self.gen_redis_configuration()
