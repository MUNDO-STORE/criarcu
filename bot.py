"""
Bot de Geração de Currículos para Telegram
==========================================
Instale as dependências:
    pip install pyTelegramBotAPI reportlab python-docx Pillow requests

Configure o token:
    export TELEGRAM_TOKEN="seu_token_aqui"

Execute:
    python bot.py
"""

import os
import io
import logging
import telebot
from telebot import types

from gerador_curriculo import GeradorCurriculo

# ── Configuração ────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

TOKEN = os.environ.get("TELEGRAM_TOKEN", "COLE_SEU_TOKEN_AQUI")
bot = telebot.TeleBot(TOKEN)

# ── Estado da conversa por usuário ──────────────────────────────────────────
# Estrutura: { user_id: { "etapa": ..., "dados": {...}, "foto_bytes": None } }
sessoes = {}

ETAPAS = [
    ("nome",            "👤 Qual é o seu nome completo?"),
    ("nascimento",      "🎂 Qual é sua data de nascimento? (ex: 28/08/1987)"),
    ("endereco",        "🏠 Qual é o seu endereço? (Bairro - Cidade - Estado)"),
    ("telefone",        "📞 Qual é o seu telefone? (ex: (66) 99999-9999)"),
    ("email",           "📧 Qual é o seu e-mail?"),
    ("cnh",             "🚗 Possui CNH? Se sim, qual categoria? (ex: AB, B, A) — ou digite *não*"),
    ("resumo",          "📝 Escreva um breve resumo profissional sobre você:"),
    ("formacao",        "🎓 Qual é a sua formação acadêmica?\n\nEx:\n*Bacharelado em Agronomia*\nAnhanguera — Conclusão: 06/07/2023"),
    ("experiencia",     "💼 Descreva sua experiência profissional.\n\nEx:\n*Técnico em Informática – Autônomo*\n• Atendimento ao cliente\n• Diagnóstico e resolução de problemas\n\nSe não tiver, escreva *sem experiência*"),
    ("competencias",    "⭐ Liste suas principais competências (uma por linha):\n\nEx:\nDisponibilidade para trabalho em campo\nCNH AB\nAprendizado rápido"),
]

TAMANHOS_FOTO = {
    "Pequena (3x4 cm)":  (85,  113),
    "Média (5x5 cm)":    (142, 142),
    "Grande (7x9 cm)":   (198, 255),
}


def sessao(uid):
    if uid not in sessoes:
        sessoes[uid] = {"etapa": 0, "dados": {}, "foto_bytes": None, "tamanho_foto": None}
    return sessoes[uid]


def resetar(uid):
    sessoes[uid] = {"etapa": 0, "dados": {}, "foto_bytes": None, "tamanho_foto": None}


# ── /start ───────────────────────────────────────────────────────────────────
@bot.message_handler(commands=["start", "novo"])
def cmd_start(msg):
    uid = msg.from_user.id
    resetar(uid)
    bot.send_message(
        uid,
        "👋 Olá! Bem-vindo ao *Bot de Currículo Profissional*!\n\n"
        "Vou te fazer algumas perguntas para montar seu currículo.\n"
        "No final, você poderá salvar em *PDF*, *Word (.docx)* ou *imprimir*.\n\n"
        "Vamos começar! 🚀",
        parse_mode="Markdown"
    )
    perguntar_etapa(uid)


def perguntar_etapa(uid):
    s = sessao(uid)
    idx = s["etapa"]
    if idx < len(ETAPAS):
        _, pergunta = ETAPAS[idx]
        bot.send_message(uid, pergunta, parse_mode="Markdown")
    else:
        perguntar_foto(uid)


# ── Coleta de respostas ──────────────────────────────────────────────────────
@bot.message_handler(func=lambda m: (
    m.from_user.id in sessoes and
    sessoes[m.from_user.id]["etapa"] < len(ETAPAS) and
    sessoes[m.from_user.id].get("aguardando") is None
))
def coletar_resposta(msg):
    uid = msg.from_user.id
    s = sessao(uid)
    idx = s["etapa"]
    chave, _ = ETAPAS[idx]
    s["dados"][chave] = msg.text.strip()
    s["etapa"] += 1
    perguntar_etapa(uid)


# ── Pergunta sobre foto ──────────────────────────────────────────────────────
def perguntar_foto(uid):
    s = sessao(uid)
    s["aguardando"] = "foto_sim_nao"
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add("📷 Sim, quero adicionar foto", "❌ Não, sem foto")
    bot.send_message(
        uid,
        "📸 Deseja adicionar uma *foto de perfil* ao currículo?",
        parse_mode="Markdown",
        reply_markup=markup
    )


@bot.message_handler(func=lambda m: (
    m.from_user.id in sessoes and
    sessoes[m.from_user.id].get("aguardando") == "foto_sim_nao"
))
def resposta_foto_sim_nao(msg):
    uid = msg.from_user.id
    s = sessao(uid)
    if "Sim" in msg.text:
        s["aguardando"] = "aguardando_foto"
        bot.send_message(
            uid,
            "📤 Envie sua foto de perfil agora:",
            reply_markup=types.ReplyKeyboardRemove()
        )
    else:
        s["aguardando"] = None
        perguntar_formato(uid)


