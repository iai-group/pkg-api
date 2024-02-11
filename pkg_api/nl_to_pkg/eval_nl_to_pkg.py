"""Evaluates the NL to PKG models."""
import csv
from typing import Dict, Any, List, Tuple
from sklearn.metrics import f1_score
from tqdm import tqdm
from pkg_api.core.annotation import PKGData
from pkg_api.core.intents import Intent
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


def eval_annotations(
    data: List[Tuple], prompt_paths: Dict[str, str], config_path: str
) -> Dict[str, Any]:
    """Evaluates the annotation model using the provided data.

    Args:
        data: List of NL to PKG annotation data.
        prompt_paths: Dictionary containing the paths to the prompt files.
        config_path: Path to the config file for the LLMconnector.

    Returns:
        Dictionary containing the evaluation metrics.
    """
    annotator = ThreeStepStatementAnnotator(prompt_paths, config_path)
    annotations = [annotator.get_annotations(row[0]) for row in tqdm(data)]

    intent_macro_f1, intent_micro_f1 = get_intent_f1_scores(data, annotations)
    preference_macro_f1, preference_micro_f1 = get_preference_f1_scores(
        data, annotations
    )
    avg_triple_correct = get_mean_correct_triple_elements(data, annotations)
    return {
        "Intent F1 (macro)": intent_macro_f1,
        "Intent F1 (micro)": intent_micro_f1,
        "Preference F1 (macro)": preference_macro_f1,
        "Preference F1 (micro)": preference_micro_f1,
        "Avg. Triple Correct": avg_triple_correct,
    }


def get_intent_f1_scores(
    groundtruth_data: List[Tuple], annotations: List[Tuple[Intent, PKGData]]
) -> Tuple[float, float]:
    """Processes the intents in the data and compute F1 scores.

    Args:
        groundtruth_data: The dataset to be processed.
        annotations: List of annotations obtained from the annotator.

    Returns:
        Tuple of macro and micro F1 scores for the intents.
    """
    true_intents = []
    predicted_intents = []
    for (_, true_intent, _, _, _, _), (pred_intent, _) in zip(
        groundtruth_data, annotations
    ):
        true_intents.append(true_intent)
        predicted_intents.append(pred_intent.name)
    intent_macro_f1 = f1_score(true_intents, predicted_intents, average="macro")
    intent_micro_f1 = f1_score(true_intents, predicted_intents, average="micro")
    return intent_macro_f1, intent_micro_f1


def get_preference_f1_scores(
    groundtruth_data: List[Tuple], annotations: List[Tuple[Intent, PKGData]]
) -> Tuple[float, float]:
    """Processes the preferences in the data and compute F1 scores.

    Args:
        groundtruth_data: The dataset to be processed.
        annotations: List of annotations obtained from the annotator.

    Returns:
        Tuple of macro and micro F1 scores for the preferences.
    """
    true_preferences = []
    predicted_preferences = []
    for (_, _, _, _, _, true_pref), (_, pkg_data) in zip(
        groundtruth_data, annotations
    ):
        true_preferences.append(true_pref)
        if pkg_data.preference:
            predicted_preferences.append(str(int(pkg_data.preference.weight)))
        else:
            predicted_preferences.append("")
    preference_macro_f1 = f1_score(
        true_preferences, predicted_preferences, average="macro"
    )
    preference_micro_f1 = f1_score(
        true_preferences, predicted_preferences, average="micro"
    )
    return preference_macro_f1, preference_micro_f1


def get_mean_correct_triple_elements(
    groundtruth_data: List[Tuple], annotations: List[Tuple[Intent, PKGData]]
) -> float:
    """Compute the mean of correctly predicted triple elements per statement.

    Args:
        groundtruth_data: The dataset to be processed.
        annotations: List of annotations obtained from the annotator.

    Returns:
        Mean of correctly predicted triple elements per statement.
    """
    correct_triples = []
    for (_, _, sub, pred, obj, _), (_, pkg_data) in zip(
        groundtruth_data, annotations
    ):
        correct_triple_count = 0
        if pkg_data.triple:
            if (
                pkg_data.triple.subject.reference.strip()
                .replace(".", "")
                .replace("?", "")
                == sub
            ):
                correct_triple_count += 1
            if (
                pkg_data.triple.predicate.reference.strip()
                .replace(".", "")
                .replace("?", "")
                == pred
            ):
                correct_triple_count += 1
            if (
                pkg_data.triple.object.reference.strip()
                .replace(".", "")
                .replace("?", "")
                == obj
            ):
                correct_triple_count += 1
        correct_triples.append(correct_triple_count)
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

    print(
        "zero shot llama2",
        eval_annotations(data, zero_shot_prompt_paths, llama2_config),
    )
    print(
        "few shot llama2",
        eval_annotations(data, few_shot_prompt_paths, llama2_config),
    )
    print(
        "zero shot mistral",
        eval_annotations(data, zero_shot_prompt_paths, mistral_config),
    )
    print(
        "few shot mistral",
        eval_annotations(data, few_shot_prompt_paths, mistral_config),
    )
