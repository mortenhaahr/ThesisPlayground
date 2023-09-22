

def get_csv_keys(markdown_file): 
    NAME_HEADER = "Header name"
    UNIT_HEADER = "Unit"
    DESCRIPTION_HEADER = "Description"
    KEEP_HEADER = "Keep (y/n)"

    EXPECTED_TABLE_HEADERS = [
        NAME_HEADER,
        UNIT_HEADER,
        DESCRIPTION_HEADER,
        KEEP_HEADER
    ]       
    
    with open(markdown_file, "r") as desc:
        text = desc.read()

    table = text[text.find('|'):text.rfind('|')]
    rows = [row.split('|')[1:5] for row in table.split('\n')]
    rows = [[value.strip() for value in row] for row in rows  ]

    headers = rows[0]
    for header in headers:
        if header not in EXPECTED_TABLE_HEADERS:
            raise ValueError(f"Unexpected header: \"{header}\"!")

    values_by_row = [
        {
            headers[i] : row[i] for i in range(len(headers))
        } for row in rows[2:]
    ]

    st = KEEP_HEADER.rfind('(') + 1
    delim = KEEP_HEADER.rfind('/')
    end = KEEP_HEADER.rfind(')')
    KEYS_FOR_KEEP = [KEEP_HEADER[st:delim], KEEP_HEADER[delim + 1:end]]  

    for row in values_by_row:
        if row[KEEP_HEADER] not in KEYS_FOR_KEEP:
            raise ValueError(f"Row ({row}) missing or wrong keep key!")

    kept_rows = [row for row in values_by_row if row[KEEP_HEADER] == KEYS_FOR_KEEP[0]]
    kept_csv_keys = [row[NAME_HEADER] for row in kept_rows]


    return kept_csv_keys


if __name__ == "__main__":
    kept_keys = get_csv_keys("header_description.md")
    print(kept_keys)