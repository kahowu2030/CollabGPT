
# Collab Room
Collab Room is a Python program that allows you to create multiple intelligent chat personas using OpenAI's GPT-3.5-turbo model to work together to accomplish a certain goal or have a fun discussion about anything!

## Features
- Generate multiple intelligent chat personas using OpenAI's GPT-3.5-turbo model and let them work together to accomplish a defined goal.
- Set custom prompts and tasks for each persona.
- Save all the generated inputs to a text file in the outputs folder.
- Generate a summary of all the inputs using OpenAI's text-davinci-002 model.

## Note
This program makes use of OpenAI's API, and you may incur costs depending on your usage. Please be aware of the token limits and the API rate limits to avoid unexpected costs.

## Prerequisites
- Python 3.6 or higher
- OpenAI API Key

## Usage
- Run the python file as follow:
```bash
python collab_room.py
```


- Set OpenAI Key
```bash
export OPENAI_API_KEY=your-api-key
```
Alternatively, you can provide the API key when prompted by the script.

- Follow the prompts to set up your chat personas, their prompts, tasks, and the goal of the conversation.
- Specify the number of rounds of conversation you would like to have, or enter -1 for infinite rounds.
- Watch the personas collaborate and generate conversations based on their tasks and the defined goal. 
- At the end of the conversation, you can choose to continue the previous goal, start a new goal, or exit the program. If desired, you can also generate a summary of the conversation.

## License
This project is licensed under the MIT License.
