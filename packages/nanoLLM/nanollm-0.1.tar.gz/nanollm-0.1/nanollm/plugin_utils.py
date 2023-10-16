import importlib
import importlib.util
import os
from tango.nanoLLM.nanollm.plugin_manager import NanoLLMPluginManager

# Example usage
#pm = NanoLLMPluginManager()
#register_plugins(pm)

PLUGINS_DIR = os.path.join(os.path.dirname(__file__), 'plugins')

def discover_plugins():
    """Discover all plugins in the plugins directory."""
    plugins = []
    for item in os.listdir(PLUGINS_DIR):
        if item.endswith('.py') and item != '__init__.py':
            plugins.append(item[:-3])  # remove .py
    return plugins

def camel_case(string):
    """Convert snake_case string to CamelCase."""
    return ''.join(word.capitalize() for word in string.split('_'))

def register_plugins(pm:NanoLLMPluginManager):
    """Dynamically import and register plugins with the provided plugin manager."""
    plugins = discover_plugins()
    for plugin_name in plugins:
        try:
            # Construct full plugin module path
            module_path = f"tango.nanoLLM.nanollm.plugins.{plugin_name}"
            
            # Import plugin module dynamically
            plugin_module = importlib.import_module(module_path)

            # Check for PLUGIN_CLASS marker
            plugin_class = getattr(plugin_module, 'PLUGIN_CLASS', None)

            # If PLUGIN_CLASS does not exist, try camel_case approach
            plugin_class_name = camel_case(plugin_name)
            if not plugin_class:
                plugin_class = getattr(plugin_module, plugin_class_name, None)
            
            if plugin_class:
                # Instantiate the plugin class and register it
                pm.register_plugin(plugin_class(), plugin_name)
            else:
                print(f"Couldn't find the plugin class {plugin_class_name} in module {module_path}")
            
        except Exception as e:
            print(f"Failed to register plugin {plugin_name}. Error: {e}")
    
def setup_plugin_manager(pm):
    register_plugins(pm)
    pm.hook().register_models(register=pm.register_model_alias)