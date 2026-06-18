# backend/modules/parser.py
import re

def extract_metadata(text):
    """
    Extract constituency name and polling booth name from the first page.
    Returns (constituency, booth).
    """
    constituency = None
    booth = None

    # Constituency pattern
    const_match = re.search(
        r'विधान\s*सभा\s*क्षेत्र\s*की\s*संख्या,\s*नाम\s*व\s*आरक्षण\s*स्थिति\s*[:\-]?\s*\d+\s*-\s*([^\n\(]+)',
        text
    )
    if const_match:
        constituency = const_match.group(1).strip()

    # Booth pattern
    booth_match = re.search(
        r'मतदान\s*केंद्र\s*की\s*संख्या\s*व\s*नाम\s*[:\-]?\s*\d+\s*-\s*([^\n]+)',
        text
    )
    if booth_match:
        booth = booth_match.group(1).strip()

    return constituency, booth


def _is_voter_id_line(line):
    """
    Return True if the line looks like a voter ID.
    Now more permissive: allows optional spaces, matches at start of line.
    """
    line = line.strip()
    # Pattern: 3-4 uppercase letters followed by 6-8 digits, possibly with leading/trailing spaces
    return bool(re.match(r'^[A-Z]{3,4}\s*\d{6,8}$', line))


def extract_voter_records(text, default_constituency=None, default_booth=None):
    """
    Extract all voter records from the full OCR text.
    Uses voter ID lines as record separators; falls back to "निर्वाचक का नाम".
    Now also splits blocks that contain multiple "निर्वाचक का नाम".
    """
    lines = text.split('\n')
    records = []
    i = 0
    n = len(lines)
    found_any_id = False

    # First pass: try to detect voter IDs
    for line in lines:
        if _is_voter_id_line(line):
            found_any_id = True
            break

    while i < n:
        line = lines[i].strip()
        start = False
        block_lines = []

        if found_any_id:
            if _is_voter_id_line(line):
                start = True
                i += 1  # skip the ID line
                # Collect all lines until the next ID or EOF
                while i < n and not _is_voter_id_line(lines[i]):
                    if lines[i].strip():
                        block_lines.append(lines[i].strip())
                    i += 1
        else:
            # Fallback: use "निर्वाचक का नाम"
            if "निर्वाचक का नाम" in line:
                start = True
                block_lines = [line]
                i += 1
                while i < n and "निर्वाचक का नाम" not in lines[i]:
                    if lines[i].strip():
                        block_lines.append(lines[i].strip())
                    i += 1

        if start and block_lines:
            block = " ".join(block_lines)
            # If the block contains multiple "निर्वाचक का नाम", split it
            if block.count("निर्वाचक का नाम") > 1:
                sub_blocks = re.split(r'(?=निर्वाचक का नाम)', block)
                for sub in sub_blocks:
                    if sub.strip():
                        record = _parse_voter_block(sub)
                        if record.get('name'):
                            record['constituency'] = default_constituency or "Unknown"
                            record['booth'] = default_booth or "Unknown"
                            records.append(record)
            else:
                record = _parse_voter_block(block)
                if record.get('name'):
                    record['constituency'] = default_constituency or "Unknown"
                    record['booth'] = default_booth or "Unknown"
                    records.append(record)
        else:
            i += 1

    return records


def _parse_voter_block(block):
    """
    Extract individual fields from a voter block.
    Now also cleans the captured values by removing any remaining field names.
    """
    record = {}

    # Name
    name_match = re.search(
        r'निर्वाचक\s*का\s*नाम\s*[:\-]?\s*([^प]+?)(?=\s+(?:पिता\s*का\s*नाम|पति\s*का\s*नाम|माता\s*का\s*नाम|गृह\s*संख्या|उम्र|आयु|लिंग|$))',
        block,
        re.UNICODE
    )
    if name_match:
        raw_name = name_match.group(1).strip()
        # Remove any leftover "निर्वाचक का नाम" or other field names that might have been captured
        raw_name = re.sub(r'निर्वाचक\s*का\s*नाम.*$', '', raw_name, flags=re.UNICODE).strip()
        record['name'] = raw_name

    # Father/Husband
    father_match = re.search(
        r'(?:पिता\s*का\s*नाम|पति\s*का\s*नाम)\s*[:\-]?\s*([^ग]+?)(?=\s+(?:गृह\s*संख्या|माता\s*का\s*नाम|उम्र|आयु|लिंग|$))',
        block,
        re.UNICODE
    )
    if father_match:
        raw_father = father_match.group(1).strip()
        # Remove any field names that might have been captured
        raw_father = re.sub(r'(?:पिता\s*का\s*नाम|पति\s*का\s*नाम).*$', '', raw_father, flags=re.UNICODE).strip()
        record['father_name'] = raw_father

    # Age
    age_match = re.search(r'(?:उम्र|आयु)\s*[:\-]?\s*(\d+)', block, re.UNICODE)
    if age_match:
        record['age'] = int(age_match.group(1))

    # Gender
    gender_match = re.search(r'लिंग\s*[:\-]?\s*(पुरुष|महिला|स्त्री)', block, re.UNICODE)
    if gender_match:
        raw = gender_match.group(1)
        if 'पुरुष' in raw:
            record['gender'] = 'पुरुष'
        elif 'महिला' in raw or 'स्त्री' in raw:
            record['gender'] = 'महिला'
        else:
            record['gender'] = raw

    return record

