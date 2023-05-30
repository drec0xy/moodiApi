api_key = "086a300e-a2b0-4ed3-9546-f1c949914689"
environment = "us-west4-gcp-free"

import pinecone

#connect to pinecone env
pinecone.init(api_key="086a300e-a2b0-4ed3-9546-f1c949914689", environment="us-west4-gcp-free")

index_name = "moodi-chatbot"
if index_name not in pinecone.list_indexes():
  pinecone.create_index(
      index_name,
      dimension=768,
      metric = "cosine"
  )

index = pinecone.Index(index_name)

import torch

from sentence_transformers import SentenceTransformer

device = 'cuda' if torch.cuda.is_available() else 'cpu'
retriver = SentenceTransformer("flax-sentence-embeddings/all_datasets_v3_mpnet-base", device = device)
#retriver

from transformers import BartTokenizer, BartForConditionalGeneration

# load bart tokenizer and model from huggingface
tokenizer = BartTokenizer.from_pretrained('vblagoje/bart_lfqa')
generator = BartForConditionalGeneration.from_pretrained('vblagoje/bart_lfqa').to("gpu")

def query_pinecone(query, top_k):
    # generate embeddings for the query
    xq = retriver.encode([query]).tolist()
    # search pinecone index for context passage with the answer
    xc = index.query(xq, top_k=top_k, include_metadata=True)
    return xc

#query = "what is the process to pay fees using mobile money"
#result = query_pinecone(query, top_k=2)
#result

from pprint import pprint

def format_query(query, context):
    # extract passage_text from Pinecone search result and add the <P> tag
    context = [f"<P> {m['metadata']['passage_text']}" for m in context]
    # concatinate all context passages
    context = " ".join(context)
    # contcatinate the query and context passages
    query = f"question: {query} context: {context}"
    return query

#query = format_query(query, result["matches"])
#pprint(query)


def generate_answer(query):
    result = query_pinecone(query, top_k=20)
    query = format_query(query, result["matches"])
    # tokenize the query to get input_ids
    inputs = tokenizer([query], max_length=1024, return_tensors="pt")
    # move the input tensor to the same device as the generator
    inputs = {k: v.to(generator.device) for k, v in inputs.items()}
    # use generator to predict output ids
    ids = generator.generate(inputs["input_ids"], num_beams=10, temperature=0.7, min_length=30, max_length=100)
    # use tokenizer to decode the output ids
    answer = tokenizer.batch_decode(ids, skip_special_tokens=True, clean_up_tokenization_spaces=True)[0]
    return answer


#pprint(query)
#generate_answer(query)