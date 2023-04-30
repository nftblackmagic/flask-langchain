from langchain.document_loaders import UnstructuredWordDocumentLoader

def decoded_doc(url) :
    loader = UnstructuredWordDocumentLoader(url)
    data = loader.load()
    web_text = ""

    for page in data:
        web_text += page.page_content + " "
    print(web_text)
    return web_text

