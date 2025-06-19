import unittest
from htmlnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_with_props(self):
        node = LeafNode("a", "Click here", {"href": "https://google.com", "target": "_blank"})
        self.assertEqual(
            node.to_html(),
            '<a href="https://google.com" target="_blank">Click here</a>'
        )

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Just text")
        self.assertEqual(node.to_html(), "Just text")

    def test_leaf_missing_value_raises(self):
        with self.assertRaises(ValueError):
            LeafNode("p", None)

    def test_leaf_empty_props(self):
        node = LeafNode("span", "Note", {})
        self.assertEqual(node.to_html(), "<span>Note</span>")

if __name__ == "__main__":
    unittest.main()
