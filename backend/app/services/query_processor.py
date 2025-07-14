import os
from typing import Dict, List, Optional, Any, Tuple

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain.chains.query_constructor.base import AttributeInfo
from langchain.retrievers.self_query.base import SelfQueryRetriever
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.agents import initialize_agent, Tool, AgentType
from langchain.memory import ConversationBufferMemory
from langchain_core.documents import Document

from app.core.config import settings


def load_vector_store(document_id: str):
    """
    Load the vector store for a specific document
    """
    vector_store_path = os.path.join(settings.VECTOR_DB_PATH, f"doc_{document_id}")
    
    if not os.path.exists(vector_store_path):
        raise ValueError(f"Vector store not found for document {document_id}")
    
    # Use HuggingFace embeddings for technical content
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    # Load the vector store
    return Chroma(persist_directory=vector_store_path, embedding_function=embeddings)


def create_metadata_filter_retriever(vectorstore, metadata_field_info):
    """
    Create a retriever with metadata filtering capabilities
    """
    llm = ChatOpenAI(temperature=0, openai_api_key=settings.OPENAI_API_KEY)
    
    return SelfQueryRetriever.from_llm(
        llm=llm,
        vectorstore=vectorstore,
        document_contents="Document sections from various file types",
        metadata_field_info=metadata_field_info,
        verbose=True
    )


def decompose_query(query_text: str):
    """
    Decompose a complex query into simpler sub-queries
    """
    llm = ChatOpenAI(temperature=0, openai_api_key=settings.OPENAI_API_KEY)
    
    prompt_template = """
    You are an expert at breaking down complex questions into simpler sub-questions.
    Given the following question, break it down into 1-3 simpler sub-questions that would help answer the original question.
    
    Original Question: {question}
    
    Sub-questions:
    """
    
    prompt = PromptTemplate(
        input_variables=["question"],
        template=prompt_template,
    )
    
    chain = LLMChain(llm=llm, prompt=prompt)
    result = chain.run(query_text)
    
    # Parse the result into a list of sub-questions
    sub_questions = [q.strip() for q in result.split('\n') if q.strip()]
    
    return sub_questions


def process_image_query(query_text: str, image_path: str):
    """
    Process a query about an image using a vision model
    """
    # This would integrate with GPT-4V or Claude Vision
    # For now, we'll use a placeholder implementation
    llm = ChatOpenAI(temperature=0, openai_api_key=settings.OPENAI_API_KEY)
    
    prompt_template = """
    Analyze the image at {image_path} and answer the following question:
    
    Question: {question}
    """
    
    prompt = PromptTemplate(
        input_variables=["image_path", "question"],
        template=prompt_template,
    )
    
    chain = LLMChain(llm=llm, prompt=prompt)
    result = chain.run(image_path=image_path, question=query_text)
    
    return result


def process_query(query_text: str, document_id: Optional[str] = None):
    """
    Process a query using LangChain and return the response with citations
    """
    # Check if OpenAI API key is available
    if not settings.OPENAI_API_KEY:
        print("Using mock implementation for testing (OpenAI API key not available)")
        # Return a mock response for testing
        return {
            "response": f"This is a mock response for the query: '{query_text}'. The OpenAI API key is not available, so we're using a mock implementation for testing.",
            "citations": [
                {
                    "content": "This is a mock citation for testing purposes.",
                    "meta_data": {"page": 1, "source": "mock_document.pdf"},
                    "document_section_id": 1
                }
            ]
        }
        
    try:
        # If document_id is provided, load the specific vector store
        if document_id:
            vectorstore = load_vector_store(document_id)
            retriever = vectorstore.as_retriever(
                search_type="mmr",
                search_kwargs={"k": 5, "fetch_k": 10}
            )
        else:
            # Load all vector stores and create a unified retriever
            # This is a placeholder for now
            raise NotImplementedError("Querying across all documents not yet implemented")
        
        # Check if the query is complex and needs decomposition
        if len(query_text.split()) > 15 or "?" in query_text[1:]:
            sub_queries = decompose_query(query_text)
            
            # Process each sub-query
            sub_results = []
            for sub_query in sub_queries:
                qa_chain = RetrievalQA.from_chain_type(
                    llm=ChatOpenAI(temperature=0, openai_api_key=settings.OPENAI_API_KEY),
                    chain_type="stuff",
                    retriever=retriever,
                    return_source_documents=True
                )
                sub_result = qa_chain({"query": sub_query})
                sub_results.append(sub_result)
            
            # Combine the results
            llm = ChatOpenAI(temperature=0, openai_api_key=settings.OPENAI_API_KEY)
            prompt_template = """
            Based on the following information, please answer the original question.
            
            Original question: {original_question}
            
            Information:
            {sub_results}
            
            Answer:
            """
            
            prompt = PromptTemplate(
                input_variables=["original_question", "sub_results"],
                template=prompt_template,
            )
            
            chain = LLMChain(llm=llm, prompt=prompt)
            final_answer = chain.run(
                original_question=query_text,
                sub_results="\n\n".join([f"Sub-question: {q}\nAnswer: {r['result']}" for q, r in zip(sub_queries, sub_results)])
            )
            
            # Collect all source documents
            source_documents = []
            for result in sub_results:
                source_documents.extend(result.get("source_documents", []))
        else:
            # For simpler queries, use a direct QA chain
            qa_chain = RetrievalQA.from_chain_type(
                llm=ChatOpenAI(temperature=0, openai_api_key=settings.OPENAI_API_KEY),
                chain_type="stuff",
                retriever=retriever,
                return_source_documents=True
            )
            
            result = qa_chain({"query": query_text})
            final_answer = result["result"]
            source_documents = result.get("source_documents", [])
        
        # Extract citations
        citations = []
        for doc in source_documents:
            citation = {
                "content": doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content,
                "meta_data": doc.metadata,  # Changed from metadata to meta_data
                "document_section_id": doc.metadata.get("section_id", 0)  # This would need to be properly set during indexing
            }
            citations.append(citation)
        
        return {
            "response": final_answer,
            "citations": citations
        }
    except Exception as e:
        import traceback
        print(f"Error in process_query: {str(e)}")
        print(traceback.format_exc())
        
        # Return a mock response for testing purposes
        return {
            "response": f"I'm sorry, I couldn't process your query due to an error: {str(e)}. This is a mock response for testing purposes.",
            "citations": []
        } 