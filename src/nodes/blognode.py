from src.states.blogstate import Sections, Blog, WorkerState
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_groq import ChatGroq
from langgraph.types import Send

class BlogNode:
    """
    A class to represent the blog node
    """

    def __init__(self,llm:ChatGroq):
        self.llm= llm


    def Orchestrator(self,state:Blog):
        """
        Generate title and sections for the blog
        """
        if "topic" in state and state['topic']:
            prompt = """You are an expert blog content writer, use Markdown formatting to generate a title
                        for the blog with topic as {topic}. This title should be maximum 10 words long,
                        creative and optimized for SEO  

                        """
            planner_llm = self.llm.with_structured_output(Sections)
            
            plan = planner_llm.invoke([
                SystemMessage("""Generate a title and plan for the blog with optimal number of sections
                              the title should be optimized for SEO and do not make the blog very long"""),
                HumanMessage(f"Here is the topic for the blog {state['topic']}")
            ])
            
            return {'title':plan.title, 'sections':plan.sections}
    
    
    def Worker(self, state:WorkerState):
        
        """ Generate content for the blog section """

        
        prompt = """You are an expert blog content writer, generate a short and concise detailed breakdown content for
                    the blog section using its title - {title} and its brief description - {description}, it should not be more
                    than a few lines.
                    """
        system_message = prompt.format(title=state['section'].title, description=state['section'].description)
        response = self.llm.invoke(system_message)
        return {"completed_sections":[response.content]}
    
    # Conditional edge function to create llm workers that each write a section of the report 
    def assign_workers(self,state:Blog):
        """ Assign a worker to each section in the plan """
        
        return [Send("Worker",{"section": s}) for s in state['sections']]
    
    def Synthesizer(self,state:Blog):
        
        completed_sections = "\n\n---\n\n".join(state['completed_sections'])
        
        response = self.llm.invoke([
            SystemMessage("You are a synthesizer node, convert the blog given to you into markdown format"),
            HumanMessage(f"Here is the blog {completed_sections}")
        ])
        
        return {"final_blog":response.content}
        
    
    
    

    # def translation(self, state: BlogState):
    #     """
    #     Translate the content to the specified language
    #     """
    #     # Skip translation if already English
    #     if state['current_language'].lower() == 'english':
    #         return state

    #     # Build translation prompt
    #     translation_prompt = """
    #     Translate the following content into {current_language}.
    #     Return ONLY a valid JSON object with this schema:
    #     {{
    #     "title": "<translated blog title>",
    #     "content": "<translated blog content>"
    #     }}

    #     ORIGINAL CONTENT:
    #     {blog_content}
    #     """

    #     blog_content = state['blog']['content']
    #     messages = [
    #         HumanMessage(translation_prompt.format(
    #             current_language=state['current_language'],
    #             blog_content=blog_content
    #         ))
    #     ]

    #     # Get structured output as Blog model
    #     translated_content = self.llm.with_structured_output(Blog).invoke(messages)

    #     # Merge with existing state (don't lose topic or language)
    #     return {
    #         **state,
    #         "blog": {
    #             **state.get("blog", {}),
    #             "title": translated_content.title,
    #             "content": translated_content.content
    #         }
    #     }

    




    
    


        
