#!/bin/bash -e

BASE_DIR="$(dirname $0)"

gsutil -m rm -R "gs://krtn/pipeline"
gsutil -m cp -r "$BASE_DIR/../src" "gs://krtn/pipeline/src"
gsutil cp "$BASE_DIR/../requirements.txt" "gs://krtn/pipeline/requirements.txt"
gsutil cp "$BASE_DIR/../setup.py" "gs://krtn/pipeline/setup.py"
gsutil cp "$BASE_DIR/init.sh" "gs://krtn/pipeline/scripts/init.sh"

gcloud dataproc workflow-templates instantiate-from-file --file "$BASE_DIR/../workflow.yaml"
