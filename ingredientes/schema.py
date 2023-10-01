import graphene
from graphene import relay, ObjectType
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from ingredientes.models import Categoria, Ingrediente, Pregunta

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

class PreguntaType(DjangoObjectType):
    class Meta:
        model = Pregunta
        fields = ("id", "texto")

class Query(ObjectType):
    category = relay.Node.Field(CategoriaNode)
    all_categorias = DjangoFilterConnectionField(CategoriaNode)
    
    questions = graphene.List(PreguntaType)
    question_by_id = graphene.Field(PreguntaType, id=graphene.String())

    ingrediente = relay.Node.Field(IngredienteNode)
    all_ingredientes = DjangoFilterConnectionField(IngredienteNode)

    def resolve_questions(root, info, **kwargs):
        # Devuelve todas las preguntas en una lista
        return Pregunta.objects.all()

    def resolve_question_by_id(root, info, id):
        # Devuelve una sola pregunta por su ID
        return Pregunta.objects.get(pk=id)

