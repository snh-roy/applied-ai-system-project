"""
Retrieval-Augmented Generation System for Mental Health Support
"""

import os
import json
import numpy as np
from typing import List, Dict, Tuple, Optional, Any
from dataclasses import dataclass
import logging
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
import hashlib

from .knowledge_base import MentalHealthResource, MentalHealthKnowledgeBase

logger = logging.getLogger(__name__)


@dataclass
class RetrievalResult:
    """Result from retrieval query"""
    resource: MentalHealthResource
    relevance_score: float
    snippet: str
    metadata: Dict[str, Any]


class RAGSystem:
    """
    Retrieval-Augmented Generation system for mental health support.
    Uses vector similarity search to find relevant resources and generates
    contextual responses.
    """
    
    def __init__(self, persist_directory: str = "./chroma_db"):
        """Initialize RAG system with vector store and knowledge base"""
        self.knowledge_base = MentalHealthKnowledgeBase()
        self.persist_directory = persist_directory
        
        # Initialize embedding model
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Initialize ChromaDB client
        self.chroma_client = chromadb.Client(Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory=persist_directory
        ))
        
        # Create or get collection
        self.collection = self._initialize_collection()
        
        # Index knowledge base if needed
        self._index_knowledge_base()
        
    def _initialize_collection(self):
        """Initialize or get ChromaDB collection"""
        try:
            collection = self.chroma_client.get_collection(
                name="mental_health_resources"
            )
            logger.info("Loaded existing collection")
        except:
            collection = self.chroma_client.create_collection(
                name="mental_health_resources",
                metadata={"hnsw:space": "cosine"}
            )
            logger.info("Created new collection")
        return collection
        
    def _generate_document_id(self, content: str) -> str:
        """Generate unique ID for document"""
        return hashlib.md5(content.encode()).hexdigest()
        
    def _index_knowledge_base(self):
        """Index all resources from knowledge base into vector store"""
        # Check if already indexed
        try:
            existing_count = self.collection.count()
            if existing_count > 0:
                logger.info(f"Collection already has {existing_count} documents")
                return
        except:
            pass
            
        documents = []
        embeddings = []
        metadatas = []
        ids = []
        
        for resource in self.knowledge_base.resources:
            # Combine title and content for embedding
            doc_text = f"{resource.title}\n{resource.content}"
            
            documents.append(doc_text)
            
            # Generate embedding
            embedding = self.embedding_model.encode(doc_text)
            embeddings.append(embedding.tolist())
            
            # Prepare metadata
            metadata = {
                "resource_id": resource.id,
                "title": resource.title,
                "category": resource.category,
                "tags": json.dumps(resource.tags),
                "applicable_moods": json.dumps(resource.applicable_moods),
                "applicable_triggers": json.dumps(resource.applicable_triggers),
                "effectiveness_rating": resource.effectiveness_rating,
                "evidence_level": resource.evidence_level,
                "source": resource.source
            }
            metadatas.append(metadata)
            
            # Generate ID
            ids.append(self._generate_document_id(doc_text))
            
        # Add to collection
        if documents:
            self.collection.add(
                documents=documents,
                embeddings=embeddings,
                metadatas=metadatas,
                ids=ids
            )
            logger.info(f"Indexed {len(documents)} resources")
            
    def retrieve_relevant_resources(
        self,
        query: str,
        mood: Optional[str] = None,
        triggers: Optional[List[str]] = None,
        n_results: int = 5
    ) -> List[RetrievalResult]:
        """
        Retrieve relevant resources based on query and context
        
        Args:
            query: User's input text or question
            mood: Current mood state
            triggers: Identified triggers
            n_results: Number of results to return
            
        Returns:
            List of relevant resources with scores
        """
        # Generate query embedding
        query_embedding = self.embedding_model.encode(query)
        
        # Build where clause for filtering
        where_conditions = {}
        if mood:
            # Filter for resources applicable to the mood
            where_conditions["$or"] = [
                {"applicable_moods": {"$contains": mood}}
            ]
            
        # Query the collection
        results = self.collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=n_results * 2,  # Get more results for post-filtering
            where=where_conditions if where_conditions else None
        )
        
        retrieval_results = []
        
        if results and results['documents']:
            for i in range(len(results['documents'][0])):
                # Get resource from knowledge base
                resource_id = results['metadatas'][0][i]['resource_id']
                resource = next((r for r in self.knowledge_base.resources 
                               if r.id == resource_id), None)
                
                if resource:
                    # Calculate relevance score
                    base_score = 1.0 - results['distances'][0][i]  # Convert distance to similarity
                    
                    # Boost score based on mood match
                    if mood and mood in resource.applicable_moods:
                        base_score *= 1.2
                        
                    # Boost score based on trigger match
                    if triggers:
                        trigger_boost = sum(1 for t in triggers 
                                          if t in resource.applicable_triggers)
                        base_score *= (1 + trigger_boost * 0.1)
                        
                    # Factor in effectiveness rating
                    base_score *= resource.effectiveness_rating
                    
                    # Extract snippet
                    snippet = resource.content[:200] + "..." if len(resource.content) > 200 else resource.content
                    
                    retrieval_results.append(RetrievalResult(
                        resource=resource,
                        relevance_score=base_score,
                        snippet=snippet,
                        metadata=results['metadatas'][0][i]
                    ))
                    
        # Sort by relevance score and return top n
        retrieval_results.sort(key=lambda x: x.relevance_score, reverse=True)
        return retrieval_results[:n_results]
        
    def generate_contextual_response(
        self,
        query: str,
        mood_analysis: Any,
        retrieved_resources: List[RetrievalResult]
    ) -> Dict[str, Any]:
        """
        Generate a contextual response using retrieved resources
        
        Args:
            query: User's input
            mood_analysis: Result from mood analyzer
            retrieved_resources: Retrieved relevant resources
            
        Returns:
            Generated response with citations
        """
        # Build context from retrieved resources
        context_parts = []
        citations = []
        
        for i, result in enumerate(retrieved_resources):
            context_parts.append(f"Resource {i+1}: {result.resource.title}")
            context_parts.append(f"Content: {result.resource.content}")
            context_parts.append("")
            
            citations.append({
                "title": result.resource.title,
                "source": result.resource.source,
                "relevance": result.relevance_score
            })
            
        context = "\n".join(context_parts)
        
        # Generate response based on mood and context
        response = self._generate_response(
            query=query,
            mood=mood_analysis.primary_mood if mood_analysis else None,
            context=context,
            resources=retrieved_resources
        )
        
        return {
            "response": response,
            "citations": citations,
            "resources_used": len(retrieved_resources),
            "confidence": np.mean([r.relevance_score for r in retrieved_resources]) if retrieved_resources else 0
        }
        
    def _generate_response(
        self,
        query: str,
        mood: Optional[str],
        context: str,
        resources: List[RetrievalResult]
    ) -> str:
        """Generate response using template-based approach"""
        # This is a simplified version - in production, you'd use an LLM
        
        if not resources:
            return "I understand you're going through something difficult. While I couldn't find specific resources matching your situation, please know that support is available. Consider reaching out to a mental health professional or calling a crisis helpline if you need immediate help."
            
        # Build response based on top resource
        top_resource = resources[0].resource
        
        response_parts = []
        
        # Acknowledge the mood if detected
        if mood:
            mood_acknowledgments = {
                "sad": "I can sense you're feeling down",
                "anxious": "I understand you're feeling anxious",
                "angry": "I hear that you're feeling frustrated",
                "stressed": "It sounds like you're under a lot of stress",
                "overwhelmed": "I can see you're feeling overwhelmed"
            }
            if mood in mood_acknowledgments:
                response_parts.append(mood_acknowledgments[mood] + ". ")
                
        # Add main recommendation
        response_parts.append(f"Based on your situation, I'd like to suggest trying {top_resource.title}. ")
        
        # Add brief explanation
        content_preview = top_resource.content.split('.')[0] + '.'
        response_parts.append(content_preview + " ")
        
        # Add effectiveness note if high
        if top_resource.effectiveness_rating > 0.8:
            response_parts.append("This technique has shown strong effectiveness in research. ")
            
        # Mention additional resources if available
        if len(resources) > 1:
            other_titles = [r.resource.title for r in resources[1:3]]
            response_parts.append(f"You might also find these helpful: {', '.join(other_titles)}. ")
            
        # Add encouragement
        response_parts.append("Remember, seeking support is a sign of strength, not weakness.")
        
        return "".join(response_parts)
        
    def add_user_feedback(
        self,
        resource_id: str,
        helpful: bool,
        user_mood: str = None
    ):
        """Record user feedback on resource helpfulness"""
        # In a production system, this would update the effectiveness ratings
        logger.info(f"Feedback recorded for {resource_id}: helpful={helpful}, mood={user_mood}")
        
    def export_index(self, filepath: str):
        """Export vector index metadata"""
        metadata = {
            "collection_name": "mental_health_resources",
            "num_documents": self.collection.count(),
            "embedding_model": "all-MiniLM-L6-v2",
            "resources": [
                {
                    "id": r.id,
                    "title": r.title,
                    "category": r.category
                }
                for r in self.knowledge_base.resources
            ]
        }
        
        with open(filepath, 'w') as f:
            json.dump(metadata, f, indent=2)
        logger.info(f"Index metadata exported to {filepath}")
        

