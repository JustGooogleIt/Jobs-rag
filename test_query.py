#!/usr/bin/env python3

from query_rag import run_query

def test_jobs_ai():
    """Test the Steve Jobs AI with a sample question"""
    
    test_questions = [
        "How should I approach product design?",
        "What's your advice on hiring?", 
        "How do you deal with failure?"
    ]
    
    print("🧠 Testing Steve Jobs RAG Chatbot\n" + "="*50)
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n{i}. Question: {question}")
        print("-" * 40)
        
        try:
            result = run_query(question, include_sources=True)
            print(f"Jobs-AI says:\n{result['answer']}\n")
            
            if result.get("sources"):
                print("Sources:")
                for source in result["sources"]:
                    print(f"- {source}")
            else:
                print("No sources available (offline mode)")
                
        except Exception as e:
            print(f"Error: {e}")
        
        print("\n" + "="*50)

if __name__ == "__main__":
    test_jobs_ai()