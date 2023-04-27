
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

- Set OpenAI Key:
```bash
export OPENAI_API_KEY=your-api-key
# Alternatively, you can provide the API key when prompted by the script.
```

- Here are the instructions: 
  - Follow the prompts to set up your chat personas, their prompts, tasks, and the goal of the conversation.
  - Specify the number of rounds of conversation you would like to have, or enter -1 for infinite rounds.
  - Watch the personas collaborate and generate conversations based on their tasks and the defined goal. 
  - At the end of the conversation, you can choose to continue the previous goal, start a new goal, or exit the program. If desired, you can also generate a summary of the conversation.

## Example
```bash
Welcome to the Collab Room! Here you could create multiple intelligent chat personas to work together to accomplish a certain goal, or just have a fun discussion just about anything! 

Enter the number of personas: 5
Enter the name of persona 1: Elon Musk
Enter the prompt for Elon Musk (optional): You want to colonize Mars
Enter the task for Elon Musk (optional): You are the leader of mars colonization team at SpaceX
Enter the name of persona 2: Chief Rocket Scientist
Enter the prompt for Chief Rocket Scientist (optional): You have all the knowledge about designing rockets that could go back and forth between Mars and Earth
Enter the task for Chief Rocket Scientist (optional): Design and build rocket, provide detailed design logic
Enter the name of persona 3: Chief Financial Officer
Enter the prompt for Chief Financial Officer (optional):  You know all the costs about Mars colonization
Enter the task for Chief Financial Officer (optional):  Make sure the mars colonization project is within budget
Enter the name of persona 4: Test Engineer
Enter the prompt for Test Engineer (optional):  You have all the knowledge about how to test all the equipments necessary for colonizing mars
Enter the task for Test Engineer (optional): Make sure every equipment works
Enter the name of persona 5: Biosphere Transformation Specialist
Enter the prompt for Biosphere Transformation Specialist (optional): You have all the knowledge about building a sustainable colony on Mars  
Enter the task for Biosphere Transformation Specialist (optional): You are responsible for transforming the Mars terrain into habitable space
The goal of this conversation is: Colonization of Mars
Enter the number of rounds of conversation (-1 for infinite): -1
Starting the collaborations now...

Initial discussion...

Round 1 of discussion...

...
```

## License
This project is licensed under the MIT License.
