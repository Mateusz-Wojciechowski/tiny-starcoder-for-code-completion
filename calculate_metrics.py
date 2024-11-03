import json
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from rouge_score import rouge_scorer
import sacrebleu
from codebleu import calc_codebleu


def load_data(json_path):
    with open(json_path, 'r') as file:
        return json.load(file)

# functions for metric calculations
def exact_match(reference, hypothesis):
    reference = reference.strip()
    hypothesis = hypothesis.strip()
    return 1 if reference == hypothesis else 0


def compute_chrf(reference, hypothesis):
    reference = reference.strip()
    hypothesis = hypothesis.strip()

    if len(hypothesis) == 0:
        return 0

    return sacrebleu.corpus_chrf([reference], [hypothesis], char_order=6, word_order=0).score


def compute_bleu(reference, hypothesis):
    reference = reference.strip()
    hypothesis = hypothesis.strip()
    reference_tokens = [reference.split()]
    hypothesis_tokens = hypothesis.split()
    return sentence_bleu(reference_tokens, hypothesis_tokens, smoothing_function=SmoothingFunction().method1)


def compute_rouge_l(reference, hypothesis):
    reference = reference.strip()
    hypothesis = hypothesis.strip()
    scorer = rouge_scorer.RougeScorer(['rougeL'], use_stemmer=True)
    score = scorer.score(reference, hypothesis)
    return score['rougeL'].fmeasure


def compute_codebleu(reference, hypothesis, lang='python'):
    reference = reference.strip()
    hypothesis = hypothesis.strip()
    return calc_codebleu([reference], [hypothesis], lang, tokenizer=None)


def evaluate_code(json_path, reference_column, hypothesis_column):
    data = load_data(json_path)
    results = []

    # calculating metrics for each entry in data
    for entry in data:
        reference = entry[reference_column]
        hypothesis = entry[hypothesis_column]

        metrics = {
            "exact_match": exact_match(reference, hypothesis),
            "chrf": compute_chrf(reference, hypothesis),
            "bleu": compute_bleu(reference, hypothesis),
            "rouge_l": compute_rouge_l(reference, hypothesis),
            "code_bleu": compute_codebleu(reference, hypothesis)['codebleu']
        }
        results.append({"reference": reference, "hypothesis": hypothesis, "metrics": metrics, 'label': entry['label']})

    return results


json_path = "completion_data/completions_labeled.json"
results_code = evaluate_code(json_path, 'correct_code', 'completed_code')
results_completions = evaluate_code(json_path, 'correct_middle', 'extracted_middle')

with open('results_data/results_code.json', 'w') as results_file:
    json.dump(results_code, results_file, indent=4)

with open('results_data/results.json', 'w') as results_file:
    json.dump(results_completions, results_file, indent=4)


