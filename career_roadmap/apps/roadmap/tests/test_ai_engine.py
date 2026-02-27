import unittest
from types import SimpleNamespace

from apps.roadmap.services.ai_engine import generate_recommendations


class AIEngineTests(unittest.TestCase):
    def test_generate_recommendations_returns_expected_shape(self):
        assessment = SimpleNamespace(
            interests=["ai_ml"],
            skills=["python", "sql", "problem_solving"],
            strong_subjects="mathematics, computer_science",
            financial_background="middle",
        )

        output = generate_recommendations(assessment)

        self.assertIn("top_3_recommendations", output)
        self.assertGreaterEqual(len(output["top_3_recommendations"]), 2)
        self.assertIn("career", output["top_3_recommendations"][0])


if __name__ == "__main__":
    unittest.main()
