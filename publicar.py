# -*- coding: utf-8 -*-
"""Republica o teste do candidato em https://dafisengenharia.github.io/teste-perfil/

   Le o arquivo JA GERADO na pasta do Drive (nao gera nada aqui: o build e o
   _fontes/montar.py, que e a fonte unica). Publica somente a pagina do
   candidato — os paineis tem gabarito e senha e nunca podem ir para a web.
"""
import os, subprocess, sys, io

AQUI = os.path.dirname(os.path.abspath(__file__))
FONTE = ("G:\Drives compartilhados\Administrativo - Dafis\Recursos Humanos - Recrutamento e "
         "Sele\u00e7\u00e3o\Teste de Perfil Comportamental\Dafis - Teste de Perfil.html")

def git(*args):
    return subprocess.run(("git",) + args, cwd=AQUI, capture_output=True, text=True, encoding="utf-8")

if not os.path.exists(FONTE):
    print("[ERRO] Nao achei o arquivo gerado:\n  " + FONTE)
    print("Rode antes:  python montar.py   na pasta _fontes")
    sys.exit(1)

html = io.open(FONTE, encoding="utf-8").read()

# trava de seguranca: se um dia alguem apontar isto para o painel, o script para
for proibido in ("function calcula", "var ALVO", "var SENHA", "function veredito", "var NARR"):
    if proibido in html:
        print("[ABORTADO] O arquivo contem '%s' — isso e do painel, nao da pagina do candidato." % proibido)
        sys.exit(2)

io.open(os.path.join(AQUI, "index.html"), "w", encoding="utf-8", newline="\n").write(html)

git("add", "-A")
if git("diff", "--cached", "--quiet").returncode == 0:
    print("Nada mudou desde a ultima publicacao.")
    sys.exit(0)
git("-c", "user.name=Dafis Engenharia", "-c", "user.email=projetos@dafisengenharia.com.br",
    "commit", "-m", "Atualiza o teste de perfil")
r = git("push")
if r.returncode != 0:
    print("[ERRO no push]\n" + (r.stderr or r.stdout)[:600]); sys.exit(3)
print("Publicado. Pode levar ~1 minuto para atualizar no link:")
print("  https://dafisengenharia.github.io/teste-perfil/")
