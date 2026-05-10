---
date: 2026-05-08
author: Archon (under programme-lead Pedro Farinha)
type: brief (figshare deposit inventory — ontology side)
status: delivery (sealed)
responds_to: sbd-ai-runtime/handover/em-curso/2026-05-08-orchestrator-archon-figshare-inventory-mini-dispatch.md
parent_dispatcher: sbd-ai-runtime/handover/em-curso/2026-05-08-orchestrator-curator-phase-a-figshare-bundle-coordination.md
authority: programme-lead Pedro Farinha 2026-05-08; Orchestrator coordinated
output_destination: Curator MANIFEST.md aggregation for figshare bundle
---

# Figshare bundle — Ontology-side artefact inventory

## TL;DR

207 files inventoried at `cycle-a-frozen-2026-05-08` (commit `6006e80`) — content-equivalent to V1 final state. SHA-256 + size per artefact, grouped by 12 categories aligned with the dispatcher's required scope. Reproducibility instructions covering deterministic build environment, execution sequence, and expected output hashes. Manual-maintained vs schema-derived distinction documented per Decision 0001 Option C.

## Anchor tags (frozen state)

| Tag | Commit | Tag object | Role |
|-----|--------|------------|------|
| `cycle-a-frozen-2026-05-08` | `6006e8071c1cf4dd284bb8232453682dee40de5b` | `eb21c916464c900c6fb92b26c264695a6ce0ce63` | Cycle A close ceremony — primary inventory anchor |
| `ontology-v1-final` | `b267cf32b6dd5f528ba29cd265a0886878bcf2a5` | `e2722ef8d3569d8a3e60a2c54012d058d751b6e8` | V1 ontology + apparatus + embeddings post-fix; identical content to cycle-a-frozen for technical artefacts |
| `ontology-v1-next-acr004-promoted` | (per FREEZE-REGISTRY item 11) | — | ACR-004 promotion landing |
| `apparatus-shacl-pyshacl-v3` | `58b1958ed87ecdc9b4b3a64f750230efa0fe57f1` | `579a799fe979ad22c73971af3cf82c7f817d1b91` | SHACL composition (2 files) — Decision 0001 Option C |
| `appsec-core-embeddings-v1.1` | `b948356468b657b388545d7a46c6e9973e45a46f` | `8318d88f70c501e2e0af8759cdfbff242e3db32a` | SBERT 212 entities |
| `ontology-v0-frozen` | `bd78a93ec5c904af30ee1e077bdc88aaaca555ac` | `604474fbd25ee010ae6a4e15172814439df5a820` | V0 baseline (preserved in-repo at `ontology/v0/` + `packages/v0/`) |

## Inventory (per-artefact SHA-256 + size + anchor)

# Inventory at tag cycle-a-frozen-2026-05-08

## Governance root (5 files)

Anchor: ontology-v1-final → b267cf3

| Path | SHA-256 | Size |
|------|---------|------|
| `AGENTS.md` | `0a4423c90471ffaf7f1769f89717326f1fba00b283a3071518c5928e50e5a2c3` | 20.9 KB |
| `FREEZE-REGISTRY.md` | `4fc3e52677bf349e61b93865f210fae49b2de291b72a47b41041ab4b859ddf06` | 37.0 KB |
| `PROGRAMME-PRESERVATION-PROTOCOL.md` | `d7b252a10385e628417ea17cd701fd5c6e87626ccb8ecdafe2f4f4833644588b` | 18.5 KB |
| `CHANGELOG.md` | `edf6b6548464aa5884ac24b7512da718e8bc24428d9522f23b94166b711b5fd5` | 4.9 KB |
| `LICENSE` | `7c0cd4f9d68b7344e82087c557b2ea0f09a10f8c3794d8649bf079c8f3b1c452` | 11.1 KB |
| `README.md` | `28dc0b3369ab20a960ce549fbc86877df7c185800cca283cb1bee9a52d0d0bec` | 3.4 KB |
| `ontology/v1.0/CHANGELOG.md` | `41bf8c444115c4f43d20adcc7cf10200001619d43ccb9308ad586faec8558a3f` | 12.9 KB |
| `ontology/README.md` | `7f8c5fb99814103070e26300405c547bb0791f75c2251e9e3ebe4ae487f6b39b` | 1.0 KB |

## Canonical YAML — V1 final working set (61 files)

Anchor: ontology-v1-final → b267cf3

