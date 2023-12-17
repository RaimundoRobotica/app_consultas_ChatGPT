from flask import Flask, render_template, request, jsonify
from langchain.chains import AnalyzeDocumentChain
from langchain.chat_models import ChatOpenAI
from langchain.chains.question_answering import load_qa_chain
from gtts import gTTS


app = Flask(__name__)
app.config['DEBUG'] = True

llm = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key="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")
qa_chain = load_qa_chain(llm, chain_type="map_reduce")
qa_document_chain = AnalyzeDocumentChain(combine_docs_chain=qa_chain)

# def generate_audio(text, filename="output.mp3"):
#     tts = gTTS(text=text, lang="sp", slow=False)
#     tts.save(filename)



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
    tts = gTTS(text=response, lang='es', slow=False)
    tts.save('output.mp3')
    audio_filename = 'output.mp3'

    return jsonify({'answer': response, 'audio_filename': audio_filename})



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)




# from flask import Flask, render_template, request, jsonify
# from langchain.chains import AnalyzeDocumentChain
# from langchain.chat_models import ChatOpenAI
# from langchain.chains.question_answering import load_qa_chain
# from gtts import gTTS
# import os

# app = Flask(__name__)

# llm = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key="YOUR_OPENAI_API_KEY")
# qa_chain = load_qa_chain(llm, chain_type="map_reduce")
# qa_document_chain = AnalyzeDocumentChain(combine_docs_chain=qa_chain)

# def transform_to_yoda_style(text):
#     words = text.split()
#     yoda_style = " ".join(words[::-1])
#     return yoda_style

# def generate_audio(text, filename="output.mp3"):
#     tts = gTTS(text=text, lang="sp", slow=False)
#     tts.save(filename)

# # ... (resto de tu código)

# @app.route('/api/query', methods=['POST'])
# def query():
#     document = request.files['document'].read().decode('utf-8')
#     question = f"{request.form['question']} Answer in the style of Yoda."

#     # Llamada a Langchain
#     response = qa_document_chain.run(input_document=document, question=question)

#     # Transformar la respuesta al estilo de Yoda
#     yoda_style_answer = transform_to_yoda_style(response['answer'])

#     # Generar síntesis de voz
#     audio_filename = "output.mp3"
#     generate_audio(yoda_style_answer, audio_filename)

#     # Almacenar en la base de datos (a implementar)

#     return jsonify({'answer': yoda_style_answer, 'audio_filename': audio_filename})

# if __name__ == '__main__':
#     app.run(debug=True)

    
#     # transforma a yoda style
#     # words = response.split().........ultimo cambio
#     # yoda_answer = " ".join(words[::-1]).............ultimo cambio
#     # Transformar la respuesta al estilo de Yoda
#     #yoda_response = yoda_style(response['answer'])
    
#     # Devolver la respuesta transformada como JSON
#     # return jsonify({'answer': yoda_response})

#     # Almacenar en la base de datos (a implementar)

#     # return jsonify({'answer': response['answer']})

# # def yoda_style(answer):
# #     # Función simple para transformar la respuesta al estilo de Yoda
# #     words = answer.split()
# #     yoda_answer = " ".join(words[::-1])  # Invertir el orden de las palabras
# #     return yoda_answer
