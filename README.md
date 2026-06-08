# 🤖 Bot de Currículo Profissional — Telegram

Gera currículos profissionais via Telegram com foto de perfil, exportação em PDF e Word.

---

## 📁 Arquivos do projeto

```
curriculo_bot/
├── bot.py                ← Bot principal
├── gerador_curriculo.py  ← Gera PDF e Word
├── requirements.txt      ← Dependências Python
├── Procfile              ← Instrução para o Railway
├── runtime.txt           ← Versão do Python
├── .gitignore            ← Arquivos ignorados pelo Git
└── README.md             ← Este guia
```

---

## PASSO 1 — Criar o bot no Telegram (BotFather)

1. Abra o Telegram no celular ou computador
2. Na busca, procure por: **@BotFather**
3. Clique em **START** ou envie `/start`
4. Envie o comando: `/newbot`
5. Digite um **nome** para o bot (ex: `Gerador de Currículos`)
6. Digite um **username** — deve terminar em "bot" (ex: `meu_curriculo_bot`)
7. O BotFather vai te enviar o **TOKEN** — salve ele! Parece assim:
   ```
   123456789:AAFabcdefghijklmnopqrstuvwxyz12345
   ```

---

## PASSO 2 — Criar conta no GitHub e subir os arquivos

1. Acesse **https://github.com** e crie uma conta gratuita
2. Clique no botão verde **"New"** (canto superior esquerdo) para criar repositório
3. Dê um nome (ex: `curriculo-bot`)
4. Marque **Private** (privado — mais seguro)
5. Clique em **"Create repository"**
6. Na página do repositório, clique em **"uploading an existing file"**
7. Arraste ou selecione TODOS estes arquivos de uma vez:
   - `bot.py`
   - `gerador_curriculo.py`
   - `requirements.txt`
   - `Procfile`
   - `runtime.txt`
   - `.gitignore`
8. Clique em **"Commit changes"** (botão verde lá embaixo)

✅ Seus arquivos já estão no GitHub!

---

## PASSO 3 — Configurar no Railway

1. Acesse **https://railway.app**
2. Clique em **"Login"** → escolha **"Login with GitHub"**
3. Autorize o acesso do Railway ao GitHub
4. Clique em **"New Project"**
5. Escolha **"Deploy from GitHub repo"**
6. Selecione o repositório `curriculo-bot` que você criou
7. O Railway vai detectar Python automaticamente e começar o deploy

---

## PASSO 4 — Adicionar o Token (OBRIGATÓRIO)

> ⚠️ Nunca coloque o token direto no código! Use variáveis de ambiente.

1. No Railway, clique no seu serviço (o quadrado que apareceu)
2. Vá na aba **"Variables"**
3. Clique em **"New Variable"**
4. Preencha assim:
   - **NAME:** `TELEGRAM_TOKEN`
   - **VALUE:** cole seu token aqui (ex: `123456789:AAFabc...`)
5. Clique em **"Add"**
6. O Railway vai reiniciar o bot automaticamente

---

## PASSO 5 — Verificar se está funcionando

1. No Railway, clique na aba **"Logs"**
2. Você deve ver a mensagem:
   ```
   🤖 Bot iniciado! Aguardando mensagens...
   ```
3. Abra o Telegram, procure pelo username do seu bot e envie `/start`
4. O bot vai responder! ✅

---

## PASSO 6 — Escolher o plano no Railway

- Railway dá **US$ 5 de crédito grátis** para testar
- Para rodar 24h/dia o mês todo, assine o plano **Hobby por US$ 5/mês**
- Vá em **Account → Billing → Add payment method**

---

## 💬 Como o usuário usa o bot

Após enviar `/start`, o bot faz as perguntas:

| # | Pergunta |
|---|----------|
| 1 | Nome completo |
| 2 | Data de nascimento |
| 3 | Endereço |
| 4 | Telefone |
| 5 | E-mail |
| 6 | CNH (ou "não") |
| 7 | Resumo profissional |
| 8 | Formação acadêmica |
| 9 | Experiência profissional |
| 10 | Competências |

Depois pergunta se quer **foto** e o **tamanho** (3x4, 5x5 ou 7x9 cm).

Por fim, o usuário escolhe o formato:
- 📄 PDF
- 📝 Word (.docx)
- 🖨️ PDF para impressão

---

## 🔄 Como atualizar o bot no futuro

1. Edite os arquivos no computador
2. Vá no GitHub → repositório → clique no arquivo → ícone de lápis ✏️ → edite → **Commit changes**
3. O Railway faz o novo deploy automaticamente em segundos!

---

## ❓ Problemas comuns

| Problema | Solução |
|----------|---------|
| Bot não responde | Verifique os Logs no Railway e confira o token |
| Erro no deploy | Veja a aba "Deployments" para detalhes do erro |
| Token inválido | Gere um novo token com /token no @BotFather |
| Bot parou | O Railway reinicia automaticamente; verifique o plano |
