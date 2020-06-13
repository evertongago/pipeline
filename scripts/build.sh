#!/bin/bash -e

BASE_DIR="$(dirname $0)"

gsutil -m rm -R "gs://deeapipe/pipeline"
gsutil -m cp -r "$BASE_DIR/../src" "gs://deeapipe/pipeline/src"
gsutil cp "$BASE_DIR/../requirements.txt" "gs://deeapipe/pipeline/requirements.txt"
gsutil cp "$BASE_DIR/../setup.py" "gs://deeapipe/pipeline/setup.py"
gsutil cp "$BASE_DIR/init.sh" "gs://deeapipe/pipeline/scripts/init.sh"

gcloud dataproc workflow-templates instantiate-from-file --file "$BASE_DIR/../workflow.yaml"
