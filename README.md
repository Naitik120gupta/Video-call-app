# Video Conferencing Application 🎥

A robust real-time video conferencing platform built with **Django**, **Django Channels** (WebSockets), and the **Agora SDK**. This application facilitates stable audio/video communication and persistent real-time chat with low latency.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Django](https://img.shields.io/badge/Django-4.x-green)
![Agora](https://img.shields.io/badge/Agora-SDK-orange)
![WebSockets](https://img.shields.io/badge/WebSockets-Django%20Channels-red)

## 📖 Overview

This project integrates **WebRTC** via the Agora SDK for high-quality video streaming and utilizes **Django Channels** to handle WebSocket connections for a seamless chat experience. It is designed to handle concurrent users efficiently with a focus on minimal latency and secure session management.

## ✨ Key Features

* **Real-Time Video/Audio**: Leverages Agora SDK to ensure stable communication with adaptive bitrate streaming.
* **Persistent Chat**: WebSocket-based chat system implemented using Django Channels.
    * *Performance*: Tested with **~20–30 concurrent users** per room.
    * *Speed*: Average message delivery latency reduced to **<200ms** via persistent connections.
* **Secure Rooms**: Token-based authentication and secure session handling to prevent unauthorized access to meeting rooms.
* **Low Latency**: Optimized architecture ensures synchronization between video streams and chat messages.

## 🛠️ Tech Stack

* **Backend Framework**: Django
* **Real-time Protocol**: Django Channels (Asynchronous Server Gateway Interface - ASGI)
* **Video/Audio Engine**: Agora RTC SDK (WebRTC)
* **Database**: SQLite (Development) / PostgreSQL (Production recommended)
* **Message Broker**: Redis (for Channel Layers)
* **Frontend**: HTML5, CSS3, JavaScript

## ⚙️ Prerequisites

Before running the project, ensure you have the following installed:

* [Python 3.8+](https://www.python.org/)
* [Redis](https://redis.io/) (Required for Django Channels)
* An [Agora.io](https://www.agora.io/) Developer Account (for App ID)

## 🚀 Installation & Setup

1.  **Clone the Repository**
    ```bash
    git clone [https://github.com/yourusername/your-repo-name.git](https://github.com/yourusername/your-repo-name.git)
    cd your-repo-name
    ```

2.  **Create and Activate Virtual Environment**
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # Mac/Linux
    source venv/bin/activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment Variables**
    Create a `.env` file in the root directory and add your Agora credentials:
    ```env
    SECRET_KEY=your_django_secret_key
    DEBUG=True
    AGORA_APP_ID=your_agora_app_id
    AGORA_APP_CERTIFICATE=your_agora_certificate
    ```

5.  **Start Redis Server**
    Ensure Redis is running on port 6379.
    ```bash
    redis-server
    ```

6.  **Run Migrations**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

7.  **Start the Application**
    Since we are using Django Channels, you might need to run via `daphne` or the standard command if `asgi.py` is configured correctly.
    ```bash
    python manage.py runserver
    ```

## 📸 Architecture

1.  **User Joins Room**: The Django backend validates the session ID.
2.  **Video Stream**: The frontend initializes the Agora Client, connecting directly to Agora's SD-RTN (Software Defined Real-time Network).
3.  **Chat Stream**: The frontend opens a WebSocket connection (`ws://`) to the Django Channels consumer.
4.  **Broadcasting**: Redis acts as the channel layer, distributing chat messages to all connected clients in the room instantly.

## 🤝 Contributing

Contributions are welcome!
1.  Fork the project.
2.  Create your feature branch (`git checkout -b feature/AmazingFeature`).
3.  Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4.  Push to the branch (`git push origin feature/AmazingFeature`).
5.  Open a Pull Request.
