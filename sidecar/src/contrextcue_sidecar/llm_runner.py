import subprocess

LLAMA_CPP_PATH = "./llama.cpp/main"    # adjust path to your llama.cpp binary
MODEL_PATH = "./models/rene.gguf"      # adjust to your quantized model file
DEFAULT_TEMP = 0.7
DEFAULT_TOKENS = 256

def rewrite_text(prompt: str, input_text: str) -> str:
    full_prompt = f"{prompt.strip()}\n\n{input_text.strip()}"
    try:
        result = subprocess.run(
            [
                LLAMA_CPP_PATH,
                "-m", MODEL_PATH,
                "-p", full_prompt,
                "--temp", str(DEFAULT_TEMP),
                "--n-predict", str(DEFAULT_TOKENS),
                "--silent-prompt"
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
            text=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"[LLM Error] {e.stderr.strip()}"
