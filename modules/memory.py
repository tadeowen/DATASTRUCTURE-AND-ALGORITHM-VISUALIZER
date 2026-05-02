import sys

class MemoryTracker:
    
    @staticmethod
    def get_size_of(obj):
        """Return approximate memory size of object (in bytes)"""
        if obj is None:
            return 0
        
        # Basic Python object overhead
        size = sys.getsizeof(obj)
        
        # For containers, add size of items recursively
        if isinstance(obj, (list, tuple, set)):
            size += sum(MemoryTracker.get_size_of(item) for item in obj)
        elif isinstance(obj, dict):
            size += sum(MemoryTracker.get_size_of(k) + MemoryTracker.get_size_of(v) 
                       for k, v in obj.items())
        
        return size

    @staticmethod
    def get_ds_memory_usage(ds_instance):
        """Return memory usage info for any data structure"""
        try:
            structure_name = ds_instance.__class__.__name__
            
            # Get the actual data
            if hasattr(ds_instance, 'display'):
                data = ds_instance.display()
            else:
                data = []

            raw_size = MemoryTracker.get_size_of(data)
            
            # Estimate node overhead for Linked Lists and Trees
            if "Linked" in structure_name or "List" in structure_name:
                node_overhead = len(data) * 40   # approx 40 bytes per node (pointers)
                total = raw_size + node_overhead
            elif "Stack" in structure_name or "Queue" in structure_name:
                total = raw_size + len(data) * 32
            else:
                total = raw_size

            return {
                'structure': structure_name,
                'elements': len(data),
                'memory_bytes': total,
                'memory_kb': round(total / 1024, 3),
                'memory_mb': round(total / (1024*1024), 5)
            }
        except:
            return {'structure': 'Unknown', 'memory_bytes': 0, 'memory_kb': 0}