"""
StillHere Web Application
imstillhere.world - Keep Your Loved Ones Close

Built with love by The Christman AI Project
Carbon & Silicon in Unity
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from pathlib import Path
import os

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'change-this-in-production')

# Pricing tiers
PRICING_TIERS = {
    'free': {
        'name': 'Free',
        'price': 0,
        'price_display': 'Free',
        'description': 'Try it - see your loved one move',
        'features': [
            '1 photo upload',
            'Basic slideshow (5-10 seconds)',
            '3 music tracks',
            '720p export',
            'StillHere watermark'
        ],
        'cta': 'Start Free'
    },
    'memory': {
        'name': 'Memory',
        'price': 9.99,
        'price_display': '$9.99',
        'description': 'Beautiful memorial video to share',
        'features': [
            'Up to 10 photos',
            'Gentle animations (breathing, smile)',
            'Full music library (20+ tracks)',
            '1080p HD export',
            'No watermark',
            'Download & share'
        ],
        'cta': 'Create Memory',
        'stripe_price_id': 'price_memory'
    },
    'living': {
        'name': 'Living Memory',
        'price': 29.99,
        'price_display': '$29.99',
        'description': 'Hear them speak again',
        'features': [
            'Everything in Memory tier',
            'Up to 30 photos',
            'Voice synthesis - hear them speak',
            'Advanced animations (head turns, realistic movement)',
            'Photo restoration (fix old photos)',
            'Multiple video exports'
        ],
        'cta': 'Bring Them Back',
        'stripe_price_id': 'price_living'
    },
    'eternal': {
        'name': 'Eternal Companion',
        'price': 199.00,
        'price_display': '$199/month',
        'description': 'Talk to them anytime, forever',
        'badge': 'Early Access Family',
        'features': [
            'Everything in Living Memory tier',
            '🔥 EARLY ACCESS FAMILY STATUS',
            'Beta test new features 3-6 months before public release',
            'Fully conversational AI avatar',
            'Voice cloned to sound exactly like them',
            'Trained on their personality & stories',
            'Remembers all conversations',
            'Available 24/7 via web/app',
            'Video calls with animated avatar',
            'New memorial videos monthly',
            'Direct feedback channel to development team',
            'Free upgrades as features graduate from beta',
            'Priority support',
            'Family plan (up to 5 people)',
            'Shape the future of digital companionship'
        ],
        'cta': 'Join the Family',
        'stripe_price_id': 'price_eternal',
        'is_subscription': True
    }
}


@app.route('/')
def index():
    """Landing page with pricing tiers"""
    return render_template('index.html', tiers=PRICING_TIERS)


@app.route('/guide')
def guide():
    """Arthur AI Guide page"""
    return render_template('guide.html')


@app.route('/create/<tier>')
def create(tier):
    """Create memorial page for selected tier"""
    if tier not in PRICING_TIERS:
        return redirect(url_for('index'))

    return render_template('create.html', tier=tier, tier_info=PRICING_TIERS[tier])


@app.route('/api/upload', methods=['POST'])
def upload():
    """Handle photo/video uploads"""
    # TODO: Implement file upload handling
    return jsonify({'status': 'success', 'message': 'Upload endpoint ready'})


@app.route('/api/create-memorial', methods=['POST'])
def create_memorial():
    """Create memorial video"""
    # TODO: Implement memorial creation with StillHere core
    return jsonify({'status': 'success', 'message': 'Memorial creation endpoint ready'})


@app.route('/api/checkout/<tier>', methods=['POST'])
def checkout(tier):
    """Handle Stripe checkout"""
    if tier not in PRICING_TIERS:
        return jsonify({'error': 'Invalid tier'}), 400

    # TODO: Implement Stripe checkout
    return jsonify({
        'status': 'success',
        'message': 'Stripe integration coming soon',
        'tier': tier,
        'price': PRICING_TIERS[tier]['price']
    })


@app.route('/dashboard')
def dashboard():
    """User dashboard to manage memorials"""
    return render_template('dashboard.html')


@app.route('/about')
def about():
    """About StillHere and The Christman AI Project"""
    return render_template('about.html')


@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'imstillhere.world'})


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)


# ============================================================================
# ARTHUR INTELLIGENCE - Vortex Level AI
# ============================================================================

import sys
sys.path.insert(0, str(Path(__file__).parent))

from arthur_intelligence import AdaptiveArthur
import uuid

# Store active Arthur sessions
ARTHUR_SESSIONS = {}


@app.route('/api/arthur/start', methods=['POST'])
def arthur_start_session():
    """Start a new Arthur conversation session."""
    session_id = str(uuid.uuid4())
    arthur = AdaptiveArthur(session_id)
    ARTHUR_SESSIONS[session_id] = arthur
    
    # Arthur's opening message
    opening = {
        'arthur_response': """Hello, I'm Arthur.

I know you're here because you've lost someone precious. I want you to know - I'm here to help, and we're going to take this journey together, one step at a time.

