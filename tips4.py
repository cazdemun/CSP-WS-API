    # return find_one(tryCatchTag(f'Error: collection {collection} not found!', lambda: db[collection].find_one({"name": name})) \
    #     .bind(lambda doc: fromNullableTag(f'Error: document {name} in {collection} not found!', doc)) \
    #     .fmap(lambda doc: doc['_id'])