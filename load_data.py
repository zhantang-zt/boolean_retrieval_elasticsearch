import json
import os

def load_nf_corpus(nf_path):
	with open(nf_path, "r", encoding="utf-8") as f:
		for index, line in enumerate(f):
			doc_dict = json.loads(line)
			title = doc_dict["title"]
			content = doc_dict["text"]
			doc_dict["full_content"] = title + " " + content
			yield doc_dict