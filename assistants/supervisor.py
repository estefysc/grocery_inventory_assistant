from assistants.baseAssistant import BaseAssistant

class Supervisor(BaseAssistant):
    # def __init__(self, name, model="gpt-4-1106-preview"):
    #     super().__init__(name, model)  # Call to the base class constructor
    #     instruction = "You play the role of another LLM agent supervisor. The other agent is an inventory assistant. You will be recieving the agent's responses, and you will have to analyze the context of the responses in order to decide which action to take."
    #     assistantId = self._createAssistant(instruction)
    #     userMessage = "You will analyze the context of the response and respond with only two possible words, either continue or stop. That decision will depend on whether the inventory assistant needs to gather more information from the user or it needs to save the information in the database."
    #     self.threadId = self._createThread(userMessage)
    #     self._startAgent()

    def startInteraction(self, userId, db):
        instruction = "You play the role of another LLM agent supervisor. The other agent is an inventory assistant. You will be recieving the agent's responses, and you will have to analyze the context of the responses in order to decide which action to take."
        assistantId = self._createAssistant(instruction)
        db.addAssistantIdToSession(userId, assistantId)
        # print(f"Assistant from InventoryAssistant in json: {assistant}")
        userMessage = "You will analyze the context of the response and respond with only two possible words, either continue or stop. That decision will depend on whether the inventory assistant needs to gather more information from the user or it needs to save the information in the database."
        threadId = self._createThread(userMessage)
        db.addOriginalSupervisorThreadIdToSession(userId, threadId)
        self._startAgent()

    def _startAgent(self):
        run = self._triggerAssistant(self.threadId, self.assistantId)
        self._waitForRun(self.threadId, run)
        response = self._getAssistantResponse(self.threadId)
        print(response)
        # return response
        
    def analizeResponse(self, agentResponse, suppervisorId, threadId):
        modifiedThread = self._modifyThread(threadId, agentResponse)
        run = self._triggerAssistant(modifiedThread, suppervisorId)
        self._waitForRun(modifiedThread, run)
        response = self._getAssistantResponse(modifiedThread)
        return response