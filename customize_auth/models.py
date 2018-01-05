from django.db import models
from django.contrib.auth.hashers import (
    check_password, make_password,
)

SEX = ((1, '男'), (-1, '女'), (0, '隐藏'))


class BaseModel(models.Model):
    name = models.CharField(max_length=255, unique=True, default='')
    description = models.TextField(blank=True, null=True)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(BaseModel):
    email = models.CharField(max_length=255, default='@example.com', verbose_name='邮箱')
    password_hash = models.CharField(max_length=255, default='123456')
    birthday = models.DateTimeField(null=True, blank=True, verbose_name='生日')
    sex = models.IntegerField(default=0, choices=SEX, verbose_name='性别')
    avatar_path = models.CharField(max_length=255, null=True, blank=True, verbose_name='头像')
    phone_number = models.CharField(max_length=11, null=True, blank=True, verbose_name='手机号')
    disabled = models.BooleanField(default=False)
    last_login = models.DateTimeField(auto_now_add=True)
    fans = models.ManyToManyField("self", related_name='star', symmetrical=False)  # 粉丝关注关系
    apprentice = models.ManyToManyField("self", related_name='master', symmetrical=False)  # 师徒关系
    blacklist = models.ManyToManyField('self', related_name='+', symmetrical=False)  # 单向黑名单
    groups = models.ManyToManyField('UserGroup', related_name='users')

    @property
    def is_authenticated(self):
        return True

    @property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, password):
        self.password_hash = make_password(password)

    def verify_password(self, passowrd):
        def setter(raw_password):
            self.password = raw_password
            self.save(update_fields=["password_hash"])
        return check_password(passowrd, self.password, setter)


class UserGroup(BaseModel):
    """用户组，用于规划用户权限"""
    permissions_groups = models.ManyToManyField('PermissionsGroup', related_name='user_groups')


class Level(BaseModel):
    """用户等级"""
    integral = models.IntegerField(default=0)
    user = models.OneToOneField('User', related_name='level', on_delete=models.CASCADE)


class Achievement(BaseModel):
    """用户成就，需要一份参考数据：指标和对应的阈值，以及达成的成就名称"""
    target = models.CharField(max_length=255, default='博文数量', choices=[])
    threshold = models.IntegerField(default=0)
    user = models.ForeignKey('User', related_name='achievements', on_delete=models.CASCADE)


class Permissions(BaseModel):
    """细化的权限树"""
    enabled = models.BooleanField(default=True)
    children = models.ManyToManyField("self", related_name='parents', symmetrical=False)  # 设计成树型

    @property
    def parent(self):
        return self.parents.first()


class PermissionsGroup(BaseModel):
    """权限组，包含若干权限树或子树，对接用户组"""
    permissions = models.ManyToManyField('Permissions', related_name='groups')


class AuthLog(BaseModel):
    """Auth模块的日志"""
    user_name = models.CharField(max_length=255, default='')
    target = models.CharField(max_length=255, default='')
    model = models.CharField(max_length=255, default='')
    index = models.IntegerField(default=1)
    operate_content = models.TextField(default='')
