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

