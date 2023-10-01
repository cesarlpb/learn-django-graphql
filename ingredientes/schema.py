import datetime
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
        # Personaliza los campos que deseas incluir o excluir aquí:
        """Determina los campos exactos que se incluirán en el tipo de objeto:"""
        # fields = ("texto", "creado_por") # Todos: __all__
        # fields = "__all__"
        """Campos exactos que se excluirán del tipo de objeto:"""
        exclude = ("top_secret",)
        # Campo extra que no está en el modelo Pregunta:
        """Nota: No se puede usar fields y exclude al mismo tiempo."""
        # Conversiones de choices a enum:
        convert_choices_to_enum = False # Necesario si en el modelo se usa string como default
    hora_actual = graphene.String()

    def resolve_hora_actual(self, info):
        now = datetime.datetime.now()
        return now.strftime("%Y-%m-%d %H:%M:%S")

# Mutación para crear una pregunta:
class CrearPreguntaMutation(graphene.Mutation):
    class Arguments:
        # Inputs para la mutación:
        texto = graphene.String(required=True)
        categoria = graphene.ID(required=True)

    # Atributos de clase que definen la respuesta de la mutación:
    question = graphene.Field(PreguntaType)

    @classmethod
    def mutate(cls, root, info, texto, categoria):
        # Crea una nueva pregunta con el texto proporcionado
        question = Pregunta(texto=texto, categoria=Categoria.objects.get(pk=categoria))
        question.save()
        
        # Retorna una instancia de la mutación:
        return CrearPreguntaMutation(question=question)

# Mutación para actualizar una pregunta:
class EditarPreguntaMutation(graphene.Mutation):
    class Arguments:
        # Inputs para la mutación:
        texto = graphene.String(required=True)
        id = graphene.ID()

    # Atributos de clase que definen la respuesta de la mutación:
    question = graphene.Field(PreguntaType)

    @classmethod
    def mutate(cls, root, info, texto, id):
        question = Pregunta.objects.get(pk=id)
        question.texto = texto
        question.save()
        # Retorna una instancia de la mutación:
        return EditarPreguntaMutation(question=question)

# Mutación para eliminar una pregunta:
class BorrarPreguntaMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)  # Se requiere el ID de la pregunta a borrar

    success = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, id):
        try:
            # Intenta borrar la pregunta con el ID proporcionado
            pregunta = Pregunta.objects.get(pk=id)
            pregunta.delete()
            success = True
        except Pregunta.DoesNotExist:
            success = False
        
        return BorrarPreguntaMutation(success=success)

class Mutation(graphene.ObjectType):
    create_question = CrearPreguntaMutation.Field()
    update_question = EditarPreguntaMutation.Field()
    delete_question = BorrarPreguntaMutation.Field()

# Paginación:
class PreguntaConnection(relay.Connection):
    class Meta:
        node = PreguntaType

class Query(ObjectType):
    category = relay.Node.Field(CategoriaNode)
    all_categorias = DjangoFilterConnectionField(CategoriaNode)
    
    # questions = graphene.List(PreguntaType) # Devuelve todas las preguntas en una lista
    questions = relay.ConnectionField(PreguntaConnection) # Devuelve todas las preguntas en una con paginación
    question_by_id = graphene.Field(PreguntaType, id=graphene.String())

    ingrediente = relay.Node.Field(IngredienteNode)
    all_ingredientes = DjangoFilterConnectionField(IngredienteNode)

    # Filters
    search_question = graphene.List(
        PreguntaType,
        keyword=graphene.String(required=True)
    )

    def resolve_search_question(self, info, keyword):
        # Utiliza el argumento "keyword" para buscar preguntas que contengan la palabra
        return Pregunta.objects.filter(texto__icontains=keyword) # __icontains: case-insensitive
    
    def resolve_questions(root, info, **kwargs):
        # Devuelve todas las preguntas en una lista
        return Pregunta.objects.all()

    def resolve_question_by_id(root, info, id):
        # Devuelve una sola pregunta por su ID
        return Pregunta.objects.get(pk=id)

