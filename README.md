# Durable Workflow for Image Metadata Processing

## Overview

This project implements a **serverless image metadata processing pipeline** using **Azure Durable Functions in Python**. When a new image is uploaded to Azure Blob Storage, the workflow extracts metadata and stores it in an Azure SQL Database.

This solution simulates a real-world event-driven architecture for content moderation or digital asset management.

---

## Features

- **Blob Trigger**: Listens for new `.jpg`, `.png`, or `.gif` files in the container.
- **Durable Orchestration**: Coordinates function flow.
- **Metadata Extraction**: Gets file size, format, width, and height.
- **SQL Storage**: Stores extracted data using Azure SQL output binding.

---

## Architecture Overview

```
[1] User uploads image to Blob Storage container: images-input
 ↓
[2] Blob Trigger Function (starter_function)
 ↓
[3] Durable Orchestrator Function
   ├──> [Activity 1] extract_metadata
   └──> [Activity 2] store_metadata (via Azure SQL Output Binding)
 ↓
[4] Azure SQL Database
```

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

## How It Works (Deployment Summary)

1. **Local Setup:**
   - Built using Python 3.10 and Azure Functions Core Tools.
   - Functions implemented: `starter_function`, `orchestrator_function`, `extract_metadata`, `store_metadata`.

2. **Deployment to Azure:**
   - Deployed via Azure CLI using `func azure functionapp publish <app-name>`.
   - Bound to Blob Storage container named `images-input`.
   - Connected to Azure SQL Database using output binding.

3. **Test Flow:**
   - Uploaded test image: `test-upload-1.jpg` to container.
   - Verified function execution using Azure Log Stream and Application Insights.
   - Confirmed metadata inserted into Azure SQL Database with query:
     ```sql
     SELECT * FROM dbo.image_metadata ORDER BY created_at DESC;
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
**Demo Video:** [Watch on YouTube](https://youtu.be/-VwC4XMAPOM)


