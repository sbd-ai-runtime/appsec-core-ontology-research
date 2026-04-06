# Contrato para Consumidores Downstream

Este documento define o contrato público de consumo de `sbd-toe-knowledge-graph` na V2 atual.

Não é roadmap, backlog ou guia de prompting.

## Princípio

O contrato público deixa de ser `Algolia-first`.

A base de consumo passa a ser:

1. `ontologia publicada`
2. `canonical substrate`
3. `skins de publicação`

Sem backward compatibility obrigatória com o modelo antigo.

## Papel deste repositório

Este repositório deve ser tratado como:

- `knowledge builder`
- `semantic indexing pipeline`
- `retrieval backend`

Não deve ser tratado como:

- runtime de chat
- MCP server
- camada de prompting
- simples proxy de Algolia

Guia específico para integração MCP:

- [prompts/downstream_requests/mcp_ontology_integration.md](../../prompts/downstream_requests/mcp_ontology_integration.md)
- [external_overlay_contract.md](./external_overlay_contract.md)

## Contrato Público por Nível

### Primário

Estes ficheiros são o contrato público principal:

- `data/publish/sbdtoe-ontology.yaml`
- `data/publish/indexes/canonical_chunks.jsonl`
- `data/publish/indexes/chunk_entity_mentions.jsonl`
- `data/publish/indexes/chunk_relation_hints.jsonl`
- `data/publish/indexes/mcp_chunks.jsonl`
- `data/publish/indexes/vector_chunks.jsonl`
- `data/publish/indexes/publication_manifest.json`
- `data/reports/run_manifest.json`

Camada opcional acima do contrato primário:

- `data/publish/overlay/external_frameworks.json`
- `data/publish/overlay/external_obligations.json`
- `data/publish/overlay/overlay_playbooks.json`
- `data/publish/overlay/overlay_mappings.jsonl`
- `data/publish/overlay/framework_overlay_index.json`

Se fores construir um MCP ou outro consumidor estruturado, começa aqui.

### Secundário

Artefactos públicos úteis para consumidores mais ricos, debug ou auditoria:

- `data/entities/evidence_patterns.json`
- `data/publish/semantic/requirement_control_links.jsonl`
- `data/publish/semantic/mechanism_control_links.jsonl`
- `data/publish/semantic/pattern_control_links.jsonl`
- `data/publish/semantic/antipattern_requirement_links.jsonl`
- `data/publish/semantic/antipattern_threat_links.jsonl`
- `data/publish/semantic/signal_evidence_links.jsonl`
- `data/publish/semantic/concepts.jsonl`
- `data/publish/semantic/mechanisms.jsonl`
- `data/publish/semantic/patterns.jsonl`
- `data/publish/semantic/antipatterns.jsonl`
- `data/publish/semantic/signals.jsonl`

### Interno / Local

Consumidores não devem depender de:

- `data/source/`
- `data/cache/`
- `data/analysis/`
- relatórios operacionais intermédios
- `data/entities/` fora dos artefactos explicitamente listados acima

## Modelo de Consumo

### 1. Ontologia

`data/publish/sbdtoe-ontology.yaml` define:

- semântica
- entidades
- relações
- `domain_mapping`
- `resolution_profiles`
- boundary explícita V2 -> V3

Consumidores MCP devem carregar este ficheiro antes de qualquer `skin`.

### 2. Canonical Substrate

`data/publish/indexes/canonical_chunks.jsonl` é a base canónica de indexação.

Cada linha é um `chunk/unit` com:

- identidade estável
- provenance
- texto base
- classificação editorial
- refs estruturadas iniciais

### 3. Derivados do Substrate

`chunk_entity_mentions.jsonl`

- normaliza `chunk -> entity`

`chunk_relation_hints.jsonl`

- materializa hints estruturados `chunk -> relation -> target`

`publication_manifest.json`

- declara builders, artefactos e contagens

### 4. Skins

`mcp_chunks.jsonl`

- skin principal para consumo MCP

`vector_chunks.jsonl`

- skin para retrieval vetorial

`Algolia`

- projection opcional futura
- não é contrato primário nesta fase

## Ordem de Autoridade

Se houver conflito entre artefactos:

1. `sbdtoe-ontology.yaml`
2. `canonical substrate`
3. `mcp/vector skins`
4. projections opcionais como `Algolia`

## Provenance e Identidade Estável

Consumidores downstream devem confiar, quando presentes, em:

- `chunk_id`
- `unit_id`
- `bundle_id`
- `document_id`
- `source_path`
- `line_start`
- `line_end`
- `run_id`
- `commit_sha`

O cliente não deve reconstruir identidade a partir de texto livre quando estes campos existem.

## Perfis Estruturados Determinísticos

### `consult()`

Input mínimo:

- `risk_level`
- `exposure`
- `data_sensitivity`
- `chapter_context` opcional
- `concerns` opcional

Output mínimo:

- `applicable_requirements`
- `active_controls`
- `required_artifacts`
- `rule_trace`

### `review()`

Input mínimo:

- tudo o que `consult()` aceita
- `observed_artifacts`
- `observed_signals`

Output mínimo:

- `expected_evidence`
- `present_evidence`
- `missing_artifacts`
- `missing_evidence`
- `expected_signals`
- `missing_signals`
- `gaps`
- `compliant`
- `risk_exposure`
- `rule_trace`

### `threats()`

Output mínimo:

- `threats`
- `mitigated_by`
- `related_antipatterns`

## MCP Mínimo

Para arrancar um MCP determinístico:

- `data/publish/sbdtoe-ontology.yaml`
- `data/publish/indexes/mcp_chunks.jsonl`
- `data/publish/indexes/chunk_entity_mentions.jsonl`
- `data/publish/indexes/chunk_relation_hints.jsonl`
- `data/publish/indexes/publication_manifest.json`

Complementos úteis:

- `data/entities/evidence_patterns.json`
- `data/publish/semantic/*.jsonl`

## Retrieval Recomendado

Ordem recomendada:

1. resolução determinística
2. retrieval estruturado em `mcp_chunks.jsonl`
3. joins explícitos via `chunk_entity_mentions.jsonl`
4. reforço via `chunk_relation_hints.jsonl`
5. retrieval vetorial opcional em `vector_chunks.jsonl`

Quando o consumidor quiser ler o manual face a `DORA`, `NIS2`, `CRA` ou `RGPD`, pode carregar adicionalmente:

6. `data/publish/overlay/*`

## O que o Consumidor Não Deve Fazer

O consumidor downstream não deve:

- reparsear o corpus Markdown
- tratar `Algolia` como source of truth
- reconstruir identidade a partir de texto
- usar embeddings para criar relações canónicas
- assumir backward compatibility com o modelo antigo

## Bundle Público de Release

Um bundle público útil deve incluir pelo menos:

- `data/publish/sbdtoe-ontology.yaml`
- `data/publish/indexes/`
- `data/reports/run_manifest.json`
- documentação mínima para consumidores

## Mudanças de Contrato

Quando o contrato público mudar, o projeto deve:

- versionar com tag `vX.Y.Z`
- atualizar este documento
- atualizar a documentação MCP associada
- regenerar os snapshots públicos afetados
