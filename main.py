from api import create_phb_embeddings
from api import retrieve_answer_phb

# create_phb_embeddings()

a = retrieve_answer_phb("What are the wizard subclasses?")
print(a)