# code-nexus-data-pipeline
Polymorphic data processing pipeline in Python using abstract classes and dynamic routing, with a plugin-based export system (CSV/JSON).

## Brief 

A scalable and extensible data processing pipeline implemented in Python, designed to demonstrate advanced object-oriented programming concepts.

The system leverages abstract base classes and polymorphism to process heterogeneous data streams through a unified interface. It dynamically routes data to appropriate processors (numeric, text, and log-based), ensuring type-safe validation and flexible ingestion.

The architecture is extended with a plugin-based output pipeline using protocol-driven design, enabling easy integration of export formats such as CSV and JSON.

Key concepts demonstrated:

* Polymorphic data handling
* Abstract class design (ABC)
* Method overriding and type specialization
* Plugin architecture with duck typing
* Clean and modular system design


## data_processor.py 

This file implements a modular data processing system using object-oriented design and abstract base classes. It defines a common interface for handling different types of data while allowing each processor to apply its own validation and transformation logic.

The system supports processing:

Numeric data
Text data
Structured log data

All processors follow a unified workflow:
validate → ingest → store → output (FIFO)

![Data Processor Workflow](https://i.imgur.com/8X9Z5sM.png)
