# Cray Freelas Bot

Projeto que automatiza envio de mensagens em sites de Freelancers

## Instalação

Instale os pacotes necessários com `pip install -r requirements.txt`

## Como usar

Rode o arquivo `main.py`, essa interface vai se abrir

![Janela principal](https://github.com/riguima/cray-freelas-bot/blob/main/docs/assets/main-window.png)

Clicando em rodar ele rodar o processo para todos os bots que foram criados, os bots
ficam monitorando por projetos novos para mandar mensagens a cada 10 minutos,
eles fazem isso para as 10 primeiras páginas

Para bots do site 99Freelas será necessário preencher um captcha para fazer o login
na plataforma, mas isso só será necessário na primeira vez que rodar o bot

Clique em Bots, uma janela para criação e remoção de bots vai se abrir

![Janela Bots](https://github.com/riguima/cray-freelas-bot/blob/main/docs/assets/bots-window.png)

Aqui poderá adicionar novos bots preenchendo os campos e clicando em "Adicionar bot"

Os campos de Email e senha são para o login na plataforma

O campo de mensagem precisa ter pelo menos 100 caracteres, pois o Workana não permite mensagens com menos que isso

Você também pode selecionar os bots que deseja remover da tabela a direita e clicar em "Remover bots"
