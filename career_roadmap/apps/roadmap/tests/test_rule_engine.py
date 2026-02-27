import unittest

from apps.roadmap.services.rule_engine import recommend_career_paths


class RuleEngineTests(unittest.TestCase):
    def test_returns_three_recommendations_for_unknown_interest(self):
        result = recommend_career_paths(
            {
                "interest": "unknown",
                "skill_level": "intermediate",
                "subject_strengths": ["mathematics"],
                "financial_background": "low",
            }
        )

        self.assertIn("top_3_recommendations", result)
        self.assertEqual(len(result["top_3_recommendations"]), 3)

    def test_includes_required_output_fields(self):
        result = recommend_career_paths(
            {
                "interest": "ai_ml",
                "skill_level": "advanced",
                "subject_strengths": ["mathematics", "computer_science"],
                "financial_background": "middle",
            }
        )

        first = result["top_3_recommendations"][0]
        self.assertIn("career", first)
        self.assertIn("reasoning", first)
        self.assertIn("estimated_salary_range_india", first)
        self.assertIn("four_year_roadmap", first)
        self.assertEqual(len(first["four_year_roadmap"]), 4)


if __name__ == "__main__":
    unittest.main()
