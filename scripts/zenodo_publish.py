#!/usr/bin/env python3
"""
Publish a release archive to Zenodo via the deposit API.

Required env vars:
  ZENODO_TOKEN              — personal access token
  VERSION                   — tag, e.g. v1.0.4
  ARCHIVE                   — path to the zip file to upload

Optional env vars:
  ZENODO_CONCEPT_RECORD_ID  — if set, creates a new version of an existing record;
                               otherwise creates a brand-new deposition.
"""

import json
import os
import re
import sys
import requests

ZENODO_SANDBOX = os.environ.get("ZENODO_SANDBOX", "").strip().lower() in ("1", "true", "yes")
ZENODO_API = "https://sandbox.zenodo.org/api" if ZENODO_SANDBOX else "https://zenodo.org/api"

TOKEN = os.environ["ZENODO_TOKEN"]
VERSION = os.environ["VERSION"]
ARCHIVE = os.environ["ARCHIVE"]
CONCEPT_ID = os.environ.get("ZENODO_CONCEPT_RECORD_ID", "").strip()

params = {"access_token": TOKEN}
json_headers = {"Content-Type": "application/json"}


CREATOR_ALLOWED = {"name", "affiliation", "orcid", "gnd"}


def load_metadata():
    with open(".zenodo.json") as f:
        meta = json.load(f)
    meta["version"] = VERSION
    meta["title"] = re.sub(r"v\d+\.\d+\.\d+", VERSION, meta["title"])
    # Strip fields not accepted by the deposit API in creators
    meta["creators"] = [
        {k: v for k, v in c.items() if k in CREATOR_ALLOWED}
        for c in meta.get("creators", [])
    ]
    return meta


def get_latest_deposit_id(concept_id):
    # Strategy 1: deposit API with all_versions=true
    # Without all_versions, published older versions are not returned.
    r = requests.get(
        f"{ZENODO_API}/deposit/depositions",
        params={
            **params,
            "q": f"conceptrecid:{concept_id}",
            "all_versions": "true",
            "sort": "mostrecent",
            "size": 1,
        },
    )
    r.raise_for_status()
    hits = r.json()
    if hits:
        print(f"Found latest deposition via deposit API: id={hits[0]['id']}")
        return hits[0]["id"]

    # Strategy 2: fallback to records API
    # The records API indexes published versions; we use the record id
    # of the latest published version as the source for newversion action.
    print(
        f"Deposit API returned no hits for concept {concept_id}; "
        f"falling back to records API..."
    )
    r = requests.get(
        f"{ZENODO_API}/records",
        params={
            "q": f"conceptrecid:{concept_id}",
            "all_versions": "true",
            "sort": "mostrecent",
            "size": 1,
            "access_token": TOKEN,
        },
    )
    r.raise_for_status()
    payload = r.json()
    record_hits = payload.get("hits", {}).get("hits", [])
    if not record_hits:
        raise SystemExit(
            f"No depositions or published records found for concept record {concept_id}. "
            f"Verify the concept record id is correct and the token has access to it."
        )
    record_id = record_hits[0]["id"]
    print(f"Found latest published version via records API: id={record_id}")
    return record_id


def create_new_version(concept_id):
    latest_id = get_latest_deposit_id(concept_id)
    r = requests.post(
        f"{ZENODO_API}/deposit/depositions/{latest_id}/actions/newversion",
        params=params,
    )
    r.raise_for_status()
    draft_url = r.json()["links"]["latest_draft"]
    dep_id = draft_url.rsplit("/", 1)[-1]
    return dep_id


def create_deposition():
    r = requests.post(
        f"{ZENODO_API}/deposit/depositions",
        params=params,
        headers=json_headers,
        json={},
    )
    r.raise_for_status()
    return r.json()["id"]


def update_metadata(dep_id, meta):
    r = requests.put(
        f"{ZENODO_API}/deposit/depositions/{dep_id}",
        params=params,
        headers=json_headers,
        json={"metadata": meta},
    )
    r.raise_for_status()


def delete_existing_files(dep_id):
    r = requests.get(f"{ZENODO_API}/deposit/depositions/{dep_id}/files", params=params)
    r.raise_for_status()
    for f in r.json():
        requests.delete(
            f"{ZENODO_API}/deposit/depositions/{dep_id}/files/{f['id']}",
            params=params,
        )


def upload_file(dep_id, filepath):
    filename = os.path.basename(filepath)
    with open(filepath, "rb") as fh:
        r = requests.post(
            f"{ZENODO_API}/deposit/depositions/{dep_id}/files",
            params=params,
            data={"filename": filename},
            files={"file": fh},
        )
    r.raise_for_status()


def publish(dep_id):
    r = requests.post(
        f"{ZENODO_API}/deposit/depositions/{dep_id}/actions/publish",
        params=params,
    )
    if not r.ok:
        print(f"Zenodo error {r.status_code}: {r.text}")
    r.raise_for_status()
    return r.json()


def write_output(key, value):
    path = os.environ.get("GITHUB_OUTPUT")
    if path:
        with open(path, "a") as f:
            f.write(f"{key}={value}\n")


def main():
    meta = load_metadata()

    if CONCEPT_ID:
        print(f"Creating new version from concept record {CONCEPT_ID}...")
        dep_id = create_new_version(CONCEPT_ID)
        update_metadata(dep_id, meta)
        delete_existing_files(dep_id)
    else:
        print("Creating new deposition...")
        dep_id = create_deposition()
        update_metadata(dep_id, meta)

    print(f"Uploading {ARCHIVE}...")
    upload_file(dep_id, ARCHIVE)

    print("Publishing...")
    result = publish(dep_id)

    doi = result.get("doi", "")
    doi_url = result.get("doi_url", "")
    print(f"DOI:  {doi}")
    print(f"URL:  {doi_url}")

    write_output("doi", doi)
    write_output("doi_url", doi_url)


if __name__ == "__main__":
    main()
