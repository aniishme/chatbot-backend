
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceInstructEmbeddings  
from langchain_community.vectorstores import FAISS
import pickle


file = "datasets/train.pdf"


pdf_reader = PdfReader(file)
text = ""

for page in pdf_reader.pages:
    text += page.extract_text()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    length_function=len
)
chunks = text_splitter.split_text(text=text)

store_name = "disastermodel"

embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-large")
VectorStore = FAISS.from_texts(chunks, embedding=embeddings)
with open(f"{store_name}.pkl", "wb") as f:
    pickle.dump(VectorStore, f)

print({"filename": file, "store_name": store_name})