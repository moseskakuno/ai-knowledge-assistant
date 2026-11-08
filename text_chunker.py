
def split_text_into_chunks(
    extracted_pages,
    chunk_size=800,
    overlap=150
):
    """
    Split extracted PDF text into smaller chunks.
    Preserve the original page numbers.
    """

    chunks = []

    for page_data in extracted_pages:

        text = page_data["text"]
        page_number = page_data["page"]

        start = 0
        chunk_index = 0

        while start < len(text):

            end = min(start + chunk_size, len(text))

            # Try to end at a word boundary
            if end < len(text):
                last_space = text.rfind(" ", start, end)

                if last_space > start:
                    end = last_space

            chunk_text = text[start:end].strip()

            if chunk_text:
                chunks.append({
                    "chunk_index": chunk_index,
                    "page": page_number,
                    "text": chunk_text
                })

                chunk_index += 1

            if end >= len(text):
                break

            start = max(start + 1, end - overlap)

    return chunks