| Path | SHA-256 | Size |
|------|---------|------|
| `ontology/appsec-core-architecture-trust-boundaries-components-draft.yaml` | `996d07a00eac4a54389be07aa5d1fcb0ac94f892d0186f65280b4b8f3f768385` | 7.5 KB |
| `ontology/appsec-core-architecture-trust-boundaries-draft.yaml` | `af97e9bfbd5cbdef1f6f332c8cdb35ae7946ecec4d3d75ab44125e06e4259a58` | 12.8 KB |
| `ontology/appsec-core-architecture-trust-boundaries-mapping-draft.yaml` | `00aa4c40840518a759c25606bbe505abbfc485d66d5962e549b0bd4bdaff7d60` | 9.6 KB |
| `ontology/appsec-core-architecture-trust-boundaries-slice-contract.yaml` | `32b17cc8a0c015d2aba30775de45c5ba7c213f557117277107f2c6f1da0f2a3c` | 6.1 KB |
| `ontology/appsec-core-cross-slice-vocabulary-v0-draft.yaml` | `b5c7859f7d9c3fb988266fea693a0cb3a1a06ad4e52bae805c2863a4dd53c6bf` | 7.1 KB |
| `ontology/appsec-core-entity-schema-v0-draft.yaml` | `491fc04f51abd1b3cc345d766ef979375d01a07d9c66fa1d728f94c6fa7014da` | 6.5 KB |
| `ontology/appsec-core-evidence-pattern-index-v0.yaml` | `5cfe10a942a3aaabf732ee7dbde9c9e34cb9c214478c4e698c566d3594c5006c` | 5.4 KB |
| `ontology/appsec-core-evidence-pattern-v0-draft.yaml` | `3a2b6b96d2cd9c90710733f2c36d44a186245a637ce2b95cd9e5c2bdfc730622` | 5.4 KB |
| `ontology/appsec-core-external-gap-analysis-v0-draft.yaml` | `8e1c46f182d9d68ea9f0d4b870978e4be207092b30ec5696c4620b7397c84132` | 5.2 KB |
| `ontology/appsec-core-identity-access-session-trust-components-draft.yaml` | `5cb975dc86c2537c1d1db583ebdccaaa0fe321d6b8eabe7d3390a4172d752f51` | 7.5 KB |
| `ontology/appsec-core-identity-access-session-trust-draft.yaml` | `79e44977d235e34160637fd05cb2cd18d33018d08953b827bb5805ab3c5b6954` | 12.9 KB |
| `ontology/appsec-core-identity-access-session-trust-mapping-draft.yaml` | `4cdcda6ebac68cac65f7e132671008127325c5943c281dfb3d77330259726cae` | 13.6 KB |
| `ontology/appsec-core-identity-access-session-trust-slice-contract.yaml` | `d19052a33ed6e2b67dd5989f02deafc22f820de10b18194f186774875cefade8` | 5.9 KB |
| `ontology/appsec-core-input-validation-safe-failure-components-draft.yaml` | `cba3561789648f0aaa838b94686f766a8a164ef79f035c57cae494bd1419b4bd` | 9.0 KB |
| `ontology/appsec-core-input-validation-safe-failure-draft.yaml` | `88f7c9aafb3524cfbdb49e6f976051f15eb2ae69ebe7b2aefe68abb529982a12` | 15.9 KB |
| `ontology/appsec-core-input-validation-safe-failure-mapping-draft.yaml` | `669120b9664c141b77952e2691e11077710a76eceaf2513098fd72707017dacf` | 10.2 KB |
| `ontology/appsec-core-input-validation-safe-failure-slice-contract.yaml` | `a967fea9c443e7fbb5e5ea40315f26dfaef39cb1787aa358e50cd17573070db2` | 7.1 KB |
| `ontology/appsec-core-integration-trust-service-security-components-draft.yaml` | `836d127100b3f4e98a14b4ec7fd7886e408b16e56dd3ac4dfb7a238fc8413b03` | 7.3 KB |
| `ontology/appsec-core-integration-trust-service-security-draft.yaml` | `2bc325956fb162a75402f75b245bec203acc9604c57c554034fb02378568d2a7` | 13.0 KB |
| `ontology/appsec-core-integration-trust-service-security-mapping-draft.yaml` | `fa0b320094580a5fd3e988d13bfa15f6580f29bf204b7ac5fb817b8086ead24a` | 10.1 KB |
| `ontology/appsec-core-integration-trust-service-security-slice-contract.yaml` | `0c25049430bdfafd3b5ffed3cc05bd3afd9c019b044f805e1e41e886b9f6e2e8` | 6.6 KB |
| `ontology/appsec-core-manual-mapping-v0-draft.yaml` | `7ad66f78a0f66181a12294874a8b8ca5ca27d952ed220596a74273b1a9ad3df7` | 7.1 KB |
| `ontology/appsec-core-release-promotion-controlled-rollout-components-draft.yaml` | `f843152576073543749985d4cf6000efe2708f1add98f367e4698bdb65aa05ab` | 11.6 KB |
| `ontology/appsec-core-release-promotion-controlled-rollout-draft.yaml` | `a4dc704542d2bcb49166d13ad28ef53b3afbfbe3f6561aee6645ba5bf0db8b54` | 15.0 KB |
| `ontology/appsec-core-release-promotion-controlled-rollout-mapping-draft.yaml` | `73b9ebbed02487095a362c5e08e2a37127c861d4b1ca30887c69cddbfbb7d36b` | 7.6 KB |
| `ontology/appsec-core-release-promotion-controlled-rollout-slice-contract.yaml` | `f8ddf6246c3b02b6e2a6c52eb9b899d38f95b98360bcf29217c9e64fe76407b8` | 6.6 KB |
| `ontology/appsec-core-secrets-protected-config-components-draft.yaml` | `f8b14e3ad25db66dabb84fb87397ba2a828b094126074be939ef4e3c2eda249e` | 6.1 KB |
| `ontology/appsec-core-secrets-protected-config-draft.yaml` | `871f2edcc24cb2f9267de3c7bf624825119a7457ae5489f20b002f9bd6e17ed7` | 11.2 KB |
| `ontology/appsec-core-secrets-protected-config-mapping-draft.yaml` | `0d3e093f57c3434eb926a1fe6436b695dd062536afc3b2340ebf9a9406f6b2b0` | 6.9 KB |
| `ontology/appsec-core-secrets-protected-config-slice-contract.yaml` | `eeecd99edb0921f6991f9aeff41b05b7f4310bfaa352089c0db19549fce83626` | 6.1 KB |
| `ontology/appsec-core-secure-configuration-baseline-integrity-cross-pilot-fit.yaml` | `c890b4ba2821f691dc2540f86e434478f26b779c104b11acd5167a8486b5e868` | 6.1 KB |
| `ontology/appsec-core-secure-configuration-baseline-integrity-draft.yaml` | `8ffda6a0cc5f970989113545da38053b1c6dfc680b84ba770964061187ace702` | 9.7 KB |
| `ontology/appsec-core-secure-configuration-baseline-integrity-future-integration.yaml` | `6d452d1a0fc24c52db7cb16376e13159601c24c326fefaa4a487e00732aa32f7` | 3.6 KB |
| `ontology/appsec-core-secure-configuration-baseline-integrity-manual-consumer-trial.yaml` | `88fb269fc5acf73e812e5c1616d0004da0d9992a4e302775bd57008b498af8c1` | 11.4 KB |
| `ontology/appsec-core-secure-configuration-baseline-integrity-validation-scaffold.yaml` | `fbdbc07318b305737b4e014ac0bf2c0aaa6811f587e9fb1525ff1619e831d0d1` | 5.4 KB |
| `ontology/appsec-core-security-event-logging-audit-trail-components-draft.yaml` | `e9df769ce0d02f8e4b4d5e5f1ea91173ca09cd0d705247c922fb0801a8bdf226` | 6.6 KB |
| `ontology/appsec-core-security-event-logging-audit-trail-draft.yaml` | `ec3325cf657a784d99eb75d432d69d632d764312aab17d3113befa6b7d0166fc` | 11.5 KB |
| `ontology/appsec-core-security-event-logging-audit-trail-mapping-draft.yaml` | `256dab9534373fcc51e86d8b2906b4ac1d45888d287e14f32f51ffe65ab742df` | 8.1 KB |
| `ontology/appsec-core-security-event-logging-audit-trail-slice-contract.yaml` | `b1b217b8b5720e10cc35db9aa7aa60289cbf80ee3f18ed99c591bf509215fb18` | 6.2 KB |
| `ontology/appsec-core-security-requirements-governance-draft.yaml` | `9e565ca19c89113346ef52321b031561b0b7509447299828a0e6d8339895dedf` | 11.0 KB |
| `ontology/appsec-core-security-requirements-manual-consumer-trial.yaml` | `b53087e7d3fd4cc5313b5314c2e352f944bac456b35806ec74407725eaa5481c` | 10.5 KB |
| `ontology/appsec-core-security-requirements-semantic-shape-read.yaml` | `d685340d129b7a6e73415707ff71465fb28fffdbed2549186ff8567954404a65` | 9.4 KB |
| `ontology/appsec-core-security-requirements-validation-scaffold.yaml` | `a56dc0eab474899ecd88a9b89afde520a0aa2b19993c38aac1b59d2e8fb34b8d` | 9.3 KB |
| `ontology/appsec-core-slice-registry-v0-draft.yaml` | `5799e53f1a039880f3148cb9d444e885e23c28968d38a64b68abd23e62a0d6c6` | 6.3 KB |
| `ontology/appsec-core-supply-chain-build-integrity-components-draft.yaml` | `4a64ec7ba1685eee74b69fcf3b011b346319f4310f2a112f9a0553fbf67a2519` | 9.6 KB |
| `ontology/appsec-core-supply-chain-build-integrity-draft.yaml` | `c1267206cf96e1c61f33b182886bed6b0e0610ecab81e6ffe0e4aa9a2334da50` | 11.2 KB |
| `ontology/appsec-core-supply-chain-build-integrity-mapping-draft.yaml` | `240de2810dfb5ebbddc0cba65ceb110e952c050c11d9dfa8272d1dbd6898e795` | 9.5 KB |
| `ontology/appsec-core-supply-chain-build-integrity-slice-contract.yaml` | `db069cf90f98c62e55db5daf2d8de5db39df66ecf159e194e0b4f20aee41bffd` | 5.3 KB |
| `ontology/appsec-core-testing-security-validation-components-draft.yaml` | `854b9feacf82921e388cbc4a2c6dd10e0b9cdb8143b8be65f40dce7e4a30fae1` | 8.9 KB |
| `ontology/appsec-core-testing-security-validation-draft.yaml` | `0c6040a867548a9f9cb56fa6af650ba7b35fa1b42e1bbcfc30314f0abb153900` | 12.2 KB |
| `ontology/appsec-core-testing-security-validation-mapping-draft.yaml` | `2c61e5aad085b7ec54d3d979704684c24f04cf7ccb41d4096c88956743ec3400` | 8.3 KB |
| `ontology/appsec-core-testing-security-validation-slice-contract.yaml` | `ad97f2a48624accc8ad7b201dbb85bb90269d13681d645ad381943ce05999680` | 6.0 KB |
| `ontology/appsec-core-threat-modeling-risk-disposition-components-draft.yaml` | `c6a12f681713123a5045df6d79f8015b704cb0da12d2887691de2d41bcd48e97` | 10.6 KB |
| `ontology/appsec-core-threat-modeling-risk-disposition-draft.yaml` | `b3f2bba65496032b27200dbf0eeb26d3352656d0b9226a605422f80182f605ee` | 13.2 KB |
| `ontology/appsec-core-threat-modeling-risk-disposition-mapping-draft.yaml` | `be837e37ab61a3441208f666a3459d176d4840c6e8062b0c2be351babd6d1a9f` | 6.9 KB |
| `ontology/appsec-core-threat-modeling-risk-disposition-slice-contract.yaml` | `57db11253685606dc7e88723ae14b209141d1434f9d6330daa950cf969661ea9` | 6.2 KB |
| `ontology/appsec-core-v0-consolidated.yaml` | `3b98831180304fdd28690f62969ae20c51d09865898f9de94049e24a44be627a` | 10.6 KB |
| `ontology/appsec-core-v0-draft.yaml` | `4a54e2254142c1da0891592cd86a2252a69a449d1f91398e81d135d993119bbf` | 12.6 KB |
| `ontology/appsec-core-v0-instance-index.yaml` | `cdc440e8532c68fe4135c3c8e9bb497de2279a795acdd547ae78a87805aea2df` | 10.2 KB |
| `ontology/appsec-core-v0-surface-contract.yaml` | `0831181e2d1635ea98c89d75252d702c21905dc4c2d1088bf4b17a2ea8d45ed3` | 5.8 KB |
| `ontology/sbdtoe-ontology.yaml` | `d2f1d319d0001732fedcdbd296104a001e147f75e00b0a281ebff516624218cf` | 30.8 KB |

