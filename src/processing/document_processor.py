"""
Document Processor Module
Orchestrates document loading, chunking, and storage
"""
import json
import os
from pathlib import Path
from typing import Dict, List
from datetime import datetime
from .document_loader import DocumentLoader
from .semantic_chunker import SemanticChunker


class DocumentProcessor:
    """
    Main orchestrator for document processing pipeline
    """
    
    def __init__(self, 
                 processed_dir: str = "data/processed",
                 bert_model: str = "all-MiniLM-L6-v2",
                 similarity_threshold: float = 0.5,
                 max_chunk_size: int = 1000,
                 min_chunk_size: int = 100):
        """
        Initialize document processor
        
        Args:
            processed_dir: Directory to store processed documents
            bert_model: BERT model name for embeddings
            similarity_threshold: Threshold for semantic chunking
            max_chunk_size: Maximum chunk size in characters
            min_chunk_size: Minimum chunk size in characters
        """
        self.loader = DocumentLoader()
        self.chunker = SemanticChunker(
            model_name=bert_model,
            similarity_threshold=similarity_threshold,
            max_chunk_size=max_chunk_size,
            min_chunk_size=min_chunk_size
        )
        self.processed_dir = Path(processed_dir)
        self.processed_dir.mkdir(parents=True, exist_ok=True)
    
    def process_document(self, 
                         file_path: str, 
                         chunking_method: str = 'semantic') -> Dict:
        """
        Process a document: load, chunk, and store
        
        Args:
            file_path: Path to document file
            chunking_method: 'semantic', 'sentence', or 'fixed'
            
        Returns:
            Processing results dictionary
        """
        # Load document
        print(f"Loading document: {file_path}")
        doc_metadata = self.loader.load_file(file_path)
        
        # Chunk text
        print(f"Chunking text using {chunking_method} method...")
        chunks = self.chunker.chunk_text(doc_metadata['text'], method=chunking_method)
        
        # Create processed document data
        processed_data = {
            'metadata': {
                'filename': doc_metadata['filename'],
                'file_path': doc_metadata['file_path'],
                'file_type': doc_metadata['file_type'],
                'file_size': doc_metadata['file_size'],
                'processed_at': datetime.now().isoformat(),
                'chunking_method': chunking_method,
                'total_chunks': len(chunks),
                'total_words': doc_metadata['word_count'],
                'total_chars': doc_metadata['text_length']
            },
            'chunks': chunks
        }
        
        # Save processed document
        output_path = self._save_processed_document(processed_data)
        processed_data['output_path'] = str(output_path)
        
        print(f"✅ Processing complete! Created {len(chunks)} chunks")
        
        return processed_data
    
    def _save_processed_document(self, data: Dict) -> Path:
        """Save processed document to JSON file"""
        filename = data['metadata']['filename']
        # Create safe filename
        safe_filename = filename.replace(' ', '_').replace('.', '_')
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_filename = f"{safe_filename}_{timestamp}.json"
        output_path = self.processed_dir / output_filename
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        return output_path
    
    def load_processed_document(self, file_path: str) -> Dict:
        """Load a previously processed document"""
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def list_processed_documents(self) -> List[Dict]:
        """List all processed documents"""
        processed_files = []
        
        for file_path in self.processed_dir.glob('*.json'):
            try:
                data = self.load_processed_document(file_path)
                processed_files.append({
                    'file_path': str(file_path),
                    'filename': data['metadata']['filename'],
                    'processed_at': data['metadata']['processed_at'],
                    'total_chunks': data['metadata']['total_chunks'],
                    'chunking_method': data['metadata']['chunking_method']
                })
            except Exception as e:
                print(f"Error loading {file_path}: {e}")
        
        # Sort by processed date (newest first)
        processed_files.sort(key=lambda x: x['processed_at'], reverse=True)
        
        return processed_files
    
    def get_document_stats(self, processed_data: Dict) -> Dict:
        """Get statistics about a processed document"""
        chunks = processed_data['chunks']
        
        if not chunks:
            return {}
        
        chunk_sizes = [chunk['char_count'] for chunk in chunks]
        word_counts = [chunk['word_count'] for chunk in chunks]
        
        return {
            'total_chunks': len(chunks),
            'avg_chunk_size': sum(chunk_sizes) / len(chunks),
            'min_chunk_size': min(chunk_sizes),
            'max_chunk_size': max(chunk_sizes),
            'avg_words_per_chunk': sum(word_counts) / len(chunks),
            'total_words': sum(word_counts),
            'total_chars': sum(chunk_sizes)
        }
    
    def search_chunks(self, processed_data: Dict, query: str, top_k: int = 5) -> List[Dict]:
        """
        Search for relevant chunks using semantic similarity
        
        Args:
            processed_data: Processed document data
            query: Search query
            top_k: Number of top results to return
            
        Returns:
            List of most relevant chunks with similarity scores
        """
        # Get query embedding
        query_embedding = self.chunker.model.encode(query)
        
        # Calculate similarities
        results = []
        for chunk in processed_data['chunks']:
            similarity = self._calculate_similarity(
                query_embedding, 
                chunk['embedding']
            )
            results.append({
                **chunk,
                'similarity': float(similarity)
            })
        
        # Sort by similarity and return top_k
        results.sort(key=lambda x: x['similarity'], reverse=True)
        return results[:top_k]
    
    def _calculate_similarity(self, emb1, emb2):
        """Calculate cosine similarity between two embeddings"""
        import numpy as np
        from sklearn.metrics.pairwise import cosine_similarity
        
        emb1 = np.array(emb1).reshape(1, -1)
        emb2 = np.array(emb2).reshape(1, -1)
        
        return cosine_similarity(emb1, emb2)[0][0]


