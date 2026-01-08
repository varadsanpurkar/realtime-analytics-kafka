from kafka import KafkaProducer
from faker import Faker
import json
import time
import random
from datetime import datetime

fake = Faker()

# Kafka Producer
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

TOPIC_NAME = 'clickstream-events'

# Sample data
PAGES = ['/home', '/products', '/about', '/contact', '/checkout', '/cart', '/profile']
EVENT_TYPES = ['page_view', 'click', 'purchase']
COUNTRIES = ['US', 'UK', 'CA', 'DE', 'FR', 'IN', 'AU']
DEVICES = ['mobile', 'desktop', 'tablet']

def generate_event():
    """Generate a random clickstream event"""
    event_type = random.choices(
        EVENT_TYPES, 
        weights=[70, 25, 5]  # More page views, fewer purchases
    )[0]
    
    event = {
        'user_id': f'user_{random.randint(1, 1000)}',
        'event_type': event_type,
        'page_url': random.choice(PAGES),
        'timestamp': datetime.utcnow().isoformat(),
        'session_id': f'session_{random.randint(1, 500)}',
        'country': random.choice(COUNTRIES),
        'device': random.choice(DEVICES),
        'revenue': round(random.uniform(10, 500), 2) if event_type == 'purchase' else None
    }
    
    return event

def produce_events(num_events=None, delay=0.5):
    """
    Produce events to Kafka
    num_events: Number of events to produce (None = infinite)
    delay: Delay between events in seconds
    """
    count = 0
    print(f"🚀 Starting event producer... Sending to topic: {TOPIC_NAME}")
    
    try:
        while True:
            event = generate_event()
            
            # Send to Kafka
            producer.send(TOPIC_NAME, value=event)
            
            count += 1
            print(f"📤 Sent event #{count}: {event['event_type']} - {event['page_url']} - User: {event['user_id']}")
            
            if num_events and count >= num_events:
                break
                
            time.sleep(delay)
            
    except KeyboardInterrupt:
        print("\n⏹️  Stopping producer...")
    finally:
        producer.flush()
        producer.close()
        print(f"✅ Produced {count} events")

if __name__ == "__main__":
    # Produce events continuously with 0.5 second delay
    produce_events(delay=0.5)