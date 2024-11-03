import json
from transformers import AutoModelForCausalLM, AutoTokenizer

checkpoint = "bigcode/tiny_starcoder_py"
device = "cpu"

tokenizer = AutoTokenizer.from_pretrained(checkpoint)
model = AutoModelForCausalLM.from_pretrained(checkpoint).to(device)


def generate_completions(json_path, output_path):
    with open(json_path, 'r') as data_file:
        completion_data = json.load(data_file)

    results = []

    for structure in completion_data:
        correct_code = structure['prefix'] + structure['middle'] + structure['suffix']

        # creating input for the model
        input_text = f"<fim_prefix>{structure['prefix']}<fim_suffix>{structure['suffix']}<fim_middle>"
        inputs = tokenizer(input_text, return_tensors="pt").to(device)

        output = model.generate(
            inputs["input_ids"],
            attention_mask=inputs["attention_mask"],
            pad_token_id=tokenizer.eos_token_id,
            max_new_tokens=30
        )

        # obtaining generated code
        completed_code = tokenizer.decode(output[0], skip_special_tokens=True)

        results.append({
            "correct_code": correct_code,
            "completed_code": completed_code,
            "correct_middle": structure['middle'],
            "prefix": structure['prefix'],
            "suffix": structure['suffix']
        })

    # saving he results into json
    with open(output_path, 'w') as output_file:
        json.dump(results, output_file, indent=4)



if __name__ == '__main__':
    generate_completions('completion_data/structured_positions.json', 'completion_data/completions.json')

