from elasticsearch_dsl import Q, Search
from elasticsearch_dsl.connections import connections
from elasticsearch_dsl.query import Match


# the input looks like: +i +like -eating ?cake
def parse_query(query):
	must_list = []
	should_list = []
	not_list = []
	for token in query.split():
		signal = token[0]
		word = token[1:]
		if signal == "+":
			must_list.append(word)
		elif signal == "-":
			not_list.append(word)
		elif signal == "?":
			should_list.append(word)
	return must_list, should_list, not_list


def generate_Q(must_list, should_list, not_list):
	must_Q = []
	should_Q = []
	not_Q = []
	for must in must_list:
		must_Q.append(Q("match", full_content=must))
	for should in should_list:
		should_Q.append(Q("match", full_content=should))
	for n in not_list:
		not_Q.append(Q("match", full_content=n))
	return must_Q, should_Q, not_Q



def search(index_name, search_query):
	must_list, should_list, not_list = parse_query(search_query)
	must_Q, should_Q, not_Q = generate_Q(must_list, should_list, not_list)
	search_query = Q('bool', must=must_Q, should=should_Q, must_not=not_Q)
	s = Search(using="default", index=index_name).query(search_query)
	response = s.execute()
	return response



def main():
	connections.create_connection(hosts=["localhost"], timeout=100, alias="default")
	index_name = "es_corpus"
	# this is an example query
	query = "+especially +first ?effects -combination"
	response = search(index_name, query)
	# for hit in response:
	# 	print(hit.title)
	# 	print(hit.content)
	# 	print("----------------")

if __name__ == "__main__":
    main()