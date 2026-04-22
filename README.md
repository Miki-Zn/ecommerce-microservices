# Event-Driven E-Commerce Microservices

![Microservices](https://img.shields.io/badge/Architecture-Microservices-orange)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688)
![RabbitMQ](https://img.shields.io/badge/RabbitMQ-Message_Broker-FF6600)

## 📖 Overview
A robust, highly scalable backend for an e-commerce platform built using an event-driven microservices architecture. This project demonstrates advanced system design patterns, distributed data management, and asynchronous inter-service communication.

## 🏗 Architecture
The system is divided into three completely independent microservices. Each service maintains its own PostgreSQL database to ensure loose coupling and high availability.

1. **Users Service:** Handles JWT authentication, user registration, and profile management.
2. **Inventory Service:** Manages product catalog and stock levels.
3. **Orders Service:** Processes customer orders and orchestrates the checkout flow.

### Event-Driven Communication (RabbitMQ)
To prevent tight coupling, services communicate asynchronously via **RabbitMQ**. 
*Example flow:* When an order is created in the `Orders Service`, an `order_created` event is published. The `Inventory Service` consumes this event and safely deducts the stock, implementing the **Saga Pattern** for distributed transactions.

## 🛠 Tech Stack
- **Framework:** Python 3.11, FastAPI
- **Databases:** PostgreSQL (Database-per-service pattern), SQLAlchemy ORM
- **Message Broker:** RabbitMQ
- **Infrastructure:** Docker, Docker Compose
- **Testing:** PyTest

## 🚀 Getting Started (Infrastructure)
Currently, the repository contains the infrastructure configuration.

```bash
# Start the RabbitMQ broker and the isolated PostgreSQL databases
docker-compose up -d