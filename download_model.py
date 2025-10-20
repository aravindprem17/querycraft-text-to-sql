import os
from huggingface_hub import hf_hub_download

# Define the model name and the specific GGUF file
MODEL_REPO = "TheBloke/sqlcoder-7B-GGUF"
MODEL_FILE = "sqlcoder-7b.Q4_K_M.gguf"
MODEL_PATH = "models"

def download_model():
    """
    Downloads the GGUF model from Hugging Face Hub.
    """
    # Ensure the target directory exists
    if not os.path.exists(MODEL_PATH):
        os.makedirs(MODEL_PATH)
        print(f"Created directory: {MODEL_PATH}")

    model_file_path = os.path.join(MODEL_PATH, MODEL_FILE)

    if os.path.exists(model_file_path):
        print(f"Model file already exists: {model_file_path}")
        return

    print(f"Downloading model '{MODEL_FILE}' from '{MODEL_REPO}'...")
    
    try:
        hf_hub_download(
            repo_id=MODEL_REPO,
            filename=MODEL_FILE,
            local_dir=MODEL_PATH,
            local_dir_use_symlinks=False
        )
        print("Download complete.")
        print(f"Model saved to: {model_file_path}")
    except Exception as e:
        print(f"An error occurred during download: {e}")

if __name__ == "__main__":
    download_model()