## V0 archived snapshot (63 files)

Anchor: ontology-v0-frozen → bd78a93 (preserved in-repo at ontology/v0/)

| Path | SHA-256 | Size |
|------|---------|------|
| `ontology/v0/appsec-core-architecture-trust-boundaries-components-draft.yaml` | `996d07a00eac4a54389be07aa5d1fcb0ac94f892d0186f65280b4b8f3f768385` | 7.5 KB |
| `ontology/v0/appsec-core-architecture-trust-boundaries-draft.yaml` | `af97e9bfbd5cbdef1f6f332c8cdb35ae7946ecec4d3d75ab44125e06e4259a58` | 12.8 KB |
| `ontology/v0/appsec-core-architecture-trust-boundaries-mapping-draft.yaml` | `00aa4c40840518a759c25606bbe505abbfc485d66d5962e549b0bd4bdaff7d60` | 9.6 KB |
| `ontology/v0/appsec-core-architecture-trust-boundaries-slice-contract.yaml` | `32b17cc8a0c015d2aba30775de45c5ba7c213f557117277107f2c6f1da0f2a3c` | 6.1 KB |
| `ontology/v0/appsec-core-cross-slice-vocabulary-v0-draft.yaml` | `b5c7859f7d9c3fb988266fea693a0cb3a1a06ad4e52bae805c2863a4dd53c6bf` | 7.1 KB |
| `ontology/v0/appsec-core-entity-schema-v0-draft.yaml` | `491fc04f51abd1b3cc345d766ef979375d01a07d9c66fa1d728f94c6fa7014da` | 6.5 KB |
| `ontology/v0/appsec-core-evidence-pattern-index-v0.yaml` | `5cfe10a942a3aaabf732ee7dbde9c9e34cb9c214478c4e698c566d3594c5006c` | 5.4 KB |
| `ontology/v0/appsec-core-evidence-pattern-v0-draft.yaml` | `3a2b6b96d2cd9c90710733f2c36d44a186245a637ce2b95cd9e5c2bdfc730622` | 5.4 KB |
| `ontology/v0/appsec-core-external-gap-analysis-v0-draft.yaml` | `8e1c46f182d9d68ea9f0d4b870978e4be207092b30ec5696c4620b7397c84132` | 5.2 KB |
| `ontology/v0/appsec-core-identity-access-session-trust-components-draft.yaml` | `5cb975dc86c2537c1d1db583ebdccaaa0fe321d6b8eabe7d3390a4172d752f51` | 7.5 KB |
| `ontology/v0/appsec-core-identity-access-session-trust-draft.yaml` | `79e44977d235e34160637fd05cb2cd18d33018d08953b827bb5805ab3c5b6954` | 12.9 KB |
| `ontology/v0/appsec-core-identity-access-session-trust-mapping-draft.yaml` | `4cdcda6ebac68cac65f7e132671008127325c5943c281dfb3d77330259726cae` | 13.6 KB |
| `ontology/v0/appsec-core-identity-access-session-trust-slice-contract.yaml` | `d19052a33ed6e2b67dd5989f02deafc22f820de10b18194f186774875cefade8` | 5.9 KB |
| `ontology/v0/appsec-core-input-validation-safe-failure-components-draft.yaml` | `e83969640ff361bfdc4a5c5848b881fb7783a305e4ebfb34f6cf40f3737adcc5` | 7.7 KB |
| `ontology/v0/appsec-core-input-validation-safe-failure-draft.yaml` | `751f4e811d608fc74d97a96f40e78a22bc3c4809e22ad25df19984bae4330a6a` | 12.6 KB |
| `ontology/v0/appsec-core-input-validation-safe-failure-mapping-draft.yaml` | `669120b9664c141b77952e2691e11077710a76eceaf2513098fd72707017dacf` | 10.2 KB |
| `ontology/v0/appsec-core-input-validation-safe-failure-slice-contract.yaml` | `ab377cfb70485b184902d8deceb2c357b64d1ed7c78d100b7fd068436474ae56` | 6.4 KB |
| `ontology/v0/appsec-core-integration-trust-service-security-components-draft.yaml` | `836d127100b3f4e98a14b4ec7fd7886e408b16e56dd3ac4dfb7a238fc8413b03` | 7.3 KB |
| `ontology/v0/appsec-core-integration-trust-service-security-draft.yaml` | `2bc325956fb162a75402f75b245bec203acc9604c57c554034fb02378568d2a7` | 13.0 KB |
| `ontology/v0/appsec-core-integration-trust-service-security-mapping-draft.yaml` | `fa0b320094580a5fd3e988d13bfa15f6580f29bf204b7ac5fb817b8086ead24a` | 10.1 KB |
| `ontology/v0/appsec-core-integration-trust-service-security-slice-contract.yaml` | `0c25049430bdfafd3b5ffed3cc05bd3afd9c019b044f805e1e41e886b9f6e2e8` | 6.6 KB |
| `ontology/v0/appsec-core-manual-mapping-v0-draft.yaml` | `7ad66f78a0f66181a12294874a8b8ca5ca27d952ed220596a74273b1a9ad3df7` | 7.1 KB |
| `ontology/v0/appsec-core-release-promotion-controlled-rollout-components-draft.yaml` | `2a8daf0a4595fd1d89e4c5967d81f2adac5e8cc3f5e8dedcdcd11ed277c0f70c` | 8.0 KB |
| `ontology/v0/appsec-core-release-promotion-controlled-rollout-draft.yaml` | `dfe2e7a0429a32a66b069586eefc3bbb586edffed9c95b4d69964be2a5e6a394` | 12.0 KB |
| `ontology/v0/appsec-core-release-promotion-controlled-rollout-mapping-draft.yaml` | `73b9ebbed02487095a362c5e08e2a37127c861d4b1ca30887c69cddbfbb7d36b` | 7.6 KB |
| `ontology/v0/appsec-core-release-promotion-controlled-rollout-slice-contract.yaml` | `202521b6b1da3045548ddab20a062477384062a554c8859239c1c6baf1561e7a` | 6.5 KB |
| `ontology/v0/appsec-core-secrets-protected-config-components-draft.yaml` | `f8b14e3ad25db66dabb84fb87397ba2a828b094126074be939ef4e3c2eda249e` | 6.1 KB |
| `ontology/v0/appsec-core-secrets-protected-config-draft.yaml` | `871f2edcc24cb2f9267de3c7bf624825119a7457ae5489f20b002f9bd6e17ed7` | 11.2 KB |
| `ontology/v0/appsec-core-secrets-protected-config-mapping-draft.yaml` | `0d3e093f57c3434eb926a1fe6436b695dd062536afc3b2340ebf9a9406f6b2b0` | 6.9 KB |
| `ontology/v0/appsec-core-secrets-protected-config-slice-contract.yaml` | `eeecd99edb0921f6991f9aeff41b05b7f4310bfaa352089c0db19549fce83626` | 6.1 KB |
| `ontology/v0/appsec-core-secure-configuration-baseline-integrity-cross-pilot-fit.yaml` | `c890b4ba2821f691dc2540f86e434478f26b779c104b11acd5167a8486b5e868` | 6.1 KB |
| `ontology/v0/appsec-core-secure-configuration-baseline-integrity-draft.yaml` | `8ffda6a0cc5f970989113545da38053b1c6dfc680b84ba770964061187ace702` | 9.7 KB |
| `ontology/v0/appsec-core-secure-configuration-baseline-integrity-future-integration.yaml` | `6d452d1a0fc24c52db7cb16376e13159601c24c326fefaa4a487e00732aa32f7` | 3.6 KB |
| `ontology/v0/appsec-core-secure-configuration-baseline-integrity-manual-consumer-trial.yaml` | `88fb269fc5acf73e812e5c1616d0004da0d9992a4e302775bd57008b498af8c1` | 11.4 KB |
| `ontology/v0/appsec-core-secure-configuration-baseline-integrity-validation-scaffold.yaml` | `fbdbc07318b305737b4e014ac0bf2c0aaa6811f587e9fb1525ff1619e831d0d1` | 5.4 KB |
| `ontology/v0/appsec-core-security-event-logging-audit-trail-components-draft.yaml` | `c3f0e1a83671e3dfa76f1d5d5983c8a4abff92cab77922a25314ea80af8dcaea` | 5.5 KB |
| `ontology/v0/appsec-core-security-event-logging-audit-trail-draft.yaml` | `ec3325cf657a784d99eb75d432d69d632d764312aab17d3113befa6b7d0166fc` | 11.5 KB |
| `ontology/v0/appsec-core-security-event-logging-audit-trail-mapping-draft.yaml` | `256dab9534373fcc51e86d8b2906b4ac1d45888d287e14f32f51ffe65ab742df` | 8.1 KB |
| `ontology/v0/appsec-core-security-event-logging-audit-trail-slice-contract.yaml` | `b1b217b8b5720e10cc35db9aa7aa60289cbf80ee3f18ed99c591bf509215fb18` | 6.2 KB |
| `ontology/v0/appsec-core-security-requirements-governance-draft.yaml` | `9e565ca19c89113346ef52321b031561b0b7509447299828a0e6d8339895dedf` | 11.0 KB |
| `ontology/v0/appsec-core-security-requirements-manual-consumer-trial.yaml` | `b53087e7d3fd4cc5313b5314c2e352f944bac456b35806ec74407725eaa5481c` | 10.5 KB |
| `ontology/v0/appsec-core-security-requirements-semantic-shape-read.yaml` | `d685340d129b7a6e73415707ff71465fb28fffdbed2549186ff8567954404a65` | 9.4 KB |
| `ontology/v0/appsec-core-security-requirements-validation-scaffold.yaml` | `a56dc0eab474899ecd88a9b89afde520a0aa2b19993c38aac1b59d2e8fb34b8d` | 9.3 KB |
| `ontology/v0/appsec-core-slice-registry-v0-draft.yaml` | `502c571054c0b47b8a85162bdcd8f40eb84a6e9b6a550cfe65b4b15ca1420e93` | 6.3 KB |
| `ontology/v0/appsec-core-supply-chain-build-integrity-components-draft.yaml` | `4ff8674d26d43ac71c811c813538c3d198a8690c230fcc5899e2eb10192b8f61` | 9.0 KB |
| `ontology/v0/appsec-core-supply-chain-build-integrity-draft.yaml` | `c1267206cf96e1c61f33b182886bed6b0e0610ecab81e6ffe0e4aa9a2334da50` | 11.2 KB |
| `ontology/v0/appsec-core-supply-chain-build-integrity-mapping-draft.yaml` | `240de2810dfb5ebbddc0cba65ceb110e952c050c11d9dfa8272d1dbd6898e795` | 9.5 KB |
| `ontology/v0/appsec-core-supply-chain-build-integrity-slice-contract.yaml` | `db069cf90f98c62e55db5daf2d8de5db39df66ecf159e194e0b4f20aee41bffd` | 5.3 KB |
| `ontology/v0/appsec-core-testing-security-validation-components-draft.yaml` | `854b9feacf82921e388cbc4a2c6dd10e0b9cdb8143b8be65f40dce7e4a30fae1` | 8.9 KB |
| `ontology/v0/appsec-core-testing-security-validation-draft.yaml` | `0c6040a867548a9f9cb56fa6af650ba7b35fa1b42e1bbcfc30314f0abb153900` | 12.2 KB |
| `ontology/v0/appsec-core-testing-security-validation-mapping-draft.yaml` | `2c61e5aad085b7ec54d3d979704684c24f04cf7ccb41d4096c88956743ec3400` | 8.3 KB |
| `ontology/v0/appsec-core-testing-security-validation-slice-contract.yaml` | `ad97f2a48624accc8ad7b201dbb85bb90269d13681d645ad381943ce05999680` | 6.0 KB |
| `ontology/v0/appsec-core-threat-modeling-risk-disposition-components-draft.yaml` | `b568a8672fe1a2818792185a71fb7d296816f21e98976021c67f900f0b8430e8` | 8.2 KB |
| `ontology/v0/appsec-core-threat-modeling-risk-disposition-draft.yaml` | `102ea387bd0bd194218209729706883e0f6e321e6a028e5875576bcd8d02d205` | 11.4 KB |
| `ontology/v0/appsec-core-threat-modeling-risk-disposition-mapping-draft.yaml` | `be837e37ab61a3441208f666a3459d176d4840c6e8062b0c2be351babd6d1a9f` | 6.9 KB |
| `ontology/v0/appsec-core-threat-modeling-risk-disposition-slice-contract.yaml` | `dab3d99477778043a79c712d4a8d6cf689069d95e51d05680b44c48c7f72a467` | 6.1 KB |
| `ontology/v0/appsec-core-v0-consolidated.yaml` | `32106ef4adb04f357502d46dbdb82a7f076d7885d789046a6a082a215e57f7af` | 10.6 KB |
| `ontology/v0/appsec-core-v0-draft.yaml` | `5c1e69fe776608741ea7420e7aa2ca00efc7f56bf07a334a903f6195865a5e60` | 12.6 KB |
| `ontology/v0/appsec-core-v0-instance-index.yaml` | `ec3c4dafe397305d6e051c2d8da5ab58dd957e7b2df68fa7825c8f67a0f0a3a2` | 9.7 KB |
| `ontology/v0/appsec-core-v0-review-snapshot-unofficial.yaml` | `7e2c450cec11f9e9445a0c7b5eca9408c17d368fac4bd7b7fef1711c4c0312da` | 12.1 KB |
| `ontology/v0/appsec-core-v0-surface-contract.yaml` | `e04da474877d7c984df2033faebd59496ef09465130a2fcc1e8010330d551683` | 5.8 KB |
| `ontology/v0/sbdtoe-ontology-v2-draft.yaml` | `d2f1d319d0001732fedcdbd296104a001e147f75e00b0a281ebff516624218cf` | 30.8 KB |
| `ontology/v0/sbdtoe-ontology.yaml` | `d2f1d319d0001732fedcdbd296104a001e147f75e00b0a281ebff516624218cf` | 30.8 KB |

