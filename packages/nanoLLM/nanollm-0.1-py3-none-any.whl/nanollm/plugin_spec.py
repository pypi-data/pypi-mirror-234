import pluggy

hookspec = pluggy.HookspecMarker("nanoLLM")
hookimpl = pluggy.HookimplMarker("nanoLLM")

class NanoLLMSpec:
    """Hook specifications for nanoLLM."""
    
    @hookspec
    def register_models(self, register):
        """Load a language model by name or path."""
        pass

    @hookspec
    def register_commands(self, cli):
        """Register additional CLI commands."""
        pass
