import unittest
from textnode import TextType, TextNode

class TestTextNode(unittest.TestCase): 
    def test_eq(self): 
        node = TextNode("This is a test node", TextType.BOLD_TEXT, None)
        node2 = TextNode("This is a test node", TextType.BOLD_TEXT, None)
        node3 = TextNode("this is a test node", TextType.CODE_TEXT, None)
        node4 = TextNode("this is a test node", TextType.IMAGE_FORMAT, None)
        self.assertEqual(node, node2)
        self.assertNotEqual(node2, node4)
        self.assertNotEqual(node3, node4)

    def test_eq_false(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT, None)
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT, None)
        self.assertEqual(node, node2)

    def test_eq_false2(self):
        node = TextNode("This is a text node", TextType.NORMAL_TEXT, None)
        node2 = TextNode("This is a text node2", TextType.NORMAL_TEXT, None)
        self.assertNotEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("This is a text node", TextType.ITALIC_TEXT, "https://www.boot.dev")
        node2 = TextNode("This is a text node", TextType.ITALIC_TEXT, "https://www.boot.dev")
        self.assertEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.NORMAL_TEXT, "https://www.boot.dev")
        self.assertEqual(
            "TextNode(This is a text node, normal, https://www.boot.dev)", repr(node)
        )

if __name__ == "__main__": 
    unittest.main()