import wandb
from crewai.tools import BaseTool
import os
from app.config import settings
import requests
from typing import Dict, Any, List, Optional
from pydantic import Field
import openai
import weave

class WeightsBiasesLLMTool(BaseTool):
    name: str = "Weights & Biases LLM Tool"
    description: str = "Generate text using hosted LLM models"
    api_key: str = Field(default_factory=lambda: settings.WANDB_API_KEY)
    client: Optional[Any] = Field(default=None, exclude=True)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.api_key and self.api_key != "your_wandb_api_key_here":
            try:
                # Initialize Weave for logging LLM calls to W&B
                weave.init("crewai/memewars")
                
                # Initialize OpenAI client with W&B inference
                self.client = openai.OpenAI(
                    base_url='https://api.inference.wandb.ai/v1',
                    api_key=self.api_key,
                    project="crewai/memewars",
                )
                print("✅ W&B Inference client initialized successfully")
            except Exception as e:
                print(f"Warning: Could not initialize W&B client: {e}")
                self.client = None
        else:
            self.client = None
    
    def _run(self, prompt: str, model: str = "deepseek-ai/DeepSeek-R1-0528", max_tokens: int = 150) -> str:
        """Generate text using W&B hosted models or fallback to OpenAI"""
        try:
            # Use W&B inference if available
            if self.client:
                response = self.client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": "You are a creative comedy writer specializing in meme captions and internet humor."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=max_tokens,
                    temperature=0.8
                )
                return response.choices[0].message.content
            else:
                # Fallback to OpenAI if W&B is not configured
                return self._fallback_generation(prompt, max_tokens)
            
        except Exception as e:
            return f"Error generating text: {str(e)}"
    
    def _fallback_generation(self, prompt: str, max_tokens: int) -> str:
        """Fallback to OpenAI if W&B is not available"""
        if not settings.OPENAI_API_KEY or settings.OPENAI_API_KEY == "your_openai_api_key_here":
            return "API key not configured for text generation"
        
        try:
            import openai
            openai.api_key = settings.OPENAI_API_KEY
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a creative comedy writer specializing in meme captions and internet humor."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=0.8
            )
            
            return response.choices[0].message.content
        except Exception as e:
            return f"Fallback generation failed: {str(e)}"
    
    async def generate_caption(self, template_context: str, theme: str, tone: str = "sarcastic") -> str:
        """Generate a meme caption based on template and theme"""
        prompt = f"""
        Template context: {template_context}
        Theme: {theme}
        Tone: {tone}
        
        Generate a funny, {tone} meme caption that fits this template and theme.
        Keep it concise and punchy.
        """
        
        return self._run(prompt, max_tokens=100)
    
    async def generate_multiple_captions(self, template_context: str, theme: str, 
                                       tone: str = "sarcastic", count: int = 3) -> List[str]:
        """Generate multiple caption options"""
        captions = []
        for i in range(count):
            caption = await self.generate_caption(template_context, theme, tone)
            captions.append(caption)
        return captions 