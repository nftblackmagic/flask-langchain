from langchain.document_loaders import SeleniumURLLoader

def decode_website(url):
    print("url",url)
    loader = SeleniumURLLoader([url])
    data = loader.load()
    web_text = ""

    for page in data:
        web_text += page.page_content + " "
    
    return web_text


