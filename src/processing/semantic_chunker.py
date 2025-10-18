"""
Semantic Chunker Module
Uses BERT embeddings to create semantically meaningful chunks
"""
import numpy as np
from typing import List, Dict, Tuple
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import re


class SemanticChunker:
    """
    BERT-based semantic chunking that groups text by semantic similarity
    """
    
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2', 
                 similarity_threshold: float = 0.5,
                 max_chunk_size: int = 1000,
                 min_chunk_size: int = 100):
        """
        Initialize the semantic chunker with BERT model
        
        Args:
            model_name: Name of the sentence-transformers model
            similarity_threshold: Threshold for semantic similarity (0-1)
            max_chunk_size: Maximum characters per chunk
            min_chunk_size: Minimum characters per chunk
        """
        self.model = SentenceTransformer(model_name)
        self.similarity_threshold = similarity_threshold
        self.max_chunk_size = max_chunk_size
        self.min_chunk_size = min_chunk_size
    
    def chunk_text(self, text: str, method: str = 'semantic') -> List[Dict]:
        """
        Chunk text using specified method
        
        Args:
            text: Input text to chunk
            method: 'semantic', 'sentence', or 'fixed'
            
        Returns:
            List of chunk dictionaries with text and embeddings
        """
        if method == 'semantic':
            return self._semantic_chunking(text)
        elif method == 'sentence':
            return self._sentence_chunking(text)
        elif method == 'fixed':
            return self._fixed_size_chunking(text)
        else:
            raise ValueError(f"Unknown chunking method: {method}")
    
    def _semantic_chunking(self, text: str) -> List[Dict]:
        """
        Chunk text based on semantic similarity using BERT embeddings
        """
        # Split into sentences
        sentences = self._split_into_sentences(text)
        
        if not sentences:
            return []
        
        # Get embeddings for all sentences
        embeddings = self.model.encode(sentences)
        
        # Group sentences into chunks based on semantic similarity
        chunks = []
        current_chunk = [sentences[0]]
        current_embedding = embeddings[0].reshape(1, -1)
        
        for i in range(1, len(sentences)):
            sentence = sentences[i]
            sentence_embedding = embeddings[i].reshape(1, -1)
            
            # Calculate similarity with current chunk
            similarity = cosine_similarity(current_embedding, sentence_embedding)[0][0]
            
            # Check if chunk size would exceed maximum
            chunk_text = ' '.join(current_chunk + [sentence])
            
            if similarity >= self.similarity_threshold and len(chunk_text) <= self.max_chunk_size:
                # Add to current chunk
                current_chunk.append(sentence)
                # Update chunk embedding (average)
                current_embedding = np.mean([current_embedding, sentence_embedding], axis=0)
            else:
                # Save current chunk and start new one
                if len(' '.join(current_chunk)) >= self.min_chunk_size:
                    chunk_dict = self._create_chunk_dict(current_chunk, len(chunks))
                    chunks.append(chunk_dict)
                
                current_chunk = [sentence]
                current_embedding = sentence_embedding
        
        # Add final chunk
        if current_chunk and len(' '.join(current_chunk)) >= self.min_chunk_size:
            chunk_dict = self._create_chunk_dict(current_chunk, len(chunks))
            chunks.append(chunk_dict)
        
        return chunks
    
    def _sentence_chunking(self, text: str) -> List[Dict]:
        """
        Chunk text by sentences, respecting max chunk size
        """
        sentences = self._split_into_sentences(text)
        chunks = []
        current_chunk = []
        
        for sentence in sentences:
            chunk_text = ' '.join(current_chunk + [sentence])
            
            if len(chunk_text) <= self.max_chunk_size:
                current_chunk.append(sentence)
            else:
                if current_chunk:
                    chunk_dict = self._create_chunk_dict(current_chunk, len(chunks))
                    chunks.append(chunk_dict)
                current_chunk = [sentence]
        
        # Add final chunk
        if current_chunk:
            chunk_dict = self._create_chunk_dict(current_chunk, len(chunks))
            chunks.append(chunk_dict)
        
        return chunks
    
    def _fixed_size_chunking(self, text: str) -> List[Dict]:
        """
        Chunk text into fixed-size chunks
        """
        chunks = []
        words = text.split()
        current_chunk = []
        
        for word in words:
            current_chunk.append(word)
            chunk_text = ' '.join(current_chunk)
            
            if len(chunk_text) >= self.max_chunk_size:
                chunk_dict = self._create_chunk_dict([chunk_text], len(chunks))
                chunks.append(chunk_dict)
                current_chunk = []
        
        # Add final chunk
        if current_chunk:
            chunk_text = ' '.join(current_chunk)
            chunk_dict = self._create_chunk_dict([chunk_text], len(chunks))
            chunks.append(chunk_dict)
        
        return chunks
    
    def _create_chunk_dict(self, sentences: List[str], chunk_id: int) -> Dict:
        """Create a chunk dictionary with text and embedding"""
        text = ' '.join(sentences)
        embedding = self.model.encode(text)
        
        return {
            'chunk_id': chunk_id,
            'text': text,
            'embedding': embedding.tolist(),
            'sentence_count': len(sentences),
            'char_count': len(text),
            'word_count': len(text.split())
        }
    
    def _split_into_sentences(self, text: str) -> List[str]:
        """Split text into sentences using simple regex"""
        # Split on sentence boundaries
        sentences = re.split(r'(?<=[.!?])\s+', text)
        # Remove empty sentences and strip whitespace
        sentences = [s.strip() for s in sentences if s.strip()]
        return sentences
    
    def get_chunk_similarity(self, chunk1: Dict, chunk2: Dict) -> float:
        """
        Calculate semantic similarity between two chunks
        
        Args:
            chunk1: First chunk dictionary
            chunk2: Second chunk dictionary
            
        Returns:
            Similarity score (0-1)
        """
        emb1 = np.array(chunk1['embedding']).reshape(1, -1)
        emb2 = np.array(chunk2['embedding']).reshape(1, -1)
        
        return cosine_similarity(emb1, emb2)[0][0]