@bot.message_handler(content_types=["photo"], func=lambda m: (
    m.from_user.id in sessoes and
    sessoes[m.from_user.id].get("aguardando") == "aguardando_foto"
))
def receber_foto(msg):
    uid = msg.from_user.id
    s = sessao(uid)
    # Pega a maior resolução
    file_id = msg.photo[-1].file_id
    file_info = bot.get_file(file_id)
    downloaded = bot.download_file(file_info.file_path)
    s["foto_bytes"] = downloaded
    s["aguardando"] = "tamanho_foto"

    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    for nome in TAMANHOS_FOTO:
        markup.add(nome)

    bot.send_message(
        uid,
        "✅ Foto recebida!\n\n📐 Qual tamanho quer usar no currículo?",
        reply_markup=markup
    )


@bot.message_handler(func=lambda m: (
    m.from_user.id in sessoes and
    sessoes[m.from_user.id].get("aguardando") == "tamanho_foto"
))
def escolher_tamanho(msg):
    uid = msg.from_user.id
    s = sessao(uid)
    nome = msg.text.strip()
    if nome in TAMANHOS_FOTO:
        s["tamanho_foto"] = TAMANHOS_FOTO[nome]
    else:
        s["tamanho_foto"] = TAMANHOS_FOTO["Média (5x5 cm)"]
    s["aguardando"] = None
    perguntar_formato(uid)


# ── Pergunta sobre formato ───────────────────────────────────────────────────
def perguntar_formato(uid):
    s = sessao(uid)
    s["aguardando"] = "formato"
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.row("📄 PDF", "📝 Word (.docx)")
    markup.add("🖨️ Imprimir (PDF otimizado)")
    bot.send_message(
        uid,
        "✅ Dados coletados! Vamos gerar seu currículo.\n\n"
        "💾 Em qual formato deseja salvar?",
        reply_markup=markup
    )


@bot.message_handler(func=lambda m: (
    m.from_user.id in sessoes and
    sessoes[m.from_user.id].get("aguardando") == "formato"
))
def escolher_formato(msg):
    uid = msg.from_user.id
    s = sessao(uid)
    s["aguardando"] = None
    texto = msg.text

    bot.send_message(uid, "⏳ Gerando seu currículo...", reply_markup=types.ReplyKeyboardRemove())

    gerador = GeradorCurriculo(s["dados"], s["foto_bytes"], s["tamanho_foto"])

    try:
        if "PDF" in texto or "Imprimir" in texto:
            otimizado = "Imprimir" in texto
            pdf_bytes = gerador.gerar_pdf(para_impressao=otimizado)
            nome_arquivo = f"curriculo_{s['dados'].get('nome','curriculo').split()[0]}.pdf"
            bot.send_document(
                uid,
                (nome_arquivo, io.BytesIO(pdf_bytes)),
                caption="✅ Currículo em PDF pronto!"
            )
        elif "Word" in texto or "docx" in texto:
            docx_bytes = gerador.gerar_docx()
            nome_arquivo = f"curriculo_{s['dados'].get('nome','curriculo').split()[0]}.docx"
            bot.send_document(
                uid,
                (nome_arquivo, io.BytesIO(docx_bytes)),
                caption="✅ Currículo em Word pronto!"
            )
    except Exception as e:
        logger.error(f"Erro ao gerar currículo: {e}", exc_info=True)
        bot.send_message(uid, f"❌ Ocorreu um erro ao gerar o currículo: {e}")
        return

    # Oferecer outro formato
    s["aguardando"] = "outro_formato"
    markup = types.InlineKeyboardMarkup()
    markup.row(
        types.InlineKeyboardButton("📄 PDF", callback_data="fmt_pdf"),
        types.InlineKeyboardButton("📝 Word", callback_data="fmt_docx"),
    )
    markup.row(
        types.InlineKeyboardButton("🔄 Novo currículo", callback_data="novo"),
        types.InlineKeyboardButton("🖨️ Para imprimir", callback_data="fmt_print"),
    )
    bot.send_message(uid, "Quer gerar em outro formato também?", reply_markup=markup)


@bot.callback_query_handler(func=lambda c: True)
def callback_handler(call):
    uid = call.from_user.id
    s = sessao(uid)
    bot.answer_callback_query(call.id)

    if call.data == "novo":
        cmd_start(call.message)
        return

    gerador = GeradorCurriculo(s["dados"], s["foto_bytes"], s["tamanho_foto"])
    try:
        if call.data == "fmt_pdf":
            dados = gerador.gerar_pdf()
            bot.send_document(uid, (f"curriculo.pdf", io.BytesIO(dados)), caption="📄 PDF gerado!")
        elif call.data == "fmt_docx":
            dados = gerador.gerar_docx()
            bot.send_document(uid, (f"curriculo.docx", io.BytesIO(dados)), caption="📝 Word gerado!")
        elif call.data == "fmt_print":
            dados = gerador.gerar_pdf(para_impressao=True)
            bot.send_document(uid, (f"curriculo_impressao.pdf", io.BytesIO(dados)), caption="🖨️ PDF para impressão!")
    except Exception as e:
        bot.send_message(uid, f"❌ Erro: {e}")


# ── /ajuda ────────────────────────────────────────────────────────────────────
@bot.message_handler(commands=["ajuda", "help"])
def cmd_ajuda(msg):
    bot.send_message(
        msg.from_user.id,
        "📋 *Comandos disponíveis:*\n\n"
        "/start — Iniciar novo currículo\n"
        "/novo — Recomeçar do zero\n"
        "/ajuda — Esta mensagem\n\n"
        "💡 Durante o preenchimento, responda cada pergunta e pressione enviar.",
        parse_mode="Markdown"
    )


# ── Iniciar ───────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    logger.info("🤖 Bot iniciado! Aguardando mensagens...")
    bot.infinity_polling()
