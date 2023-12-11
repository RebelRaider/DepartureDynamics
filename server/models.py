from tortoise import Tortoise, fields
from tortoise.models import Model

class UserModel(Model):
    id = fields.IntField(pk=True, generated=True)
    title = fields.CharField(max_length=255, unique=True)

class History(Model):
    id = fields.IntField(pk=True, generated=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    
    model_name = fields.CharField(max_length=255)
    output_file_name = fields.CharField(max_length=255)
    user_upload = fields.CharField(max_length=255)
    
    async def json(self):
        return {
            'id': self.id,
            'created_at': self.created_at,
            'model_name': self.model_name,
            'output_file_name': self.output_file_name,
            'user_upload': self.user_upload
        }

class User(Model):
    id = fields.IntField(pk=True, generated=True)
    username = fields.CharField(max_length=255, unique=True)
    first_name = fields.CharField(max_length=255)
    last_name = fields.CharField(max_length=255)
    email = fields.CharField(max_length=255, unique=True)
    password = fields.CharField(max_length=255)
    created_at = fields.DatetimeField(auto_now_add=True)

    models = fields.ManyToManyField('models.UserModel')
    history = fields.ManyToManyField('models.History')
    