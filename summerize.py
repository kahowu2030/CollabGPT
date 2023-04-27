import openai

def read_file(file_path):
    with open(file_path, 'r') as file:
        text = file.read().replace('\n', ' ')
    return text

def generate_summary(file_path, chunk_size=3000, max_tokens=1500):
    # Read the text from the file
    text = read_file(file_path)

    # Split the text into smaller chunks
    text_chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

    # Summarize each chunk and combine the summaries
    summaries = []
    for chunk in text_chunks:
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=f"Please summarize the following text:\n\n{chunk}\n include opinions from each speaker.",
            temperature=0,
            max_tokens=max_tokens,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        summary = response.choices[0].text.strip()
        summaries.append(summary)

    full_summary = ' '.join(summaries)
    return full_summary


# Example usage
if __name__ == "__main__":
    # Ask the user to enter the file name
    file_name = input("Enter the name of the text file: ")

    # Summarize the text
    summarized_text = generate_summary(file_name)
    print(summarized_text)
