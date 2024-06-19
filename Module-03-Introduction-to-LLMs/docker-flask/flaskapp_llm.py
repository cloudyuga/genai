from flask import Flask, request, jsonify
from transformers import GPT2LMHeadModel, GPT2Tokenizer

app = Flask(__name__)

model_name = "gpt2"
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPT2LMHeadModel.from_pretrained(model_name)

@app.route("/generate", methods=["POST"])
def generate_text():
    try:
        # Get the prompt from the request JSON
        prompt = request.json.get("prompt", "")

        print(prompt)
        # Tokenize the input prompt
        inputs = tokenizer(prompt, return_tensors="pt")

        print(inputs)
        # Generate text based on the input_ids
        outputs = model.generate(inputs["input_ids"], max_new_tokens=40)

        # Decode the generated output and remove special tokens
        generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

        # Return the generated text as JSON response
        return jsonify({"generated_text": generated_text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)


# to access
# curl -X POST "http://localhost:5001/generate" -H "Content-Type: application/json" -d '{"prompt": "Once upon a time"}'

