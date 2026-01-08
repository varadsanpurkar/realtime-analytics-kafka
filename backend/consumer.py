from kafka import KafkaConsumer
import json
from datetime import datetime
from database import SessionLocal, ClickEvent, init_db

# Initialize database
init_db()

# Kafka Consumer
consumer = KafkaConsumer(
    'clickstream-events',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='clickstream-consumer-group',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

def process_event(event_data):
    """Process and save event to database"""
    db = SessionLocal()
    try:
        # Parse timestamp
        timestamp = datetime.fromisoformat(event_data['timestamp'])
        
        # Create database record
        click_event = ClickEvent(
            user_id=event_data['user_id'],
            event_type=event_data['event_type'],
            page_url=event_data['page_url'],
            timestamp=timestamp,
            session_id=event_data['session_id'],
            country=event_data['country'],
            device=event_data['device'],
            revenue=event_data.get('revenue')
        )
        
        db.add(click_event)
        db.commit()
        
        return True
    except Exception as e:
        print(f"❌ Error processing event: {e}")
        db.rollback()
        return False
    finally:
        db.close()

def consume_events():
    """Consume events from Kafka and process them"""
    print("🎧 Starting event consumer...")
    print(f"📊 Listening for events on topic: clickstream-events")
    
    count = 0
    try:
        for message in consumer:
            event_data = message.value
            
            # Process the event
            if process_event(event_data):
                count += 1
                print(f"✅ Processed event #{count}: {event_data['event_type']} - {event_data['user_id']}")
            
    except KeyboardInterrupt:
        print("\n⏹️  Stopping consumer...")
    finally:
        consumer.close()
        print(f"📦 Processed {count} events total")

if __name__ == "__main__":
    consume_events()