def predict_salary(salary_from: int, salary_to: int):
    if not salary_from:
        return int(salary_to * 0.8)
    if not salary_to:
        return int(salary_from * 1.2)
    return int((salary_from + salary_to)/2)
