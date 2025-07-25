import azure.functions as func
import datetime
import logging
import json
import base64
from PIL import Image
from io import BytesIO
from azure.durable_functions import DurableOrchestrationClient, DurableOrchestrationContext

app = func.FunctionApp()

# Blob Trigger: This function is called when a new image is uploaded to the container
from azure.durable_functions import DurableOrchestrationClient

@app.function_name(name="starter_function")
@app.blob_trigger(arg_name="myblob", path="images-input/{name}", connection="AzureWebJobsStorage")
@app.durable_client_input("client")  # <-- ✅ must match function parameter name
async def starter_function(myblob: func.InputStream, client: DurableOrchestrationClient):
    logging.info(f"Triggered by blob: {myblob.name}")
    logging.info(f"Size: {myblob.length} bytes")

    instance_id = await client.start_new("orchestrator_function", None, myblob.name)
    logging.info(f"Started orchestration with ID = '{instance_id}'")


# Orchestrator Function: Coordinates activity functions
@app.orchestration_trigger(context_name="context")
def orchestrator_function(context: DurableOrchestrationContext):
    blob_name = context.get_input()

    # Step 1: Extract metadata
    metadata = yield context.call_activity("extract_metadata_activity", blob_name)

    # Step 2: Store metadata in SQL
    yield context.call_activity("store_metadata_activity", metadata)

    return "Orchestration completed"

# Activity Function: Extract image metadata from blob
# This function downloads the image blob from Azure Storage,
# uses Pillow to read its format, dimensions, and calculates file size,
# then returns a metadata dictionary to the orchestrator.
@app.activity_trigger(input_name="blob_name")
def extract_metadata_activity(blob_name: str):
    from azure.storage.blob import BlobServiceClient
    import os

    # Get the storage connection string
    connect_str = os.getenv("AzureWebJobsStorage")
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    container_client = blob_service_client.get_container_client("images-input")
    
    blob_name = os.path.basename(blob_name)  # safely extract the image
    blob_client = container_client.get_blob_client(blob_name)
    blob_data = blob_client.download_blob().readall()

    # Open image using Pillow
    image = Image.open(BytesIO(blob_data))
    width, height = image.size
    image_format = image.format

    # Calculate file size in KB
    file_size_kb = round(len(blob_data) / 1024, 2)

    # Build metadata dictionary
    metadata = {
        "file_name": blob_name,
        "file_size_kb": file_size_kb,
        "width": width,
        "height": height,
        "format": image_format
    }

    return metadata


# Activity Function: Store metadata into Azure SQL Database using output binding
@app.activity_trigger(input_name="metadata")
def store_metadata_activity(metadata: dict):
    import pyodbc
    import os

    logging.info(f"Inserting metadata into Azure SQL DB: {metadata}")

    # Get the connection string
    conn_str = os.getenv("SQLConnectionString")

    # Connect to Azure SQL
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    # Insert query
    insert_sql = """
        INSERT INTO dbo.image_metadata (file_name, file_size_kb, width, height, format)
        VALUES (?, ?, ?, ?, ?)
    """

    cursor.execute(
        insert_sql,
        metadata["file_name"],
        metadata["file_size_kb"],
        metadata["width"],
        metadata["height"],
        metadata["format"]
    )

    conn.commit()
    cursor.close()
    conn.close()

    return metadata

