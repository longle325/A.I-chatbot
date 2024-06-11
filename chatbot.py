import torch
from transformers import AutoConfig, AutoModelForCausalLM, AutoTokenizer
class ChatBot:
    """
    A class to represent a conversational AI chatbot.

    Attributes
    ----------
    model_path : str
        Path to the pre-trained language model.
    device : str
        The device to run the model on (default is "cuda:1").
    config : AutoConfig
        Configuration for the pre-trained model.
    model : AutoModelForCausalLM
        The pre-trained language model for causal language modeling.
    tokenizer : AutoTokenizer
        The tokenizer for processing input and output text.
    prompt_template : str
        Template for formatting input instructions to the model.

    Methods
    -------
    __init__(model_path, device="cuda:1", torch_dtype=torch.bfloat16):
        Initializes the ChatBot with the specified model path, device, and data type.
    
    generate_response(instruction):
        Generates a response from the chatbot based on the given instruction.
    """

    def __init__(self, model_path, device="cuda:1", torch_dtype=torch.bfloat16):
        """
        Initializes the ChatBot with the specified model path, device, and data type.

        Parameters
        ----------
        model_path : str
            Path to the pre-trained language model.
        device : str, optional
            The device to run the model on (default is "cuda:1").
        torch_dtype : torch.dtype, optional
            The data type for the model's tensors (default is torch.bfloat16).
        """
        self.model_path = model_path
        self.device = device
        self.config = AutoConfig.from_pretrained(model_path, trust_remote_code=True)
        self.config.init_device = device

        self.model = AutoModelForCausalLM.from_pretrained(model_path, config=self.config, torch_dtype=torch_dtype, trust_remote_code=True)
        self.model.eval()

        self.tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
        self.prompt_template = "### Câu hỏi: {instruction}\n### Trả lời:"

    def generate_response(self, instruction):
        """
        Generates a response from the chatbot based on the given instruction.

        Parameters
        ----------
        instruction : str
            The input instruction or question from the user.

        Returns
        -------
        str
            The generated response from the chatbot.
        """
        
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
