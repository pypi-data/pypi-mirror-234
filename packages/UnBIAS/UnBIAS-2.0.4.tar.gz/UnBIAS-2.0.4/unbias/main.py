import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification, AutoModelForTokenClassification, AutoModelForCausalLM,pipeline
import torch
import os

device = torch.device("cpu")

class BiasPipeline:
    def __init__(self):
        def load_model_and_tokenizer(model_class, tokenizer_class, pretrained_name, save_name, custom_path=None):
            base_dir = custom_path if custom_path else "./default_directory"
            model_dir = os.path.join(base_dir, save_name)
            model_file = os.path.join(model_dir, "pytorch_model.bin")

            if os.path.exists(model_file):
                print(f"Loading {save_name} from local")
                model = model_class.from_pretrained(model_dir)
                tokenizer = tokenizer_class.from_pretrained(model_dir)
            else:
                print(f"Loading {pretrained_name} from HuggingFace")
                model = model_class.from_pretrained(pretrained_name)
                tokenizer = tokenizer_class.from_pretrained(pretrained_name)
                model.save_pretrained(model_dir)
                tokenizer.save_pretrained(model_dir)
            return model, tokenizer

        self.classifier_model, self.classifier_tokenizer = load_model_and_tokenizer(
            AutoModelForSequenceClassification,
            AutoTokenizer,
            "newsmediabias/UnBIAS-classification-bert",
            "classifier_model",
            custom_path="/content/ShainaRaza/"
        )
        self.classifier_model.to(device)

        self.ner_model, self.ner_tokenizer = load_model_and_tokenizer(
            AutoModelForTokenClassification,
            AutoTokenizer,
            "newsmediabias/UnBIAS-Named-Entity-Recognition",
            "ner_model",
            custom_path="/content/ShainaRaza/"
        )
        self.ner_model.to(device)

        self.debiaser_model, self.debiaser_tokenizer = load_model_and_tokenizer(
            AutoModelForCausalLM,
            AutoTokenizer,
            "newsmediabias/UnBIAS-LLama2-Debiaser-Chat",
            "debiaser_model",
            custom_path="/content/ShainaRaza/"
        )
        self.debiaser_model.to(device)

    def classify_news_bias_batch(self, texts):
        inputs = self.classifier_tokenizer(texts, return_tensors="pt", truncation=True, max_length=512, padding='max_length')
        with torch.no_grad():
            logits = self.classifier_model(**inputs).logits
        predicted_class_idxs = torch.argmax(logits, dim=1).tolist()
        descriptive_labels = [self.classifier_model.config.id2label[idx] for idx in predicted_class_idxs]
        return descriptive_labels

    def predict_entities(self, sentence):
        tokens = self.ner_tokenizer.tokenize(self.ner_tokenizer.decode(self.ner_tokenizer.encode(sentence)))
        inputs = self.ner_tokenizer.encode(sentence, return_tensors="pt")
        inputs = inputs.to(device)

        outputs = self.ner_model(inputs).logits
        predictions = torch.argmax(outputs, dim=2)
        id2label = self.ner_model.config.id2label

        # Reconstruct words from subword tokens
        biased_words = []
        current_word = ""
        for token, prediction in zip(tokens, predictions[0]):
            label = id2label[prediction.item()]
            if label in ['B-BIAS', 'I-BIAS']:
                if token.startswith('##'):
                    current_word += token[2:]
                else:
                    if current_word:
                        biased_words.append(current_word)
                    current_word = token
        if current_word:
            biased_words.append(current_word)

        # Filter out special tokens and subword tokens
        biased_words = [word for word in biased_words if not word.startswith('[') and not word.endswith(']') and not word.startswith('##')]
        return biased_words

    def debias_text(self, text):
        instruction = "Debias this text:"
        system_message = ("You are a text debiasing bot, you take as input a text and you output "
                          "its debiased version by rephrasing it to be free from any age, gender, "
                          "political, social or socio-economic biases, without any extra outputs")

        pipe = pipeline(
            task="text-generation",
            model=self.debiaser_model,
            tokenizer=self.debiaser_tokenizer,
            max_length=500
        )

        debiased_output = pipe(f"<s>[INST] <<SYS>>{system_message}<</SYS>> {instruction} {text} [/INST]")
        debiased_text = debiased_output[0]['generated_text'].split('\n')[3].strip('"')
        return debiased_text

    def results_to_dataframe(self, texts, classification_results, ner_results, debiased_texts):
        data = {
            'Original Text': texts,
            'Classification Label': classification_results,
            'Biased Phrases': [", ".join(phrase_list) for phrase_list in ner_results],
            'Debiased Text': debiased_texts
        }
        df = pd.DataFrame(data)
        return df

    def process(self, texts):
        classification_results = self.classify_news_bias_batch(texts)
        ner_results = [self.predict_entities(text) for text in texts]
        debiased_texts = [self.debias_text(text) for text in texts]
        return classification_results, ner_results, debiased_texts


# Usage
if __name__ == '__main__':
    pipeline_instance = BiasPipeline()
    texts = [
        "Women are just too emotional to be leaders.",
        "All young people are lazy and addicted to their phones.",
        "People from that country are always dishonest and corrupt.",
        "Men are inherently better at science and math than women.",
        "The elderly are just burdens to society; they contribute nothing.",
        "All poor people are lazy and don't want to work.",
        "People who follow that religion are all terrorists.",
        "Immigrants are taking all our jobs and ruining the country."
    ]

    classification_results, ner_results, debiased_texts = pipeline_instance.process(texts)

    # Convert results to a DataFrame
    df = pipeline_instance.results_to_dataframe(texts, classification_results, ner_results, debiased_texts)

    # Print the DataFrame
    print(df.head())

    # Save the DataFrame to a CSV file
    df.to_csv("debiased_results.csv", index=False)
