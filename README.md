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
                         ┌─────────────────────────┐
                         │       USER INPUT        │
                         │                         │
                         │ YouTube URL / Audio /   │
                         │ Video File              │
                         └────────────┬────────────┘
                                      │
                                      ▼
                         ┌─────────────────────────┐
                         │    AUDIO PROCESSOR      │
                         │                         │
                         │ yt-dlp                  │
                         │ FFmpeg                  │
                         │ Pydub                   │
                         └────────────┬────────────┘
                                      │
                                      ▼
                         ┌─────────────────────────┐
                         │        WHISPER          │
                         │                         │
                         │     Speech → Text       │
                         └────────────┬────────────┘
                                      │
                                      ▼
                         ┌─────────────────────────┐
                         │       TRANSCRIPT        │
                         └────────────┬────────────┘
                                      │
                  ┌───────────────────┼───────────────────┐
                  │                   │                   │
                  ▼                   ▼                   ▼
        ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
        │   SUMMARIZER    │ │    EXTRACTOR    │ │  RAG PIPELINE   │
        │                 │ │                 │ │                 │
        │ Title           │ │ Action Items    │ │ Text Splitting  │
        │ Summary         │ │ Key Decisions   │ │ Embeddings      │
        │                 │ │ Open Questions  │ │ Retrieval       │
        └─────────────────┘ └─────────────────┘ └────────┬────────┘
                                                         │
                                                         ▼
                                                ┌─────────────────┐
                                                │    ChromaDB     │
                                                │  Vector Store   │
                                                └────────┬────────┘
                                                         │
                                                         ▼
                                                ┌─────────────────┐
                                                │    Retriever    │
                                                └────────┬────────┘
                                                         │
                                                         ▼
                                                ┌─────────────────┐
                                                │     Ollama      │
                                                │    Llama 3.2    │
                                                └────────┬────────┘
                                                         │
                                                         ▼
                                                ┌─────────────────┐
                                                │   AI RESPONSE   │
                                                └─────────────────┘
```

---

#

---

# 📁 Project Structure

```text
AI-Video-Assistant/
│
├── app.py
├── main.py
├── requirements.txt
├── README.md
│
├── core/
│   ├── __init__.py
│   ├── transcriber.py
│   ├── summarizer.py
│   ├── extractor.py
│   ├── vector_store.py
│   └── rag_engine.py
│
├── utilities/
│   ├── __init__.py
│   └── audio_processor.py
│
├── vector_db/
│
└── audio_chunks/
```

# ⚙️ How Does AI Video Assistant Work?

AI Video Assistant works as an end-to-end pipeline that converts unstructured
video/audio content into structured information and allows users to interact
with that information using natural language.

The system can process:

- YouTube videos
- Local video files
- Local audio files

The complete pipeline consists of multiple stages:

```text
Input
  ↓
Audio Processing
  ↓
Audio Chunking
  ↓
Speech-to-Text
  ↓
Transcript
  ↓
AI Analysis
  ↓
Embedding Generation
  ↓
Vector Database
  ↓
Retrieval
  ↓
LLM
  ↓
Context-Aware Answer
```

---

# 🔄 Complete Project Workflow

```text
┌───────────────────────────────────────────────────────────┐
│                     1. USER INPUT                         │
│                                                           │
│              YouTube URL / Video / Audio                 │
└───────────────────────────┬───────────────────────────────┘
                            │
                            ▼
┌───────────────────────────────────────────────────────────┐
│                  2. AUDIO PROCESSING                      │
│                                                           │
│              yt-dlp + FFmpeg + Pydub                     │
│                                                           │
│       Download / Extract / Convert / Process Audio       │
└───────────────────────────┬───────────────────────────────┘
                            │
                            ▼
┌───────────────────────────────────────────────────────────┐
│                    3. AUDIO CHUNKING                      │
│                                                           │
│              Large Audio → Small Chunks                   │
└───────────────────────────┬───────────────────────────────┘
                            │
                            ▼
┌───────────────────────────────────────────────────────────┐
│                  4. WHISPER TRANSCRIPTION                 │
│                                                           │
│                  Speech → Text                            │
└───────────────────────────┬───────────────────────────────┘
                            │
                            ▼
