def test_file_search_called(result):
    assert result["searched"]


def test_answer_from_policy(result):
    answer = result["answer"]
    assert "250" in answer and ("receipt" in answer.lower())


def test_expense_policy_cited(result):
    assert "expenses.md" in result["cited"]
