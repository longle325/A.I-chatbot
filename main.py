import torch
from transformers import AutoConfig, AutoModelForCausalLM, AutoTokenizer

class ChatBot:
    def __init__(self, model_path, device="cuda:3", torch_dtype=torch.bfloat16):
        self.model_path = model_path
        self.device = device
        self.config = AutoConfig.from_pretrained(model_path, trust_remote_code=True)
        self.config.init_device = device

        self.model = AutoModelForCausalLM.from_pretrained(model_path, config=self.config, torch_dtype=torch_dtype, trust_remote_code=True)
        self.model.eval()

        self.tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
        self.prompt_template = "### Câu hỏi: {instruction}\n### Trả lời:"

    def generate_response(self, instruction):
        input_prompt = self.prompt_template.format(instruction=instruction)
        input_ids = self.tokenizer(input_prompt, return_tensors="pt")

        outputs = self.model.generate(
            inputs=input_ids["input_ids"].to(self.device),
            attention_mask=input_ids["attention_mask"].to(self.device),
            do_sample=True,
            temperature=1.0,
            top_k=50,
            top_p=0.9,
            max_new_tokens=1024,
            eos_token_id=self.tokenizer.eos_token_id,
            pad_token_id=self.tokenizer.pad_token_id
        )

        response = self.tokenizer.batch_decode(outputs, skip_special_tokens=True)[0]
        response = response.split("### Trả lời:")[1]
        return response.strip()

    def chat(self):
        while True:
            print("User: ",end= "")
            instruction = input()
            if instruction.strip() == "/stop": exit()
            response = self.generate_response(instruction)
            print(f"\nBot: {response}\n")
if __name__ == "__main__":
    model_path = "vinai/PhoGPT-4B-Chat"
    bot = ChatBot(model_path)
    bot.chat()
