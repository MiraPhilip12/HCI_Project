import pandas as pd

RESULTS_FILE = "backend_python/data/results.csv"


def save_result(student_id, question_id, selected_option, correct_option, time_taken):
    is_correct = selected_option == correct_option

    try:
        df = pd.read_csv(RESULTS_FILE)
    except FileNotFoundError:
        df = pd.DataFrame(columns=[
            "result_id",
            "student_id",
            "question_id",
            "selected_option",
            "is_correct",
            "time_seconds"
        ])

    result_id = len(df) + 1

    df.loc[len(df)] = {
        "result_id": result_id,
        "student_id": student_id,
        "question_id": question_id,
        "selected_option": selected_option,
        "is_correct": is_correct,
        "time_seconds": time_taken
    }

    df.to_csv(RESULTS_FILE, index=False)
    return is_correct
