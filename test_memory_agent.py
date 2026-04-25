from agent_with_memory import ai_agent_with_memory

print("AI Agent with Memory(type 'exit' to quit)\n) - test_memory_agent.py:3")

while True:
    user_msg = input("You: ")
    if user_msg.lower() == "exit":
        break
    reply = ai_agent_with_memory(user_msg)
    print("Agent: - test_memory_agent.py:10", reply)