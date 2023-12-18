import unittest
from flask_testing import TestCase
from app import guardar_en_base_de_datos, app

class TestApp(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        return app

    def test_index_route(self):
        response = self.client.get('/')
        self.assert200(response)

    def test_query_route(self):
        with open('demo/test_document.txt', 'rb') as test_document:
            response = self.client.post('/api/query', data=dict(
                document=(test_document, 'test_document.txt'),
                question='What is the answer?'
            ), follow_redirects=True)
            
            self.assert200(response)
            # Aquí puedes agregar más aserciones según lo que esperas en la respuesta

    def test_guardar_en_base_de_datos(self):
        guardar_en_base_de_datos('Test question', 'Test answer', 'test_file.txt')

if __name__ == '__main__':
    unittest.main()