import graphene
from graphene_django import DjangoObjectType

from ingredientes.models import Categoria, Ingrediente

class CategoryType(DjangoObjectType):
    class Meta:
        model = Categoria
        fields = ("id", "name", "description", "tags")

class IngredientType(DjangoObjectType):
    class Meta:
        model = Ingrediente
        fields = ("id", "name", "notas", "categoria")

class Query(graphene.ObjectType):
    all_ingredients = graphene.List(IngredientType)
    category_by_name = graphene.Field(CategoryType, name=graphene.String(required=True))
    hello_world = graphene.String()

    def resolve_hello_world(root, info):
        return "Hello World!"

    def resolve_all_ingredients(root, info):
        # We can easily optimize query count in the resolve method
        return Ingrediente.objects.select_related("categoria").all()

    def resolve_category_by_name(root, info, name):
        try:
            return Categoria.objects.get(name=name)
        except Categoria.DoesNotExist:
            return None

schema = graphene.Schema(query=Query)

