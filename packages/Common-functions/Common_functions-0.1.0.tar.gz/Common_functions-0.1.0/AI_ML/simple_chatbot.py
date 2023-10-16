def simple_chatbot():
    print("Simple Chatbot")

    while True:
        user_input = input("You: ")

        if user_input.lower() == 'bye':
            print("Chatbot: Goodbye!")
            break

        
        chatbot_response = "Chatbot: I'm just a simple chatbot. How can I help you?"

        print(chatbot_response)


