"""
Vector Database Manager
Manages multiple vector store collections and provides unified interface
"""
from pathlib import Path
from typing import List, Dict, Optional
import json
from datetime import datetime
from .vector_store import FAISSVectorStore


class VectorDBManager:
    """
    Manages multiple FAISS vector stores (collections)
    """
    
    def __init__(self, base_path: str = "data/vector_db"):
        """
        Initialize vector database manager
        
        Args:
            base_path: Base directory for storing vector databases
        """
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)
        
        # Track active collections
        self.collections = {}  # name -> VectorStore instance
        self.collections_info = self._load_collections_info()
    
    def _load_collections_info(self) -> Dict:
        """Load information about available collections"""
        info_path = self.base_path / "collections.json"
        
        if info_path.exists():
            with open(info_path, 'r') as f:
                return json.load(f)
        
        return {}
    
    def _save_collections_info(self):
        """Save collections information"""
        info_path = self.base_path / "collections.json"
        
        with open(info_path, 'w') as f:
            json.dump(self.collections_info, f, indent=2)
    
    def create_collection(self,
                         name: str,
                         dimension: int = 384,
                         index_type: str = "Flat",
                         metric: str = "L2",
                         description: str = "") -> FAISSVectorStore:
        """
        Create a new vector store collection
        
        Args:
            name: Collection name
            dimension: Embedding dimension
            index_type: FAISS index type
            metric: Distance metric
            description: Collection description
            
        Returns:
            FAISSVectorStore instance
        """
        if name in self.collections:
            raise ValueError(f"Collection '{name}' already exists")
        
        # Create vector store
        store = FAISSVectorStore(
            dimension=dimension,
            index_type=index_type,
            metric=metric
        )
        
        # Store in memory
        self.collections[name] = store
        
        # Save metadata
        self.collections_info[name] = {
            'created_at': datetime.now().isoformat(),
            'last_updated': datetime.now().isoformat(),
            'dimension': dimension,
            'index_type': index_type,
            'metric': metric,
            'description': description,
            'path': str(self.base_path / name)
        }
        
        self._save_collections_info()
        
        return store
    
    def get_collection(self, name: str, auto_load: bool = True) -> Optional[FAISSVectorStore]:
        """
        Get a collection by name
        
        Args:
            name: Collection name
            auto_load: Automatically load from disk if not in memory
            
        Returns:
            FAISSVectorStore instance or None
        """
        # Check if already loaded
        if name in self.collections:
            return self.collections[name]
        
        # Try to load from disk
        if auto_load and name in self.collections_info:
            collection_path = Path(self.collections_info[name]['path'])
            
            if collection_path.exists():
                store = FAISSVectorStore.load(str(collection_path))
                self.collections[name] = store
                return store
        
        return None
    
    def list_collections(self) -> List[Dict]:
        """List all available collections"""
        collections = []
        
        for name, info in self.collections_info.items():
            # Get current stats if loaded
            if name in self.collections:
                stats = self.collections[name].get_stats()
            else:
                # Try to load stats from disk
                stats_path = Path(info['path']) / "stats.json"
                if stats_path.exists():
                    with open(stats_path, 'r') as f:
                        stats = json.load(f)
                else:
                    stats = {}
            
            collections.append({
                'name': name,
                'description': info.get('description', ''),
                'dimension': info.get('dimension', 384),
                'index_type': info.get('index_type', 'Flat'),
                'created_at': info.get('created_at', ''),
                'last_updated': info.get('last_updated', ''),
                'total_vectors': stats.get('total_vectors', 0),
                'total_documents': stats.get('total_documents', 0),
                'loaded': name in self.collections
            })
        
        return collections
    
    def save_collection(self, name: str):
        """Save a collection to disk"""
        if name not in self.collections:
            raise ValueError(f"Collection '{name}' not found in memory")
        
        collection_path = self.base_path / name
        self.collections[name].save(str(collection_path))
        
        # Update last_updated
        if name in self.collections_info:
            self.collections_info[name]['last_updated'] = datetime.now().isoformat()
            self._save_collections_info()
    
    def delete_collection(self, name: str):
        """Delete a collection"""
        # Remove from memory
        if name in self.collections:
            del self.collections[name]
        
        # Remove files
        if name in self.collections_info:
            collection_path = Path(self.collections_info[name]['path'])
            
            if collection_path.exists():
                import shutil
                shutil.rmtree(collection_path)
            
            # Remove from info
            del self.collections_info[name]
            self._save_collections_info()
    
    def add_document(self,
                    collection_name: str,
                    doc_id: str,
                    chunks: List[Dict]) -> bool:
        """
        Add document chunks to a collection
        
        Args:
            collection_name: Name of the collection
            doc_id: Document ID
            chunks: List of chunk dicts with 'embedding' and metadata
            
        Returns:
            Success status
        """
        collection = self.get_collection(collection_name)
        
        if collection is None:
            raise ValueError(f"Collection '{collection_name}' not found")
        
        # Extract embeddings and metadata
        embeddings = []
        metadata = []
        
        for chunk in chunks:
            if 'embedding' in chunk:
                embeddings.append(chunk['embedding'])
                
                # Create metadata without embedding (to save space)
                meta = {k: v for k, v in chunk.items() if k != 'embedding'}
                meta['doc_id'] = doc_id
                metadata.append(meta)
        
        if not embeddings:
            return False
        
        # Add to collection
        import numpy as np
        embeddings_array = np.array(embeddings, dtype=np.float32)
        collection.add_vectors(embeddings_array, metadata, doc_id=doc_id)
        
        return True
    
    def search(self,
              collection_name: str,
              query_embedding: List[float],
              k: int = 5,
              filter_doc_id: Optional[str] = None) -> List[Dict]:
        """
        Search in a collection
        
        Args:
            collection_name: Name of the collection
            query_embedding: Query embedding vector
            k: Number of results
            filter_doc_id: Optional document ID to filter
            
        Returns:
            List of search results
        """
        collection = self.get_collection(collection_name)
        
        if collection is None:
            raise ValueError(f"Collection '{collection_name}' not found")
        
        import numpy as np
        query_array = np.array(query_embedding, dtype=np.float32)
        
        return collection.search(query_array, k=k, filter_doc_id=filter_doc_id)
    
    def get_collection_stats(self, name: str) -> Dict:
        """Get statistics for a collection"""
        collection = self.get_collection(name)
        
        if collection is None:
            return {}
        
        return collection.get_stats()
    
    def get_document_chunks(self, collection_name: str, doc_id: str) -> List[Dict]:
        """Get all chunks for a document"""
        collection = self.get_collection(collection_name)
        
        if collection is None:
            return []
        
        return collection.get_document_chunks(doc_id)


