# NIST OLIR Validation Tool JAR — Defence-in-Depth Verification

**Date:** 2026-05-09
**Verifier:** Cartographer (closure dispatcher 2026-05-09 Step 1)
**Authority:** programme-lead Pedro Farinha 2026-05-09 (Option C ratified)

## JAR provenance

- **Canonical URL:** https://csrc.nist.gov/Projects/olir/validation-tool
- **Canonical version:** OLIR Validation Tool 4.9.9 (released 2023-05-18)
- **Canonical SHA3-256:** `5809e7d93dc243fa2cf2e495bd7117404c9f9ba6df254a4b8be738f58176f074`
- **Provenance investigation:** programme-lead Pedro Farinha 2026-05-09; csrc.nist.rip identified as unofficial archive (page self-discloses "Official websites do not use .rip"); v3.22 from 2021 is stale — IGNORED.

## SHA3-256 verification (downloaded JAR matches canonical)

```
$ python3 -c "import hashlib; print(hashlib.sha3_256(open(\"/tmp/olir_validator.jar\",\"rb\").read()).hexdigest())"
5809e7d93dc243fa2cf2e495bd7117404c9f9ba6df254a4b8be738f58176f074
```

**Verdict:** ✅ MATCH (canonical hash provenance confirmed)

## jarsigner -verify -verbose -certs (defence in depth)

```
$ jarsigner -verify -verbose -certs /tmp/olir_validator.jar | tail -10
        576 Thu Jun 18 20:06:14 WEST 2009 org/apache/http/UnsupportedHttpVersionException.class
          0 Thu Jun 18 20:05:28 WEST 2009 META-INF/maven/org.apache.httpcomponents/httpcore/
       4889 Thu Jun 18 20:05:28 WEST 2009 META-INF/maven/org.apache.httpcomponents/httpcore/pom.xml
        119 Thu Jun 18 20:06:26 WEST 2009 META-INF/maven/org.apache.httpcomponents/httpcore/pom.properties

  s = signature was verified 
  m = entry is listed in manifest
  k = at least one certificate was found in keystore

jar is unsigned.
```

**Verdict:** "jar is unsigned"

## Programme-level interpretation

Per closure dispatcher 2026-05-09 §"Result interpretation":

> "jar is unsigned" → ⚠️ canonical hash provenance still strong; document as defence-in-depth limitation per Pedro's verdict.

Outcome: **proceed to Steps 2-6** (signature invalid would have escalated). NIST does not sign this distribution; canonical SHA3-256 anchored to the canonical NIST URL is sufficient evidence trail. JAR is **safe to execute for signature verification only** per dispatcher; xlsx-roundtrip execution remains deferred to Phase B.

## File metadata

```
-rw-r--r--@ 1 pedrofarinha  wheel  17411655  9 mai 01:01 /tmp/olir_validator.jar
```

## Cross-references

- Closure dispatcher: `sbd-ai-runtime/handover/em-curso/2026-05-09-orchestrator-cartographer-olir-closure-and-jarsigner-dispatch.md`
- OLIR exports: `data/p7_olir_audit/p7_v2_corrected/v7/olir_exports/` (101 OLIR-format files; 66 Step 2 + 35 Schema 1.1)
- NIST OLIR JSON Schema 1.1 validator: `scripts/olir/validate_olir_jsonschema.py` (31/31 PASS)
- Step 2 generation methodology: `agentic/briefs/2026-05-09-olir-conversion-methodology.md`
