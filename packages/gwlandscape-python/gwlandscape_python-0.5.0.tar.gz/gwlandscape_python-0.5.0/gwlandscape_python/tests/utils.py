import graphql


def compare_graphql_query(a, b):
    return graphql.language.parse(a, no_location=True) == graphql.language.parse(b, no_location=True)
