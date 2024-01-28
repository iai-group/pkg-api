"""Evaluates the NL to PKG models."""
import csv

from sklearn.metrics import f1_score

from pkg_api.nl_to_pkg.annotators.three_step_annotator import (
    ThreeStepStatementAnnotator,
)


def load_data(path: str) -> list:
    """Loads a csv data file containing NL to PKG test.

    Args:
        path: Path to the file containing the data.

    Returns:
        List of NL to PKG annotation data.
    """
    with open(path, "r") as f:
        reader = csv.reader(f, skipinitialspace=True, delimiter=",")
        next(reader)  # Skip the header row
        data = list(reader)
    return data


def eval_intent(data: list) -> None:
    """Evaluates the intent model.

    Args:
        data: List of NL to PKG annotation data.
    """
    annotator = ThreeStepStatementAnnotator()
    true_intents = []
    predicted_intents = []
    true_preference = []
    predict_preferene = []
    true_triples = []
    predicted_triples = []
    correct_triples = []
    for row in data:
        intent, pkg_data = annotator.get_annotations(row[0])
        print(f"Statement: {row}, Intent: {intent}, PKG data: {pkg_data}")
        true_intents.append(row[1])
        predicted_intents.append(intent.name)
        true_preference.append(row[5])
        if pkg_data.preference:
            predict_preferene.append(str(int(pkg_data.preference.weight)))
        else:
            predict_preferene.append("")
        true_triples.append(row[2:5])
        correct_triple = 0
        num_all_correct_triples = 0
        if pkg_data.triple:
            if pkg_data.triple.subject == row[2]:
                correct_triple += 1
            if pkg_data.triple.predicate == row[3]:
                correct_triple += 1
            if pkg_data.triple.object == row[4]:
                correct_triple += 1
            if correct_triple == 3:
                num_all_correct_triples += 1
            predicted_triples.append(
                [
                    pkg_data.triple.subject,
                    pkg_data.triple.predicate,
                    pkg_data.triple.object,
                ]
            )
        else:
            predicted_triples.append(["", "", ""])
        correct_triples.append(correct_triple)

    intent_macro_f1 = f1_score(true_intents, predicted_intents, average="macro")
    pref_macro_f1 = f1_score(
        true_preference, predict_preferene, average="macro"
    )
    avg_triple_correct = sum(correct_triples) / len(correct_triples)
    for true_int, pred_int, true_pref, pred_pref in zip(
        true_intents, predicted_intents, true_preference, predict_preferene
    ):
        print(f"{true_int}, {pred_int}, {true_pref}, {pred_pref}")
    for true_triple, pred_triple in zip(true_triples, predicted_triples):
        print(f"{true_triple}, {pred_triple}")
    print(num_all_correct_triples)

    print(f"Intent macro F1: {intent_macro_f1}")
    intent_micro_f1 = f1_score(true_intents, predicted_intents, average="micro")
    print(f"Intent micro F1: {intent_micro_f1}")
    print(f"Preference macro F1: {pref_macro_f1}")
    pref_micro_f1 = f1_score(
        true_preference, predict_preferene, average="micro"
    )
    print(f"Preference micro F1: {pref_micro_f1}")
    print(f"Average triple correct: {avg_triple_correct}")


if __name__ == "__main__":
    data = load_data("data/nl_annotations/test.csv")
    eval_intent(data)
