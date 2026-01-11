import os
import json
import re
import argparse
from typing import List, Dict, Any
from openai import OpenAI
from tqdm import tqdm

# ================= Configuration =================
# Default Judge Model as specified in Section 4.4 of the paper (GPT-4o)
DEFAULT_JUDGE_MODEL = "gpt-4o"

# Path to the prompt template file
PROMPT_FILE = "evaluate prompt.md"
# =================================================

# Initialize OpenAI Client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def parse_prompt_file(file_path: str) -> Dict[str, str]:
    """
    Parses the Markdown file to extract prompt templates for different task types.
    
    Structure expectation:
    # type Task Name
    [Prompt Content]
    
    Args:
        file_path: Path to the evaluate prompt.md file.
        
    Returns:
        Dictionary mapping task types to their specific prompt templates.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Prompt file not found: {file_path}")

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split content by the '# type' header
    sections = re.split(r'^# type\s+(.+)$', content, flags=re.MULTILINE)
    
    prompts = {}
    # re.split results in [header, type_name, content, type_name, content...]
    # We iterate starting from index 1 with a step of 2
    for i in range(1, len(sections), 2):
        task_types_raw = sections[i].strip()
        prompt_content = sections[i+1].strip()
        
        # Handle cases where multiple tasks share one prompt (separated by comma or Chinese comma)
        # e.g., "Mnestic Trigger Analysis、Temporal Reasoning"
        task_types = [t.strip() for t in re.split(r'[、,]', task_types_raw)]
        
        for t in task_types:
            prompts[t] = prompt_content

    print(f"✅ Successfully loaded {len(prompts)} prompt templates from {file_path}")
    return prompts

def evaluate_single_item(item: Dict, prompt_template: str, model: str) -> Dict:
    """
    Evaluates a single model response using the LLM-as-a-Judge protocol.
    
    Args:
        item: Dictionary containing 'question', 'reference_answer', and 'model_answer'.
        prompt_template: The specific prompt string for this task type.
        model: The judge model to use (e.g., gpt-4o).
        
    Returns:
        Dictionary containing the evaluation score and reasoning.
    """
    # 1. Fill the template placeholders
    user_question = item.get('question', '')
    ref_answer = item.get('reference_answer', '')
    model_ans = item.get('model_answer', '')
    
    # Replace placeholders defined in the prompt file
    final_prompt = prompt_template.replace('{{question}}', str(user_question))\
                                  .replace('{{reference_answer}}', str(ref_answer))\
                                  .replace('{{model_answer}}', str(model_ans))

    # 2. Call the LLM Judge
    # As per paper Section 4.4, we use a rigorous rubric-based scoring.
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are an impartial judge evaluating AI model outputs based on strict criteria."},
                {"role": "user", "content": final_prompt}
            ],
            temperature=0, # Deterministic output for reproducibility
            response_format={"type": "json_object"} # Enforce JSON format for parsing
        )
        
        result_text = response.choices[0].message.content
        result_json = json.loads(result_text)
        
        return {
            "id": item.get('id'),
            "task_type": item.get('task_type'),
            "score": result_json.get('score'),
            "reasoning": result_json.get('reasoning'),
            "status": "success"
        }
        
    except Exception as e:
        print(f"❌ Error processing Item ID {item.get('id')}: {e}")
        return {
            "id": item.get('id'),
            "task_type": item.get('task_type'),
            "score": 0,
            "reasoning": f"Evaluation Error: {str(e)}",
            "status": "error"
        }

def main():
    parser = argparse.ArgumentParser(description="KnowMe-Bench LLM-as-a-Judge Evaluator")
    parser.add_argument("--input_file", type=str, required=True, help="JSON file containing model outputs merged with ground truth.")
    parser.add_argument("--output_file", type=str, default="evaluation_results.json", help="Path to save the evaluation output.")
    parser.add_argument("--judge_model", type=str, default=DEFAULT_JUDGE_MODEL, help="The OpenAI model to serve as the judge (default: gpt-4o).")
    args = parser.parse_args()

    # 1. Load Prompt Templates
    try:
        prompts_map = parse_prompt_file(PROMPT_FILE)
    except Exception as e:
        print(f"Error loading prompts: {e}")
        return

    # 2. Load Input Data
    with open(args.input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"🚀 Starting evaluation for {len(data)} items using {args.judge_model}...")
    
    results = []
    
    # 3. Main Evaluation Loop
    for item in tqdm(data, desc="Evaluating"):
        task_type = item.get('task_type')
        
        if task_type not in prompts_map:
            # Fallback or Skip if task type isn't defined in the prompt file
            # Warning: Ensure input JSON 'task_type' matches headers in MD file exactly
            print(f"⚠️  Warning: No prompt found for task type '{task_type}' (ID: {item.get('id')})")
            results.append({
                "id": item.get('id'),
                "error": "Task type not found in prompt file",
                "status": "skipped"
            })
            continue
            
        template = prompts_map[task_type]
        eval_result = evaluate_single_item(item, template, args.judge_model)
        results.append(eval_result)

    # 4. Calculate Statistics
    valid_scores = [r['score'] for r in results if r.get('status') == 'success' and isinstance(r.get('score'), (int, float))]
    avg_score = sum(valid_scores) / len(valid_scores) if valid_scores else 0

    # 5. Save Results
    output_data = {
        "meta": {
            "judge_model": args.judge_model,
            "total_items": len(data),
            "evaluated_items": len(valid_scores),
            "average_score": round(avg_score, 4)
        },
        "details": results
    }

    with open(args.output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Evaluation complete!")
    print(f"📊 Average Score: {avg_score:.2f} / 5.0")
    print(f"📄 Full detailed results saved to: {args.output_file}")

if __name__ == "__main__":
    main()
