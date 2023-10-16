# Build
```python -m build```

# Upload
```python -m twine upload dist/* --config-file .pypirc```

# Usage
## Define a Node
Each Node requires the super.init call to be made with the **kwargs parameter. 
This is used to pass the node's name and other parameters to the super class. 
A run method also needs to be defined. This is the method that will be called when the node is executed.
```
class Example(Node):
    def __init__(self, a, b, **kwargs):
        super().__init__(**kwargs)
        
    def run(self, *args, **kwargs):
        pass
```

## Define a Graph
A graph is a collection of nodes. The graph is responsible for executing the nodes in the correct order.
```
graph_def = {
    "__node_name__": {
        "node": "__node_import_path__",
        "node_settings": {
            "__init_param__": "__init_value__,
        }, 
        "params": {
            "__runtime_param__": "__param_value__",
        }
    }
}
```
An example looks like this:
```
graph_def = {
    "example": {
        "node": "example.Example",
        "node_settings": {
            "a": 1,
            "b": 2,
        }, 
        "params": {
            "c": 3,
        }
    }
}
```
Instead of hardcoding the values for the node settings and params, you can also reference other nodes.
```
graph_def = {
    "example": {
        "node": "example.Example",
        "node_settings": {
            "a": 1,
            "b": 2,
        }, 
        "params": {
            "c": 3,
        }
    },
    "example2": {
        "node": "example.Example",
        "node_settings": {
            "a": 1,
            "b": 2,
        }, 
        "params": {
            "c": "//example",
        }
    }
}
```
You can also pass a reference of another node using ```node://__node_name__```. This will pass the node object to the node's run or init method.
```
graph_def = {
    "example": {
        "node": "example.Example",
        "node_settings": {
            "a": 1,
            "b": "node://example2",
        }, 
        "params": {
            "c": 3,
        }
    },
    "example2": {
        "node": "example.Example",
        "node_settings": {
            "a": 1,
            "b": 2,
        }, 
        "params": {
            "c": 3,
        }
    }
}
```
Instead of hardcoding setting values in teh graph, you can also reference a value in the settings file using ```settings://__setting_name__```.
```
graph_def = {
    "example": {
        "node": "example.Example",
        "node_settings": {
            "a": 1,
            "b": "node://example2",
        }, 
        "params": {
            "c": "settings:example/c",
        }
    },
    "example2": {
        "node": "example.Example",
        "node_settings": {
            "a": 1,
            "b": 2,
        }, 
        "params": {
            "c": 3,
        }
    }
}
```
The corresponding settings file would look like this:
```
graph_settings: {
    "example": {
        "c": 3,
    }
}
```
## Execute a Graph
```
from grandpa import GraphRuntime
from graph_def import graph_def
from graph_settings import graph_settings


gr = GraphRuntime()
gr.add_graph("example", graph_def, graph_settings)
gr.init_graph("example")
result = gr.router.get_value("//example_node")
print(result)
```

## Other useful features
### Use tasks to automatically run jobs in parallel
```
class Example(Node):
    def __init__(self, a, b, **kwargs):
        super().__init__(**kwargs)
        
    def method_with_long_execution_time(self, *args, **kwargs):
        time.sleep(10)
        
    def run(self, *args, **kwargs):
        tasks = [self.switch.execute_task(self.method_with_long_execution_time) for i in range(10)]
        return [task.get_result() for task in tasks]  
```
### Queue data in a worker queue to always have data available once the node is called
```
class Example(Node):
    def __init__(self, a, b, **kwargs):
        super().__init__(**kwargs)
        self.queue = self.switch.add_worker_queue(self.method_with_long_execution_time)
        
    def method_with_long_execution_time(self, *args, **kwargs):
        time.sleep(10)
        return 5
        
    def run(self, *args, **kwargs):
        return self.queue.get()
```