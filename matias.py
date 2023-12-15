from flask import Flask, render_template, request, jsonify
from langchain.chains import AnalyzeDocumentChain
from langchain.chat_models import ChatOpenAI
from langchain.chains.question_answering import load_qa_chain
import sqlite3

app = Flask(__name__)
app.config['DEBUG'] = True

llm = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key="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")
qa_chain = load_qa_chain(llm, chain_type="map_reduce")
qa_document_chain = AnalyzeDocumentChain(combine_docs_chain=qa_chain)

def guardar_en_base_de_datos(consulta, respuesta):
    # Nombre del archivo de la base de datos
    db_file = 'bbdd_pruebas.db'

    # Crear una conexión a la base de datos (esto también crea el archivo si no existe)
    conn = sqlite3.connect(db_file)

    # Crear un cursor para ejecutar comandos SQL
    cursor = conn.cursor()

    try:
        # Comando SQL para insertar datos en la tabla
        insert_data_query = 'INSERT INTO consultas_respuestas (consulta, respuesta) VALUES (?, ?)'

        # Ejecutar el comando SQL para insertar los datos
        cursor.execute(insert_data_query, (consulta, respuesta))

        # Confirmar la inserción de datos
        conn.commit()

        print("Datos insertados en la base de datos.")
    except Exception as e:
        # En caso de un error, imprimirlo
        print(f"Error al insertar datos en la base de datos: {e}")
    finally:
        # Cerrar el cursor y la conexión
        cursor.close()
        conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/query', methods=['POST'])
def query():
    document = request.files['document'].read().decode('utf-8')
    question = request.form['question']

    # Llamada a Langchain
    response = qa_document_chain.run(input_document=document, question=question)

    # Almacenar en la base de datos
    guardar_en_base_de_datos(question, response)

    return jsonify({'answer': response, 'question': question})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)