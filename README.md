# Tutorial

[Queries & Object Types](https://docs.graphene-python.org/projects/django/en/latest/queries/)

@TODO: copiar queries aquí.

Crear pregunta:

```graphql
mutation {
  createQuestion(texto: "Texto de la nueva pregunta", categoria: "1") {
    question {
      id
      texto
      creadoPor
      categoria {
        name
      }
    }
  }
}
```

Editar pregunta:

```graphql
mutation {
  updateQuestion(id: 1, texto: "Texto editado 1") {
    question {
      id
      texto
    }
  }
}
```

Borrar pregunta:

```graphql
mutation {
  deleteQuestion(id: 1) {
    success
  }
}
```