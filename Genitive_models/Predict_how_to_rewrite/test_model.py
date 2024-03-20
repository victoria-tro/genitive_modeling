import pickle

# Load model and vectorizer
print("\nLOADING MODEL AND VECTORIZER ...")
with open('models/finalized_model.pkl', 'rb') as loaded_model_file:
    model = pickle.load(loaded_model_file)

with open('models/vectorizer.pkl', 'rb') as loaded_vect_file:
    vect = pickle.load(loaded_vect_file)


# Test model on a single sentence
print("TESTING ...\n")
my_sent = ["EUs nye regler"]
print("Tested the phrase:", my_sent)
my_sent = vect.transform(my_sent)
predicted = model.predict(my_sent)
probability = model.predict_proba(my_sent)
print("I predict the category:", predicted)
print("My class predictions on this sentence", probability)
print("Explanation of categories: -s = 0, sine = 1, preposisjon = 2, sammenkrivning = 3, omskriving = 4\n")
