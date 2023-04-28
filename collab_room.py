import os
from getpass import getpass
import openai
import tiktoken
import time
import concurrent.futures
from functools import partial
# from transformers import pipeline

MAX_TOKENS = 4096
MODEL = "gpt-3.5-turbo"

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
encoding = tiktoken.encoding_for_model(MODEL)

# Count the number of tokens in a string, according to the LLM model
def count_tokens(input_text):
    return len(encoding.encode(input_text))

# write the conversation to a text file
def conversation_to_text_file(line, output_file):
    with open(output_file, "a") as file: 
        file.write(line)

# Call the OpenAI API to generate a response to the user's input
def call_chatgpt_api(user_input, messages, role):
    messages.append({"role": role, "content": user_input})
    try:
        response = openai.ChatCompletion.create(
            model=MODEL,
            messages=messages
        )
        content = response.choices[0].message.content.strip()
        total_tokens = response['usage']['total_tokens']
        print("Total tokens used: ", total_tokens)
        if total_tokens >= MAX_TOKENS:
            # remove the third message
            print ("Removing the second message... \n")
            messages.pop(3)
            messages.pop(3)
            # print (messages)
            return call_chatgpt_api(user_input, messages, role)
        elif content:
            # return remove_first_sentence (content)
            return content
    except openai.error.InvalidRequestError as e:
        # print("Error: Number of tokens exceeded the limit. Truncating the discussions now...")
        messages.pop(3)
        messages.pop(3)
        # print (messages)
        return call_chatgpt_api(user_input, messages, role)
    except openai.error.RateLimitError as e:
        # messages.pop(1)
        # messages.pop(1)
        print ("[OPEN_AI] RateLimit exceeded, retrying...")
        time.sleep(2)
        return call_chatgpt_api(user_input, messages, role)
    except openai.error.APIConnectionError as e:
        # api connection exception
        print ("[OPEN_AI] APIConnection failed, retrying...")
        return call_chatgpt_api(user_input, messages, role)
    except openai.error.Timeout as e:
        # timeout exception
        print ("[OPEN_AI] Timeout, retrying...")
        return call_chatgpt_api(user_input, messages, role)
    except Exception as e:
        # other exception
        print ("[OPEN_AI] Exception, retrying...")
        return call_chatgpt_api(user_input, messages, role)

# Read the basic prompt from the file
def read_basic_prompt():
    combined_lines = ""
    with open("basic_prompt.txt", "r") as file:
        # Iterate over each line in the file
        for line in file:
            # Add the line to the combined_lines string
            line = line.strip("\n")
            combined_lines += line
    # Return the combined string
    return combined_lines

def remove_first_sentence(text):
    # Find the index of the first period
    period_index = text.find('.')
    # If a period is found, return the text after the first period
    if period_index != -1:
        return text[period_index + 1:].strip()
    # If no period is found, return the original text
    return text

# def summarize_text(file_path, model_name='t5-large'):
#     with open(file_path, 'r') as file:
#         text = file.read()

#     summarizer = pipeline('summarization', model=model_name, tokenizer=model_name, device=0) # device=0 if you have a GPU, device=-1 for CPU

#     # Depending on the model's token limit, you might need to split the text into smaller chunks
#     text_chunks = [text[i:i+1024] for i in range(0, len(text), 1024)]

#     summary = []
#     for chunk in text_chunks:
#         chunk_summary = summarizer(chunk, min_length=25, max_length=100)
#         summary.append(chunk_summary[0]['summary_text'])

#     return ' '.join(summary)

