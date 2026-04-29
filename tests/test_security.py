import unittest

from smart_notepad.security import SecurityError, create_password_record, decrypt_text, encrypt_text, is_encrypted, verify_password


class SecurityTests(unittest.TestCase):
    def test_encrypts_and_decrypts_text(self) -> None:
        encrypted = encrypt_text("segredo", "senha-forte")

        self.assertTrue(is_encrypted(encrypted))
        self.assertEqual(decrypt_text(encrypted, "senha-forte"), "segredo")

    def test_rejects_wrong_password(self) -> None:
        encrypted = encrypt_text("segredo", "senha-forte")

        with self.assertRaises(SecurityError):
            decrypt_text(encrypted, "senha-errada")

    def test_password_record_verification(self) -> None:
        record = create_password_record("senha-forte")

        self.assertTrue(verify_password("senha-forte", record))
        self.assertFalse(verify_password("outra-senha", record))


if __name__ == "__main__":
    unittest.main()