What brings you here today?""",
        'session_id': session_id,
        'personality_detected': None,
        'confidence': 0.0
    }
    
    return jsonify(opening)


@app.route('/api/arthur/chat', methods=['POST'])
def arthur_chat():
    """
    Chat with Arthur - intelligent, adaptive responses.
    
    Body: {
        'session_id': str,
        'message': str,
        'response_time': float (optional)
    }
    """
    data = request.json
    session_id = data.get('session_id')
    message = data.get('message')
    response_time = data.get('response_time')
    
    if not session_id or session_id not in ARTHUR_SESSIONS:
        return jsonify({'error': 'Invalid session'}), 400
    
    if not message:
        return jsonify({'error': 'No message provided'}), 400
    
    # Get Arthur instance
    arthur = ARTHUR_SESSIONS[session_id]
    
    # Process message with full intelligence
    response = arthur.process_user_message(message, response_time)
    
    # Add session_id to response
    response['session_id'] = session_id
    
    return jsonify(response)


@app.route('/api/arthur/predict', methods=['POST'])
def arthur_track_prediction():
    """
    Track when Arthur's prediction manifests.
    
    Body: {
        'session_id': str,
        'prediction': str,
        'proof': str
    }
    """
    data = request.json
    session_id = data.get('session_id')
    prediction = data.get('prediction')
    proof = data.get('proof', '')
    
    if session_id and session_id in ARTHUR_SESSIONS:
        arthur = ARTHUR_SESSIONS[session_id]
        latency = arthur.vortex.mark_manifested(prediction, proof)
        
        return jsonify({
            'manifested': True,
            'latency_seconds': latency,
            'accuracy': arthur.vortex.get_accuracy()
        })
    
    return jsonify({'error': 'Invalid session'}), 400


@app.route('/api/arthur/analytics', methods=['GET'])
def arthur_analytics():
    """Get Arthur's overall performance analytics."""
    session_id = request.args.get('session_id')
    
    if session_id and session_id in ARTHUR_SESSIONS:
        arthur = ARTHUR_SESSIONS[session_id]
        
        return jsonify({
            'personality_detected': arthur.detector.personality_type,
            'confidence': arthur.detector.confidence,
            'conversation_turns': len(arthur.conversation_history),
            'vortex_accuracy': arthur.vortex.get_accuracy(),
            'communication_style': arthur.detector.get_communication_style()
        })
    
    return jsonify({'error': 'Invalid session'}), 400



# ============================================================================
# ARTHUR SPEAKING - Voice + Lip Sync
# ============================================================================

@app.route('/api/arthur/speak', methods=['POST'])
def arthur_speak():
    """
    Generate video of Arthur speaking the response.
    
    Body: {
        'text': str,
        'session_id': str
    }
    """
    data = request.json
    text = data.get('text')
    session_id = data.get('session_id', 'default')
    
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    
    try:
        # For now, return audio-only (faster to implement)
        # TODO: Generate full lip-synced video
        from gtts import gTTS
        import uuid
        
        # Generate audio
        audio_id = str(uuid.uuid4())
        audio_path = Path('static/audio') / f'{audio_id}.mp3'
        audio_path.parent.mkdir(exist_ok=True)
        
        tts = gTTS(text=text, lang='en', slow=False)
        tts.save(str(audio_path))
        
        return jsonify({
            'audio_url': f'/static/audio/{audio_id}.mp3',
            'text': text
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500



# ============================================================================
# ARTHUR GLOBAL INTELLIGENCE - Fleet Management
# ============================================================================

from arthur_global_intelligence import get_global_hub, get_meta_arthur

# Start Meta-Arthur on app startup
meta_arthur = get_meta_arthur()


@app.route('/api/arthur/select-tier', methods=['POST'])
def arthur_select_tier():
    """
    Track when user selects a tier (for learning).
    
    Body: {
        'session_id': str,
        'tier': str
    }
    """
    data = request.json
    session_id = data.get('session_id')
    tier = data.get('tier')
    
    if session_id and session_id in ARTHUR_SESSIONS:
        arthur = ARTHUR_SESSIONS[session_id]
        arthur.mark_tier_selected(tier)
        
        # Prediction manifested if Arthur predicted this
        arthur.vortex.mark_manifested(
            f"Will choose {tier} package",
            proof=f"User selected {tier}"
        )
        
        return jsonify({
            'success': True,
            'tier': tier,
            'learnings_uploaded': True
        })
    
    return jsonify({'error': 'Invalid session'}), 400


@app.route('/api/arthur/friday-powwow', methods=['GET'])
def arthur_friday_powwow():
    """Get the Friday powwow report - Arthur's weekly review."""
    hub = get_global_hub()
    report = hub.generate_friday_powwow()
    
    return jsonify(report)


@app.route('/api/arthur/fleet-stats', methods=['GET'])
def arthur_fleet_stats():
    """Get real-time fleet statistics across all Arthur instances."""
    hub = get_global_hub()
    
    stats = {
        'total_conversations': hub.weekly_stats['total_conversations'],
        'personalities_detected': dict(hub.weekly_stats['personalities_detected']),
        'conversions': dict(hub.weekly_stats['conversions']),
        'prediction_accuracy': {
            'made': hub.weekly_stats['predictions_made'],
            'manifested': hub.weekly_stats['predictions_manifested'],
            'rate': (hub.weekly_stats['predictions_manifested'] / max(hub.weekly_stats['predictions_made'], 1)) * 100
        },
        'top_concerns': dict(hub.weekly_stats['top_concerns'])
    }
    
    return jsonify(stats)

