import discord

async def support_command(interaction: discord.Interaction):
    patreon_link = "https://www.patreon.com/seuusuario"
    github_link = "https://github.com/seurepositorio"
    description = (
        "🌟 **Apoie Nosso Projeto!**\n\n"
        "Estamos trabalhando arduamente para trazer uma experiência rica e envolvente com o Plexcord, "
        "um bot projetado para facilitar o controle do VLC Media Player diretamente do Discord e oferecer "
        "informações detalhadas sobre seus filmes favoritos. Nosso objetivo é tornar a interação com suas mídias "
        "o mais simples e agradável possível.\n\n"
        "🔗 Se você gosta do que estamos fazendo e deseja apoiar o projeto, considere fazer uma doação "
        "através do nosso Patreon. Seu apoio é crucial para continuar desenvolvendo melhorias e novas funcionalidades.\n\n"
        f"💡 **[Apoie-nos no Patreon]({patreon_link})**\n\n"
        "Além disso, você pode explorar nosso projeto open-source no GitHub e contribuir com ideias, sugestões ou melhorias:\n\n"
        f"🔧 **[Confira no GitHub]({github_link})**\n\n"
        "Agradecemos sinceramente sua contribuição e suporte. Juntos, podemos levar este projeto ainda mais longe!"
    )

    embed = discord.Embed(title="Suporte ao Projeto", description=description, color=discord.Color.gold())
    await interaction.response.send_message(embed=embed, ephemeral=True)