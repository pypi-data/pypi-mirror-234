from .javascript_generator import JavascriptGenerator


class TypescriptGenerator(JavascriptGenerator):
    """
    TypeScript specific generator. For more information about the generator methods, refer to GeneratorBase.
    """

    # Override JavaScriptGenerator method.
    def _create_property(self, name: str, value: str):
        return f'public static readonly {name} = {value};'
