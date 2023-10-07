# functionality defining the shape and properties of computation nodes, and how
# they connect to each other in pipelines
from abc import ABC, abstractclassmethod
import re
from typing import Dict

from vectorshift.consts import *

# A parent class for all nodes. Shouldn't be initialized by the user directly.
class NodeTemplate(ABC):
    # __init__ should place NodeOutput args last (before optional args)
    # TODO: think about where we might want to use @property.
    def __init__(self):
        # Each node has a certain type, also called an "ID" in Mongo. The _id
        # of the node is formed by appending a counter to the node type.
        self.node_type:str = None
        self._id:str = None
        # Every node has zero or more inputs or outputs.
        self._inputs:Dict[str, NodeOutput] = {}
        
    # Inputs are a dictionary of NodeOutputs keyed by input fields (the in-edge 
    # labels in the no-code graph/the target handle for the node's in-edge).
    def inputs(self): return self._inputs
    # Outputs should be a dictionary of NodeOutputs keyed by output fields (the
    # out-edge labels/the source handle for the node's out-edge). Invariant: 
    # a key should equal the corresponding value's output_field.
    def outputs(self): raise NotImplementedError("Subclasses should implement this!")
    # For syntactic sugar, class-specific methods can also return specific 
    # outputs rather than the entire dict.

    # The dictionary that corresponds with the JSON serialization of the node. 
    # This should return a subset of how a node object is stored as part of a
    # pipeline in Mongo, specifically, the following attributes: type, id, and
    # data (and all subfields therein). This should only be called after an id
    # has been assigned to the node.
    # NB: the JSON fields id/data.id and type/data.nodeType are the same
    @abstractclassmethod
    def json_rep(self):
        raise NotImplementedError("Subclasses should implement this!")

# A wrapper class for outputs from nodes, for basic "type"-checks and to figure
# out how nodes connect to each other. NOT the same as OutputNode, which is 
# a node that represents the final result of a pipeline.
class NodeOutput:
    def __init__(self, source:NodeTemplate, output_field:str, output_type:str):
        # The Node object producing this output.
        self.source = source
        # The specific output field from the source node (the node handle).
        self.output_field = output_field
        # A string roughly corresponding to the output type. (Strings are 
        # flimsy, but they will do the job.) TODO: This isn't really used now, 
        # but in the future this field could be used to ascribe general data 
        # types to outputs for better "type"-checking if needed.
        self.output_type = output_type
    def __str__(self):
        return f"Node output {self.output_type}"

# Each node subclasses NodeTemplate and takes in class-specific parameters 
# depending on what the node does.
 
# Let's try to avoid more than one level of subclassing.

###############################################################################
# HOME                                                                        #
###############################################################################

# Input nodes themselves don't have inputs; they define the start of a pipeline.
class InputNode(NodeTemplate):
    def __init__(self, name:str, input_type:str):
        super().__init__()
        self.node_type = "customInput"
        self.name = name
        # Text or File
        if input_type not in INPUT_NODE_TYPES:
            raise ValueError(f"Input node type {input_type} not supported.")
        self.input_type = input_type
        
    def output(self): 
        # Input nodes can produce anything in INPUT_NODE_TYPES, so we mark
        # the specific type here.
        return NodeOutput(
            source=self, 
            output_field="value", 
            output_type=self.input_type
        )
    
    def outputs(self):
        o = self.output()
        return {o.output_field: o}
        
    def json_rep(self):
        # TODO: category and task_name can probably be made into class variables too.
        return {
            "id": self._id,
            "type": self.node_type,
            "data": {
                "id": self._id,
                "nodeType": self.node_type,
                "inputName": self.name,
                "inputType": self.input_type.capitalize(),
                "category": "input",
                "task_name": "input"
            }
        }

class OutputNode(NodeTemplate):
    def __init__(self, name:str, output_type:str, input:NodeOutput):
        super().__init__()
        self.node_type = "customOutput"
        self._inputs = {"value": input}
        self.name = name
        # Text or File
        if output_type not in OUTPUT_NODE_TYPES:
            raise ValueError(f"Output node type {output_type} not supported.")
        self.output_type = output_type

    def outputs(self): return None
    
    def json_rep(self):
        return {
            "id": self._id,
            "type": self.node_type,
            "data": {
                "id": self._id,
                "nodeType": self.node_type,
                "outputName": self.name,
                "outputType": self.output_type.capitalize(),
                "category": "output",
                "task_name": "output"
            }
        }