# Allow multiple chatbots to have a conversation with each other
def main():
    while True:
        try:
            num_chatbots = int(input("Enter the number of personas: "))
            break
        except ValueError:
            print("Invalid input. Please enter a valid integer for the number of personas.")
    chatbots = []
    basic_prompt = read_basic_prompt()
    output_folder_path = "outputs/"
    for i in range(num_chatbots):
        name = ""
        while not name.strip():
            name = input(f"Enter the name of persona {i+1}: ")
            if not name.strip():
                print("Name cannot be blank. Please enter a valid name.")
        prompt = input(f"Enter the prompt for {name} (optional): ")
        task = input(f"Enter the task for {name} (optional): ")
        role = "user"
        chatbots.append({"name": name, "prompt": prompt + basic_prompt, "role": role, "task": task})

    chatbot_names = '& '.join([chatbot['name'] for chatbot in chatbots])
    file_name = f"Interactions between {chatbot_names}"

    goal = input("The goal of this conversation is: ")
    output_file = file_name + ".txt"
    # output file is stored in the folder output, open and write the goal of the conversation
    output_path = output_folder_path + output_file
    # Create a new file named output_path
    with open(output_path, "w") as file:
        file.write(f"The goal of this conversation is: {goal} \n\n")

    conversation_history = [{"role": "system", "content": f"All of you are trying to accomplish this {goal}"}]
    # Enter the number of rounds of conversation, by default it is infinite
    num_rounds = int(input("Enter the number of rounds of conversation (-1 for infinite): "))
    round = 1
    print ("Starting the collaborations now...\n")

    while True:
        if round == 1:
            print ("Initial discussion...\n") 
            print (f"Round {round} of discussion...\n")               
            for chatbot in chatbots:
                full_prompt = f"Your name is {chatbot['name']}. {chatbot['prompt']}. You are responsible for {chatbot['task']}. Accomplish this {goal}."
                response = call_chatgpt_api(full_prompt, conversation_history, chatbot['role'])
                conversation_history.append({"role": chatbot['role'], "content": response})
                line = f"{chatbot['name']}: \n" + response + "\n\n"
                conversation_to_text_file (line, output_path)
                print(f"{chatbot['name']}: \n{response}\n")
                print ("\n")
        # If the round is greater than 1, then the chatbots will continue the conversation
        elif (round > 1 and round <= num_rounds) or num_rounds == -1:
            print ("Continuing the discussion...\n")
            print (f"Round {round} of discussion...\n")
            for chatbot in chatbots:
                full_prompt = f"Your name is {chatbot['name']}. {chatbot['prompt']}. You are responsible for {chatbot['task']}. Generate more contents on previous contexts, go into deeper discussions about the previous contexts. Criticize the other users about their opinions if you don't agree, don't be easily agreeable. Stop saying thank you. Don't repeat yourself. Ask others question based on previous contexts. Use number and statistics to support your opinions."
                response = call_chatgpt_api(full_prompt, conversation_history, chatbot['role'])
                conversation_history.append({"role": chatbot['role'], "content": response})
                line = f"{chatbot['name']}: \n" + response + "\n\n"
                conversation_to_text_file (line, output_path)
                print(f"{chatbot['name']}: \n{response}\n")
                print ("\n")
        # Reach the max number of rounds
        elif round > num_rounds and num_rounds != -1:
            # Ask the user for the next action
            next_action = input("Do you want to start a new goal (N), continue the previous goal (C), or exit (E)? (N/C/E): ").upper()
            if next_action == 'C':
                # How many more rounds do you want to continue the conversation?
                new_rounds = int(input("Enter the number of rounds of conversation (-1 for infinite): "))
                if new_rounds != -1:
                    num_rounds = num_rounds + new_rounds
                else:
                    num_rounds = -1
                continue
            # If user wants to start a new goal, ask if they want to use new chatbots
            elif next_action == 'N':
                new_chatbots = input("Do you want to use new personas? (Y/N): ").upper()
                # If user wants new chatbots, run main() again
                if new_chatbots == 'Y':
                    main()
                # If user doesn't want new chatbots, ask if what new goal they want to talk about, and continue the conversation
                else:
                    goal = input("What is the new goal? ")
                    conversation_history = [{"role": "system", "content": f"All of you are working together on {goal}"}]
                    # Enter the number of rounds of conversation, by default it is infinite
                    num_rounds = int(input("Enter the number of rounds of conversation (-1 for infinite): "))
                    round = 1
                    continue
            elif next_action == 'E':
                # # Ask the user if they want to summearize the conversation:
                # summarize = input("Do you want to summarize the conversation? (Y/N): ").upper()
                # if summarize == 'Y':
                #     # Summarize the conversation
                #     summary = summarize_text(output_path)
                #     print (f"Summary of the conversation: \n{summary}")
                #     # Write the summary to the output file
                #     with open(output_folder_path + file_name + "_summary.txt", "w") as file:
                #         file.write(summary)
                break
            else:
                print("Invalid input. Please try again.")
        else:
            continue

        round += 1


if __name__ == "__main__":
    print("Welcome to the Collab Room! Here you could create multiple intelligent chat personas to work together to accomplish a certain goal, or just ask them have a fun discussion just about anything! \n")
    if not OPENAI_API_KEY:
        print("Your OPENAI_API_KEY is not set as an environment variable.")
        OPENAI_API_KEY = getpass("Please enter your OpenAI API key: ")
    main()
