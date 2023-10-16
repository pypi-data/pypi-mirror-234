class YamlManipulator:
    def read_yaml(self):
        """Load content file"""
        try:
            with open(self.path, 'r') as file:
                data = self.yaml.load(file)
                if data is None:
                    data = {}
        except FileNotFoundError:
            data = {}
        return data

    def save_yaml(self, data):
        """Save file updated"""
        with open(self.path, 'w') as file:
            self.yaml.dump(data, file)

    def create_empty_yaml(self):
        """Create an empty file"""
        open(self.path, 'w').close()

    def add_data(self, new_data):
        """Add new data content"""
        data = self.read_yaml()

        if data is None:
            data = {}

        data.update(new_data)
        self.save_yaml(data)

    def remove_data(self, keys):
        """Remove data with base key"""
        data = self.read_yaml()
        for key in keys:
            data.pop(key, None)
        self.save_yaml(data)