"""Evaluates the NL to PKG models."""
import csv
from typing import Dict, Any
from sklearn.metrics import f1_score
from tqdm import tqdm
from pkg_api.nl_to_pkg.annotators.three_step_annotator import (
    ThreeStepStatementAnnotator,
    _DEFAULT_PROMPT_PATHS
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

from typing import List, Tuple

def eval_annotations(data: List[Tuple], prompt_paths: Dict[str, str], config_path: str) -> Dict[str, Any]:
    """Evaluates the intent model using the provided data.

    Args:
        data: List of NL to PKG annotation data.
    """
    annotator = ThreeStepStatementAnnotator(prompt_paths, config_path)
    annotations = [annotator.get_annotations(row[0]) for row in tqdm(data)]

    intent_macro_f1, intent_micro_f1 = process_intents(data, annotations)
    preference_macro_f1, preference_micro_f1 = process_preferences(data, annotations)
    avg_triple_correct = process_triples(data, annotations)
    return {"Intent F1 (macro)": intent_macro_f1, "Intent F1 (micro)": intent_micro_f1, "Preference F1 (macro)": preference_macro_f1, "Preference F1 (micro)": preference_micro_f1, "Avg. Triple Correct": avg_triple_correct}


def process_intents(data: List[Tuple], annotations: List) -> Tuple[List, List]:
    """Processes the intents in the data.

    Args:
        data: The dataset to be processed.
        annotations: List of annotations obtained from the annotator.

    Returns:
        Macro and micro F1 scores for the intents.
    """
    true_intents = []
    predicted_intents = []
    for (_, true_intent, _, _, _, _), (pred_intent, _) in zip(data, annotations):
        true_intents.append(true_intent)
        predicted_intents.append(pred_intent.name)
    intent_macro_f1 = f1_score(true_intents, predicted_intents, average="macro")
    intent_micro_f1 = f1_score(true_intents, predicted_intents, average="micro")
    return intent_macro_f1, intent_micro_f1

def process_preferences(data: List[Tuple], annotations: List) -> Tuple[List, List]:
    """Processes the preferences in the data.

    Args:
        data: The dataset to be processed.
        annotations: List of annotations obtained from the annotator.

    Returns:
        Macro and micro F1 scores for the preferences.
    """
    true_preference = []
    predict_preferene = []
    for (_, _, _, _, _, true_pref), (_, pkg_data) in zip(data, annotations):
        true_preference.append(true_pref)
        if pkg_data.preference:
            predict_preferene.append(str(int(pkg_data.preference.weight)))
        else:
            predict_preferene.append("")
    preference_macro_f1 = f1_score(true_preference, predict_preferene, average="macro")
    preference_micro_f1 = f1_score(true_preference, predict_preferene, average="micro")
    return preference_macro_f1, preference_micro_f1


def process_triples(data: List[Tuple], annotations: List) -> Tuple[List, List, List, int]:
    """Processes the triples in the data.

    Args:
        data: The dataset to be processed.
        annotations: List of annotations obtained from the annotator.

    Returns:
        Average number of correctly predicted triples.
    """

    correct_triples = []
    for (_, _, sub, pred, obj, _), (_, pkg_data) in zip(data, annotations):
        correct_triple_count = 0
        if pkg_data.triple:
            if pkg_data.triple.subject.strip().replace(".", "").replace("?", "") == sub:
                correct_triple_count += 1
            if pkg_data.triple.predicate.strip().replace(".", "").replace("?", "") == pred:
                correct_triple_count += 1
            if pkg_data.triple.object.strip().replace(".", "").replace("?", "") == obj:
                correct_triple_count += 1
        correct_triples.append(correct_triple_count)
        print(correct_triple_count, sub, pred, obj, pkg_data.triple)
    return sum(correct_triples) / len(correct_triples)


if __name__ == "__main__":
    data = load_data("data/nl_annotations/test.csv")
    zero_shot_prompt_paths = {
        "intent": "data/llm_prompts/default/intent.txt",
        "triple": "data/llm_prompts/default/triple.txt",
        "preference": "data/llm_prompts/default/preference.txt",
    }
    few_shot_prompt_paths = {
        "intent": "data/llm_prompts/cot/intent.txt",
        "triple": "data/llm_prompts/cot/triple.txt",
        "preference": "data/llm_prompts/cot/preference.txt",
    }
    llama2_config = "pkg_api/nl_to_pkg/llm/configs/llm_config_llama2.yaml"
    mistral_config = "pkg_api/nl_to_pkg/llm/configs/llm_config_mistral.yaml"
    
    print("zero shot llama2", eval_annotations(data, zero_shot_prompt_paths, llama2_config))
    print("few shot llama2", eval_annotations(data, few_shot_prompt_paths, llama2_config))
    print("zero shot mistral", eval_annotations(data, zero_shot_prompt_paths, mistral_config))
    print("few shot mistral", eval_annotations(data, few_shot_prompt_paths, mistral_config))