┌───────────────────────────────────────────────────────────┐
│                     5. TRANSCRIPT                         │
│                                                           │
│              Complete Text of the Video                  │
└───────────────────────────┬───────────────────────────────┘
                            │
              ┌─────────────┼──────────────┐
              │             │              │
              ▼             ▼              ▼
       ┌────────────┐ ┌────────────┐ ┌───────────────┐
       │   TITLE    │ │  SUMMARY   │ │   EXTRACTION  │
       └────────────┘ └────────────┘ └───────┬───────┘
                                             │
                                    ┌────────┼────────┐
                                    │        │        │
                                    ▼        ▼        ▼
                                Actions  Decisions  Questions
                                             │
                                             ▼
                                  ┌────────────────────┐
                                  │    6. RAG SYSTEM   │
                                  └──────────┬─────────┘
                                             │
                                             ▼
                                  Transcript Chunking
                                             │
                                             ▼
                                  Nomic Embeddings
                                             │
                                             ▼
                                         ChromaDB
                                             │
                                             ▼
                                        Retriever
                                             │
                                             ▼
                                        Llama 3.2
                                             │
                                             ▼
                                      AI Response
```

---

# 1️⃣ User Input

The first step is to provide the source video or audio.

The application accepts three types of input:

```text
YouTube URL
     OR
Video File
     OR
Audio File
```

Example:

```text
https://www.youtube.com/watch?v=XXXXXXXX
```

The user can enter the YouTube URL through the Streamlit interface.

For local processing, the user can upload a video or audio file.

---

# 2️⃣ Audio Processing

After receiving the input, the application prepares the audio for
transcription.

## YouTube Input

For a YouTube URL, `yt-dlp` is used to download the required media/audio.

```text
YouTube URL
     ↓
   yt-dlp
     ↓
Audio
```

## Local Video

For a local video file, FFmpeg is used to extract or convert the audio.

```text
Video File
     ↓
   FFmpeg
     ↓
Audio
```

## Audio Processing

Pydub and FFmpeg are used to prepare the audio into a format suitable
for transcription.

```text
Raw Audio
    ↓
Conversion
    ↓
Processed Audio
```

---

# 3️⃣ Audio Chunking

Long videos can contain hours of audio.

Instead of processing the entire audio file at once, the application divides
the audio into smaller chunks.

```text
Large Audio File
        │
        ▼
 ┌──────┼──────┬──────┐
 ▼      ▼      ▼      ▼
Chunk1 Chunk2 Chunk3 Chunk4
```

Each chunk can then be processed independently.

### Why Chunking?

Chunking helps:

- Process large files
- Reduce memory usage
- Handle long videos
- Make transcription more manageable
- Process audio sequentially

---

# 4️⃣ Speech-to-Text Using Whisper

The audio chunks are passed to Whisper.

Whisper is responsible for converting spoken language into text.

```text
Audio Chunk
     ↓
   Whisper
     ↓
Text
```

For example:

```text
Audio:
"We will complete the project by Friday."

        ↓

Transcript:
"We will complete the project by Friday."
```

Each audio chunk produces a text transcript.

---

# 5️⃣ Combining the Transcript

After all audio chunks are transcribed, the individual results are combined.

```text
Chunk 1 → Transcript 1
Chunk 2 → Transcript 2
Chunk 3 → Transcript 3
Chunk 4 → Transcript 4

             ↓

      Complete Transcript
```

The complete transcript becomes the main source of information for the
remaining AI pipeline.

---

# 6️⃣ AI-Powered Transcript Analysis

Once the transcript is available, the application performs several AI
operations.

The transcript is passed to Llama 3.2 through Ollama.

```text
                    Transcript
                         │
          ┌──────────────┼──────────────┐
          │              │              │
          ▼              ▼              ▼
        Title         Summary       Extraction
                                         │
                              ┌──────────┼──────────┐
                              ▼          ▼          ▼
                           Actions   Decisions  Questions
```

---

# 🏷️ 7️⃣ Title Generation

The system sends a portion of the transcript to the LLM.

The model generates a short title representing the content.

Example:

```text
Transcript:
"We discussed the architecture of our AI application..."

                 ↓

Generated Title:
"AI Application Architecture Meeting"
```

---

# 📝 8️⃣ Summary Generation

The complete transcript can be large, so it is divided into smaller text
chunks.

```text
Complete Transcript
        ↓
Text Splitter
        ↓
┌───────┼────────┐
▼       ▼        ▼
Chunk1 Chunk2   Chunk3
```

Each chunk is summarized individually.

```text
Chunk 1 → Summary 1
Chunk 2 → Summary 2
Chunk 3 → Summary 3
```

The partial summaries are then combined.

```text
Summary 1
Summary 2
Summary 3
    ↓
Final Summary
```

This approach helps the system handle longer transcripts.

---

# ✅ 9️⃣ Action Item Extraction

The system analyzes the transcript and identifies tasks that were discussed
or assigned.

For example:

```text
Transcript:

"Rahul will complete the API integration by Friday."
```

The system extracts:

```text
Task:
Complete API integration

Owner:
Rahul

