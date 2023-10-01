import graphene

import ingredientes.schema

# import ingredientes.schema.Query
# import ingredientes.schema.Mutation


class Query(ingredientes.schema.Query, graphene.ObjectType):
    # Esta clase heredará de varias consultas a medida que comencemos 
    # a agregar más aplicaciones a nuestro proyecto.
    pass

# class Mutation(
#     ingredientes.schema.Mutation, 
#     graphene.ObjectType
# ):
#     pass

schema = graphene.Schema(query=Query)