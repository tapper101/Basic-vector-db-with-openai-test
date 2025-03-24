def chunk_excel_rows(excel_data):
    """
    Creates text chunks from Excel rows, excluding the header (first row).
    Each chunk is a textual representation of the row data.
    """
    header = excel_data[0]
    rows = excel_data[1:]

    chunks = []
    for row in rows:
        chunk_lines = [f"{header[i]}: {row[i]}" for i in range(len(header))]
        chunk_text = "\n".join(chunk_lines)
        chunks.append(chunk_text)
    
    return chunks

def extract_excel_metadata(excel_data):
    """
    Creates metadata by sampling up to the first 7 rows (excluding header) from each column.
    Useful for capturing the data context and structure.
    """
    header = excel_data[0]
    rows = excel_data[1:8]  # First 7 rows after header

    metadata = {}
    for col_idx, col_name in enumerate(header):
        sample_values = [str(row[col_idx]) for row in rows if row[col_idx] is not None]
        metadata[col_name] = sample_values

    return metadata