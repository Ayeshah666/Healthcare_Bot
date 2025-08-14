import openai
import re
from typing import Optional

class HealthChatbot:
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo"):
        """
        Initialize the chatbot with API key and model
        
        Args:
            api_key: OpenAI API key
            model: Which LLM model to use (default: gpt-3.5-turbo)
        """
        openai.api_key = api_key
        self.model = model
        self.safety_keywords = [
            "prescribe", "diagnose", "treatment", "take this", 
            "you should take", "medical advice", "you need", 
            "you must", "emergency", "immediately"
        ]
        self.disclaimer = (
            "\n\nDisclaimer: I am an AI assistant providing general health information. "
            "My responses are not medical advice. Please consult a qualified healthcare "
            "professional for personal medical concerns."
        )

    def _contains_unsafe_content(self, text: str) -> bool:
        """
        Check if response contains potentially unsafe medical advice
        
        Args:
            text: The response text to check
            
        Returns:
            bool: True if unsafe content detected
        """
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in self.safety_keywords)

    def _sanitize_response(self, response: str) -> str:
        """
        Clean up the response and add disclaimer if needed
        
        Args:
            response: The raw response from the LLM
            
        Returns:
            str: Sanitized response
        """
        # Remove any markdown formatting
        response = re.sub(r'\*\*|\*|`', '', response)
        
        # Add disclaimer if response seems like medical advice
        if self._contains_unsafe_content(response):
            response = f"{response}{self.disclaimer}"
            
        return response.strip()

    def generate_response(self, query: str, temperature: float = 0.7) -> Optional[str]:
        """
        Generate a response to a health query
        
        Args:
            query: The user's health question
            temperature: Controls randomness (0-1)
            
        Returns:
            str: The generated response or None if error
        """
        try:
            # Carefully engineered prompt
            system_prompt = (
                "You are MediBot, a friendly and cautious AI health assistant. "
                "Your role is to provide general health information while being "
                "extremely careful not to give medical advice. Follow these rules:\n"
                "1. Be informative but never diagnostic\n"
                "2. Only share publicly available health facts\n"
                "3. Always suggest consulting a doctor for personal concerns\n"
                "4. Use simple, clear language suitable for non-experts\n"
                "5. If unsure, say you don't know\n"
                "6. Keep responses under 150 words unless more detail is specifically requested"
            )
            
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": query}
                ],
                temperature=temperature,
                max_tokens=300
            )
            
            return self._sanitize_response(response.choices[0].message['content'])
            
        except Exception as e:
            print(f"Error generating response: {e}")
            return None

    def chat_loop(self):
        """Run an interactive chat session"""
        print("MediBot: Hello! I'm your health information assistant. Ask me general health questions.")
        print("Type 'quit' to exit.\n")
        
        while True:
            try:
                user_input = input("You: ")
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print("MediBot: Stay healthy! Goodbye.")
                    break
                    
                if not user_input.strip():
                    continue
                    
                response = self.generate_response(user_input)
                if response:
                    print(f"\nMediBot: {response}\n")
                else:
                    print("MediBot: I encountered an error. Please try again.")
                    
            except KeyboardInterrupt:
                print("\nMediBot: Goodbye!")
                break


# Example usage
if __name__ == "__main__":
    # Initialize with your OpenAI API key
    # Get one at: https://platform.openai.com/api-keys
    API_KEY = "your-api-key-here"  # Replace with your actual key
    
    bot = HealthChatbot(API_KEY)
    
    # Run in interactive mode
    bot.chat_loop()
    
    # Or test specific queries
    # print(bot.generate_response("What causes a sore throat?"))
    # print(bot.generate_response("Is paracetamol safe for children?"))