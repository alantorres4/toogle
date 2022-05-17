from ply import lex
import re
import string
import hashlib
import os
import shutil
import math

# NODE CLASS ============================================================================================================================
class Node:
    def __init__(self, docid, wt):
        self.docid = docid # initialize docid
        self.wt = wt # initialize wt
        self.next = None # next node should be Null at first

# LINKED LIST CLASS =====================================================================================================================
class L:
    def __init__(self):
        self.head = None
        self.tail = None
        self.total_nodes = 0

    def insert(self, docid, wt): # Inserts new node to END of list
        new_node = Node(docid, wt)
        self.total_nodes += 1
        if self.head == None:
            new_node.next = None
            self.head = new_node
            self.tail = new_node
            self.tail.next = None
        elif new_node.wt >= self.head.wt: # new node is the new head
            new_node.next = self.head
            self.head = new_node
        else:
            current_node = self.head
            while current_node.next != None and current_node.next.wt > new_node.wt:
                current_node = current_node.next

            if current_node.next == None:
                self.tail = current_node
                new_node.next = None
                self.tail.next = new_node
                self.tail = new_node
                self.tail.next = None
            else:
                new_node.next = current_node.next
                current_node.next = new_node

    def remove_tail(self): # Removes the tail node to keep it bounded to top 10
        previous_node = self.head
        current_node = previous_node.next
        while current_node.next != None:
            previous_node = previous_node.next
            current_node = current_node.next
        self.tail = previous_node
        self.tail.next = None

    def print_list(self, docid_to_token): # Prints top ten list
        current_directory = os.getcwd()
        map_file = current_directory + "/output/map.txt"
        MAP_RECORD_SIZE = 14

        with open(map_file, 'r') as f:
            current_node = self.head
            table = ""
            if current_node:
                headers = "<thead><tr><th>Document Name:</th><th>Term(s):</th><th>Weights(x100):</th></tr></thead><tbody>"
                table += headers
                for i in range(10):
                    if current_node:
                        f.seek(0,0)
                        f.seek(MAP_RECORD_SIZE * current_node.docid)
                        document_name = f.readline()
                        #TODO HW5: using the docid, find the tokens that match to it from docid_to_token[] (ex: docid_to_token = [[docid, token1],[docid, token2]]
                        # loop through docid_to_token[] and if docid_to_token[i][0] == docid: add 'docid_to_token[i][1] to list of tokens
                        list_of_tokens_from_docid = []
                        for i in range(len(docid_to_token)):
                            if docid_to_token[i][0] == current_node.docid:
                                list_of_tokens_from_docid.append(docid_to_token[i][1])

                        string_of_tokens_from_docid = ""
                        for token in list_of_tokens_from_docid:
                            string_of_tokens_from_docid += token + " "

                        table += f"<tr><td><a href='300Files/{document_name.strip()}' target='_blank'>{document_name.strip()}</a></td><td>{string_of_tokens_from_docid}</td><td>{current_node.wt*100}</td></tr>"
                        current_node = current_node.next
                    else:
                        table += "<tr><td> - </td><td> - </td><td> - </td></tr>"
        print(f"<table> {table} </tbody></table><br><br><br><br>")


