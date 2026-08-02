from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

vec = model.encode("A cat is sleeping on the couch")
print(vec.shape)
print(vec[:5])

from numpy import dot
from numpy.linalg import norm

v1 = model.encode("A cat is sleeping on the couch")
v2 = model.encode("A kitten is nappping on the sofa")

similarity = dot(v1, v2) / (norm(v1) * norm(v2))
print(f"Similarity: {similarity:.4f}")