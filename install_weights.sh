#!/bin/bash
set -e 

wget -O models_bundle.zip https://huggingface.co/Gurbanov/New_model/blob/main/models.zip

unzip -o models_bundle.zip -d .

rm models_bundle.zip

echo "done"
