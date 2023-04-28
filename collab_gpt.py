import os
from getpass import getpass
import openai
import tiktoken
import time

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

# Summerize all the conversations in the text file, yet to be implemented
# def summarize_text(output_path):
#     return

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
            # print ("Removing the second message... \n")
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
def read_basic_prompt(language):
    combined_lines = ""
    with open("basic_prompt_" + language + ".txt", "r") as file:
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

# Allow multiple chatbots to have a conversation with each other
def main():
    # while True:
        # Ask if the user want to load template or not
    output_folder_path = "outputs/"
    language = input("Enter the language of for the following discussion English/Chinese): ").lower()
    load_template = input("Do you want to load previous personas template? (y/n): ").upper()
    print ("\n")
    if load_template == "N":
        while True:
            try:
                num_chatbots = int(input("Enter the number of personas: "))
                break
            except ValueError:
                print("Invalid input. Please enter a valid integer for the number of personas.")
        chatbots = []
        basic_prompt = read_basic_prompt(language)
        for i in range(num_chatbots):
            name = ""
            while not name.strip():
                name = input(f"Enter the name of persona {i+1}: ")
                if not name.strip():
                    print("Name cannot be blank. Please enter a valid name.")
            prompt = input(f"Enter the prompt for {name} (optional): ")
            # if there is no period in prompt, add the period to the end of the prompt
            if prompt and prompt[-1] != ".":
                prompt += "."
            task = input(f"Enter the task for {name} (optional): ")
            # if there is no period in task, add the period to the end of the task
            if task and task[-1] != ".":
                task += "."
            role = "user"
            chatbots.append({"name": name, "prompt": prompt + basic_prompt, "role": role, "task": task})
        # save the chatbots as a string to a file
        with open("template.txt", 'w') as file:
            file.write(str(chatbots))
    else:
        with open("template.txt", 'r') as file:
            # Read the contents of the file
            file_contents = file.read()
            # Convert the contents to a Python list using eval()
            chatbots = eval(file_contents)
            # print the chatbots list line by line
            for chatbot in chatbots:
                print("Loaded Persona: " + str(chatbot) + "\n")

    # Ask the user to input a file name
    file_name = input("Enter a file name to save the discussions: ")

    goal = input("The goal of this discussion is: ")
    output_file = file_name + ".txt"
    # output file is stored in the folder output, open and write the goal of the conversation
    output_path = output_folder_path + output_file
    # Create a new file named output_path
    with open(output_path, "w") as file:
        file.write(f"The goal of this discussion is: {goal} \n\n")


    conversation_history = [{"role": "system", "content": f"All of you are trying to accomplish this {goal}"}]
    # Enter the number of rounds of conversation, by default it is infinite
    num_rounds = int(input("Enter the number of rounds of conversation (-1 for infinite): "))
    round = 1
    print ("Starting the discussions now...\n")

    while True:
        if round == 1:
            print ("Initial discussion...\n") 
            print (f"Round {round} of discussion...\n")               
            for chatbot in chatbots:
                # English version of the prompt
                if language == "english":
                    full_prompt = f"Your name is {chatbot['name']}. {chatbot['prompt']} You are responsible for {chatbot['task']} Accomplish this {goal}."
                elif language == "chinese":
                    full_prompt = f"你的名字是 {chatbot['name']}. {chatbot['prompt']}. 你要完成此任务 {chatbot['task']} 并达成此目标 {goal}."
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
            # if round is equal to num_rounds, then the chatbots will end the discussion and summerize their views. 
            if round == num_rounds and num_rounds != -1:
                print ("Ending the discussion...\n")
                for chatbot in chatbots:
                    if language == "english":
                        full_prompt = f"Your name is {chatbot['name']}. {chatbot['prompt']}. Base on previous contexts, summerize your views and you opinions on other users' views."
                    elif language == "chinese":
                        full_prompt = f"你的名字是 {chatbot['name']}. {chatbot['prompt']}. 基于之前的上下文，总结你的观点和总结你对其他用户观点的看法"
                    response = call_chatgpt_api(full_prompt, conversation_history, chatbot['role'])
                    conversation_history.append({"role": chatbot['role'], "content": response})
                    line = f"{chatbot['name']}: \n" + response + "\n\n"
                    conversation_to_text_file (line, output_path)
                    print(f"{chatbot['name']}: \n{response}\n")
                    print ("\n")
            elif round < num_rounds or num_rounds == -1:
                for chatbot in chatbots:
                    if language == "english":
                        full_prompt = f"Your name is {chatbot['name']}. {chatbot['prompt']}. You are responsible for {chatbot['task']} Generate more contents on previous contexts, go into deeper discussions about the previous contexts. Criticize the other users about their opinions if you don't agree, don't be easily agreeable. Stop saying thank you. Don't repeat yourself. Ask others question based on previous contexts. Use number and statistics to support your claims."
                    elif language == "chinese":
                        full_prompt = f"你的名字是 {chatbot['name']}. {chatbot['prompt']}. 你要完成此任务 {chatbot['task']} 基于上下文，生成更多内容并进行深入讨论。批判对方观点，刁难对方，挑战对方。不要轻易同意任何人观点。不要说谢谢。不要重复自己。基于上下文向其它用户提出更多尖锐的问题。使用数字和统计数据支持您的观点。"
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
                    with open(output_path, "a") as file:
                        file.write(f"The goal of this conversation is: {goal} \n\n")
                    num_rounds = int(input("Enter the number of rounds of conversation (-1 for infinite): "))
                    round = 1
                    continue
            elif next_action == 'E':
                # Ask the user if they want to summearize the conversation:
                summarize = input("Do you want to summarize the conversation? (Y/N): ").upper()
                if summarize == 'Y':
                    print ("Yet to be implemented...")
                    # # Summarize the conversation
                    # summary = summarize_text(output_path)
                    # print (f"Summary of the conversation: \n{summary}")
                    # # Write the summary to the output file
                    # with open(output_folder_path + file_name + "_summary.txt", "w") as file:
                    #     file.write(summary)
                break
            else:
                print("Invalid input. Please try again.")
        else:
            continue

        round += 1


if __name__ == "__main__":
    print("\nWelcome to the CollabGPT! Here you could create multiple intelligent chat personas to work together to accomplish a certain goal, or just ask them to have a fun discussion about a given topic! \n")
    if not OPENAI_API_KEY:
        print("Your OPENAI_API_KEY is not set as an environment variable.")
        OPENAI_API_KEY = getpass("Please enter your OpenAI API key: ")
    main()
