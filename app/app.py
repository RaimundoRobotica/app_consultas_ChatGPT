from flask import Flask, render_template, request, jsonify
from langchain.chains import AnalyzeDocumentChain
from langchain.chat_models import ChatOpenAI
from langchain.chains.question_answering import load_qa_chain
import pymysql
import pyttsx3

app = Flask(__name__)
app.config['DEBUG'] = True

llm = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key="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")
qa_chain = load_qa_chain(llm, chain_type="map_reduce")
qa_document_chain = AnalyzeDocumentChain(combine_docs_chain=qa_chain)

def guardar_en_base_de_datos(consulta, respuesta, archivo_nombre):
    # Información de conexión a la base de datos de AWS
    username = "admin"
    password = "elgrupo4"
    host = "database-2.cuwmrnsvir86.eu-north-1.rds.amazonaws.com"
    port = 3306
    database = "database-2"  # Reemplaza con el nombre de tu base de datos

    # Conectar a la base de datos
    connection = pymysql.connect(
        host=host,
        user=username,
        password=password,
        database=database,
        port=port,
        cursorclass=pymysql.cursors.DictCursor
    )

    # Crear un cursor para ejecutar comandos SQL
    cursor = connection.cursor()

    try:
        # Comando SQL para insertar datos en la tabla
        insert_data_query = 'INSERT INTO consultas (consulta, respuesta, archivo) VALUES (%s, %s, %s)'

        # Ejecutar el comando SQL para insertar los datos
        cursor.execute(insert_data_query, (consulta, respuesta, archivo_nombre))

        # Confirmar la inserción de datos
        connection.commit()

        print("Datos insertados en la base de datos.")
    except Exception as e:
        # En caso de un error, imprimirlo
        print(f"Error al insertar datos en la base de datos: {e}")
    finally:
        # Cerrar el cursor y la conexión
        cursor.close()
        connection.close()

@app.route('/')
def index():
    return render_template('../templates/index3.html')

@app.route('/api/query', methods=['POST'])
def query():
    document = request.files['document']
    question = f"{request.form['question']} contesta al estilo de Yoda."#.....simple simple simple
    
    # Almacenar el archivo subido por el usuario
    if document:
        archivo_nombre = document.filename
        document_content = document.read().decode('utf-8')  # Leer el contenido del archivo
    else:
        archivo_nombre = None
        document_content = None

    # Llamada a Langchain
    response = qa_document_chain.run(input_document=document_content, question=question)
    # print(response)

    rate = 130
    lang = 'es'

    engine = pyttsx3.init()
    engine.setProperty('rate',rate)
    engine.setProperty('voice', f'com.apple.speech.synthesis.voice.samantha.premium{lang}') #if lang == 'es' else lang)
    engine.say(response)
    engine.runAndWait()

    # Almacenar en la base de datos
    guardar_en_base_de_datos(question, response, archivo_nombre)
    # print({'consulta': question, 'archivo': archivo_nombre, 'respuesta': response})
    return jsonify({'answer': response})
    # return jsonify({'consulta': question, 'archivo': archivo_nombre, 'respuesta': response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


