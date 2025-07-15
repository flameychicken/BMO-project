from llama_cpp import Llama

llm = Llama(
    model_path="models/llama-model.gguf",
    n_ctx=2048,
)

def get_response(user_input: str) -> str:
    # Use the chat format expected by Mistral
    prompt = f"<s>[INST] {user_input.strip()} [/INST]"

    try:
        result = llm(prompt, max_tokens=100, stop=["</s>"])
        output = result["choices"][0]["text"].strip()

        # Avoid weird empty responses
        if not output or output.lower() in ["please?", "uh...", ""]:
            return "Sorry, I didn't catch that. Could you repeat the question?"
        
        return output

    except Exception as e:
        print(f"❌ LLM error: {e}")
        return "There was an error generating a response."
