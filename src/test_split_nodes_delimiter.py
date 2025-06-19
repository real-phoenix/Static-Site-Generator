import unittest
from text_to_html_node_conversion import split_nodes_delimiter
from textnode import TextNode, TextType

class TestInlineMarkdown(unittest.TestCase):
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.NORMAL_TEXT, None)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD_TEXT)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.NORMAL_TEXT, None),
                TextNode("bolded", TextType.BOLD_TEXT, None),
                TextNode(" word", TextType.NORMAL_TEXT, None),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.NORMAL_TEXT, None
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD_TEXT)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.NORMAL_TEXT, None),
                TextNode("bolded", TextType.BOLD_TEXT, None),
                TextNode(" word and ", TextType.NORMAL_TEXT, None),
                TextNode("another", TextType.BOLD_TEXT, None),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.NORMAL_TEXT, None
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD_TEXT)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.NORMAL_TEXT, None),
                TextNode("bolded word", TextType.BOLD_TEXT, None),
                TextNode(" and ", TextType.NORMAL_TEXT, None),
                TextNode("another", TextType.BOLD_TEXT, None),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.NORMAL_TEXT, None)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC_TEXT)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.NORMAL_TEXT, None),
                TextNode("italic", TextType.ITALIC_TEXT, None),
                TextNode(" word", TextType.NORMAL_TEXT, None),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.NORMAL_TEXT, None)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD_TEXT)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC_TEXT)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD_TEXT, None),
                TextNode(" and ", TextType.NORMAL_TEXT, None),
                TextNode("italic", TextType.ITALIC_TEXT, None),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.NORMAL_TEXT, None)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE_TEXT)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.NORMAL_TEXT, None),
                TextNode("code block", TextType.CODE_TEXT, None),
                TextNode(" word", TextType.NORMAL_TEXT, None),
            ],
            new_nodes,
        )


if __name__ == "__main__":
    unittest.main()