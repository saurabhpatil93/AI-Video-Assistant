# 🎥 AI Video Assistant

AI Video Assistant is an AI-powered application that converts YouTube videos and local audio/video files into **transcripts, summaries, action items, key decisions, open questions, and interactive Q&A**.

It uses **Whisper for transcription, Ollama with Llama 3.2 for AI processing, Nomic Embed Text for embeddings, ChromaDB for vector storage, LangChain for RAG, and Streamlit for the web interface.**

---

## 🚀 Features

- 🎙️ Video/Audio to Text using Whisper
- 📝 Automatic video/meeting summarization
- 🏷️ Automatic title generation
- ✅ Action item extraction
- 🔑 Key decision extraction
- ❓ Open question extraction
- 💬 RAG-based conversational Q&A
- 🔎 Semantic search over transcripts
- 🧠 Local LLM processing using Ollama
- 🗄️ ChromaDB vector database
- 🌐 Interactive Streamlit UI
- ▶️ Supports YouTube URLs and local media files
- 🌍 English and Hinglish transcription support

---

# 🏗️ Architecture

```text
                         ┌──────────────────────┐
                         │      USER INPUT      │
                         │                      │
                         │ YouTube URL / File   │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │   Audio Processor    │
                         │                      │
                         │ yt-dlp / FFmpeg      │
                         │ Pydub                │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │       Whisper        │
                         │                      │
                         │    Speech → Text     │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │      Transcript      │
                         └──────────┬───────────┘
                                    │
                ┌───────────────────┼───────────────────┐
                │                   │                   │
                ▼                   ▼                   ▼
       ┌────────────────┐  ┌────────────────┐  ┌─────────────────┐
       │  Summarizer    │  │   Extractor    │  │  RAG Pipeline   │
       │                │  │                │  │                 │
       │ Title          │  │ Action Items   │  │ Text Splitting  │
       │ Summary        │  │ Decisions      │  │ Embeddings      │
       │                │  │ Questions      │  │ Retrieval       │
       └────────────────┘  └────────────────┘  └───────┬─────────┘
                                                        │
                                                        ▼
                                               ┌─────────────────┐
                                               │    ChromaDB     │
                                               │  Vector Store   │
                                               └───────┬─────────┘
                                                       │
                                                       ▼
                                               ┌─────────────────┐
                                               │    Retriever    │
                                               └───────┬─────────┘
                                                       │
                                                       ▼
                                               ┌─────────────────┐
                                               │     Ollama      │
                                               │    Llama 3.2    │
                                               └───────┬─────────┘
                                                       │
                                                       ▼
                                               ┌─────────────────┐
                                               │   AI Response   │
                                               └─────────────────┘



