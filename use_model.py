import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

model_name = "VietAI/gpt-neo-1.3B-vietnamese-news"
peft_model_id = "./fine_tuned_gpt2_model_final"

tokenizer = AutoTokenizer.from_pretrained(peft_model_id)
model = AutoModelForCausalLM.from_pretrained(model_name)
model = PeftModel.from_pretrained(model, peft_model_id)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)


def generate_response(prompt, max_length=500):
    input_text = f"Người dùng: {prompt}"
    input_ids = tokenizer.encode(input_text, return_tensors="pt").to(device)

    with torch.no_grad():
        output = model.generate(
            input_ids,
            max_length=max_length,
            temperature=0.7,
            top_p=0.9,
            pad_token_id=tokenizer.eos_token_id
        )

    response = tokenizer.decode(output[0], skip_special_tokens=True)
    if "Chatbot:" in response:
        response = response.split("Chatbot:")[1].strip()
    else:
        response = response.strip()
    return response

while True:
    question = input()
    if question == "stop":
        break
    answer = generate_response(question)
    print(answer)
