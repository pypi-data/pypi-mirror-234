import os


class DocumentationContainer:
    def __init__(self, docs_dir):
        self.docs = self._discover_docs(docs_dir)

    def _discover_docs(self, docs_dir):
        docs = {}
        for file_name in os.listdir(docs_dir):
            if file_name.endswith('md'):
                docs[file_name.split('.')[0]] = os.path.join(docs_dir, file_name)
        return docs

    def get(self, topic):
        doc_file = self.docs.get(topic.lower())
        if doc_file is None:
            raise FileNotFoundError("No topic available named {}".format(topic))
        with open(doc_file) as doc_file_ptr:
            return doc_file_ptr.read()

    def list(self):
        return sorted(self.docs.keys())