## OWL TTL exports (4 files)

Anchor: ontology-v1-final → b267cf3 (regenerated by build_owl.py)

| Path | SHA-256 | Size |
|------|---------|------|
| `formal/appsec_core/02-owl/exports/alt-formats/appsec-core-v1.0.jsonld` | `bf243aa17c29434f09f38fa4b80ebf06c4cd829ff0d61d557e4006b6e53f0e62` | 270.2 KB |
| `formal/appsec_core/02-owl/exports/alt-formats/appsec-core-v1.0.nt` | `4515c0f680ead59954ca957d5f7feb12a5dbb62449193ce1c64ec7464ce1203c` | 325.5 KB |
| `formal/appsec_core/02-owl/exports/alt-formats/appsec-core-v1.0.owl` | `dc0a80e1cf31cb6613886a476285988cff292c168e2431e6151c4f5349c8b484` | 161.0 KB |
| `formal/appsec_core/02-owl/exports/appsec-core-v0-bounded-v1.ttl` | `89b4ac1f1eb687ce92bc22526a430f0a5671ef7c1f4bb9c55a4d2f211a5aaf3b` | 81.1 KB |

## SHACL apparatus-v3 (2 files; composition declared per Decision 0001)

Anchor: apparatus-shacl-pyshacl-v3 → 58b1958

