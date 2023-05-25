from dataclasses import dataclass


@dataclass
class Project:
    """
    Classe de dados que represa um projeto
    Parameters:
        url: Url do projeto
        category: Categoria do projeto, Ex: "Web, Mobile & Software"
        name: Nome do projeto
        client_name: Nome do cliente que é o dono do projeto
    """

    url: str
    category: str
    name: str
    client_name: str


@dataclass
class Message:
    """
    Classe de dados que representa uma mensagem
    Parameters:
        project: Projeto correspondente a mensagem, que é uma instância da classe Project
        text: String que é o texto da mensagem
    """

    project: Project
    text: str
