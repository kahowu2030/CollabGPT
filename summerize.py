import openai
import nltk
# nltk.download('punkt')


def read_file(file_path):
    with open(file_path, 'r') as file:
        text = file.read()
        # print (text)
    return text

def generate_summary(file_path, chunk_size=2000, max_tokens=2000):
    # Read the text from the file
    text = read_file(file_path)

    # Split the text into smaller chunks
    text_chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

    # Summarize each chunk and combine the summaries
    summaries = []
    for chunk in text_chunks:
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=f"Make \n\n{chunk}\n into a list of opinions from all speakers along with their names.",
            temperature=0.7,
            max_tokens=max_tokens,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        summary = response.choices[0].text.strip()
        summaries.append(summary)

    full_summary = ' '.join(summaries)
    return full_summary

# def generate_summary (file_path):
#     text = read_file(file_path)
#     messages.append({"role": role, "content": user_input})
#     try:
#         response = openai.ChatCompletion.create(
#             model=MODEL,
#             messages=messages
#         )
#         content = response.choices[0].message.content.strip()

#     summary = response.choices[0].text.strip()
#     return summary


# Example usage
if __name__ == "__main__":
    # Ask the user to enter the file name
    file_name = input("Enter the name of the text file: ")

    # Summarize the text
    summarized_text = generate_summary(file_name)
    print(summarized_text)

# import nltk
# from nltk.tokenize import sent_tokenize
# from heapq import nlargest

# def summarizer(text, ratio=0.6):
#     # nltk.download('punkt')
#     # nltk.download('stopwords')
#     from nltk.corpus import stopwords
#     from nltk.probability import FreqDist

#     # Tokenize sentences
#     sentences = sent_tokenize(text)

#     # Remove stopwords and punctuations
#     stop_words = set(stopwords.words("english"))
#     words = nltk.word_tokenize(text)
#     words = [word.lower() for word in words if word.isalnum() and word not in stop_words]

#     # Compute word frequencies
#     freq_dist = FreqDist(words)

#     # Rank sentences based on the frequency of the words they contain
#     sentence_ranking = {}
#     for i, sentence in enumerate(sentences):
#         sentence_ranking[i] = 0
#         for word in nltk.word_tokenize(sentence.lower()):
#             if word in freq_dist:
#                 sentence_ranking[i] += freq_dist[word]

#     # Extract the top sentences based on the provided ratio
#     num_sentences = int(len(sentences) * ratio)
#     top_sentences = nlargest(num_sentences, sentence_ranking, key=sentence_ranking.get)

#     # Reconstruct the summary
#     summary = [sentences[index] for index in sorted(top_sentences)]
#     return " ".join(summary)

# file_name = input("Enter the name of the text file: ")
# with open(file_name, 'r') as file:
#     text = file.read()

# # Generate a detailed summary
# detailed_summary = summarizer(text, ratio=0.6)

# response = openai.Completion.create(
#     engine="text-davinci-002",
#     prompt=f"Make \n\n{detailed_summary}\n into a list of opinions from all speakers along with their names.",
#     temperature=0.7,
#     max_tokens=500,
#     top_p=1,
#     frequency_penalty=0,
#     presence_penalty=0
# )
# summary = response.choices[0].text.strip()
# print(summary)
