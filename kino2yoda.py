from flask import Flask, render_template, request, jsonify
from langchain.chains import AnalyzeDocumentChain
from langchain.chat_models import ChatOpenAI
from langchain.chains.question_answering import load_qa_chain

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
    question = request.form['question']
    context='contesta como si fueras Yoda'

    # Llamada a Langchain
    
    response = qa_document_chain.run(input_document=document, question=question, 
                                     context = context)
    
    # transforma a yoda style
    # words = response.split().........ultimo cambio
    # yoda_answer = " ".join(words[::-1]).............ultimo cambio
    # Transformar la respuesta al estilo de Yoda
    #yoda_response = yoda_style(response['answer'])
    return jsonify({'answer': response})
    # Devolver la respuesta transformada como JSON
    # return jsonify({'answer': yoda_response})

    # Almacenar en la base de datos (a implementar)

    # return jsonify({'answer': response['answer']})

# def yoda_style(answer):
#     # Función simple para transformar la respuesta al estilo de Yoda
#     words = answer.split()
#     yoda_answer = " ".join(words[::-1])  # Invertir el orden de las palabras
#     return yoda_answer

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)