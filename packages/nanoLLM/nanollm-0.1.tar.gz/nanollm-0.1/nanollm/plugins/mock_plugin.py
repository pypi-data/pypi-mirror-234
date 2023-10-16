from tango.nanoLLM.nanollm.plugin_spec import hookimpl

class MockPlugin:
    """A mock plugin for testing."""
    
    @hookimpl
    def register_models(self, register):
        #print(f"MockPlugin's llm_load_model method invoked with register: {register}")
        pass

