class TestExample:

    def test_short_phrase(self):
        phrase = input("Set a phrase: ")
        expected_len = 15
        assert len(phrase) < expected_len, f"The number of characters is equal to or greater than {expected_len}"
