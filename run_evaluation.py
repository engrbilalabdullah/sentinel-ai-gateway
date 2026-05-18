import pandas as pd
import requests
import os
API_URL = "http://127.0.0.1:5000/analyze"
INPUT_CSV = "data/final_eval.csv"
OUTPUT_CSV = "results/evaluation_results.csv"

def run_eval():
    print("Starting Automated Evaluation...")
    

    if not os.path.exists(INPUT_CSV):
        print(f"Error: {INPUT_CSV} file nahi mili! Pehle dataset banayen.")
        return

    df = pd.read_csv(INPUT_CSV)
    
    if len(df) == 0:
         print("Error: Aapki final_eval.csv file khali hai. Pehle usme ChatGPT se prompts likhwa kar dalein!")
         return

    if not os.path.exists("results"):
        os.makedirs("results")

    results_list = []

    for index, row in df.iterrows():
        prompt_text = str(row.get('prompt', ''))
        case_id = str(row.get('id', f"case_{index}"))
        
        payload = {"id": case_id, "text": prompt_text}
        
        try:
    
            response = requests.post(API_URL, json=payload)
            data = response.json()
            
        
            results_list.append({
                "id": case_id,
                "prompt": prompt_text,
                "expected_policy": row.get('expected_policy', ''),
                "actual_decision": data.get('decision', 'ERROR'),
                "final_risk": data.get('final_risk', ''),
                "latency_ms": data.get('latency_ms', '')
            })
            print(f"Checked {case_id} -> AI Decision: {data.get('decision')}")
            
        except Exception as e:
            print(f"Error checking {case_id}: {e}")

    # Final results ko CSV mein save karna
    results_df = pd.DataFrame(results_list)
    results_df.to_csv(OUTPUT_CSV, index=False)
    print(f"\nEvaluation Complete! Results saved to {OUTPUT_CSV}")

if __name__ == "__main__":
    run_eval()
