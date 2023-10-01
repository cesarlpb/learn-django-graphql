import graphene
from graphene import relay, ObjectType
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from ingredientes.models import Categoria, Ingrediente

# Graphene mapeará automáticamente los campos del modelo Category en el CategoryNode. 
# Esto se configura en la clase Meta del CategoryNode (como puedes ver a continuación).
class CategoriaNode(DjangoObjectType):
    class Meta:
        model = Categoria
        filter_fields = ['name', 'description']
        interfaces = (relay.Node, )

class IngredienteNode(DjangoObjectType):
    class Meta:
        model = Ingrediente
        # Filtros más avanzados:
        filter_fields = {
            'name': ['exact', 'icontains', 'istartswith'],
            'notas': ['exact', 'icontains'],
            'categoria': ['exact'],
            'categoria__name': ['exact'],
        }
        interfaces = (relay.Node, )

class Query(ObjectType):
    category = relay.Node.Field(CategoriaNode)
    all_categorias = DjangoFilterConnectionField(CategoriaNode)

    ingrediente = relay.Node.Field(IngredienteNode)
    all_ingredientes = DjangoFilterConnectionField(IngredienteNode)

