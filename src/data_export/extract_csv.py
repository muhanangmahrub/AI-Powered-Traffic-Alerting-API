import pandas as pd
from src.config.settings import TRAFFIC_DATA_FILE
from src.data_ingestion.firestore_utils import get_all_documents

# Name of the collection to export
collection_name = "traffic_data"

def extract_csv():
    # Fetch all documents
    docs = get_all_documents(collection_name)
    data_list = []
    for doc in docs:
        doc_dict = doc.to_dict()
        doc_dict["id"] = doc.id
        data_list.append(doc_dict)

    # Convert to DataFrame
    df = pd.DataFrame(data_list)

    # Save to CSV
    df.to_csv(f"{TRAFFIC_DATA_FILE}{collection_name}.csv", index=False)
    print(f"✅ Exported {len(df)} documents to {collection_name}.csv")
