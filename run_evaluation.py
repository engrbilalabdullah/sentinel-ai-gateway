import pandas as pd
import requests
import os

# API ka address jo abhi terminal mein chal raha hai
API_URL = "http://127.0.0.1:5000/analyze"
INPUT_CSV = "data/final_eval.csv"
OUTPUT_CSV = "results/evaluation_results.csv"

def run_eval():
    print("Starting Automated Evaluation...")
    
    # Check karna ke final_eval.csv file maujood hai ya nahi
    if not os.path.exists(INPUT_CSV):
        print(f"Error: {INPUT_CSV} file nahi mili! Pehle dataset banayen.")
        return

    # Data load karna
    df = pd.read_csv(INPUT_CSV)
    
    # Agar dataset khali hai (sirf headings hain)
    if len(df) == 0:
         print("Error: Aapki final_eval.csv file khali hai. Pehle usme ChatGPT se prompts likhwa kar dalein!")
         return

    # Results/ folder banana agar nahi hai
    if not os.path.exists("results"):
        os.makedirs("results")

    results_list = []

    # Ek ek kar ke prompt API ko bhejna
    for index, row in df.iterrows():
        prompt_text = str(row.get('prompt', ''))
        case_id = str(row.get('id', f"case_{index}"))
        
        payload = {"id": case_id, "text": prompt_text}
        
        try:
            # API ko data bhejna aur result lena
            response = requests.post(API_URL, json=payload)
            data = response.json()
            
            # Result ko list mein save karna
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