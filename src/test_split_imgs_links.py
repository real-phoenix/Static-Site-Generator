import unittest
from text_to_html_node_conversion import split_nodes_image, split_nodes_link, text_to_textnodes, split_nodes_delimiter, markdown_to_blocks
from blocknode import block_to_block_type
from textnode import TextNode, TextType

class TestSplitImgLinks(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.NORMAL_TEXT, 
            None
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.NORMAL_TEXT, None),
                TextNode("image", TextType.IMAGE_FORMAT, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.NORMAL_TEXT, None),
                TextNode(
                    "second image", TextType.IMAGE_FORMAT, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.NORMAL_TEXT,
            None
            )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.NORMAL_TEXT, None),
                TextNode("to boot dev", TextType.LINK_FORMAT, "https://www.boot.dev"),
                TextNode(" and ", TextType.NORMAL_TEXT, None),
                TextNode(
                    "to youtube", TextType.LINK_FORMAT, "https://www.youtube.com/@bootdotdev"
                ),
            ], 
            new_nodes, 
        )

    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.NORMAL_TEXT,
            None
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.NORMAL_TEXT, None),
                TextNode("image", TextType.IMAGE_FORMAT, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.COM/IMAGE.PNG)",
            TextType.NORMAL_TEXT,
            None
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE_FORMAT, "https://www.example.COM/IMAGE.PNG"),
            ],
            new_nodes,
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.NORMAL_TEXT,
            None
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.NORMAL_TEXT, None),
                TextNode("image", TextType.IMAGE_FORMAT, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.NORMAL_TEXT, None),
                TextNode(
                    "second image", TextType.IMAGE_FORMAT, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev) with text that follows",
            TextType.NORMAL_TEXT,
            None
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.NORMAL_TEXT, None),
                TextNode("link", TextType.LINK_FORMAT, "https://boot.dev"),
                TextNode(" and ", TextType.NORMAL_TEXT, None),
                TextNode("another link", TextType.LINK_FORMAT, "https://blog.boot.dev"),
                TextNode(" with text that follows", TextType.NORMAL_TEXT, None),
            ],
            new_nodes,
        )
    
    def test_split_text_to_textnodes(self): 
        node = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(node)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.NORMAL_TEXT, None),
                TextNode("text", TextType.BOLD_TEXT, None),
                TextNode(" with an ", TextType.NORMAL_TEXT, None),
                TextNode("italic", TextType.ITALIC_TEXT, None),
                TextNode(" word and a ", TextType.NORMAL_TEXT, None),
                TextNode("code block", TextType.CODE_TEXT, None),
                TextNode(" and an ", TextType.NORMAL_TEXT, None),
                TextNode("obi wan image", TextType.IMAGE_FORMAT, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.NORMAL_TEXT, None),
                TextNode("link", TextType.LINK_FORMAT, "https://boot.dev"),
            ],
            new_nodes,
        )
    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.NORMAL_TEXT, None)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD_TEXT)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC_TEXT)
        self.assertEqual(
            [
                TextNode("bold", TextType.BOLD_TEXT, None),
                TextNode(" and ", TextType.NORMAL_TEXT, None),
                TextNode("italic", TextType.ITALIC_TEXT, None),
            ],
            new_nodes,
        )

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_block_type(self): 
        test1 = block_to_block_type("# Heading")
        test2 = block_to_block_type("1. Item\n2. Next")
        self.assertEqual("heading", test1)
        self.assertEqual("ordered_list", test2)

if __name__ == "__main__":
    unittest.main()