import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import time
from tools.tools import load_training_data, add_to_training_data
from bot import SimpleSpacyBot


    


if __name__ == "__main__":
    time.sleep(5)
    bot = SimpleSpacyBot()
    training_data = load_training_data("training_data.txt")
    bot.train(training_data)

    while True:
        user_message = input("Você: ")
        if user_message.lower() in ["sair", "exit"]:
            print("Bot: Até logo!")
            break
        response = bot.respond(user_message)
        print(f"Bot: {response}")
