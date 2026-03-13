#!/bin/bash

echo "Starting Ollama server..."
ollama serve &
SERVE_PID=$!

echo "Waiting for Ollama server to be active..."
while ! ollama list | grep -q 'NAME'; do
  sleep 1
done

ollama pull mxbai-embed-large
ollama pull qwen3.5:0.8b

wait $SERVE_PID