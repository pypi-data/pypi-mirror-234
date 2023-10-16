import os

from ruamel.yaml import YAML

from jtech.manipulate.yaml_manipulator import YamlManipulator


class GenerateDockerCompose(YamlManipulator):
    def __init__(self, param, path):
        self.param = param
        self.path = path
        self.yaml = YAML()
        self.yaml.preserve_quotes = True

    def generate_mongodb_service(self):
        """Generate MongoDB Service"""
        mongodb = {
            'jtech-mongodb-server': {
                'container_name': 'jtech-mongodb-server',
                'image': 'mongo:4.4.6',
                'restart': 'always',
                'ports': ['27017:27017'],
                'volumes': ['$PWD/storage/mongo:/data/db'],
                'networks': ['dev-services']
            }
        }
        data = self.read_yaml()
        if 'services' not in data or data['services'] is None:
            data['services'] = {}
        data['services'].update(mongodb)
        self.save_yaml(data)

    def generate_redis_server_service(self):
        """Generate Redis Server Service"""
        redis_server = {
            'jtech-redis-server': {
                'container_name': 'jtech-redis-server',
                'image': 'redis',
                'restart': 'always',
                'command': 'redis-server --requirepass root',
                'ports': ['6379:6379'],
                'networks': ['dev-services']
            }
        }
        data = self.read_yaml()
        if 'services' not in data or data['services'] is None:
            data['services'] = {}
        data['services'].update(redis_server)
        self.save_yaml(data)

    def generate_keycloak_service(self):
        """Generate Keycloak Service"""
        keycloak_service = {
            'jtech-keycloak-service': {
                'container_name': 'jtech-keycloak-service',
                'image': 'quay.io/keycloak/keycloak:18.0.0',
                'restart': 'always',
                'environment': {
                    'DB_VENDOR': 'h2',
                    'KEYCLOAK_ADMIN': 'admin',
                    'KEYCLOAK_ADMIN_PASSWORD': 'admin'
                },
                'networks': ['dev-services'],
                'volumes': ['./keycloak/ssl.sh:/init.sh'],
                'ports': ['18080:8080'],
                'entrypoint': ['/opt/keycloak/bin/kc.sh', 'start-dev']
            }
        }
        data = self.read_yaml()
        if 'services' not in data or data['services'] is None:
            data['services'] = {}
        data['services'].update(keycloak_service)
        self.save_yaml(data)

    def generate_redpanda_console_service(self):
        """Generate Redpanda Console Service"""
        redpanda_console = {
            'jtech-redpanda-console': {
                'image': 'docker.redpanda.com/redpandadata/console:latest',
                'ports': ['8080:8080'],
                'environment': {
                    'KAFKA_BROKERS': 'localhost:9092'
                },
                'network_mode': 'host'
            }
        }
        data = self.read_yaml()
        if 'services' not in data or data['services'] is None:
            data['services'] = {}
        data['services'].update(redpanda_console)
        self.save_yaml(data)

    def generate_zipkin_server_service(self):
        """Generate Zipkin Server Service"""
        zipkin_server = {
            'jtech-zipkin-server': {
                'container_name': 'jtech-zipkin-server',
                'image': 'openzipkin/zipkin',
                'restart': 'always',
                'ports': ['9411:9411'],
                'networks': ['dev-services']
            }
        }
        data = self.read_yaml()
        if 'services' not in data or data['services'] is None:
            data['services'] = {}
        data['services'].update(zipkin_server)
        self.save_yaml(data)

    def generate_zookeeper_server_service(self):
        """Generate Zookeeper Server Service"""
        zookeeper_server = {
            'jtech-zookeeper-server': {
                'container_name': 'jtech-zookeeper-server',
                'image': 'confluentinc/cp-zookeeper:latest',
                'restart': 'always',
                'networks': ['dev-services'],
                'environment': {
                    'ZOOKEEPER_CLIENT_PORT': '2181',
                    'ZOOKEEPER_TICK_TIME': '2000'
                }
            }
        }
        data = self.read_yaml()
        if 'services' not in data or data['services'] is None:
            data['services'] = {}
        data['services'].update(zookeeper_server)
        self.save_yaml(data)

    def generate_kafka_server_service(self):
        """Generate Kafka Server Service"""
        kafka_server = {
            'jtech-kafka-server': {
                'container_name': 'jtech-kafka-server',
                'image': 'confluentinc/cp-kafka:latest',
                'restart': 'always',
                'networks': ['dev-services'],
                'depends_on': ['jtech-zookeeper-server'],
                'ports': ['9092:9092'],
                'environment': {
                    'KAFKA_BROKER_ID': '1',
                    'KAFKA_ZOOKEEPER_CONNECT': 'zookeeper:2181',
                    'KAFKA_ADVERTISED_LISTENERS': 'PLAINTEXT://jtech-kafka-server:29092,PLAINTEXT_HOST://localhost:9092',
                    'KAFKA_LISTENER_SECURITY_PROTOCOL_MAP': 'PLAINTEXT:PLAINTEXT,PLAINTEXT_HOST:PLAINTEXT',
                    'KAFKA_INTER_BROKER_LISTENER_NAME': 'PLAINTEXT',
                    'KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR': '1'
                }
            }
        }
        data = self.read_yaml()
        if 'services' not in data or data['services'] is None:
            data['services'] = {}
        data['services'].update(kafka_server)
        self.save_yaml(data)

    def generate_rabbitmq_service(self):
        """Generate RabbitMQ Service"""
        rabbitmq = {
            'jtech-rabbitmq-service': {
                'image': 'rabbitmq:3.8.11-management',
                'mem_limit': '521m',
                'ports': ['5672:5672', '15672:15672'],
                'volumes': ['$PWD/storage/rabbitmq:/var/lib/rabbitmq'],
                'environment': [
                    'RABBITMQ_ERLANG_COOKIE=secret_pass',
                    'RABBITMQ_DEFAULT_USER=root',
                    'RABBITMQ_DEFAULT_PASS=root'
                ],
                'healthcheck': {
                    'test': ['CMD', 'rabbitmqctl', 'status'],
                    'interval': '5s',
                    'timeout': '2s',
                    'retries': 60
                }
            }
        }
        data = self.read_yaml()

        if 'services' not in data or data['services'] is None:
            data['services'] = {}

        data['services'].update(rabbitmq)
        self.save_yaml(data)

    def generate_mosquitto_service(self):
        """Generate Mosquitto Service"""
        mosquitto = {
            'jtech-mosquitto-service': {
                'image': 'eclipse-mosquitto',
                'network_mode': 'host',
                'volumes': [
                    './conf:/config',
                    './data:/data',
                    './log:/log'
                ]
            }
        }
        data = self.read_yaml()
        data.update(mosquitto)
        self.save_yaml(data)

    def generate(self):
        """Generate based with choice"""
        self.create_empty_yaml()
        plain = {
            'version': '3.0',
            'services': None,
            'networks': {
                "dev-services": None
            }
        }
        self.add_data(plain)
        data = self.read_yaml()
        self.save_yaml(data)

        if self.param.mongo:
            self.generate_mongodb_service()

        if self.param.redis:
            self.generate_redis_server_service()

        if self.param.kafka:
            self.generate_zookeeper_server_service()
            self.generate_kafka_server_service()
            self.generate_redpanda_console_service()

        if self.param.zipkin:
            self.generate_zipkin_server_service()

        if self.param.rabbitmq:
            self.generate_rabbitmq_service()
