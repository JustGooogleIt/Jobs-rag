#!/usr/bin/env python3

from query_rag import run_query

try:
    result = run_query("What's your advice on product design?", include_sources=True)
    print("Success!")
    print(f"Answer: {result['answer']}")
    if result.get('sources'):
        print(f"Sources: {result['sources']}")
except Exception as e:
    print(f"Detailed error: {e}")
    import traceback
    traceback.print_exc()