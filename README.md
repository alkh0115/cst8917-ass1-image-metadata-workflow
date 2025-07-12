# Durable Workflow for Image Metadata Processing

## Overview

This project implements a **serverless image metadata processing pipeline** using **Azure Durable Functions in Python**. When a new image is uploaded to Azure Blob Storage, the workflow extracts metadata and stores it in an Azure SQL Database.

This solution simulates a real-world event-driven architecture for content moderation or digital asset management.

---

## Architecture

```mermaid
flowchart TD
    A[Blob Upload: images-input container] --> B[Blob Trigger Function: starter_function]
    B --> C[Durable Orchestrator Function]
    C --> D[Activity Function: extract_metadata]
    C --> E[Activity Function: store_metadata with SQL Binding]
    E --> F[Azure SQL Database]

---

## Features

- **Blob Trigger**: Listens for new `.jpg`, `.png`, or `.gif` files in the container.
- **Durable Orchestration**: Coordinates function flow.
- **Metadata Extraction**: Gets file size, format, width, and height.
- **SQL Storage**: Stores extracted data using Azure SQL output binding.

---

## Project Structure

```bash
.
├── .vscode/ # VS Code configuration
├── .funcignore # Files to ignore when publishing to Azure
├── .gitignore # Git ignored files
├── README.md # Assignment documentation
├── function_app.py # Contains all functions: starter, orchestrator, and activity functions
├── host.json # Azure Functions host config
├── requirements.txt # Python dependencies (azure-functions, pillow, pyodbc, etc.)
```

---

## How to Test

1. Upload a `.jpg`, `.png`, or `.gif` to the **`images-input`** blob container.
2. The function app will automatically:
   - Trigger on upload
   - Extract metadata
   - Store results in Azure SQL
3. You can verify the inserted metadata by running:
   ```sql
   SELECT * FROM dbo.image_metadata ORDER BY created_at DESC;
   ```

---

## Technologies Used

- Azure Blob Storage (Trigger)
- Azure Durable Functions (Python)
- Azure SQL Database (Output Binding)
- Azure Function App (Deployed)
- VS Code & GitHub

---

## Deployment Details

- Resource Group: `rg-image-metadata`
- Function App: `imgmetadatafnalkh0115`
- Storage Account: `imgmetadatastorage`
- SQL Server: `sqlserverimgmetakh`
- SQL DB: `imgmetadata`
- Blob Container: `images-input`

---

## YouTube Demo


