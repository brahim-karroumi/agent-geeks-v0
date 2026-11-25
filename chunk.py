from data import GUIDE

# 1. Chunking
chunks = [p.strip() for p in GUIDE.split("\n\n")]
print(len(chunks), "chunks\n")

# 2. Keyword search
STOPWORDS = {"how", "much", "is", "the", "where", "can", "i", "a", "and", "to", "in"}

def clean(text):
    return {w.strip("?.,:!").lower() for w in text.split()}

def keyword_search(question):
    words = clean(question) - STOPWORDS
    return [c for c in chunks if words & clean(c)]

# Test 1
q1 = "How much is Majorelle?"
print(q1, "->", keyword_search(q1))

# Test 2
q2 = "Where can I see something blue and peaceful Chefchaouen?"
print(q2, "->", keyword_search(q2) or "NOTHING FOUND ❌")