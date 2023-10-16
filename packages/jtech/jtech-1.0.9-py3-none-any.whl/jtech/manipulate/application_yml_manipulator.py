from ruamel.yaml import YAML

from jtech.manipulate.yaml_manipulator import YamlManipulator


class ApplicationYmlManipulator(YamlManipulator):
    """
    Manipulate Application YML
    """

    def __init__(self, path):
        self.path = path
        self.yaml = YAML()

    def generate_header(self, project, package):
        """Create header file"""
        header_data = {
            'spring': {
                'application': {
                    'name': project,
                    'version': '1.0.0-SNAPSHOT'
                },
                'profiles': {
                    'active': '${PROFILE:dev}'
                }
            },
            'management': {
                'endpoints': {
                    'web': {
                        'exposure': {
                            'include': '*'
                        }
                    }
                }
            },
            'server': {
                'port': '${PORT:0}',
                'forward-headers-strategy': 'framework'
            },
            'logging': {
                'level': {
                    'root': "info",
                    'org.springframework.web': "info",
                    package: "debug"
                },
                'file': {
                    "name": "./logs/${spring.application.name}.log"
                }
            },
            'springdoc': {
                'api-docs': {
                    'groups': {
                        'enabled': 'true'
                    },
                    'path': '/doc/' + project + '/v3/api-documents'
                },
                'swagger-ui': {
                    'enabled': 'true',
                    'path': '/doc/' + project + '/v1/api.html'
                }
            },
            'api': {
                'version': 'v1',
                'description': 'Description here',
                'url': {
                    'homologation': 'http://${HOMOLOGATION_SERVER:172.30.1.24}:${HOMOLOGATION_PORT:8081}',
                    'production': '${PRODUCTION_URI:http://${spring.application.name}.jtech.com.br}'
                }
            }
        }
        self.create_empty_yaml()
        self.add_data(header_data)
        data = self.read_yaml()
        self.save_yaml(data)

    def generate_kafka_configuration(self):
        """Generate Kafka Configuration"""
        kafka = {
            'kafka': {
                'bootstrap-servers': '${KAFKA_HOST:localhost}:${KAFKA_PORT:9092}',
                'listener': {
                    'ack-mode': 'MANUAL_IMMEDIATE',
                    'concurrency': 5
                },
                'producer': {
                    'bootstrap-servers': '${KAFKA_HOST:localhost}:${KAFKA_PORT:9092}',
                    'key-serializer': 'org.apache.kafka.common.serialization.StringSerializer',
                    'value-serializer': 'org.springframework.kafka.support.serializer.JsonSerializer'
                },
                'consumer': {
                    'bootstrap-servers': '${KAFKA_HOST:localhost}:${KAFKA_PORT:9092}',
                    'auto-offset-reset': 'earliest',
                    'key-deserializer': 'org.apache.kafka.common.serialization.StringDeserializer',
                    'value-deserializer': 'org.apache.kafka.common.serialization.StringDeserializer',
                    'groups-id': '${SYSTEM_INSTANCE:666}'
                },
                'properties': {
                    'spring': {
                        'json': {
                            'trusted': {
                                'packages': '*'
                            }
                        }
                    }
                },

            }
        }
        data = self.read_yaml()
        if 'spring' not in data:
            data['spring'] = {}
        data['spring'].update(kafka)
        self.save_yaml(data)

    def generate_redis_configuration(self):
        """Generate Redis Configuration"""
        redis = {
            'data': {
                'redis': {
                    'port': '${REDIS_PORT:6379}',
                    'host': '${REDIS_HOST:localhost}',
                    'database': '${REDIS_DB:0}',
                    'password': '${REDIS_PASS:root}'
                }
            }
        }
        data = self.read_yaml()
        if 'spring' not in data:
            data['spring'] = {}
        data['spring'].update(redis)
        self.save_yaml(data)

    def generate_jpa_configuration(self):
        """Generate JPA Configuration"""
        datasource = {
            'datasource': {
                'driverClassName': 'org.postgresql.Driver',
                'url': 'jdbc:postgresql://${DS_URL:localhost}:${DS_PORT:5432}/${DS_DATABASE:sansys_database}',
                'password': '${DS_PASS:postgres}',
                'username': '${DS_USER:postgres}'
            },
            'jpa': {
                'database-platform': 'org.hibernate.dialect.PostgreSQLDialect',
                'show-sql': 'true',
                'hibernate': {
                    'ddl-auto': 'none'
                },
                'generate-ddl': 'false'
            }
        }
        data = self.read_yaml()
        if 'spring' not in data:
            data['spring'] = {}
        data['spring'].update(datasource)
        self.save_yaml(data)

    def generate_mongodb_configuration(self, project):
        """Generate MongoDB Configuration"""
        mongodb = {
            'mongodb': {
                'host': '${MONGODB_HOST:localhost}',
                'database': project + "_db",
                'port': '${MONGODB_PORT:27017}'
            }
        }
        data = self.read_yaml()
        if 'spring' not in data:
            data['spring'] = {}
        spring_data = data['spring'].get('data', {})
        spring_data.update(mongodb)
        data['spring']['data'] = spring_data
        self.save_yaml(data)

    def generate_zipkin_configuration(self):
        """Generate Zipkin Configuration"""
        zipkin = {
            'zipkin': {
                'base-url': 'http://${ZIPKIN_SERVER:localhost}:${ZIPKIN_PORT:9411}'
            },
            'sleuth': {
                'sampler': {
                    'probability': 1.0
                }
            }
        }
        data = self.read_yaml()
        if 'spring' not in data:
            data['spring'] = {}
        data['spring'].update(zipkin)
        self.save_yaml(data)

    def generate_config_server_configuration(self):
        """Generate Config Server Configuration"""
        config_server = {
            'config': {
                'import': 'optional:configserver:http://${CONFIG_HOST:localhost}:${CONFIG_PORT:8888}/'
            }
        }
        data = self.read_yaml()
        if 'spring' not in data:
            data['spring'] = {}
        data['spring'].update(config_server)
        self.save_yaml(data)

    def generate_eureka_client_configuration(self):
        eureka_client = {
            'eureka': {
                'instance': {
                    'instance-id': '${spring.application.name}::${spring.application.instance_id:${random.value}}',
                    'prefer-ip-address': 'true',
                    'hostname': '${EUREKA_HOST:localhost}'
                },
                'client': {
                    'service-url': {
                        'defaultZone': 'http://${EUREKA_USER:root}:${EUREKA_PASS:root}@${EUREKA_SERVER:localhost}:${EUREKA_PORT:8761}/eureka'
                    }
                }
            }
        }
        self.add_data(eureka_client)
        data = self.read_yaml()
        self.save_yaml(data)
