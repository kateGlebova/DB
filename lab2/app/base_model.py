class BaseModel:
    table_name = ''
    columns = {}
    primary_key = 'id'
    null = []
    ref = {}

    def __init__(self, session, id=None):
        self.session = session
        self._id = id
        self._loaded = False
        self._modified = False
        self._fields = {}

    @classmethod
    def get_all(cls, session):
        return [cls(session, row[cls.primary_key]) for row in session.get_list(cls)]

    def __getattr__(self, item):
        if item in self.columns:
            self._load()
            return self._fields[item]
        raise AttributeError

    def __setattr__(self, key, value):
        if key in self.columns:
            self._fields[key] = value
            self._modified = True

        super().__setattr__(key, value)

    def _load(self):
        if self._loaded or self._modified:
            return

        self._fields = self.session.get_one(self, self._id)
        self._loaded = True

    def _update(self):
        if not self._modified:
            return

        self._modified = False
        self.session.update(self, self._id, self._fields)

    def _insert(self):
        self._id = self.session.create(self, self._fields)[self.primary_key]
        self._modified = True

    def delete(self):
        self.session.delete(self, self._id)

    def save(self):
        if self._id:
            self._update()
        else:
            self._insert()

    @property
    def id(self):
        return self.__id
