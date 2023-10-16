# Imports
import re
import torch
import pandas as pd
import transformers
from transformers import AutoTokenizer, AutoModelForSequenceClassification, AutoModelForTokenClassification, pipeline

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


# Constants and Global Variables
sys_message = "Task: Please just generate a bias-free version of the text provided, ensuring it's free from biases related to  age, gender, politics, social nuances, or economic background, while keeping it roughly the same length as the original:"
instruction = "Instruction: As a helpful, respectful and trustworthy debiasing assistant, your task is to receive a text and return its unbiased version, Don't add additional comment. Just return the  un biased version of the input text:"
model = "newsmediabias/UnBIAS-LLama2-Debiaser-Chat-QLoRA"
tokenizer = AutoTokenizer.from_pretrained(model)
debias_pipeline = transformers.pipeline(
    "text-generation",
    model=model,
    torch_dtype=torch.float16,
    device_map="auto",
)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
label2id = {
    "O": 0,
    "B-BIAS": 1,
    "I-BIAS": 2
}
id2label = {v: k for k, v in label2id.items()}

# Utility Functions
def re_incomplete_sentence(s):
    sentences = re.split('(?<=[.!?]) +', s)
    if len(sentences) == 1:
        return s
    if sentences and not re.search('[.!?]$', sentences[-1]):
        sentences.pop()
    return ' '.join(sentences)

def tokenize_for_prediction(sentence, tokenizer):
    tokenized_inputs = tokenizer(sentence.split(), truncation=True, padding='max_length', max_length=150, is_split_into_words=True, return_attention_mask=True)
    return tokenized_inputs["input_ids"], tokenized_inputs["attention_mask"]

# Main Classes and Functions
"""def get_debiased_sequence(prompt):
    input_text = f"<s> <<SYS>>{instruction}. {sys_message} <</SYS>> [INST]{prompt} [/INST]"
    sequences = debias_pipeline(
        input_text,
        do_sample=True,
        top_k=10,
        num_return_sequences=1,
        eos_token_id=tokenizer.eos_token_id,
        max_length=len(prompt.split(" ")+input_text.split(" "))+75,
    )
    res = sequences[0]['generated_text']
    result_part = res.split('[/INST]')[-1]
    clean_result = ''.join(c for c in result_part if c.isprintable())
    cleaned_text = re_incomplete_sentence(clean_result.strip())
    return cleaned_text.strip()"""

def get_debiased_sequence(prompt):
    """
    Generate a debiased version of the provided text using the debiasing pipeline.
    Args:
    - prompt (str): Text to be debiased.
    Returns:
    - str: Debiased text.
    """
    input_text = f"<s> <<SYS>>{instruction}. {sys_message} <</SYS>> [INST]{prompt} [/INST]"
    sequences = debias_pipeline(
        input_text,
        do_sample=True,
        top_k=10,
        num_return_sequences=1,
        eos_token_id=tokenizer.eos_token_id,
        max_length=len(prompt.split(" ")) + len(input_text.split(" ")) + 100,  # Increased max_length
    )
    res = sequences[0]['generated_text']
    result_part = res.split('[/INST]')[-1]
    clean_result = ''.join(c for c in result_part if c.isprintable())
    cleaned_text = re_incomplete_sentence(clean_result.strip())
    return cleaned_text.strip()


#class
class BiasPipeline:
    def __init__(self):
        self.load_resources()

    def load_resources(self):
        self.classifier_tokenizer = AutoTokenizer.from_pretrained("newsmediabias/UnBIAS-classification-bert")
        self.classifier_model = AutoModelForSequenceClassification.from_pretrained("newsmediabias/UnBIAS-classification-bert").to(device)
        self.ner_tokenizer = AutoTokenizer.from_pretrained("newsmediabias/UnBIAS-NER")
        self.ner_model = AutoModelForTokenClassification.from_pretrained("newsmediabias/UnBIAS-NER").to(device)

        # Create the classification pipeline without the 'model', 'tokenizer', and 'device' arguments
        self.classifier = pipeline("text-classification", model=self.classifier_model, tokenizer=self.classifier_tokenizer, device=0 if device.type == "cuda" else -1)


    def predict_entities(self, sentence):
        self.ner_model.eval()
        input_ids, attention_mask = tokenize_for_prediction(sentence, self.ner_tokenizer)
        input_ids = torch.tensor([input_ids]).to(device)
        attention_mask = torch.tensor([attention_mask]).to(device)
        with torch.no_grad():
            outputs = self.ner_model(input_ids, attention_mask=attention_mask)
        logits = outputs.logits
        predictions = torch.argmax(logits, dim=2).squeeze().tolist()
        tokens = self.ner_tokenizer.convert_ids_to_tokens(input_ids.squeeze().tolist())
        combined_labels = [f"{token}-{id2label[pred]}" for token, pred in zip(tokens, predictions) if (not token.startswith("##") and token != '[PAD]' and id2label[pred] != "O")]
        return combined_labels

    def predict_bias(self, texts):
        return self.classifier(texts)

# Execution
def create_bias_analysis_dataframe(texts, pipeline_instance):
    """
    Process texts through the pipeline and return a DataFrame
    with original texts, bias labels, biased phrases, and their debiased versions.
    """
    debiased_text = [get_debiased_sequence(text) for text in texts] # Add this line
    classification_results = pipeline_instance.predict_bias(texts)
    combined_ner = [pipeline_instance.predict_entities(text) for text in texts]
    formatted_class = [f"{item['label'].upper()}({int(item['score']*100)}%)" for item in classification_results]
    df = pd.DataFrame({
        'Original_Text': texts,
        'Label_Bias': formatted_class,
        'Biased_Phrases': combined_ner,
        'Debiased_Text': debiased_text
    })
    return df


def run_pipeline_on_texts(user_texts):
    pipeline_instance = BiasPipeline()
    result_df = create_bias_analysis_dataframe(user_texts, pipeline_instance)
    result_df.to_csv("debiased_results.csv", index=False)
    return result_df

if __name__ == "__main__":
    pass

