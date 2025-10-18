"""
FAISS Vector Store
Handles vector storage, indexing, and similarity search using FAISS
"""
import faiss
import numpy as np
import pickle
import json
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from datetime import datetime


class FAISSVectorStore:
    """
    Vector store using FAISS for efficient similarity search
    """
    
    def __init__(self, 
                 dimension: int = 384,
                 index_type: str = "Flat",
                 metric: str = "L2"):
        """
        Initialize FAISS vector store
        
        Args:
            dimension: Dimension of embeddings (384 for MiniLM, 768 for MPNet)
            index_type: FAISS index type ('Flat', 'IVF', 'HNSW')
            metric: Distance metric ('L2' or 'IP' for inner product/cosine)
        """
        self.dimension = dimension
        self.index_type = index_type
        self.metric = metric
        
        # Create FAISS index
        self.index = self._create_index()
        
        # Store metadata for each vector
        self.metadata = []  # List of dicts with chunk info
        self.doc_chunks = {}  # Map doc_id -> list of chunk indices
        
        # Statistics
        self.stats = {
            'total_vectors': 0,
            'total_documents': 0,
            'created_at': datetime.now().isoformat(),
            'last_updated': datetime.now().isoformat()
        }
    
    def _create_index(self) -> faiss.Index:
        """Create FAISS index based on type"""
        if self.index_type == "Flat":
            # Exact search, slowest but most accurate
            if self.metric == "L2":
                return faiss.IndexFlatL2(self.dimension)
            else:  # Inner Product (for cosine similarity with normalized vectors)
                return faiss.IndexFlatIP(self.dimension)
        
        elif self.index_type == "IVF":
            # Inverted file index, faster approximate search
            nlist = 100  # number of clusters
            quantizer = faiss.IndexFlatL2(self.dimension)
            if self.metric == "L2":
                index = faiss.IndexIVFFlat(quantizer, self.dimension, nlist)
            else:
                index = faiss.IndexIVFFlat(quantizer, self.dimension, nlist, faiss.METRIC_INNER_PRODUCT)
            return index
        
        elif self.index_type == "HNSW":
            # Hierarchical Navigable Small World, very fast approximate search
            M = 32  # number of connections per layer
            index = faiss.IndexHNSWFlat(self.dimension, M)
            return index
        
        else:
            raise ValueError(f"Unknown index type: {self.index_type}")
    
    def add_vectors(self, 
                    embeddings: np.ndarray, 
                    metadata: List[Dict],
                    doc_id: Optional[str] = None) -> List[int]:
        """
        Add vectors to the index
        
        Args:
            embeddings: numpy array of shape (n, dimension)
            metadata: list of metadata dicts for each vector
            doc_id: optional document ID to group chunks
            
        Returns:
            List of vector IDs (indices in the index)
        """
        # Ensure embeddings are float32
        embeddings = np.array(embeddings, dtype=np.float32)
        
        # Normalize vectors if using inner product (for cosine similarity)
        if self.metric == "IP":
            faiss.normalize_L2(embeddings)
        
        # Get starting index
        start_idx = self.index.ntotal
        
        # Add to FAISS index
        self.index.add(embeddings)
        
        # Store metadata
        vector_ids = []
        for i, meta in enumerate(metadata):
            idx = start_idx + i
            meta['vector_id'] = idx
            meta['added_at'] = datetime.now().isoformat()
            self.metadata.append(meta)
            vector_ids.append(idx)
        
        # Track document chunks
        if doc_id:
            if doc_id not in self.doc_chunks:
                self.doc_chunks[doc_id] = []
                self.stats['total_documents'] += 1
            self.doc_chunks[doc_id].extend(vector_ids)
        
        # Update statistics
        self.stats['total_vectors'] = self.index.ntotal
        self.stats['last_updated'] = datetime.now().isoformat()
        
        return vector_ids
    
    def search(self, 
               query_embedding: np.ndarray,
               k: int = 5,
               filter_doc_id: Optional[str] = None) -> List[Dict]:
        """
        Search for similar vectors
        
        Args:
            query_embedding: Query vector
            k: Number of results to return
            filter_doc_id: Optional document ID to filter results
            
        Returns:
            List of dicts with similarity scores and metadata
        """
        # Ensure query is float32 and 2D
        query_embedding = np.array(query_embedding, dtype=np.float32).reshape(1, -1)
        
        # Normalize if using inner product
        if self.metric == "IP":
            faiss.normalize_L2(query_embedding)
        
        # Search
        if filter_doc_id and filter_doc_id in self.doc_chunks:
            # Filter by document
            doc_indices = self.doc_chunks[filter_doc_id]
            # Search more to account for filtering
            distances, indices = self.index.search(query_embedding, min(k * 3, self.index.ntotal))
            
            # Filter results
            results = []
            for dist, idx in zip(distances[0], indices[0]):
                if idx in doc_indices and len(results) < k:
                    results.append({
                        'vector_id': int(idx),
                        'distance': float(dist),
                        'similarity': self._distance_to_similarity(float(dist)),
                        **self.metadata[idx]
                    })
        else:
            # Regular search
            distances, indices = self.index.search(query_embedding, k)
            
            results = []
            for dist, idx in zip(distances[0], indices[0]):
                if idx >= 0 and idx < len(self.metadata):  # Valid index
                    results.append({
                        'vector_id': int(idx),
                        'distance': float(dist),
                        'similarity': self._distance_to_similarity(float(dist)),
                        **self.metadata[idx]
                    })
        
        return results
    
    def _distance_to_similarity(self, distance: float) -> float:
        """Convert distance to similarity score (0-1)"""
        if self.metric == "IP":
            # Inner product is already similarity
            return distance
        else:
            # L2 distance to similarity (higher distance = lower similarity)
            return 1.0 / (1.0 + distance)
    
    def get_by_id(self, vector_id: int) -> Optional[Dict]:
        """Get metadata for a specific vector ID"""
        if 0 <= vector_id < len(self.metadata):
            return self.metadata[vector_id]
        return None
    
    def get_document_chunks(self, doc_id: str) -> List[Dict]:
        """Get all chunks for a document"""
        if doc_id not in self.doc_chunks:
            return []
        
        return [self.metadata[idx] for idx in self.doc_chunks[doc_id]]
    
    def list_documents(self) -> List[str]:
        """List all document IDs in the store"""
        return list(self.doc_chunks.keys())
    
    def remove_document(self, doc_id: str) -> bool:
        """
        Remove a document and its chunks
        Note: FAISS doesn't support deletion, so this marks as deleted in metadata
        """
        if doc_id not in self.doc_chunks:
            return False
        
        # Mark chunks as deleted in metadata
        for idx in self.doc_chunks[doc_id]:
            if idx < len(self.metadata):
                self.metadata[idx]['deleted'] = True
        
        # Remove from doc_chunks
        del self.doc_chunks[doc_id]
        self.stats['total_documents'] -= 1
        self.stats['last_updated'] = datetime.now().isoformat()
        
        return True
    
    def save(self, path: str):
        """Save index and metadata to disk"""
        path = Path(path)
        path.mkdir(parents=True, exist_ok=True)
        
        # Save FAISS index
        index_path = path / "index.faiss"
        faiss.write_index(self.index, str(index_path))
        
        # Save metadata and stats
        data = {
            'metadata': self.metadata,
            'doc_chunks': self.doc_chunks,
            'stats': self.stats,
            'dimension': self.dimension,
            'index_type': self.index_type,
            'metric': self.metric
        }
        
        metadata_path = path / "metadata.pkl"
        with open(metadata_path, 'wb') as f:
            pickle.dump(data, f)
        
        # Save human-readable stats
        stats_path = path / "stats.json"
        with open(stats_path, 'w') as f:
            json.dump(self.stats, f, indent=2)
        
        print(f"✅ Vector store saved to {path}")
    
    @classmethod
    def load(cls, path: str) -> 'FAISSVectorStore':
        """Load index and metadata from disk"""
        path = Path(path)
        
        # Load metadata first to get configuration
        metadata_path = path / "metadata.pkl"
        with open(metadata_path, 'rb') as f:
            data = pickle.load(f)
        
        # Create instance with saved configuration
        store = cls(
            dimension=data['dimension'],
            index_type=data['index_type'],
            metric=data['metric']
        )
        
        # Load FAISS index
        index_path = path / "index.faiss"
        store.index = faiss.read_index(str(index_path))
        
        # Restore metadata and stats
        store.metadata = data['metadata']
        store.doc_chunks = data['doc_chunks']
        store.stats = data['stats']
        
        print(f"✅ Vector store loaded from {path}")
        print(f"   Vectors: {store.stats['total_vectors']}, Documents: {store.stats['total_documents']}")
        
        return store
    
    def get_stats(self) -> Dict:
        """Get statistics about the vector store"""
        return {
            **self.stats,
            'dimension': self.dimension,
            'index_type': self.index_type,
            'metric': self.metric,
            'documents': len(self.doc_chunks)
        }
    
    def reset(self):
        """Reset the vector store (clear all data)"""
        self.index = self._create_index()
        self.metadata = []
        self.doc_chunks = {}
        self.stats = {
            'total_vectors': 0,
            'total_documents': 0,
            'created_at': datetime.now().isoformat(),
            'last_updated': datetime.now().isoformat()
        }


