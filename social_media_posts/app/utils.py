from passlib.context import CryptContext
from sentence_transformers import SentenceTransformer

pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

# model = SentenceTransformer(
#     "all-MiniLM-L6-v2"
# )

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# def generate_embedding(text: str):

#     embedding = model.encode(text)

#     return embedding.tolist()