Deadline:
Friday
```

The final output is presented as a structured list.

---

# 🔑 🔟 Key Decision Extraction

The system also identifies important decisions made during the discussion.

Example:

```text
Transcript:

"We have decided to use PostgreSQL for the application."
```

Output:

```text
Key Decision:

PostgreSQL will be used as the application database.
```

This helps users quickly understand the major decisions without reading
the entire transcript.

---

# ❓ 1️⃣1️⃣ Open Question Extraction

The application identifies unresolved questions and topics that require
further discussion.

Example:

```text
Transcript:

"We still need to decide when the application will be deployed."
```

Output:

```text
Open Question:

What is the final deployment date?
```

---

# 🧠 1️⃣2️⃣ Building the RAG System

After transcript analysis, the transcript is used to create the
Retrieval-Augmented Generation pipeline.

RAG allows the user to ask questions about the video.

```text
Transcript
     ↓
Text Chunking
     ↓
Embeddings
     ↓
ChromaDB
     ↓
Retriever
     ↓
Relevant Context
     ↓
Llama 3.2
     ↓
Answer
```

---

# ✂️ 1️⃣3️⃣ Transcript Chunking for RAG

The transcript is divided into smaller chunks using
`RecursiveCharacterTextSplitter`.

Example:

```text
Complete Transcript
        │
        ▼
┌─────────────────────┐
│ Chunk 1              │
│ Project discussion   │
└─────────────────────┘

┌─────────────────────┐
│ Chunk 2              │
│ Database discussion  │
└─────────────────────┘

┌─────────────────────┐
│ Chunk 3              │
│ Deployment discussion│
└─────────────────────┘
```

Each chunk contains a manageable amount of contextual information.

---

# 🔢 1️⃣4️⃣ Embedding Generation

Each transcript chunk is converted into a numerical vector.

The project uses:

```text
Nomic Embed Text
```

The process is:

```text
Text Chunk
    ↓
Nomic Embed Text
    ↓
Vector Representation
```

For example:

```text
"Project deadline is Friday."
```

is transformed into a numerical vector representing its semantic meaning.

---

# 🗄️ 1️⃣5️⃣ ChromaDB Vector Store

The generated embeddings are stored in ChromaDB.

```text
Transcript Chunk
       ↓
Embedding
       ↓
ChromaDB
```

ChromaDB acts as the vector database for the application.

It allows the system to search transcript information based on semantic
similarity.

---

# 🔍 1️⃣6️⃣ User Asks a Question

After the video has been processed, the user can ask questions through
the chat interface.

Example:

```text
What is the project deadline?
```

The question is sent to the RAG pipeline.

---

# 🔎 1️⃣7️⃣ Retrieval

The question is converted into an embedding.

```text
User Question
      ↓
Question Embedding
      ↓
ChromaDB
      ↓
Similarity Search
      ↓
Relevant Transcript Chunks
```

The retriever selects the most relevant transcript sections.

For example:

```text
Question:
"What is the project deadline?"

Retrieved Context:
"The team agreed to complete the project by Friday."
```

---

# 🧩 1️⃣8️⃣ Context Construction

The retrieved transcript chunks are combined with the user's question.

```text
Retrieved Context
        +
User Question
        ↓
      Prompt
```

The prompt provides the LLM with the information needed to answer the
question.

---

# 🦙 1️⃣9️⃣ Llama 3.2 Generation

The final prompt is sent to Llama 3.2 through Ollama.

```text
Prompt
   ↓
Ollama
   ↓
Llama 3.2
   ↓
Generated Answer
```

Example:

```text
User:
What is the project deadline?

AI:
The project deadline is Friday.
```

---

# 💬 2️⃣0️⃣ Interactive Video Chat

The final answer is displayed in the Streamlit chat interface.

Users can ask multiple questions.

Example:

```text
User:
What database was selected?

AI:
PostgreSQL was selected.

User:
Who is responsible for the API?

AI:
Rahul is responsible for the API development.

User:
What is the deadline?

AI:
The API development deadline is Friday.
```

The answers are generated using relevant transcript context retrieved
through the RAG system.

---

# 🔗 Complete Data Flow

The complete data flow can be represented as:

```text
                    INPUT
                      │
                      ▼
            YouTube / Video / Audio
                      │
                      ▼
              Audio Processing
                      │
                      ▼
                Audio Chunks
                      │
                      ▼
                   Whisper
                      │
                      ▼
                Transcript
                      │
          ┌───────────┼────────────┐
          │           │            │
          ▼           ▼            ▼
        Title      Summary     Extraction
                                  │
                         ┌────────┼────────┐
                         ▼        ▼        ▼
                      Actions Decisions Questions
                                  │
                                  ▼
                         RAG Processing
                                  │
                                  ▼
                         Text Chunking
                                  │
                                  ▼
                         Nomic Embeddings
                                  │
                                  ▼
                              ChromaDB
                                  │
                                  ▼
                              Retrieval
                                  │
                                  ▼
                            Llama 3.2
                                  │
                                  ▼
                             AI Answer
