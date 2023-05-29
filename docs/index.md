# Cray Freelas Bot

Projeto que automatiza envio de mensagens em sites de Freelancers

## Instalação

Instale os pacotes necessários com `pip install -r requirements.txt`

## Como usar

Rode o arquivo `cray_freelas_bot/main.py`, essa interface vai se abrir

![Janela principal](https://www.github.com/riguima/cray-freelas-bot/docs/assets/main-window.png)

Clicando em rodar ele roda o processo para todos os bots que foram criados, os bots
ficam monitorando por projetos novos para mandar mensagens a cada minuto

Para bots do site 99Freelas será necessário preencher um captcha para fazer o login
na plataforma, mas isso só será necessário na primeira vez que rodar o bot

Para cada bot criado ele vai abrir um navegador

Clique em Bots, uma janela para criação e remoção de bots vai se abrir

![Janela Bots](https://www.github.com/riguima/cray-freelas-bot/docs/assets/bots-window.png)

Aqui poderá adicionar novos bots preenchendo os campos e clicando em "Adicionar bot"

O campo de mensagem precisa ter pelo menos 100 caracteres, pois o Workana não permite mensagens com menos que isso

Você também pode selecionar os bots que deseja remover da tabela a direita e clicar em "Remover bots"
