# Notebook LLM - Multimodal Research Assistant

A production-ready multimodal RAG system that can ingest, process, and reason over complex documents containing text, images, tables, charts, and code snippets - similar to NotebookLM but with enhanced multimodal capabilities.

## Features

- **Comprehensive Document Processing**: Handle 10+ file formats including PDF, DOCX, HTML, CSV, Excel, PowerPoint, Jupyter notebooks, and image files
- **Advanced Multimodal Understanding**: Process and understand relationships between text, images, tables, charts, and code within documents
- **Intelligent Document Structure**: Maintain document hierarchy and relationships between sections
- **Advanced Query Capabilities**: Support complex queries requiring reasoning across multiple modalities
- **Production Features**: User authentication, document management, query history, and real-time collaboration
- **Custom Embedding Strategy**: Domain-specific embeddings for technical content
- **Export & Integration**: Allow users to export insights and integrate with other tools

## Architecture

- **Backend**: FastAPI with LangChain integration
- **Frontend**: React with Material UI
- **Document Processing**: Custom pipeline using LangChain, Unstructured, and Docling
- **Multimodal AI**: Integration with vision models (GPT-4V, Claude Vision) for image understanding
- **Vector Database**: ChromaDB with metadata filtering and hybrid search

## Getting Started

### Prerequisites

- Python 3.9+
- Node.js 16+
- PostgreSQL (optional, SQLite used by default)

### Backend Setup

1. Navigate to the backend directory:
   ```
   cd backend
   ```

2. Create a virtual environment:
   ```
   python -m venv myenv
   # On Windows: myenv\Scripts\activate
   # On Unix/MacOS: source myenv/bin/activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file with the following content:
   ```
   # API Configuration
   API_V1_STR=/api/v1
   PROJECT_NAME=Notebook LLM
   SECRET_KEY=your_secret_key_here_change_this_in_production
   ACCESS_TOKEN_EXPIRE_MINUTES=11520

   # CORS Configuration
   BACKEND_CORS_ORIGINS=["http://localhost:3000"]

   # Database Configuration
   DATABASE_URL=sqlite:///./notebook_llm.db

   # Vector Database Configuration
   VECTOR_DB_PATH=./vector_db

   # Document Storage
   DOCUMENT_STORAGE_PATH=./document_storage

   # LLM Configuration
   # Replace with your actual API keys
   OPENAI_API_KEY=your_openai_api_key_here
   # ANTHROPIC_API_KEY=your_anthropic_api_key_here
   ```

5. Run the application:
   ```
   uvicorn app.main:app --reload --host 0.0.0.0
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```
   cd frontend
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Start the development server:
   ```
   npm start
   ```

4. The frontend will be available at `http://localhost:3000`

## Usage

1. Register a new account or log in with the default admin account:
   - Email: admin@example.com
   - Password: admin

2. Upload documents through the upload interface

3. View your documents in the dashboard

4. Click on a document to view its contents and ask questions

5. Use natural language queries to extract information from your documents

## Document Processing Pipeline

1. **Document Upload**: Files are uploaded and stored on the server
2. **Document Parsing**: Documents are parsed using appropriate loaders based on file type
3. **Content Extraction**: Text, images, tables, and code are extracted
4. **Document Chunking**: Content is split into manageable chunks
5. **Embedding Generation**: Chunks are embedded using domain-specific models
6. **Vector Storage**: Embeddings are stored in the vector database
7. **Metadata Indexing**: Document structure and relationships are preserved

## Query Processing Pipeline

1. **Query Analysis**: User queries are analyzed to determine intent
2. **Query Decomposition**: Complex queries are broken down into sub-queries
3. **Retrieval**: Relevant document sections are retrieved using hybrid search
4. **Response Generation**: LLM generates responses based on retrieved content
5. **Citation Generation**: Sources are cited for transparency

## Project Structure

```
.
├── backend/
│   ├── app/
│   │   ├── api/              # API endpoints
│   │   ├── core/             # Core functionality
│   │   ├── db/               # Database models and session
│   │   ├── models/           # SQLAlchemy models
│   │   ├── schemas/          # Pydantic schemas
│   │   ├── services/         # Business logic
│   │   └── utils/            # Utility functions
│   ├── requirements.txt      # Python dependencies
│   └── run.py                # Application entry point
├── frontend/
│   ├── public/               # Static files
│   ├── src/
│   │   ├── components/       # React components
│   │   ├── context/          # React context
│   │   ├── hooks/            # Custom hooks
│   │   ├── pages/            # Page components
│   │   ├── services/         # API services
│   │   └── utils/            # Utility functions
│   └── package.json          # Node.js dependencies
└── README.md                 # Project documentation
```

## Troubleshooting

### CORS Issues

If you encounter CORS errors when making requests from the frontend to the backend:

1. Make sure the backend is running and accessible
2. Check that the CORS configuration in `backend/app/main.py` includes your frontend URL
3. Verify that the API endpoints in the frontend services are correctly pointing to your backend URL

### OpenAI API Key Issues

If you encounter errors related to the OpenAI API key:

1. Make sure you have set a valid OpenAI API key in the `.env` file
2. Check that the API key is being properly loaded by the application
3. If you don't have an OpenAI API key, the application will use mock responses for testing purposes

### Database Issues

If you encounter database-related errors:

1. Make sure the database file exists and is accessible
2. Check that the database URL in the `.env` file is correct
3. If using PostgreSQL, ensure the database server is running and accessible

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- LangChain for providing the framework for building LLM applications
- Unstructured and Docling for document processing capabilities
- OpenAI and Anthropic for providing powerful language models
- FastAPI and React for the web application framework 