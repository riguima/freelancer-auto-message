class UnreleasedProjectError(Exception):

    def __init__(self) -> None:
        super().__init__('Projeto ainda não disponivel para sua conta')
