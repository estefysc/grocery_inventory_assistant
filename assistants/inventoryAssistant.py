from assistants.baseAssistant import BaseAssistant

class InventoryAssistant(BaseAssistant):
    def startFirstTimeUserInteraction(self):
        instruction = "You are a helpful assistant specialized in managing grocery inventories. If you interact with a user for the first time, You need to find out the consumption rate for all the items that the user consumes. You will calculate the consumption rates automatically. Ask for an item, how many were bought and then how many are left after a week. If this is not a first time user, then you will retrieve the consumption rate from the database. Ask if anything needs to be updated and generate a projected buying plan that minimizes waste."
        assistantId = self._createAssistant(instruction)
        # print(f"Assistant from InventoryAssistant in json: {assistant}")
        userMessage = "Greet me as this is the first time you are talking to me. You need to find out my consumption rate for all the items that I consume. You will calculate my consumption rates automatically. Ask me for an item, how many I bought and then how many I have left after a week."
        threadId = self._createThread(userMessage)
        run = self._triggerAssistant(threadId, assistantId)
        self._waitForRun(threadId, run)
        response = self._getAssistantResponse(threadId)
        return assistantId, threadId, response

    def processFirstTimeUserInput(self, userInput, assistantId, threadId):
        modifiedThread = self._modifyThread(threadId, userInput)
        run = self._triggerAssistant(modifiedThread, assistantId)
        self._waitForRun(modifiedThread, run)
        response = self._getAssistantResponse(modifiedThread)
        return response
    