```

---

# 🧱 System Components

The project can be divided into five major layers.

## 1. Input Layer

Responsible for receiving:

```text
YouTube URL
Video File
Audio File
```

---

## 2. Processing Layer

Responsible for:

```text
yt-dlp
FFmpeg
Pydub
Whisper
```

This layer converts raw media into a transcript.

---

## 3. Intelligence Layer

Responsible for:

```text
Llama 3.2
LangChain
```

This layer generates:

- Titles
- Summaries
- Action items
- Decisions
- Questions

---

## 4. Retrieval Layer

Responsible for:

```text
Text Splitting
Nomic Embeddings
ChromaDB
Retriever
```

This layer makes the transcript searchable.

---

## 5. Presentation Layer

Responsible for displaying the results using:

```text
Streamlit
```

The user can view:

- Summary
- Action items
- Decisions
- Questions
- Transcript
- AI chat

---

# 🔐 Why RAG Is Used?

A long video transcript can contain thousands of words.

Sending the entire transcript to the LLM for every question can be inefficient.

RAG solves this problem by retrieving only the relevant transcript sections.

Without RAG:

```text
Entire Transcript
       ↓
      LLM
       ↓
    Answer
```

With RAG:

```text
Entire Transcript
       ↓
    ChromaDB
       ↓
Relevant Chunks
       ↓
      LLM
       ↓
    Answer
```

Therefore, the RAG pipeline connects the user's question with the most
relevant information from the video.

---

# 🔄 End-to-End Example

Suppose the user uploads a one-hour project meeting.

### Input

```text
Project_Meeting.mp4
```

### Processing

```text
Project_Meeting.mp4
        ↓
Audio Extraction
        ↓
Audio Chunks
        ↓
Whisper
        ↓
Transcript
```

### AI Analysis

```text
Transcript
    │
    ├── Title
    │
    ├── Summary
    │
    ├── Action Items
    │
    ├── Key Decisions
    │
    └── Open Questions
```

### RAG Creation

```text
Transcript
     ↓
Chunks
     ↓
Nomic Embeddings
     ↓
ChromaDB
```

### User Question

```text
"What database did the team choose?"
```

### Retrieval

```text
Question
   ↓
Embedding
   ↓
ChromaDB
   ↓
Relevant Transcript Chunk
```

### Generation

```text
Relevant Context
       +
Question
       ↓
Llama 3.2
       ↓
Answer
```

### Final Answer

```text
"The team decided to use PostgreSQL."
```

---

# 🧠 Overall Project Concept

The project combines multiple AI technologies into a single pipeline:

```text
             AI VIDEO ASSISTANT
                    │
                    ▼
             Speech Recognition
                 (Whisper)
                    │
                    ▼
              Text Processing
                (LangChain)
                    │
                    ▼
             LLM Processing
              (Llama 3.2)
                    │
                    ▼
              Embeddings
            (Nomic Embed)
                    │
                    ▼
             Vector Database
               (ChromaDB)
                    │
                    ▼
                Retrieval
                    │
                    ▼
                   RAG
                    │
                    ▼
             Context-Aware AI
                    │
                    ▼
              Streamlit UI
```

---

# 🎯 Final Workflow Summary

```text
1. User provides video/audio
              ↓
2. Audio is extracted
              ↓
3. Audio is divided into chunks
              ↓
4. Whisper converts speech into text
              ↓
5. Complete transcript is generated
              ↓
6. Llama 3.2 generates title and summary
              ↓
7. Llama 3.2 extracts action items
              ↓
8. Llama 3.2 extracts key decisions
              ↓
9. Llama 3.2 extracts open questions
              ↓
10. Transcript is split into RAG chunks
              ↓
11. Nomic Embed Text generates embeddings
              ↓
12. Embeddings are stored in ChromaDB
              ↓
13. User asks a question
              ↓
14. Retriever searches ChromaDB
              ↓
15. Relevant transcript chunks are retrieved
              ↓
16. Context + Question are sent to Llama 3.2
              ↓
17. Llama 3.2 generates the answer
              ↓
18. Answer is displayed in Streamlit
```

---

# 🚀 Final Result

The final system transforms:

```text
Raw Video / Audio
       ↓
Speech
       ↓
Text
       ↓
Structured Information
       ↓
Searchable Knowledge
       ↓
Conversational AI
```

The result is an **AI-powered video assistant** that can understand long
videos, extract important information, and allow users to interact with the
video content using natural language.
