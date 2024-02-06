import streamlit as st

from app import Chatbot




if "chatbot" not in st.session_state:
    st.session_state.chatbot = None

def initialize_bot(api_key):
    if st.session_state.chatbot is None:
        st.session_state.chatbot = Chatbot(api_key)
    pass

def reinit_bot():
    st.session_state.chatbot = None



def handle_chat_input(prompt):
    if prompt == 'Lucas':
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("assistant"):
            response = "Ama mucho a Joaqui"
            st.markdown(response)
    else:
        if st.session_state.chatbot is None:
            st.markdown("Debes insertar tu api key para usar el bot")
            return
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("assistant"):
            response = st.session_state.chatbot.ask_question(prompt)
            st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})



def print_all_messages(messages):
    for message in messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

def main():
    st.header("Soy MarxGPT")

    if "messages" not in st.session_state:
        st.session_state.messages = []
    with st.sidebar:

        input_text = st.text_input("Ingresa tu api key de OpenAI:")
        if st.button("Enviar"):
            initialize_bot(input_text)
            
        
        if st.button("Reiniciar bot"):
            reinit_bot()
        
    
    print_all_messages(st.session_state.messages)
    if st.session_state.chatbot is not None and st.session_state.chatbot.is_inicialized:
        prompt = st.chat_input("Preguntame acerca del manifiesto comunista")
        if prompt:
            handle_chat_input(prompt)


if __name__ == "__main__":
    main()