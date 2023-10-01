import graphene

import ingredientes.schema


class Query(ingredientes.schema.Query, graphene.ObjectType):
    # Esta clase heredará de varias consultas a medida que comencemos 
    # a agregar más aplicaciones a nuestro proyecto.
    pass

schema = graphene.Schema(query=Query)