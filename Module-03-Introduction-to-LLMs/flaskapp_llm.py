# Text Generation App
from flask import Flask, request, jsonify
from transformers import AutoModelForCausalLM, AutoTokenizer

app = Flask(__name__)

# Load model and tokenizer
model = AutoModelForCausalLM.from_pretrained("gpt2")
tokenizer = AutoTokenizer.from_pretrained("gpt2")

@app.route("/generate", methods=["POST"])
def generate_text():
    try:
        # Get the prompt from the JSON payload
        prompt = request.json.get("prompt", "")
        if not prompt:
            return jsonify({"error": "Prompt is required."}), 400

        # Tokenize the prompt
        input_ids = tokenizer(prompt, return_tensors="pt").input_ids

        # Generate text using sampling and temperature
        gen_tokens = model.generate(
            input_ids,
            do_sample=True,
            temperature=0.9,
            max_length=100,
        )

        # Decode the generated tokens
        gen_text = tokenizer.batch_decode(gen_tokens, skip_special_tokens=True)[0]

        return jsonify({"generated_text": gen_text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)


# to access
# curl -X POST "http://localhost:5001/generate" -H "Content-Type: application/json" -d '{"prompt": "Once upon a time"}'