class SimpleRAGInterface:
    """Simplified interface for RAG system"""
    
    def __init__(self, rag_system: RAGSystem):
        self.rag = rag_system
        
    def get_support(
        self,
        user_input: str,
        mood: str = None,
        triggers: List[str] = None
    ) -> str:
        """Get mental health support for user input"""
        # Retrieve relevant resources
        resources = self.rag.retrieve_relevant_resources(
            query=user_input,
            mood=mood,
            triggers=triggers,
            n_results=3
        )
        
        if not resources:
            return "I'm here to support you. While I couldn't find specific resources for your situation, please consider reaching out to a mental health professional for personalized help."
            
        # Build simple response
        top_resource = resources[0].resource
        response = f"Based on what you've shared, I recommend trying: {top_resource.title}\n\n"
        response += f"{top_resource.content}\n\n"
        
        if len(resources) > 1:
            response += "Other helpful resources:\n"
            for r in resources[1:]:
                response += f"- {r.resource.title}\n"
                
        return response
        
    def get_crisis_support(self) -> str:
        """Get immediate crisis support information"""
        crisis_info = self.rag.knowledge_base.get_crisis_resources()
        
        response = "If you're in crisis, please reach out for help immediately:\n\n"
        
        for hotline in crisis_info['hotlines']:
            response += f"• {hotline['name']}: {hotline['number']} ({hotline['availability']})\n"
            
        response += "\nImmediate steps you can take:\n"
        for step in crisis_info['immediate_steps'][:3]:
            response += f"- {step}\n"
            
        return response