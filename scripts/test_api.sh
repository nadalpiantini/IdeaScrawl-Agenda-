#!/bin/bash
# API testing script for IdeaScrawl Agenda

API_URL="http://localhost:8000"

echo "🧪 Testing IdeaScrawl Agenda API"
echo "================================"

# Test health endpoint
echo "1. Health Check..."
response=$(curl -s -w "%{http_code}" -o /tmp/health_response "$API_URL/health")
if [ "$response" = "200" ]; then
    echo "✅ Health check passed"
    cat /tmp/health_response | jq '.' 2>/dev/null || cat /tmp/health_response
else
    echo "❌ Health check failed (HTTP $response)"
    exit 1
fi

echo ""

# Test generate-page endpoint
echo "2. Generate Page Test..."
cat > /tmp/test_payload.json << EOF
{
  "title": "API Test",
  "text": "This is a test message to validate the generate-page endpoint is working correctly.",
  "timestamp": $(date +%s)000
}
EOF

response=$(curl -s -w "%{http_code}" -o /tmp/generate_response \
    -X POST "$API_URL/generate-page" \
    -H "Content-Type: application/json" \
    -d @/tmp/test_payload.json)

if [ "$response" = "200" ]; then
    echo "✅ Generate page test passed"
    cat /tmp/generate_response | jq '.' 2>/dev/null || cat /tmp/generate_response
else
    echo "❌ Generate page test failed (HTTP $response)"
    cat /tmp/generate_response
    exit 1
fi

echo ""
echo "🎉 All API tests passed!"
echo ""
echo "💡 Next steps:"
echo "   - Install Chrome extension from /extension folder"
echo "   - Visit chat.openai.com to test full pipeline"

# Cleanup
rm -f /tmp/health_response /tmp/generate_response /tmp/test_payload.json