\# 📊 Real-Time Analytics Dashboard



\[⬅️ Back to Portfolio](../)



A production-ready event streaming pipeline built with Apache Kafka that processes and visualizes clickstream data in real-time.



!\[Python](https://img.shields.io/badge/Python-3.8+-blue.svg)

!\[Kafka](https://img.shields.io/badge/Apache%20Kafka-7.5.0-black.svg)

!\[React](https://img.shields.io/badge/React-18+-61DAFB.svg)



\## 🎯 Overview



This project simulates a high-traffic e-commerce platform tracking user interactions (page views, clicks, purchases) and displays real-time insights through an interactive dashboard.



\### Features



\- ⚡ Real-time event streaming with Apache Kafka

\- 📈 Live dashboard updating every 5 seconds

\- 🔄 Microservices architecture

\- 💾 PostgreSQL database with optimized indexes

\- 🎨 Modern React UI with Recharts

\- 🐳 Fully containerized with Docker



\## 🏗️ Architecture

```

Producer → Kafka → Consumer → PostgreSQL → API → React Dashboard

```



\## 🚀 Quick Start



\### Prerequisites

\- Docker \& Docker Compose

\- Python 3.8+

\- Node.js 16+



\### Setup



1\. \*\*Start infrastructure\*\*

```bash

&nbsp;  docker-compose up -d

```

&nbsp;  Wait 60 seconds.



2\. \*\*Setup backend\*\*

```bash

&nbsp;  cd backend

&nbsp;  python -m venv venv

&nbsp;  venv\\Scripts\\activate

&nbsp;  pip install -r requirements.txt

&nbsp;  python -c "from database import init\_db; init\_db()"

```



3\. \*\*Run services (3 terminals)\*\*

```bash

&nbsp;  # Terminal 1

&nbsp;  python consumer.py

&nbsp;  

&nbsp;  # Terminal 2

&nbsp;  python producer.py

&nbsp;  

&nbsp;  # Terminal 3

&nbsp;  python api.py

```



4\. \*\*Start frontend\*\*

```bash

&nbsp;  cd frontend

&nbsp;  npm install

&nbsp;  npm run dev

```



5\. \*\*Open dashboard:\*\* http://localhost:5173



\## 🛠️ Tech Stack



\- \*\*Apache Kafka\*\* - Event streaming

\- \*\*Python \& FastAPI\*\* - Backend \& API

\- \*\*React \& Recharts\*\* - Frontend

\- \*\*PostgreSQL\*\* - Database

\- \*\*Docker\*\* - Containerization



\## 📊 What I Learned



\- Event-driven architecture patterns

\- Apache Kafka and stream processing

\- Microservices design

\- Real-time data pipelines

\- Docker containerization

\- Full-stack development



\## 📸 Screenshots



\*(Add screenshots here)\*



\## 🔮 Future Enhancements



\- Add Kafka Streams for aggregations

\- Implement user authentication

\- Deploy to AWS

\- Add monitoring with Grafana



\## 📝 Detailed Setup



See \[SETUP.md](./SETUP.md) for detailed instructions.



\## 📄 License



MIT License



---



Built with ❤️ as part of my software engineering portfolio

