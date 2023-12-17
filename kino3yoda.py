from flask import Flask, render_template, request, jsonify
from langchain.chains import AnalyzeDocumentChain
from langchain.chat_models import ChatOpenAI
from langchain.chains.question_answering import load_qa_chain
from gtts import gTTS
import pyttsx3


app = Flask(__name__)
app.config['DEBUG'] = True

llm = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key="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")
qa_chain = load_qa_chain(llm, chain_type="map_reduce")
qa_document_chain = AnalyzeDocumentChain(combine_docs_chain=qa_chain)





@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/query', methods=['POST'])
def query():
    document = request.files['document'].read().decode('utf-8')
    # question = request.form['question']
    question = f"{request.form['question']} contesta al estilo de Yoda."#.....simple simple simple


    # Llamada a Langchain
    
    response = qa_document_chain.run(input_document=document, question=question)
    
    rate = 150
    lang = 'es'
    engine = pyttsx3.init()
    engine.setProperty('rate',rate)
    engine.setProperty('voice', f'com.apple.speech.synthesis.voice.{lang}' if lang == 'es' else lang)
    engine.say(response)
    engine.runAndWait()

    

    return jsonify({'answer': response})



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)