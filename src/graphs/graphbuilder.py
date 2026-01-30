from langgraph.graph import StateGraph, START, END
from src.llms.groqllm import GroqLLM
from src.states.blogstate import Blog
from src.nodes.blognode import BlogNode

class GraphBuilder:
    def __init__(self, llm):
        self.llm = llm
        self.graph = StateGraph(Blog)
    
    def build_topic_graph(self):
        """
        Build a graph to generate blogs based on topic
        """
        self.blog_node_obj = BlogNode(self.llm)
        ## Nodes

        self.graph.add_node("Orchestrator",self.blog_node_obj.Orchestrator)
        self.graph.add_node("Worker",self.blog_node_obj.Worker)
        self.graph.add_node("Synthesizer",self.blog_node_obj.Synthesizer)
        #Edges

        self.graph.add_edge(START, 'Orchestrator')
        self.graph.add_conditional_edges('Orchestrator',self.blog_node_obj.assign_workers,['Worker'])
        self.graph.add_edge('Worker','Synthesizer')
        self.graph.add_edge("Synthesizer",END)

        return self.graph
    
    # def build_language_graph(self):

    #     """
    #     Build a graph to generate a blog based on the topic and then translate it in a 
    #     different language
    #     """

    #     self.blog_node_obj = BlogNode(self.llm)
    #     ## Nodes

    #     self.graph.add_node("Title_Creation",self.blog_node_obj.title_creation)
    #     self.graph.add_node("Content_Generation",self.blog_node_obj.content_generation)
    #     self.graph.add_node("Translation",self.blog_node_obj.translation)

    #     #Edges

    #     self.graph.add_edge(START, 'Title_Creation')
    #     self.graph.add_edge('Title_Creation','Content_Generation')
    #     self.graph.add_edge('Content_Generation','Translation')
        
    #     self.graph.add_edge('Translation',END)

    #     return self.graph

    
    def setup_graph(self, usecase):
        if usecase=="topic":
            return self.build_topic_graph().compile()
        # elif usecase=='language':
        #     return self.build_language_graph().compile()

## Below code is for langsmith langgraph studio
llm = GroqLLM().get_llm()

##Get the graph
graph_builder = GraphBuilder(llm)
graph = graph_builder.build_topic_graph().compile()