| Path | SHA-256 | Size |
|------|---------|------|
| `formal/appsec_core/03-shacl/shapes/appsec-core-v0-shapes.ttl` | `d30e716f470bc8570248509aa21285f71fb41062641ebc6d4e3fd4cf082413f9` | 11.5 KB |
| `formal/appsec_core/03-shacl/shapes/consumer-conformance-shapes.ttl` | `0b7821367d0b4ec8cbcabc1ef498e2a40b86fc01a4938c4132cdf6c3c26743c1` | 23.8 KB |

## SHACL validation reports (10 files)

Anchor: apparatus-shacl-pyshacl-v3 → 58b1958 (composed-shapes pyshacl conformance)

| Path | SHA-256 | Size |
|------|---------|------|
| `formal/appsec_core/05-validation/reports/appsec-core-v0-shacl-validation-report.md` | `87e26215df13276ac14ebc78423fc90fce3060083defbbed0888d60d9cf3097a` | 1.3 KB |
| `formal/appsec_core/05-validation/reports/appsec-core-v0-shacl-validation-summary.json` | `d1aa48c1798dfbc8e57b99bd559a9662b407f2b86da88cb4ab1746427f90a615` | 2.7 KB |
| `formal/appsec_core/05-validation/reports/appsec-core-v1-pyshacl-report.txt` | `77debc800e6c973b66475968bdf71e2e667df8f4108e7f5299fe1651e6606dc9` | 33 B |
| `formal/appsec_core/05-validation/reports/appsec-core-v1-pyshacl-results-graph.ttl` | `4a53a3befd9bcdb7273ef3d6e47a83be519927771faee49ef0d2a44ee23be2be` | 147 B |
| `formal/appsec_core/05-validation/reports/appsec-core-v1-pyshacl-summary.json` | `27a4831276a4eb036c8fa8009c814e07c7eedf1253ff69efb4d1141ad032a581` | 3.0 KB |
| `formal/appsec_core/05-validation/reports/appsec-core-v1-pyshacl-v2-bucket-a-report.md` | `b72ebe45de3b05f896e5a83cdbcfc2c0054fef1840231f0df9ebf46b9530c7b1` | 1.9 KB |
| `formal/appsec_core/05-validation/reports/appsec-core-v1-pyshacl-v2-bucket-a-summary.json` | `ae5607b4ed54b1979211c29f691cd084baa8403c4e2dbc48566afe87524280ce` | 2.0 KB |
| `formal/appsec_core/05-validation/reports/appsec-core-v1-pyshacl-v2-bucket-b-fixture.ttl` | `bef69eba2e46f10603f3f47163954a0debe4d254d17d0148c715b3504aaf7c60` | 2.9 KB |
| `formal/appsec_core/05-validation/reports/appsec-core-v1-pyshacl-v2-bucket-b-report.md` | `c53561d2b8c404dd6ec2fec06fa7fc75d0f080a39d416cd790823363e068cca3` | 3.2 KB |
| `formal/appsec_core/05-validation/reports/appsec-core-v1-pyshacl-v2-bucket-b-summary.json` | `dca6744406bf8cdf3be10123124eca3b380bc0b6edf8a2106520281df71b8f9d` | 7.2 KB |

## Embeddings v1.1 (7 files; SBERT all-MiniLM-L6-v2 @ c9745ed1)

Anchor: appsec-core-embeddings-v1.1 → b948356

| Path | SHA-256 | Size |
|------|---------|------|
| `formal/appsec_core/08-embeddings/README.md` | `094e16ed1cc032713695a6073476e66e0d1ead8bbc7e36bcc90941a51e1f62f7` | 7.8 KB |
| `formal/appsec_core/08-embeddings/augmentation-rule.yaml` | `124aed7347f1242a0716c1e877853624f8d8746ed671e711234778c296203251` | 11.2 KB |
| `formal/appsec_core/08-embeddings/augmented-text-corpus.json` | `5951fd82e4b7547b37989af5b2f403ff3fd5e8b484b760ce4c565a6756b96c42` | 140.3 KB |
| `formal/appsec_core/08-embeddings/build-script.py` | `de78f5c8586ecc08f005bf91db31917a7813933a93e9c50d32d701e95a2978d2` | 17.8 KB |
| `formal/appsec_core/08-embeddings/embeddings-all-MiniLM-L6-v2-c9745ed1.npz` | `17f6aac496b9896dae977a83745480322e1594a214bd9aa7b905f2cf9ddf23c8` | 328.9 KB |
| `formal/appsec_core/08-embeddings/embeddings-manifest.json` | `f25df6a853a74391936f362a31f4836f1f971380f55fa1d83d67ab5a4fe66f80` | 1.9 KB |
| `formal/appsec_core/08-embeddings/format-conventions-snippet.md` | `44d9e94225aa3e002f8d36fc5e81b39ba7053a7f7cfe0afb9535cbf960a30cbb` | 8.9 KB |

## Top-level build scripts (2 files)

Anchor: ontology-v1-final → b267cf3

| Path | SHA-256 | Size |
|------|---------|------|
| `scripts/consumer_conformance_validator.py` | `5539047170813d198e857938c252704826a6f0fbaf6b4825af9ea42eebe177ab` | 15.9 KB |
| `scripts/formalize_appsec_core.py` | `b5a1e103674b91860de83453670bd1baa5637fcf263f39c15063035b878a4638` | 496 B |

## Python formalization module (11 files)

Anchor: ontology-v1-final → b267cf3 (CLI + build + validate logic)

