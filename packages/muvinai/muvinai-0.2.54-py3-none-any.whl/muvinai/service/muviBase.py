class MuviBase:
    def __init__(self, data=None):
        self.data = data if data else {}
        self._to_update = {}

    def update(self, **kwargs):
        for k, v in kwargs.items():
            if hasattr(self, k):
                setattr(self, k, v)

            if k == 'id':
                self.data['_id'] = v
                continue

            self.data[k] = v
            self._to_update[k] = v