# HTMLLEXER CLASS ===========================================================================================================================
class HTMLLexer(object):
    tokens = (
        'TAG',
        'TEXT_TAG',
        'FLOAT',
        'TIME',
        'COMMA_NUMBER',
        'HYPENATED',
        'ABBREVIATED',
        'WORD',
        'WHITESPACE',
        'PUNCTUATION',
        'GRAVE'
    )

    def t_TAG(self, t):
        r'\s*<[^>]*>\s*'
        pass

    def t_TEXT_TAG(self, t):
        r'(\w+<[^>]*>\w+)+'
        t.value = re.sub("<[^>]*>", "", t.value)
        t.value = str(t.value).lower()
        return t

    def t_HYPENATED(self, t):
        r"(\w+-\w+)(-\w+)*"
        t.value = re.sub("-*", "", t.value)
        t.value = str(t.value).lower()
        return t

    def t_FLOAT(self, t):
        r"[-+]?\d*\.\d+"
        t.value = str(abs(int(float(t.value))))
        return t

    def t_COMMA_NUMBER(self, t):
        r"(\d*,\d+)+"
        t.value = re.sub(",", "", t.value)
        return t

    def t_TIME(self, t):
        r"\w+:\w+"
        t.value = re.sub(":", "", t.value)
        return t

    def t_ABBREVIATED(self, t):
        r"(\w+\.\w+)(\.\w+)*"
        t.value = re.sub("\.", "", t.value)
        t.value = str(t.value).lower()
        return t

    def t_WORD(self, t):
        r'\w+'
        t.value = str(t.value).lower()
        return t

    def t_PUNCTUATION(self, t):
        r'[!"#$%&\'\(\)\*\+,-./:;<=>?@\[\]^_`{|}~\\/]'
        pass

    def t_GRAVE(self, t):
        r'(?i)^(?:(?![×Þß÷þø])[-\'0-9a-zÀ-ÿ])+$'
        t.lexer.skip(1)

    def t_WHITESPACE(self, t):
        r'\s+'
        pass

    def t_error(self,t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    def build(self,**kwargs):
        self.lexer = lex.lex(module=self, **kwargs)
        self.frequency = {}
# --------------------------------------------------------------------------------------------------
    def hashfunction(self,key, ht_size):
        h = hashlib.sha1()
        h.update(bytes(key, encoding="ascii")) # encoding="utf-8"
        return int(h.hexdigest(), 16)%ht_size

    ht_size = 150000 # 150000 for big collection, 20 for small
    number_of_documents_in_collection = 300 # 300 for big collection, 5 for small
    Acc = [0.0]*number_of_documents_in_collection # Initialize Accumulator[]
    docid_to_token = [] #TODO HW5: used to keep track of what tokens match to what document id

    def sortAccumulator(self, docid_to_token):
        top_ten = L()

        for i in range(len(self.Acc)):
            if self.Acc[i] != 0.0:
                if top_ten.total_nodes < 10:
                    top_ten.insert(i, self.Acc[i]) # Insert and sort the (docid, wt)
                else:
                    if self.Acc[i] > top_ten.tail.wt:
                        top_ten.insert(i, self.Acc[i])
                        top_ten.remove_tail()
        top_ten.print_list(docid_to_token)

    def add_to_accumulator(self, token):
        if token == "_empty" or token == "_deleted":
            print(f"<p style='width:100%;text-align:center;'>[-] {token} is not an acceptable query. Try something else!</p>")
            return

        current_directory = os.getcwd()
        dict_file = current_directory + "/output/dict.txt"
        post_file = current_directory + "/output/post.txt"

        DICT_RECORD_SIZE = 35 # changed from 31 for the edited HW3 code
        POST_RECORD_SIZE = 26

        # 1) Calculate bucket = hf(token)
        bucket = self.hashfunction(token, self.ht_size)

        # 2) Seek to dict[bucket]
        with open(dict_file, 'r') as f:
            f.seek(0,0)
            f.seek(DICT_RECORD_SIZE * bucket)
            record = f.readline()
            token_from_record = record.split()[0].strip()
            while token_from_record != token:
                bucket += 1
                f.seek(0,0)
                f.seek(DICT_RECORD_SIZE * bucket)
                record = f.readline() #    token, num_docs, start
                token_from_record = record.split()[0].strip() # get token from record
                if token_from_record == "_empty":
                    print(f"<p style='width:100%;text-align:center;'>[-] No documents found for '{token}'</p>")
                    return

            # 3) Read token, num_docs, start
            num_docs = record.split()[1].strip() # get num_docs from record
            start = record.split()[2].strip() # get start from record


        # 4) Seek to post[bucket]
        with open(post_file, 'r') as f:
            # 5) Loop num_docs times:
            f.seek(0,0)
            f.seek(POST_RECORD_SIZE * (int)(start))
            for i in range((int)(num_docs)):
                # 6) Read posting(s)
                record = f.readline()
                doc_id = (int)(record.split()[0].strip()) # get doc_id from record
                wt = (float)(record.split()[1].strip()) # get wt from record
                # 7) Add 'wt' to Acc[docid]
                self.Acc[doc_id] += wt
                #TODO HW5: Add [docid, token] to docid_to_token[]
                self.docid_to_token.append([doc_id, token])

    def tokenizeFile(self, inputFile):
        tokens = []
        #read the file and tokenize
        with open(inputFile,'rb') as f:
            for line in f:
                line = line.decode(errors='ignore')
                self.lexer.input(line)
                while True:
                    tok = self.lexer.token()
                    if not tok:
                        break

                    tokens.append(tok.value)
                    self.add_to_accumulator(tok.value)

        self.sortAccumulator(self.docid_to_token)
