import openai
import os
import time

from abc import ABC, abstractmethod
from openai import OpenAI

api_key = os.environ.get("OPENAI_API_KEY")
 # Defaults to os.environ.get("OPENAI_API_KEY")
client = OpenAI()

class BaseAssistant(ABC):
    def __init__(self, name, model="gpt-4-1106-preview"):
        self.name = name
        self.model = model
        self.tools = [{"type": "code_interpreter"}]

    def _createAssistant(self, instruction):
        assistant = client.beta.assistants.create(
            # name="Grocery Inventory Assistant",
            name = self.name,
            # instructions="You are a helpful assistant specialized in managing grocery inventories. If you interact with a user for the first time, You need to find out the consumption rate for all the items that the user consumes. You will calculate the consumption rates automatically. Ask for an item, how many were bought and then how many are left after a week. If this is not a first time user, then you will retrieve the consumption rate from the database. Ask if anything needs to be updated and generate a projected buying plan that minimizes waste.",
            instructions = instruction,
            tools = self.tools,
            model = self.model
        )
        return assistant

    def _createThread(self, userMessage):
        thread = client.beta.threads.create()
        message = client.beta.threads.messages.create(
            thread_id = thread.id,
            role="user",
            # content="Greet me as this is the first time you are talking to me. You need to find out my consumption rate for all the items that I consume. You will calculate my consumption rates automatically. Ask me for an item, how many I bought and then how many I have left after a week."
            content = userMessage
        )
        return thread.id
    
    def _modifyThread(self, threadId, userMessage):
        message = client.beta.threads.messages.create(
            thread_id = threadId,
            role="user",
            content = userMessage
        )
        return threadId

    def _triggerAssistant(self, threadId, assistantId):
        run = client.beta.threads.runs.create(
        thread_id = threadId,
        assistant_id = assistantId
        )
        return run

    def _waitForRun(self, threadId, run):
        while run.status == "queued" or run.status == "in_progress":
            run = client.beta.threads.runs.retrieve(
            thread_id = threadId,
            run_id = run.id
            )
        time.sleep(0.5)
        return run

    def _getAssistantResponse(self, threadId):
        # Display the Assistant's Response
        messages = client.beta.threads.messages.list(
        thread_id = threadId
        )
        response = messages.data[0].content[0].text.value
        return response

    # def startFirstTimeUserInteraction(self):
    #     instruction = "You are a helpful assistant specialized in managing grocery inventories. If you interact with a user for the first time, You need to find out the consumption rate for all the items that the user consumes. You will calculate the consumption rates automatically. Ask for an item, how many were bought and then how many are left after a week. If this is not a first time user, then you will retrieve the consumption rate from the database. Ask if anything needs to be updated and generate a projected buying plan that minimizes waste."
    #     assistant = self.__createAssistant(instruction)
    #     userMessage = "Greet me as this is the first time you are talking to me. You need to find out my consumption rate for all the items that I consume. You will calculate my consumption rates automatically. Ask me for an item, how many I bought and then how many I have left after a week."
    #     threadId = self.__createThread(userMessage)
    #     run = self.__triggerAssistant(threadId, assistant.id)
    #     self.__waitForRun(threadId, run)
    #     response = self.__getAssistantResponse(threadId)
    #     return assistant.id, threadId, response

    # def processFirstTimeUserInput(self, userInput, assistantId, threadId):
    #     modifiedThread = self.__modifyThread(threadId, userInput)
    #     run = self.__triggerAssistant(modifiedThread, assistantId)
    #     self.__waitForRun(modifiedThread, run)
    #     response = self.__getAssistantResponse(modifiedThread)
    #     return response