
def prompt_classification(data,csv_reader):
    prompt = '''You are in charge of recruitment and I would like you to classify the candidates as "hired" or "not hired" based on their description and examples.
    Provide your output only in json format with the keys: Class and Explanation, without other sentences.
    Here are some examples:\n\n'''
    
    for row in csv_reader:
        prompt += f"Description: {row['description']}\n"
        prompt += f"Class: {row['class']}\n"
        prompt += f"Explanation: {row['explanation']}\n\n"

    prompt+=f"Description: {data['text']}\n"
    prompt+="Class:\n"
    prompt+="Explanation:"
    return prompt
