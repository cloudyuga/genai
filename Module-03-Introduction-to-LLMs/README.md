# 🦙 How to Run Ollama Locally

Ollama is a tool that lets you run AI models like LLaMA on your computer – **no internet or cloud required**!

---

## ✅ Step 1: Install Ollama

### For Windows, macOS, or Linux:

##### On Windows use the following link:

https://ollama.com/download/windows

Download OllamaSetup.exe and install Ollama

##### For macOS use the following link

https://ollama.com/download/mac

Download Ollama-darwin.zip file to install Ollama

##### For Linux machine,

Open your terminal and run:

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

## ✅ Step 2: Start the Ollama Service

After installation, run the following command from terminal:
```
ollama serve
```
This starts the Ollama backend service on your machine.

## ✅ Step 3: Pull a Model

For example, to download and use the llama2 model:

```
ollama pull llama2
```
You only need to do this once. It downloads the model to your machine.

## ✅ Step 4: Chat with the Model

Now run the model:
```
ollama run llama2
```
Start chatting with the AI right in your terminal!


#  ✅ API call

Example using curl:

curl -X POST http://localhost:11434/api/generate -d '{
  "model": "llama2",
  "prompt":"Why is the sky blue?"
 }'

 Our ollama is running at http://localhost:11434

# 🚀 Popular Models You Can Use

- llama4
- llama3
- mistral
- gemma
- codellama
- phi
- orca-mini
  
Check more at: https://ollama.com/library
