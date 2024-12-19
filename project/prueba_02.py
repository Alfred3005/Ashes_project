from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch



tokenizer = AutoTokenizer.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')

model = AutoModelForSequenceClassification.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')

tokens = tokenizer.encode('te amo como no tienes idea', return_tensors='pt')

result = model(tokens)

result.logits

score= int(torch.argmax(result.logits))+1

