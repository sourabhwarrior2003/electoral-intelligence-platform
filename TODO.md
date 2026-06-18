# TODO: Update parser.py and process_service.py with OCR fixes

## Task Overview
Replace existing parser.py and process_service.py with updated versions that handle:
1. More robust voter ID detection (optional spaces)
2. Multi-record block splitting
3. Cleaning leftover Hindi field names from extracted values

## Steps to Complete:

### Step 1: Update backend/modules/parser.py
- [x] Read current parser.py
- [x] Update `_is_voter_id_line` to allow optional spaces
- [x] Update `extract_voter_records` to split blocks with multiple "निर्वाचक का नाम"
- [x] Update `_parse_voter_block` to clean leftover field names

### Step 2: Update backend/services/process_service.py
- [x] Read current process_service.py
- [x] Update `clean_voter_data` to remove Hindi field names

### Step 3: Test the changes
- [ ] Run the application to verify the parser works correctly

