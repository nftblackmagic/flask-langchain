from flask import Flask, render_template, jsonify, request
from urllib.parse import unquote
from langchain import OpenAI, PromptTemplate, LLMChain
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains.mapreduce import MapReduceChain
from langchain.prompts import PromptTemplate
from langchain.docstore.document import Document
from langchain.chains.summarize import load_summarize_chain
from decouple import config

from web import decode_website

import textwrap
import os
import nltk
nltk.data.path.append('nltk_data')

os.environ["OPENAI_API_KEY"] = config('OPENAI_API_KEY')
app = Flask(__name__)

    
def summarize_webpage(text):
    llm = OpenAI(temperature=0)
    text_splitter = CharacterTextSplitter()
    texts = text_splitter.split_text(text)
    print(len(texts))
    docs = [Document(page_content=t) for t in texts[:4]]
    # chain = load_summarize_chain(llm, 
    #                          chain_type="map_reduce")


    # output_summary = chain.run(docs)
    # wrapped_text = textwrap.fill(output_summary, width=100)
    # print(wrapped_text)
    chain = load_summarize_chain(llm, chain_type="stuff")
    prompt_template = """Write a concise bullet point summary of the following:


    {text}


    CONSCISE SUMMARY IN BULLET POINTS:"""

    BULLET_POINT_PROMPT = PromptTemplate(template=prompt_template, 
                            input_variables=["text"])
    
    chain = load_summarize_chain(llm, 
                             chain_type="stuff", 
                             prompt=BULLET_POINT_PROMPT)

    output_summary = chain.run(docs)

    wrapped_text = textwrap.fill(output_summary, 
                                width=100,
                                break_long_words=False,
                                replace_whitespace=False)
    print(wrapped_text)

    return wrapped_text


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/data', methods=['GET','POST'])
def get_data():
    if request.method == 'GET':
        sample_data = {
            'message': 'Hello, Flask API!',
            'data': [1, 2, 3, 4, 5]
        }
        print ("DEBUG",sample_data)
        return jsonify(sample_data)
    elif request.method == 'POST':
        print ("DEBUG request",request)
        encode_url = unquote(unquote(request.args.get('url')))
        print ("DEBUG encode_url",encode_url)
        if not encode_url:
            return jsonify({'error': 'URL is required'}), 400

        decoded_text = decode_website(encode_url)

        print ("DEBUG decoded_text",decoded_text)

        summary = summarize_webpage(decoded_text)

        response = {
            'submitted_url': encode_url,
            'summary': summary,
        }

        return jsonify(response)
        

@app.route('/api/submit', methods=['POST'])
def submit():
    data = request.json
    print("DEBUG",data)
    url = data.get('url', '')

    if not url:
        return jsonify({'error': 'URL is required'}), 400

    response = {
        'submitted_url': url
    }
    return jsonify(response)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5001))
    app.run(debug=True, host='0.0.0.0', port=port)


