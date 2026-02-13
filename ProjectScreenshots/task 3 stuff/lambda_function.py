from azure.storage.blob import BlobServiceClient
import pandas as pd
import io, json, os

def process_nutritional_data_from_azurite():

    # Azurite connection string
    connect_str = (
        "DefaultEndpointsProtocol=http;"
        "AccountName=devstoreaccount1;"
        "AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;"
        "BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;"
    )
    # Connect to Azurite
    blob_service = BlobServiceClient.from_connection_string(
        connect_str,
        api_version="2025-11-05"
    )

    # Names of the container and file you uploaded
    container_name = "datasets"
    blob_name = "All_Diets.csv"

    # Access blob data
    container_client = blob_service.get_container_client(container_name)
    blob_client = container_client.get_blob_client(blob_name)

    # Download CSV
    file_bytes = blob_client.download_blob().readall()
    df = pd.read_csv(io.BytesIO(file_bytes))

    # Compute averages per diet type
    avg_macros = df.groupby("Diet_type")[["Protein(g)", "Carbs(g)", "Fat(g)"]].mean()

    # Save to JSON for NoSQL simulation
    os.makedirs("simulated_nosql", exist_ok=True)
    results = avg_macros.reset_index().to_dict(orient='records')

    with open("simulated_nosql/results.json", "w") as f:
        json.dump(results, f, indent=4)

    print("✔ Data processed successfully!")
    print("✔ Output saved in simulated_nosql/results.json")

if __name__ == "__main__":
    process_nutritional_data_from_azurite()