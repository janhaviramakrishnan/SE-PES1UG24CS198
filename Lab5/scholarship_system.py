
"""Scholarship screening system with configurable merit scoring."""

import ast
import json
import operator

results = {}
MERIT_FORMULA = "gpa * 10 + credits * 2"
INCOME_LIMIT = 800000
CUTOFF = 85


def _evaluate_expression(node, variables):
    """Safely evaluate supported arithmetic expressions."""
    allowed_operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
    }

    if isinstance(node, ast.Constant) and type(node.value) in (int, float):
        return node.value

    if isinstance(node, ast.Name) and node.id in variables:
        return variables[node.id]

    if isinstance(node, ast.BinOp) and type(node.op) in allowed_operators:
        left = _evaluate_expression(node.left, variables)
        right = _evaluate_expression(node.right, variables)

        if isinstance(node.op, ast.Pow) and abs(right) > 10:
            raise ValueError("Exponent is too large")

        return allowed_operators[type(node.op)](left, right)

    if isinstance(node, ast.UnaryOp):
        value = _evaluate_expression(node.operand, variables)

        if isinstance(node.op, ast.USub):
            return -value

        if isinstance(node.op, ast.UAdd):
            return value

    raise ValueError("Unsupported or unsafe merit formula")


def calculate_merit_score(gpa, credit_count, formula=MERIT_FORMULA):
    """Calculate merit using the configured formula."""
    expression = ast.parse(formula, mode="eval")
    variables = {"gpa": gpa, "credits": credit_count}
    score = _evaluate_expression(expression.body, variables)

    if not isinstance(score, (int, float)) or not (
        float("-inf") < score < float("inf")
    ):
        raise ValueError("Merit score must be finite")

    return score


def evaluate_applicant(
    student_id, test_scores, logs=None, formula=MERIT_FORMULA
):
    """Evaluate an applicant and record their eligibility."""
    if logs is None:
        logs = []

    gpa = test_scores["gpa"]
    credit_count = test_scores.get("credits", 0)
    income = test_scores.get("income", 0)

    score = calculate_merit_score(gpa, credit_count, formula)
    eligible = score >= CUTOFF and income < INCOME_LIMIT

    results[student_id] = {"score": score, "eligible": eligible}
    logs.append(f"{student_id} scored {score}")

    return eligible


def change_formula(new_formula):
    """Validate a new merit formula and return it."""
    expression = ast.parse(new_formula, mode="eval")
    allowed_names = {"gpa", "credits"}

    for node in ast.walk(expression):
        if isinstance(node, ast.Name) and node.id not in allowed_names:
            raise ValueError(f"Unsupported variable: {node.id}")

        if isinstance(node, ast.Call):
            raise ValueError("Function calls are not allowed")

    _evaluate_expression(expression.body, {"gpa": 1, "credits": 1})

    return new_formula


def persist_results(file="scholarships.json"):
    """Save scholarship results as JSON."""
    with open(file, "w", encoding="utf-8") as results_file:
        json.dump(results, results_file, indent=2)


def load_results(file="scholarships.json"):
    """Load saved results while handling expected file errors."""
    try:
        with open(file, "r", encoding="utf-8") as results_file:
            loaded_results = json.load(results_file)

        return loaded_results if isinstance(loaded_results, dict) else {}

    except (OSError, json.JSONDecodeError):
        return {}


def print_shortlist():
    """Print eligible applicants and their merit scores."""
    print("Shortlisted applicants:")

    for student_id, applicant in results.items():
        if applicant.get("eligible"):
            print(f"  {student_id} score = {applicant['score']}")


def main():
    """Run the scholarship screening program."""
    evaluate_applicant(
        "U001", {"gpa": 9.1, "credits": 4, "income": 450000}
    )
    evaluate_applicant(
        "U002", {"gpa": 7.2, "credits": 1, "income": 300000}
    )
    evaluate_applicant(
        "U003", {"gpa": 12.5, "credits": -3, "income": -1}
    )
    evaluate_applicant("U004", {"gpa": 6.5})

    merit_formula = MERIT_FORMULA
    formula = input("Merit formula (Enter to keep default): ").strip()

    if formula:
        try:
            merit_formula = change_formula(formula)
        except (
            ValueError,
            SyntaxError,
            TypeError,
            ZeroDivisionError,
        ) as error:
            print(f"Invalid merit formula: {error}")
            return

    evaluate_applicant(
        "U005",
        {"gpa": 8.4, "credits": 3, "income": 600000},
        formula=merit_formula,
    )

    persist_results()
    results.update(load_results())
    print_shortlist()


if __name__ == "__main__":
    main()