| Path | SHA-256 | Size |
|------|---------|------|
| `formal/appsec_core/python/src/appsec_core_formalization/__init__.py` | `633f76e529b02be74c50e0fc76f6374c0e8caf3bddb31744865405270b45f1b7` | 99 B |
| `formal/appsec_core/python/src/appsec_core_formalization/build_inventory.py` | `1fa3820effe8e2a41c3a5256002263e879ca4c5374be97f38cd808c00cec5952` | 4.8 KB |
| `formal/appsec_core/python/src/appsec_core_formalization/build_label_catalog.py` | `c883e7504004cd4ae14ba147e96ad5e14cb3667d6ef068e4e5bc922766a7e652` | 10.5 KB |
| `formal/appsec_core/python/src/appsec_core_formalization/build_owl.py` | `e327b2ed21606f8806993aa3ed245ebaf1065c1ab304b6b4d09c1642e4d1f404` | 23.6 KB |
| `formal/appsec_core/python/src/appsec_core_formalization/build_shacl.py` | `b0acc983e7f5f46680db304d4f20165fe45f92a2b578cd3653583e335da886f1` | 15.0 KB |
| `formal/appsec_core/python/src/appsec_core_formalization/cli.py` | `c73c102d3cccaecc96fac77157396ed7d81167c6a34c5480c39c195ab1e4040b` | 3.1 KB |
| `formal/appsec_core/python/src/appsec_core_formalization/paths.py` | `da3e6ea2a4cfc93f35739120eb5a9a0730e575f6bcf06b88a6c252895826613c` | 2.0 KB |
| `formal/appsec_core/python/src/appsec_core_formalization/source_bundle.py` | `0ed83edf55520bd74363d9b3d81e3a4836f41473bd8ce6d244e907835eb0fdd5` | 9.3 KB |
| `formal/appsec_core/python/src/appsec_core_formalization/validate_pyshacl.py` | `3bd29e8a641eed5e49a7bb31b2c4d7f17242efb92db3598b640967477a200f45` | 9.5 KB |
| `formal/appsec_core/python/src/appsec_core_formalization/validate_shacl.py` | `52e64960c0026909976a96e6e19484795dca9f786c74a736f214aa0b6fcfc787` | 9.8 KB |
| `formal/appsec_core/python/src/appsec_core_formalization/yaml_utils.py` | `38ee681588c7e02ce7c582b4be89b3cbc541aba21b632a3a35e17b6d770699b8` | 670 B |

## Decision records (1 files)

Anchor: various commit anchors per record

| Path | SHA-256 | Size |
|------|---------|------|
| `agentic/decisions/0001-consumer-conformance-shapes-ontology-owned.md` | `f64a27094c5e5ecbb3d1f77beb609c574b9caf30c38fab75c7ad317fe32e428f` | 7.1 KB |

## Audit briefs at cycle-a-frozen (5 files)

Anchor: various commit anchors

| Path | SHA-256 | Size |
|------|---------|------|
| `agentic/briefs/2026-04-17-archon-3-paper-supply.md` | `372445d511888589df70d30c19df77ec89f4f60b8e1ba155e5c708bc8be5f44b` | 3.4 KB |
| `agentic/briefs/2026-04-17-signal-evidencepattern-model-asymmetry.md` | `cc35bcb515f5035b798d6b3d37f85d993a1f2d655e934e7defaf2393a0b047e8` | 9.1 KB |
| `agentic/briefs/2026-04-17-tmr005-tmr008-remapping-scope-audit.md` | `630cbd987e9996587ec72acd09913cd3ee40d1113cfb3f2e18022147e33430b3` | 11.2 KB |
| `agentic/briefs/2026-05-03-archon-part-b-shacl-tier2.md` | `9456e993d0d8e2354ca18dd5d13f21adeb4b9c4c01ad31e4ca34189e16e22dc8` | 6.1 KB |
| `agentic/briefs/2026-05-05-acr004-output-rendering-slice-boundary.md` | `f57ccccad0fa16893b7b2564a29b14849d03dd1783c1768c3ee55017860d5278` | 15.5 KB |

## v0 / v0.1 release packages — immutable (32 files)

Anchor: ontology-v0-frozen lineage

| Path | SHA-256 | Size |
|------|---------|------|
| `packages/ontology/appsec-core/v0.1/MANIFEST.yaml` | `2b34b9335f4ea72699cb8beb42186b4cbca959dad5ec495630c19088441bdc72` | 4.0 KB |
| `packages/ontology/appsec-core/v0.1/README.md` | `a38a7240f4d8f4f8203541a7c6219fe0ebd7e82c210b4074bfd5d1d5f9cc6c34` | 1.1 KB |
| `packages/ontology/appsec-core/v0.1/formal/appsec-core-v0-bounded-v1.ttl` | `f6438a36f5fdcf1d1f4ab33ba1bbe2c89cfa7245d2f40435c63d55c5b4d8e268` | 53.7 KB |
| `packages/ontology/appsec-core/v0.1/formal/appsec-core-v0-class-model.svg` | `bedd59deae96fb1af6a564d84d7df9a8bb6351ff10af18683dc96c0b37ab9fb8` | 23.8 KB |
| `packages/ontology/appsec-core/v0.1/formal/appsec-core-v0-shacl-shapes.svg` | `8bb1e9fcb7b0baea6f19a46200fead4e1a06000730362738f2028a04d1e8bea6` | 34.8 KB |
| `packages/ontology/appsec-core/v0.1/formal/appsec-core-v0-shacl-validation-report.md` | `502e455ee54c94a15c3c1d2a8426e40e32536116af3d31d358484167ed5108ad` | 1.3 KB |
| `packages/ontology/appsec-core/v0.1/formal/appsec-core-v0-shacl-validation-summary.json` | `a311f7eb3160db9c1da830ac972ba775dfffda43ee76c9d76337251a8f248e7e` | 2.7 KB |
| `packages/ontology/appsec-core/v0.1/formal/appsec-core-v0-shapes.ttl` | `9c0780780805a465b099369c7b297ea739ebd2e887341b0d6be315855828495f` | 11.5 KB |
| `packages/ontology/appsec-core/v0.1/formal/appsec-core-v0-slice-entity-coverage.svg` | `2cec92a0e93b97903db531271fc34b9f12d4fb1bbf5ee9c294054cfcedf23778` | 24.8 KB |
| `packages/ontology/appsec-core/v0.1/formal/appsec-core-v0-ten-slice-overview.svg` | `e16b2c3caa92445576bc720cf4d2ed0e11d7ec7fe628357a6ca7d4373cafc9e1` | 17.6 KB |
| `packages/ontology/appsec-core/v0.1/ontology/appsec-core-evidence-pattern-index-v0.yaml` | `5cfe10a942a3aaabf732ee7dbde9c9e34cb9c214478c4e698c566d3594c5006c` | 5.4 KB |
| `packages/ontology/appsec-core/v0.1/ontology/appsec-core-evidence-pattern-v0-draft.yaml` | `3a2b6b96d2cd9c90710733f2c36d44a186245a637ce2b95cd9e5c2bdfc730622` | 5.4 KB |
| `packages/ontology/appsec-core/v0.1/ontology/appsec-core-slice-registry-v0-draft.yaml` | `502c571054c0b47b8a85162bdcd8f40eb84a6e9b6a550cfe65b4b15ca1420e93` | 6.3 KB |
| `packages/ontology/appsec-core/v0.1/ontology/appsec-core-v0-consolidated.yaml` | `32106ef4adb04f357502d46dbdb82a7f076d7885d789046a6a082a215e57f7af` | 10.6 KB |
| `packages/ontology/appsec-core/v0.1/ontology/appsec-core-v0-instance-index.yaml` | `ec3c4dafe397305d6e051c2d8da5ab58dd957e7b2df68fa7825c8f67a0f0a3a2` | 9.7 KB |
| `packages/ontology/appsec-core/v0.1/ontology/appsec-core-v0-surface-contract.yaml` | `e04da474877d7c984df2033faebd59496ef09465130a2fcc1e8010330d551683` | 5.8 KB |
| `packages/ontology/appsec-core/v0/MANIFEST.yaml` | `2b34b9335f4ea72699cb8beb42186b4cbca959dad5ec495630c19088441bdc72` | 4.0 KB |
| `packages/ontology/appsec-core/v0/README.md` | `a38a7240f4d8f4f8203541a7c6219fe0ebd7e82c210b4074bfd5d1d5f9cc6c34` | 1.1 KB |
| `packages/ontology/appsec-core/v0/formal/appsec-core-v0-bounded-v1.ttl` | `f6438a36f5fdcf1d1f4ab33ba1bbe2c89cfa7245d2f40435c63d55c5b4d8e268` | 53.7 KB |
| `packages/ontology/appsec-core/v0/formal/appsec-core-v0-class-model.svg` | `bedd59deae96fb1af6a564d84d7df9a8bb6351ff10af18683dc96c0b37ab9fb8` | 23.8 KB |
| `packages/ontology/appsec-core/v0/formal/appsec-core-v0-shacl-shapes.svg` | `8bb1e9fcb7b0baea6f19a46200fead4e1a06000730362738f2028a04d1e8bea6` | 34.8 KB |
| `packages/ontology/appsec-core/v0/formal/appsec-core-v0-shacl-validation-report.md` | `502e455ee54c94a15c3c1d2a8426e40e32536116af3d31d358484167ed5108ad` | 1.3 KB |
| `packages/ontology/appsec-core/v0/formal/appsec-core-v0-shacl-validation-summary.json` | `a311f7eb3160db9c1da830ac972ba775dfffda43ee76c9d76337251a8f248e7e` | 2.7 KB |
| `packages/ontology/appsec-core/v0/formal/appsec-core-v0-shapes.ttl` | `9c0780780805a465b099369c7b297ea739ebd2e887341b0d6be315855828495f` | 11.5 KB |
| `packages/ontology/appsec-core/v0/formal/appsec-core-v0-slice-entity-coverage.svg` | `2cec92a0e93b97903db531271fc34b9f12d4fb1bbf5ee9c294054cfcedf23778` | 24.8 KB |
| `packages/ontology/appsec-core/v0/formal/appsec-core-v0-ten-slice-overview.svg` | `e16b2c3caa92445576bc720cf4d2ed0e11d7ec7fe628357a6ca7d4373cafc9e1` | 17.6 KB |
| `packages/ontology/appsec-core/v0/ontology/appsec-core-evidence-pattern-index-v0.yaml` | `5cfe10a942a3aaabf732ee7dbde9c9e34cb9c214478c4e698c566d3594c5006c` | 5.4 KB |
| `packages/ontology/appsec-core/v0/ontology/appsec-core-evidence-pattern-v0-draft.yaml` | `3a2b6b96d2cd9c90710733f2c36d44a186245a637ce2b95cd9e5c2bdfc730622` | 5.4 KB |
| `packages/ontology/appsec-core/v0/ontology/appsec-core-slice-registry-v0-draft.yaml` | `502c571054c0b47b8a85162bdcd8f40eb84a6e9b6a550cfe65b4b15ca1420e93` | 6.3 KB |
| `packages/ontology/appsec-core/v0/ontology/appsec-core-v0-consolidated.yaml` | `32106ef4adb04f357502d46dbdb82a7f076d7885d789046a6a082a215e57f7af` | 10.6 KB |
| `packages/ontology/appsec-core/v0/ontology/appsec-core-v0-instance-index.yaml` | `ec3c4dafe397305d6e051c2d8da5ab58dd957e7b2df68fa7825c8f67a0f0a3a2` | 9.7 KB |
| `packages/ontology/appsec-core/v0/ontology/appsec-core-v0-surface-contract.yaml` | `e04da474877d7c984df2033faebd59496ef09465130a2fcc1e8010330d551683` | 5.8 KB |

