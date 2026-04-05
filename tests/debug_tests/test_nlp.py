from app.nlp.text_processing import split_sentences, preprocess_sentence

text = "The boy kicked the ball. He ran after it."

sentences = split_sentences(text)

print("Sentences:")
print(sentences)

print("\nTokens:")

for s in sentences:
    print(preprocess_sentence(s))
