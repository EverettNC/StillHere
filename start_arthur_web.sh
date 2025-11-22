#!/bin/bash

echo "Starting Arthur Web Interface..."
echo ""
echo "Family members can access at:"
echo "  http://localhost:8501"
echo ""
echo "Or share this link if on same network:"
LOCAL_IP=$(ipconfig getifaddr en0 || ipconfig getifaddr en1 || echo "localhost")
echo "  http://$LOCAL_IP:8501"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

cd "$(dirname "$0")"
streamlit run arthur_web.py --server.port 8501 --server.address 0.0.0.0
