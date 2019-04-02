from pynamodb.models import Model


class BaseModel(Model):
    def set_attributes(self, **attrs):
        self.update(actions=[getattr(self.__class__, k).set(v) for k, v in attrs.items()])

    @classmethod
    def get_one(cls, _id):
        rslt = list(cls.query(_id))
        if len(rslt) > 0:
            return rslt[0]
        raise ValueError(f'{cls.__name__} :: {_id} was not found.')