## Post-cycle-a-frozen audit briefs (1 files; HEAD of main = 496f6f5+)

Anchor: HEAD of main (post 2026-05-08 cycle-a-frozen)

| Path | SHA-256 | Size |
|------|---------|------|
| `agentic/briefs/2026-05-08-p7-pass-6-ontology-audit-delivery.md` | `5105d8fa37a8db33700a57c0c09d376c43be4e68baf62490f9d3a9cb3e3c0631` | 12.9 KB |

# TOTAL: 207 files inventoried

## Reproducibility instructions

### Environment specification (Decision 0003 Amendment 1 §F)

| Dimension | Value |
|-----------|-------|
| OS | Darwin x86_64 (uname -sm: `Darwin x86_64`) |
| Python | 3.10.1 |
| transformers | 4.57.1 |
| torch | 2.2.2 |
| numpy | 1.24.4 |
| pyshacl | 0.31.0 |
| rdflib | 7.6.0 |
| SBERT model | `sentence-transformers/all-MiniLM-L6-v2` |
| HF revision SHA | `c9745ed1d9f207416be6d2e6f8de32d1f16199bf` |
| Encoder max tokens | 256 |
| Pooling | mean (attention-mask-weighted) |
| Normalize | L2 (p=2, dim=1) |

Bit-identical .npz output requires identical OS architecture + Python interpreter + library versions + model snapshot. Cross-architecture identity is NOT guaranteed; the manifest records arch + lib versions for diagnostic purposes (`embeddings-manifest.json` `platform` and `library_versions` blocks).

### Execution sequence

```
# 1. Clone or extract bundle
git clone https://github.com/SbD-ToE/sbd-toe-ontology.git
cd sbd-toe-ontology
git checkout cycle-a-frozen-2026-05-08

# 2. Install build dependencies (optional extras)
python3 -m pip install -e .[formal-validation]   # adds pyshacl + rdflib

# 3. Regenerate OWL TTL exports from canonical YAML
python3 scripts/formalize_appsec_core.py owl-starter
# Expected output: formal/appsec_core/02-owl/exports/appsec-core-v0-bounded-v1.ttl
# Expected SHA-256: 89b4ac1f1eb687ce92bc22526a430f0a5671ef7c1f4bb9c55a4d2f211a5aaf3b

# 4. Regenerate ontology-only SHACL shapes (does NOT touch consumer-conformance-shapes.ttl)
python3 scripts/formalize_appsec_core.py shacl-starter
# Expected output: formal/appsec_core/03-shacl/shapes/appsec-core-v0-shapes.ttl
# Expected SHA-256: d30e716f470bc8570248509aa21285f71fb41062641ebc6d4e3fd4cf082413f9

# 5. In-house bounded SHACL validation
python3 scripts/formalize_appsec_core.py validate-shacl
# Expected: conforms=True, 0 violations across 6 shapes (Slice 10 / CO 75 / P 69 / M 58 / A 57 / EP 0)

# 6. W3C-canonical pyshacl validation against COMPOSED apparatus-v3 shapes
PYTHONPATH=formal/appsec_core/python/src python3 -m appsec_core_formalization.validate_pyshacl
# Expected: conforms=True, 0 violations (data 1824 / shapes 396 = 298 ontology + 98 consumer-conformance modulo prefix overlap)
# Expected SHA-256 (composed shapes graph members):
#   appsec-core-v0-shapes.ttl       d30e716f470bc8570248509aa21285f71fb41062641ebc6d4e3fd4cf082413f9
#   consumer-conformance-shapes.ttl 0b7821367d0b4ec8cbcabc1ef498e2a40b86fc01a4938c4132cdf6c3c26743c1

# 7. Regenerate SBERT embeddings (deterministic given env match)
cd formal/appsec_core/08-embeddings
python3 build-script.py
# Expected outputs:
#   augmented-text-corpus.json  SHA-256: 5951fd82e4b7547b37989af5b2f403ff3fd5e8b484b760ce4c565a6756b96c42
#   embeddings-all-MiniLM-L6-v2-c9745ed1.npz  SHA-256: 17f6aac496b9896dae977a83745480322e1594a214bd9aa7b905f2cf9ddf23c8
#   shape: (212, 384) float32 L2-normalized
```

