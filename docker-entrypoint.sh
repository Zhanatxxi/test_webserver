#!/bin/sh
echo 'i work'

alembic upgrade head

python api.py