# Text data. This is possibly even a little redundant because we can pass in
# plaintext inputs as additional params to nodes (without instantiating them
# as separate nodes) through code. Right now though I'm trying to get a 1:1 
# correspondance between no-code and code construction; we can discuss this.
class TextNode(NodeTemplate):
    # Text nodes can either just be blocks of text in themselves, or also take
    # other text nodes as inputs (e.g. with text variables like {{Context}}, 
    # {{Task}}). In the latter case, an additional argument text_inputs should
    # be passed in as a dict of input variables to Outputs.
    def __init__(self, text:str, text_inputs:dict = None):
        super().__init__()
        self.node_type = "text"
        self.text = text
        # if there are required inputs, they should be of the form {{}} - each
        # of them is a text variable
        text_vars = re.findall(r'\{\{([^{}]+)\}\}', self.text)
        self.text_vars = []
        # remove duplicates while preserving order
        [self.text_vars.append(v) for v in text_vars if v not in self.text_vars]
        
        # if there are variables, we expect them to be matched with inputs
        # they should be passed in a dictionary with the
        # arg name text_inputs. E.g. {"Context": ..., "Task": ...}
        if text_inputs:
            if type(text_inputs) != dict:
                raise TypeError("text_inputs must be a dictionary of text variables to node outputs.")
            num_inputs = len(text_inputs.keys())
            num_vars = len(self.text_vars)
            if num_inputs != num_vars:
                raise ValueError(f"Number of text inputs ({num_inputs}) does not match number of text variables ({num_vars}).")
            if sorted(list(set(text_inputs.keys()))) != sorted(self.text_vars):
                raise ValueError("Names of text inputs and text variables do not match.")
            self._inputs = text_inputs
        else:
            if len(self.text_vars) > 0:
                raise ValueError("text_inputs must be passed in if there are text variables.")
            
    def output(self): 
        return NodeOutput(source=self, output_field="output", output_type="text")
    
    def outputs(self):
        o = self.output()
        return {o.output_field: o}
        
    def json_rep(self):
        input_names = self.text_vars if len(self.text_vars) > 0 else "None"
        return {
            "id": self._id,
            "type": self.node_type,
            "data": {
                "id": self._id,
                "nodeType": self.node_type,
                "text": self.text,
                "inputNames": input_names,
                "formatText": True,
                "category": "task",
                "task_name": "text",
            } 
        }

# Data transformations.
class URLLoaderNode(NodeTemplate):
    # TODO: does this node need chunk params?
    def __init__(self, url_input:NodeOutput, **kwargs):
        super().__init__()
        self.node_type = "dataLoader"
        self._inputs = {"url": url_input}
        self.chunk_size, self.chunk_overlap, self.func = 400, 0, "default"
        for optional_param_arg in ["chunk_size", "chunk_overlap", "func"]:
            if optional_param_arg in kwargs:
                setattr(self, optional_param_arg, kwargs[optional_param_arg])
    
    def output(self): 
        return NodeOutput(source=self, output_field="output", output_type=None)
    
    def outputs(self):
        o = self.output()
        return {o.output_field: o}
    
    def json_rep(self):
        return {
            "id": self._id,
            "type": self.node_type,
            "data": {
                "id": self._id,
                "nodeType": self.node_type,
                # TODO: check if this is the correct loaderType
                "loaderType": "URL",
                "function": self.func,
                "chunkSize": str(self.chunk_size),
                "chunkOverlap": self.chunk_overlap,
                "category": "task",
                "task_name": "load_file"
            }
        }
        
class FileLoaderNode(NodeTemplate):
    def __init__(self, file_input:NodeOutput, **kwargs):
        super().__init__()
        self.node_type = "dataLoader"
        if file_input.output_type != "InputNode.file":
            raise ValueError("Must take a file from an input node.")
        self._inputs = {"file": file_input}
        self.chunk_size, self.chunk_overlap, self.func = 400, 0, "default"
        for optional_param_arg in ["chunk_size", "chunk_overlap", "func"]:
            if optional_param_arg in kwargs:
                setattr(self, optional_param_arg, kwargs[optional_param_arg])
                
    def output(self): 
        return NodeOutput(source=self, output_field="output", output_type=None)

    def outputs(self):
        o = self.output()
        return {o.output_field: o}
    
    def json_rep(self):
        return {
            "id": self._id,
            "type": self.node_type,
            "data": {
                "id": self._id,
                "nodeType": self.node_type,
                "loaderType": "File",
                "function": self.func,
                "chunkSize": str(self.chunk_size),
                "chunkOverlap": self.chunk_overlap,
                "category": "task",
                "task_name": "load_file"
            }
        }

