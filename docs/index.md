# Cray Freelas Bot

Projeto que automatiza envio de mensagens em sites de Freelancers

## Instalação

Você vai precisar ter o [Python](https://www.python.org/) instalado para rodar a aplicação

Depois de instalar o Python instale os pacotes necessários com `pip install -r requirements.txt`

## Como usar

Rode o arquivo `main.py`, essa interface vai se abrir

![Janela principal](https://cray-freelas-bot.readthedocs.io/pt/latest/assets/main-window.png)

Clicando em rodar ele roda o processo para todos os bots que foram criados, os bots
ficam monitorando por projetos novos para mandar mensagens a cada 10 minutos,
eles fazem isso para as 10 primeiras páginas

Para bots do site 99Freelas será necessário preencher um captcha para fazer o login
na plataforma, mas isso só será necessário na primeira vez que rodar o bot

Clique em Bots, uma janela para criação e remoção de bots vai se abrir

![Janela Bots](https://cray-freelas-bot.readthedocs.io/pt/latest/assets/bots-window.png)

Aqui poderá adicionar novos bots preenchendo os campos e clicando em __Adicionar bot__

Os campos de Email e senha são para o login na plataforma

O campo de caminho para relatório é a pasta onde será criada a planilha com todas
as informações das mensagens enviadas

O campo de mensagem precisa ter pelo menos __100__ caracteres, pois o Workana não permite mensagens com menos que isso

No campo de mensagens você pode colocar as seguintes marcações no texto que serão
substituidas por outras informações:

- __{saudação}__ = Substitui por Bom dia, Boa tarde ou Boa noite de acordo com o horário
- __{nome do cliente}__ = Substitui pelo nome do cliente
- __{nome do projeto}__ = Substitui pelo nome do projeto
- __{categoria}__ = Substitui pela categoria do projeto, por exemplo: Web, Mobile & Software
- __{nome da conta}__ = Substitui pelo nome da conta na plataforma

Você também pode selecionar os bots que deseja remover da tabela a direita e clicar em __Remover bots__
