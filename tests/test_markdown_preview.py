import unittest

from smart_notepad.markdown_preview import parse_markdown


class MarkdownPreviewTests(unittest.TestCase):
    def test_parses_common_markdown_blocks(self) -> None:
        blocks = parse_markdown("# Titulo\n\n- item\n- [x] feito\n> citacao\n```py\nprint('ok')\n```")

        kinds = [block.kind for block in blocks]

        self.assertIn("heading", kinds)
        self.assertIn("bullet", kinds)
        self.assertIn("checkbox", kinds)
        self.assertIn("quote", kinds)
        self.assertIn("code", kinds)


if __name__ == "__main__":
    unittest.main()

