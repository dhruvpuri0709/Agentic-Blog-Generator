from src.states.blogstate import BlogState
from langchain_core.messages import SystemMessage, HumanMessage
from src.states.blogstate import Blog

class BlogNode:
    """
    A class to represent the blog node
    """

    def __init__(self,llm):
        self.llm= llm


    def title_creation(self,state:BlogState):
        """
        Generate title for the blog
        """
        if "topic" in state and state['topic']:
            prompt = """You are an expert blog content writer, use Markdown formatting to generate a title
                        for the blog with topic as {topic}. This title should be maximum 10 words long,
                        creative and optimized for SEO  

                        """
            
            system_message = prompt.format(topic = state['topic'])
            response = self.llm.invoke(system_message)
            return {'blog':{'title':response.content}}
    
    
    def content_generation(self, state:BlogState):
        """
        Generate content for the blog
        """

        
        prompt = """You are an expert blog content writer, use Markdown formatting to 
                    generate a detailed breakdown content for the blog based on the topic - {topic} and 
                    title - {title}
                    """
        system_message = prompt.format(topic=state['topic'], title=state['blog']['title'])
        response = self.llm.invoke(system_message)
        return {"blog": {"title": state['blog']['title'], "content": response.content}}
    
    from langchain.schema import HumanMessage

    def translation(self, state: BlogState):
        """
        Translate the content to the specified language
        """
        # Skip translation if already English
        if state['current_language'].lower() == 'english':
            return state

        # Build translation prompt
        translation_prompt = """
        Translate the following content into {current_language}.
        Return ONLY a valid JSON object with this schema:
        {{
        "title": "<translated blog title>",
        "content": "<translated blog content>"
        }}

        ORIGINAL CONTENT:
        {blog_content}
        """

        blog_content = state['blog']['content']
        messages = [
            HumanMessage(translation_prompt.format(
                current_language=state['current_language'],
                blog_content=blog_content
            ))
        ]

        # Get structured output as Blog model
        translated_content = self.llm.with_structured_output(Blog).invoke(messages)

        # Merge with existing state (don't lose topic or language)
        return {
            **state,
            "blog": {
                **state.get("blog", {}),
                "title": translated_content.title,
                "content": translated_content.content
            }
        }

    




    
    


        
