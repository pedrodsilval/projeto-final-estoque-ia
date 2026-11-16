"""Serviço de Inteligência Artificial para análise de estoque usando Pandas + Ollama."""

from __future__ import annotations

import pandas as pd
from sqlalchemy.orm import Session
import ollama

import models

DEFAULT_MODEL = "gemma3:12b"


def get_estoque_dataframe(db: Session) -> pd.DataFrame:
    """Extrai snapshot do estoque do banco e converte em DataFrame estruturado."""
    produtos = db.query(models.ProdutoModel).all()
    if not produtos:
        return pd.DataFrame(
            columns=["id", "nome", "categoria", "quantidade", "estoque_minimo", "preco", "valor_total", "abaixo_minimo"]
        )

    data = [
        {
            "id": p.id,
            "nome": p.nome,
            "categoria": p.categoria,
            "quantidade": p.quantidade,
            "estoque_minimo": p.estoque_minimo,
            "preco": p.preco,
            "valor_total": round(p.quantidade * p.preco, 2),
            "abaixo_minimo": p.quantidade <= p.estoque_minimo,
        }
        for p in produtos
    ]
    return pd.DataFrame(data)


def gerar_sumario_estatistico(df: pd.DataFrame) -> str:
    """Gera resumo tabular e métricas calculadas pelo Pandas."""
    if df.empty:
        return "Estoque atualmente vazio (0 itens cadastrados)."

    total_itens = int(df["quantidade"].sum())
    total_skus = len(df)
    valor_total_estoque = float(df["valor_total"].sum())
    abaixo_minimo = df[df["abaixo_minimo"] == True]

    resumo_cat = df.groupby("categoria").agg(
        total_produtos=("id", "count"),
        unidades=("quantidade", "sum"),
        valor_investido=("valor_total", "sum"),
    ).reset_index()

    linhas_alerta = []
    for _, row in abaixo_minimo.iterrows():
        linhas_alerta.append(
            f"- {row['nome']} (Categoria: {row['categoria']}): "
            f"Atual={row['quantidade']} un | Mínimo={row['estoque_minimo']} un"
        )
    alertas_str = "\n".join(linhas_alerta) if linhas_alerta else "Nenhum produto em nível crítico."

    return (
        f"--- MÉTRICAS GERAIS (PANDAS) ---\n"
        f"Total de SKUs diferentes: {total_skus}\n"
        f"Total de unidades em estoque: {total_itens}\n"
        f"Valor total do patrimônio em estoque: R$ {valor_total_estoque:,.2f}\n\n"
        f"--- RESUMO POR CATEGORIA ---\n"
        f"{resumo_cat.to_string(index=False)}\n\n"
        f"--- PRODUTOS EM ESTOQUE CRÍTICO (<= MÍNIMO) ---\n"
        f"{alertas_str}\n\n"
        f"--- TABELA COMPLETA DE PRODUTOS ---\n"
        f"{df[['id', 'nome', 'categoria', 'quantidade', 'estoque_minimo', 'preco', 'valor_total']].to_string(index=False)}"
    )


def responder_pergunta_estoque(db: Session, pergunta: str, model: str = DEFAULT_MODEL) -> str:
    """Analisa pergunta em linguagem natural sobre o estoque usando Pandas + Ollama."""
    df = get_estoque_dataframe(db)
    sumario = gerar_sumario_estatistico(df)

    system_prompt = (
        "Você é um consultor especialista em gestão de estoque e supply chain. "
        "Você tem acesso ao resumo analítico e à base de dados do estoque calculada pelo Pandas. "
        "Responda à pergunta do usuário de forma clara, profissional, objetiva e baseada ESTRITAMENTE "
        "nos dados fornecidos. Faça contas quando solicitado e aponte valores em R$."
    )

    user_content = (
        f"Dados do Estoque Atualizados:\n\n"
        f"{sumario}\n\n"
        f"Pergunta do usuário: {pergunta}"
    )

    response = ollama.chat(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content},
        ],
        options={"temperature": 0.2},
    )
    return response["message"]["content"]


def gerar_relatorio_executivo(db: Session, model: str = DEFAULT_MODEL) -> str:
    """Gera relatório executivo detalhado e automatizado do estoque usando Pandas + Ollama."""
    df = get_estoque_dataframe(db)
    sumario = gerar_sumario_estatistico(df)

    system_prompt = (
        "Você é um Diretor de Operações e Supply Chain. "
        "Gere um Relatório Executivo formal e bem estruturado (em Markdown) com base nos dados do estoque. "
        "O relatório deve conter: "
        "1. Diagnóstico Geral do Estoque (visão consolidada de valores e volumes); "
        "2. Alertas Críticos de Reposição (produtos em falta ou com risco iminente); "
        "3. Análise por Categoria (onde está o maior capital imobilizado); "
        "4. Recomendações Estratégicas e Plano de Ação para compras."
    )

    user_content = (
        f"Gere o Relatório Executivo com base no snapshot de estoque consolidado abaixo:\n\n"
        f"{sumario}"
    )

    response = ollama.chat(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content},
        ],
        options={"temperature": 0.3},
    )
    return response["message"]["content"]