###############################################################################
# LLMS                                                                        #
###############################################################################

class OpenAILLMNode(NodeTemplate):
    def __init__(self, model:str, system_input:NodeOutput, prompt_input:NodeOutput, **kwargs):
        super().__init__()
        self.node_type = "llmOpenAI"
        # example simple type-check: inputs should be text
        if system_input.output_type != "text" or prompt_input.output_type != "text":
            raise ValueError("LLM inputs must be from text nodes.")
        if model not in SUPPORTED_OPENAI_LLMS:
            raise ValueError(f"Invalid model {model}.")
        self.model = model 
        # the user might have passed in more model params through kwargs
        self.max_tokens, self.temp, self.top_p = 1024, 1., 1.
        for optional_param_arg in ["max_tokens", "temperature", "top_p"]:
            if optional_param_arg in kwargs:
                setattr(self, optional_param_arg, kwargs[optional_param_arg])
        self._inputs = {"system": system_input, "prompt": prompt_input}
    
    def output(self): 
        return NodeOutput(source=self, output_field="response", output_type="text")
    
    def outputs(self):
        o = self.output()
        return {o.output_field: o}
    
    def json_rep(self):
        return {
            "id": self._id,
            "type": self.node_type,
            "data": {
                "id": self._id,
                "nodeType": self.node_type,
                "model": self.model,
                "maxTokens": self.max_tokens,
                "temperature": str(round(self.temp, 2)),
                "topP": str(round(self.top_p, 2)),
                "category": "task",
                "task_name": "llm_openai"
            }
        }

###############################################################################
# MULTIMODAL                                                                  #
###############################################################################

###############################################################################
# VECTORDB                                                                    #
###############################################################################

class VectorDBLoaderNode(NodeTemplate):
    def __init__(self, input:NodeOutput, **kwargs):
        super().__init__()
        self.node_type = "vectorDBLoader"
        self._inputs = {"documents": input}
        self.func, self.chunk_size, self.chunk_overlap = "default", 400, 0
        for optional_param_arg in ["func", "chunk_size", "chunk_overlap"]:
            if optional_param_arg in kwargs:
                setattr(self, optional_param_arg, kwargs[optional_param_arg])
    
    def output(self):
        return NodeOutput(source=self, output_field="database", output_type=None)

    def outputs(self):
        o = self.output()
        return {o.output_field: o}
    
    def json_rep(self):
        return {
            "id": self._id,
            "type": self.node_type,
            "data": {
                "id": self._id,
                "nodeType": self.node_type,
                "function": self.func,
                "category": "task",
                "task_name": "load_vector_db"
            }
        }

class VectorDBReaderNode(NodeTemplate):
    def __init__(self, query_input:NodeOutput, database_input:NodeOutput, **kwargs):
        super().__init__()
        self.node_type = "vectorDBReader"
        self._inputs = {"query": query_input, "database": database_input}
        self.func, self.max_docs_per_query = "default", 2
        for optional_param_arg in ["func", "max_docs_per_query"]:
            if optional_param_arg in kwargs:
                setattr(self, optional_param_arg, kwargs[optional_param_arg])
    
    def output(self):
        return NodeOutput(source=self, output_field="results", output_type=None)
    
    def outputs(self):
        o = self.output()
        return {o.output_field: o}
    
    def json_rep(self):
        return {
            "id": self._id,
            "type": self.node_type,
            "data": {
                "id": self._id,
                "nodeType": self.node_type,
                "function": self.func,
                "category": "task",
                "task_name": "query_vector_db",
                "maxDocsPerQuery": self.max_docs_per_query
            }
        }

###############################################################################
# LOGIC                                                                       #
###############################################################################

###############################################################################
# CHAT                                                                        #
###############################################################################