import draw_image
import unittest


class TestDraw(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    # </helper>

    def test_create(self):
        self.assertTrue(draw_image.create([{
            "char": "上野駅青森駅間を東北本線",
            "size": "full",
            "color": "#55aaff",
            "background": "#010211"
        }],
            outputFile="a.jpg",
            height=32
        ))

    def _CHAR_TEST(self):
        return {
            "char": "上野駅青森駅間を東北本線",
            "size": "full",
            "color": "#55aaff",
            "background": "#010211"
        }

    def test_full_chars(self):
        canvas = draw_image.full_chars(self._CHAR_TEST())
        assert canvas.width==384
        assert canvas.height==32

    def test_one_char(self):
        canvas = draw_image.full_chars(self._CHAR_TEST())

        print(type(draw_image.put_one_char(0,0,"駅",canvas)) )
#        assert draw_image.one_char(0,0,"駅",canvas) is "駅"Traceback (most recent call last):
