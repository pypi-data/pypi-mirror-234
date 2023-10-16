class ParamConfiguration:
    def __init__(self, base_dir, spring_version, project, package, banner_text, jpa=False, mongo=False, samples=True,
                 redis=False, kafka=False, eureka_client=False,
                 config_server=False, zipkin=False, rabbitmq=False):
        self.base_dir = base_dir
        self.project = project
        self.package = package
        self.jpa = jpa
        self.mongo = mongo
        self.samples = samples
        self.redis = redis
        self.kafka = kafka
        self.config_server = config_server
        self.zipkin = zipkin
        self.spring_version = spring_version
        self.eureka_client = eureka_client
        self.rabbitmq = rabbitmq
        self.banner_text = banner_text
