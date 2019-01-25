import srv
import unittest

# https://a2c.bitbucket.io/flask/testing.html


class TestMyAppTestCase(unittest.TestCase):

    def setUp(self):
        self.app = srv.app.test_client()

    def tearDown(self):
        pass

    def test_first_test(self):

        # see https://a2c.bitbucket.io/flask/api.html#response-objects

        rv = self.app.get('/')
        assert 200 == rv.status_code

        body = rv.data.decode()
        assert 'ppm' in body


if __name__ == '__main__':
    unittest.main()
