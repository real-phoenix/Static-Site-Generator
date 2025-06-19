import unittest
from htmlnode import HTMLNode


class TesHTMLtNode(unittest.TestCase): 
    def test_props_to_html_with_multiple_attributes(self):
        node = HTMLNode(tag="a", props={"href": "https://example.com", "target": "_blank"})
        expected = ' href="https://example.com" target="_blank"'
        self.assertEqual(node.props_to_html(), expected)

    def test_props_to_html_empty(self):
        node = HTMLNode(tag="div")
        self.assertEqual(node.props_to_html(), "")

    def test_repr_includes_all_fields(self):
        node = HTMLNode(tag="p", value="Hello", children=[], props={"class": "intro"})
        repr_output = repr(node)
        self.assertIn("tag='p'", repr_output)
        self.assertIn("value='Hello'", repr_output)
        self.assertIn("'class': 'intro'", repr_output)
    
    def test_to_html_props(self):
        node = HTMLNode(
            "div",
            "Hello, world!",
            None,
            {"class": "greeting", "href": "https://boot.dev"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' class="greeting" href="https://boot.dev"',
        )

    def test_values(self):
        node = HTMLNode(
            "div",
            "I wish I could read",
        )
        self.assertEqual(
            node.tag,
            "div",
        )
        self.assertEqual(
            node.value,
            "I wish I could read",
        )
        self.assertEqual(
            node.children,
            [],
        )
        self.assertEqual(
            node.props,
            {},
        )

    def test_repr(self):
        node = HTMLNode(
            "p",
            "What a strange world",
            None,
            {"class": "primary"},
        )
        self.assertEqual(
            node.__repr__(),
            "HTMLNode(tag='p', value='What a strange world', children= [], props={'class': 'primary'})",
        )

if __name__ == "__main__": 
    unittest.main()