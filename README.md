# Controle Remoto Bot

**Controle Remoto** é um bot do Discord que permite controlar o VLC Media Player direto do seu servidor Discord. Você pode reproduzir, pausar, parar e checar o status de suas mídias, além de obter informações detalhadas sobre filmes através da integração com a API do The Movie Database (TMDB).

## Funcionalidades

- Controle remoto do VLC Media Player.
- Informações detalhadas sobre filmes.
- Integração com TMDB.
- Suporte para contribuições via Patreon e GitHub.

## Configurações Iniciais

Antes de executar o bot, você precisará configurar algumas credenciais para garantir que o bot possa acessar suas APIs necessárias. Siga as etapas abaixo para gerar e configurar suas credenciais.

### 1. Gerar o Token do Bot do Discord

1. **Crie uma Conta de Desenvolvedor Discord:**
   - Visite o [Portal do Discord para Desenvolvedores](https://discord.com/developers/applications).
   - Faça login ou crie uma nova conta.

2. **Crie uma Nova Aplicação:**
   - Clique em "New Application".
   - Dê um nome para sua aplicação e clique em "Create".

3. **Configure o Bot:**
   - Vá para a seção "Bot" e clique em "Add Bot".

4. **Obtenha o Token do Bot:**
   - Clique em "Reset Token" para gerar um novo token.
   - Copie e mantenha seguro este token.

5. **Conceda Permissões ao Bot:**
   - Na aba "OAuth2", em "URL Generator", selecione os escopos necessários para gerar o link de convite do bot.

### 2. Obtenha a Chave da API do TMDB

1. **Crie uma Conta no TMDB:**
   - Visite o [TMDB](https://www.themoviedb.org/) e faça login.

2. **Acesse as Configurações de API:**
   - Clique no ícone de usuário -> "Settings" -> "API".

3. **Requisite a Chave de API:**
   - Siga o processo para obter uma chave de API.

### 3. Configurar a Senha do VLC Media Player

1. **Abra o VLC Media Player:**
   - Inicie o VLC.

2. **Acesse as Configurações de Interface Web:**
   - Vá em "Tools" -> "Preferences".
   - Escolha “All” para mostrar todas as configurações.

3. **Habilitar Controle Remoto:**
   - Em "Interface" -> "Main interfaces" ative "Web".

4. **Configurar a Senha:**
   - Em "Main interfaces" -> "Lua", configure uma senha em "Lua HTTP".
   - Salve e reinicie o VLC.

### Configuração do Arquivo `.env`

Depois de gerar suas credenciais, crie um arquivo `.env` na raiz do projeto com o seguinte conteúdo:

```plaintext
DISCORD_TOKEN=seu_token_discord
VLC_PASSWORD=sua_senha_vlc
TMDB_API_KEY=sua_chave_api_tmdb