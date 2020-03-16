#!/bin/bash
(./recipe_render.py $(ls json/*.json) && rm *.log *.aux json/*.tex && rm output/*.pdf && mv *.pdf output/ && echo "Done!") || echo "Failed :("
