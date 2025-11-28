curl --request POST \
  --url https://api.exa.ai/contents \
  --header "x-api-key: $EXA_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "urls": ["https://celestegame.fandom.com/wiki/Celeste_Wiki"],
    "subpages": 10,
    "text": true
  }'