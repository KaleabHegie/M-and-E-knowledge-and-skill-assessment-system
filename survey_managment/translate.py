from deep_translator import GoogleTranslator

# below is a way to translate the questions in greeting page
Questions = [
    "What is your name?",
    "How are you doing today?",
    "What can I help you with?"
]

translated_questions = []

target_lang = 'es'

for question in Questions:
    translated_question = GoogleTranslator(target=target_lang).translate(question)
    translated_questions.append(translated_question)

print(translated_questions)