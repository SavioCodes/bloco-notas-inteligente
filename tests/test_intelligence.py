import unittest

from smart_notepad.intelligence import analyze_note


class AnalyzeNoteTests(unittest.TestCase):
    def test_suggests_title_from_first_line(self) -> None:
        analysis = analyze_note("Plano semanal\n- [ ] Revisar projeto\nPesquisar ideias")

        self.assertEqual(analysis.suggested_title, "Plano semanal")

    def test_detects_todos_and_tags(self) -> None:
        analysis = analyze_note("Reuni\u00e3o do projeto\nTODO: enviar ata\nA\u00e7\u00e3o: revisar prazo")

        self.assertGreaterEqual(len(analysis.todos), 2)
        self.assertIn("reuniao", analysis.suggested_tags)
        self.assertIn("tarefa", analysis.suggested_tags)

    def test_empty_note_has_safe_defaults(self) -> None:
        analysis = analyze_note("")

        self.assertEqual(analysis.suggested_title, "Nota sem titulo")
        self.assertEqual(analysis.stats.words, 0)
        self.assertEqual(analysis.stats.reading_minutes, 0)


if __name__ == "__main__":
    unittest.main()
