#!/usr/bin/env python3
"""
Script to extract MongoDB schema for the 'events' collection.
Shows unique values for fields with 10 or fewer unique values.
"""

import os
from pymongo import MongoClient
from dotenv import load_dotenv
from collections import defaultdict
from typing import Any, Dict, Set

# Load environment variables from .env file
load_dotenv()

def get_type_name(value: Any) -> str:
    """Get a human-readable type name for a value."""
    if value is None:
        return "null"
    elif isinstance(value, bool):
        return "boolean"
    elif isinstance(value, int):
        return "integer"
    elif isinstance(value, float):
        return "number"
    elif isinstance(value, str):
        return "string"
    elif isinstance(value, list):
        return "array"
    elif isinstance(value, dict):
        return "object"
    else:
        return type(value).__name__

def analyze_collection_schema(collection, sample_size: int = 10000):
    """
    Analyze the schema of a MongoDB collection.
    
    Args:
        collection: MongoDB collection object
        sample_size: Number of documents to sample for schema analysis
    
    Returns:
        Dictionary with field information including types and unique values
    """
    field_info = defaultdict(lambda: {
        'types': set(),
        'unique_values': set(),
        'count': 0,
        'null_count': 0
    })
    
    # Sample documents from the collection
    documents = list(collection.find().limit(sample_size))
    total_docs = len(documents)
    
    if total_docs == 0:
        return {}, 0
    
    # Analyze each document
    for doc in documents:
        for field, value in doc.items():
            field_info[field]['count'] += 1
            field_info[field]['types'].add(get_type_name(value))
            
            if value is None:
                field_info[field]['null_count'] += 1
            else:
                # Only track unique values if we haven't exceeded the limit yet
                if len(field_info[field]['unique_values']) <= 10:
                    # Convert unhashable types to strings for storage
                    if isinstance(value, (dict, list)):
                        field_info[field]['unique_values'].add(str(value))
                    else:
                        field_info[field]['unique_values'].add(value)
    
    return field_info, total_docs

def format_schema_output(field_info: Dict, total_docs: int, collection_name: str):
    """
    Format the schema information as a readable string.
    
    Args:
        field_info: Dictionary with field information
        total_docs: Total number of documents analyzed
        collection_name: Name of the collection
    
    Returns:
        Formatted string describing the schema
    """
    output_lines = []
    output_lines.append("=" * 80)
    output_lines.append(f"Schema Analysis for Collection: {collection_name}")
    output_lines.append(f"Documents Analyzed: {total_docs}")
    output_lines.append("=" * 80)
    output_lines.append("")
    
    # Sort fields alphabetically
    sorted_fields = sorted(field_info.items())
    
    for field_name, info in sorted_fields:
        output_lines.append(f"Field: {field_name}")
        output_lines.append(f"  Present in: {info['count']}/{total_docs} documents ({info['count']/total_docs*100:.1f}%)")
        
        # Show types
        types_str = ", ".join(sorted(info['types']))
        output_lines.append(f"  Type(s): {types_str}")
        
        # Show null count if applicable
        if info['null_count'] > 0:
            output_lines.append(f"  Null values: {info['null_count']}")
        
        # Show unique values if 15 or fewer
        unique_count = len(info['unique_values'])
        if unique_count <= 15 and unique_count > 0:
            output_lines.append(f"  Unique values ({unique_count}):")
            for value in sorted(info['unique_values'], key=str):
                # Truncate very long values for display
                value_str = str(value)
                if len(value_str) > 100:
                    value_str = value_str[:97] + "..."
                output_lines.append(f"    - {value_str}")
        else:
            output_lines.append(f"  Unique values: {unique_count} (> 10, treated as string)")
        
        output_lines.append("")
    
    return "\n".join(output_lines)

def main():
    """Main function to extract and save schema to file."""
    # Get MongoDB connection string and database name from environment
    connection_string = os.getenv("MDB_MCP_CONNECTION_STRING")
    database_name = os.getenv("MDB_MCP_DATABASE")
    output_file = "events_schema.txt"
    
    if not connection_string:
        print("Error: MDB_MCP_CONNECTION_STRING not found in .env file")
        return
    
    if not database_name:
        print("Error: MDB_MCP_DATABASE not found in .env file")
        return
    
    try:
        # Connect to MongoDB
        print(f"Connecting to MongoDB...")
        client = MongoClient(connection_string)
        db = client[database_name]
        collection = db["events"]
        
        # Check if collection exists
        if "events" not in db.list_collection_names():
            print(f"Warning: Collection 'events' does not exist in database '{database_name}'")
            return
        
        print(f"Analyzing schema for collection 'events'...")
        
        # Analyze the schema
        field_info, total_docs = analyze_collection_schema(collection)
        
        if total_docs == 0:
            print("Collection 'events' is empty.")
            return
        
        # Format the output
        output = format_schema_output(field_info, total_docs, "events")
        
        # Write to file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(output)
        
        print(f"✓ Schema analysis complete!")
        print(f"✓ Results saved to: {output_file}")
        
        # Close the connection
        client.close()
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

