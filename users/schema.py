from django.contrib.auth import get_user_model

import graphene
from django.db import models
from graphene_django import DjangoObjectType
from graphene_django.converter import convert_django_field


@convert_django_field.register(models.BigIntegerField)
def convert_big_int_to_float(field, registry=None):
    return graphene.Float(required=True)


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()


class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        cpf = graphene.Float(convert_big_int_to_float(graphene.Int()))
        password = graphene.String(required=True)
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)

    def mutate(self, info, cpf, password, first_name, last_name):
        user = get_user_model()(
            cpf=cpf,
            first_name=first_name,
            last_name=last_name,
        )
        user.set_password(password)
        user.save()

        return CreateUser(user=user)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()


class Query(graphene.ObjectType):
    me = graphene.Field(UserType)
    users = graphene.List(UserType)

    def resolve_users(self, info):
        return get_user_model().objects.all()

    def resolve_me(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged!')
        return user
