# Política de Versionamento e Distribuição de Artefactos

Este documento define o que fica versionado no Git, o que entra no bundle de release e o que deve ser tratado como output interno/local.

## Princípio geral

Este repositório publica dois tipos de produto:

1. software e automação do pipeline;
2. snapshots semânticos públicos úteis para retrieval e auditoria.

O objetivo não é versionar toda a working copy do manual nem todos os intermediários do pipeline.

## Matriz por diretório

| Caminho | Git | Release bundle | Contrato público | Notas |
| --- | --- | --- | --- | --- |
| `data/source/` | não | não | não | working copy local da fonte canónica; não é artefacto de distribuição |
| `data/cache/` | não | não | não | cache operacional e estado incremental |
| `data/publish/` | sim | sim | **sim, primário** | records prontos para retrieval downstream |
| `data/publish/overlay/` | sim | sim | **sim, opcional** | camada publicada opcional para leituras regulatórias curadas; não substitui o runtime principal |
| `data/reports/run_manifest.json` | sim | sim | **sim** | provenance e metadata da execução que originou os snapshots públicos |
| `data/reports/external_overlay_summary.json` | não | não | não | resumo local de execução do builder de overlay; útil para revisão, mas não faz parte do contrato público |
| `data/reports/algolia_publish_plan.json` | sim | sim | secundário | metadata útil sobre counts, índices e modo de publicação |
| `data/reports/*.md` | não | não por defeito | não | relatórios legíveis para debugging e revisão local |
| `data/reports/evaluation_report.json` | não | não por defeito | não | snapshot de avaliação, útil mas não tratado como contrato estável |
| `data/analysis/chapter_semantic_model.json` | sim | sim | **sim, secundário** | snapshot público da reconstrução semântica por capítulo |
| `data/analysis/chapter_bundle_graph.json` | sim | sim | **sim, secundário** | snapshot público do grafo de relações por capítulo |
| outros ficheiros em `data/analysis/` | não | não por defeito | não | outputs de auditoria interna, profiling e classificação |
| snapshots públicos em `data/entities/` | sim | sim | **sim, secundário** | entidades estruturadas úteis para consumidores avançados |
| `data/entities/extraction_plan.json` | não | não | não | planeamento interno de extratores |
| `data/entities/role_drift_report.json` | não | não | não | diagnóstico de qualidade e drift interno |

## Ordem de consumo recomendada

Consumidores downstream devem usar primeiro:

1. `data/publish/sbdtoe-ontology.yaml`
2. `data/publish/indexes/publication_manifest.json`
3. `data/publish/indexes/canonical_chunks.jsonl`
4. `data/publish/indexes/mcp_chunks.jsonl`
5. `data/publish/indexes/vector_chunks.jsonl`
6. `data/reports/run_manifest.json`

Snapshots secundários úteis para debug, auditoria ou consumidores mais ricos:

- `data/publish/indexes/chunk_entity_mentions.jsonl`
- `data/publish/indexes/chunk_relation_hints.jsonl`
- `data/analysis/chapter_semantic_model.json`
- `data/analysis/chapter_bundle_graph.json`
- snapshots públicos em `data/entities/`

Camadas opcionais publicadas:

- `data/publish/overlay/*` para leituras regulatórias como `DORA`, `NIS2`, `CRA` e `RGPD`

Relatórios locais que não definem contrato:

- `data/reports/external_overlay_summary.json`

## Regra para releases

Uma tag `vX.Y.Z` só deve ser criada depois de:

- regenerar os snapshots públicos relevantes;
- rever diffs em `data/publish/`;
- rever provenance em `data/reports/run_manifest.json`;
- validar localmente o bundle com `python -m sbdtoe_indexing.release_bundle`.

O bundle público existe para consumo downstream. Não deve incluir:

- `.venv/`
- `__pycache__/`
- caches
- working copy completa em `data/source/`
- segredos
- lixo de desenvolvimento
- relatórios locais cujo papel é apenas resumir uma execução específica do builder

## Regra para mudanças de contrato

Se uma alteração muda estrutura, campos, naming ou significado dos snapshots públicos:

- atualiza `README.md`;
- atualiza `docs/operations/consumer_contract.md`;
- atualiza este documento;
- regenera os snapshots públicos afetados.
