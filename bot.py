@bot.message_handler(commands=["start", "novo"])
def cmd_start(msg):

    # Se veio de grupo, direciona para o privado
    if msg.chat.type in ["group", "supergroup"]:
        bot.reply_to(
            msg,
            "👋 Para criar seu currículo, converse comigo no privado:\n\n"
            "👉 https://t.me/curriculo_pro_bot\n\n"
            "Depois envie /start."
        )
        return

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