### Manual-maintained vs schema-derived distinction (Decision 0001 Option C)

Critical for reproducibility: the apparatus SHACL skin is a **two-file composition**, with two different regeneration lifecycles.

| File | Source | Regen lifecycle | Touched by `build_shacl.py` |
|------|--------|-----------------|----------------------------|
| `formal/appsec_core/03-shacl/shapes/appsec-core-v0-shapes.ttl` | YAML schema | Schema-derived deterministic; regenerated whenever ontology entity schema or instance set changes | ✅ Yes |
| `formal/appsec_core/03-shacl/shapes/consumer-conformance-shapes.ttl` | Decision 0003 + Amendment 1 model invariants | Hand-maintained; updated only via cross-persona dispatcher when Decision 0003 amends model invariants | ❌ No (regen-safety boundary) |

Pyshacl runner (`validate_pyshacl.py`) loads BOTH files and merges them into a single shapes graph before validation. Apparatus tags (`apparatus-shacl-pyshacl-vN`) declare both files explicitly in their FREEZE-REGISTRY entry.

### Expected verification SHA-256 at each output stage

| Stage | Output file | Expected SHA-256 |
|-------|-------------|------------------|
| YAML canonical | `ontology/appsec-core-v0-instance-index.yaml` | `cdc440e8532c68fe4135c3c8e9bb497de2279a795acdd547ae78a87805aea2df` |
| OWL TTL | `formal/appsec_core/02-owl/exports/appsec-core-v0-bounded-v1.ttl` | `89b4ac1f1eb687ce92bc22526a430f0a5671ef7c1f4bb9c55a4d2f211a5aaf3b` |
| SHACL ontology shapes | `formal/appsec_core/03-shacl/shapes/appsec-core-v0-shapes.ttl` | `d30e716f470bc8570248509aa21285f71fb41062641ebc6d4e3fd4cf082413f9` |
| SHACL consumer-conformance shapes | `formal/appsec_core/03-shacl/shapes/consumer-conformance-shapes.ttl` | `0b7821367d0b4ec8cbcabc1ef498e2a40b86fc01a4938c4132cdf6c3c26743c1` |
| Bounded validator summary | `formal/appsec_core/05-validation/reports/appsec-core-v0-shacl-validation-summary.json` | `d1aa48c1798dfbc8e57b99bd559a9662b407f2b86da88cb4ab1746427f90a615` |
| Pyshacl summary | `formal/appsec_core/05-validation/reports/appsec-core-v1-pyshacl-summary.json` | `27a4831276a4eb036c8fa8009c814e07c7eedf1253ff69efb4d1141ad032a581` |
| Augmented text corpus | `formal/appsec_core/08-embeddings/augmented-text-corpus.json` | `5951fd82e4b7547b37989af5b2f403ff3fd5e8b484b760ce4c565a6756b96c42` |
| NPZ embeddings | `formal/appsec_core/08-embeddings/embeddings-all-MiniLM-L6-v2-c9745ed1.npz` | `17f6aac496b9896dae977a83745480322e1594a214bd9aa7b905f2cf9ddf23c8` |
| Embeddings manifest | `formal/appsec_core/08-embeddings/embeddings-manifest.json` | `f25df6a853a74391936f362a31f4836f1f971380f55fa1d83d67ab5a4fe66f80` |

## Cross-repository references (companion artefacts not in ontology repo)

For independent reproduction of the V1 evidence chain, the following companions live in sister repositories:

| Repository | Path | Role | SHA-256 |
|------------|------|------|---------|
| `sbd-toe-knowledge-graph` | `data/publish/runtime/evidence_patterns.json` | v0 supporting index of 213 evidence patterns (Codex publish surface; declared by `appsec-core-evidence-pattern-index-v0.yaml`) | `89305ffcd279bdeb071bad48566cb96d11d524eeafdddd157ce6078bab95e394` |
| `sbd-toe-knowledge-graph` | `data/entities/evidence_patterns.json` | Source-of-truth inventory before publication | `9a82b04b9d2b6b636f034505db80048332ec87448dec6b17f4a99b61674b858b` |
| `sbd-toe-mcp-poc` | `data/publish/runtime/evidence_patterns.json` | Bit-identical mirror of publish surface | (same as kg publish) |
| `securitybydesign-oss-mcp` | `data/publish/runtime/evidence_patterns.json` | Bit-identical mirror of publish surface | (same as kg publish) |
| `ExternalSourcesInventory` | (substrate v7 SUPPLIER) | Empirical conformance evidence (zero EvidencePattern claims at v7) | `596783ed984d9c0e8c8ef6439a0eaee8fbaf2d863af37138cde8fad55d62be04` |

## V0→V1 cycle deltas (audit reference for §6 paper prose)

| Source | +CO | +P | +M | +A | Total |
|--------|----:|---:|---:|---:|------:|
| ACR-001 (Repository coverage) | 3 | 3 | 3 | 4 | 13 |
| ACR-002 (Security Requirements Lifecycle) | 1 | 2 | 2 | 0 | 5 |
| ACR-004 (Output Rendering Safety) | 1 | 1 | 1 | 0 | 3 |
| Within-slice refinement (4 missing Mechanisms) | 0 | 0 | 4 | 0 | 4 |
| **Net delta** | **+5** | **+6** | **+10** | **+4** | **+25** |
| **V0 → V1** | **70 → 75** | **63 → 69** | **48 → 58** | **53 → 57** | **234 → 259** |

Full per-entity attribution with introducing commits: see `agentic/briefs/2026-05-08-p7-pass-6-ontology-audit-delivery.md`.

## EvidencePattern V1 disposition (figshare relevance)

- Class declarative shape retained: `EvidencePatternShape` defined at `apparatus-shacl-pyshacl-v3` with `target_node_count = 0`, violations = 0.
- Populated graph V1 = 0 EvidencePattern instances (substrate v7 corroborates).
- v0 supporting index of 213 patterns: canonical preservation in `sbd-toe-knowledge-graph` publish surface (cross-repo reference above); declared as `source_alignment` block in `ontology/appsec-core-evidence-pattern-index-v0.yaml`.

Full disposition prose: see `agentic/briefs/2026-05-08-p7-pass-6-ontology-audit-delivery.md` §"3-4 sentence prose for §2.2 / §6.1".

## References

- Inbound mini-dispatch: `sbd-ai-runtime/handover/em-curso/2026-05-08-orchestrator-archon-figshare-inventory-mini-dispatch.md`
- Parent dispatcher (Curator coordination): `sbd-ai-runtime/handover/em-curso/2026-05-08-orchestrator-curator-phase-a-figshare-bundle-coordination.md`
- P7 Pass 6 ontology audit (sister deliverable, same day): `agentic/briefs/2026-05-08-p7-pass-6-ontology-audit-delivery.md`
- Architectural decision (Option C apparatus composition): `agentic/decisions/0001-consumer-conformance-shapes-ontology-owned.md`
- ACR-004 promotion brief: `agentic/briefs/2026-05-05-acr004-output-rendering-slice-boundary.md`
- v1.1-draft cumulative changes: `ontology/v1.0/CHANGELOG.md`
- FREEZE-REGISTRY (full tag history): `FREEZE-REGISTRY.md`
- Embeddings reproducibility ratification: Decision 0003 Amendment 1 §F (`ExternalSourcesInventory/agentic/decisions/0003-normalization-algorithm-redesign-2026-05-03-amendment-1-claims-not-chains.md`)
