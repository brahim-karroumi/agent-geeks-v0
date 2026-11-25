from embedding import build_local_db, get_collection

collection = get_collection()

if collection.count() == 0:
    print("Building Chroma collection...", flush=True)
    print(build_local_db(), flush=True)
else:
    print(
        f"Chroma already contains {collection.count()} records.",
        flush=True,
    )