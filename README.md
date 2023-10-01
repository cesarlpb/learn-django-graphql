# Tutorial

[Queries & Object Types](https://docs.graphene-python.org/projects/django/en/latest/queries/)

@TODO: copiar queries aquí.

Query con paginación:

```graphql
{
    questions (first: 3, after: "YXJyYXljb25uZWN0aW9uOjEwNQ==") {
        pageInfo {
        startCursor
        endCursor
        hasNextPage
        hasPreviousPage
        }
        edges {
        cursor
        node {
            id
            texto
        }
        }
    }
}
```