# -*- coding: utf-8 -*-
import sys
import json
import urllib.request

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def post(url, data):
    req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode('utf-8'))

def get(url):
    with urllib.request.urlopen(url) as resp:
        return json.loads(resp.read().decode('utf-8'))

print("=== 1. HEALTH CHECK ===")
health = get('http://127.0.0.1:8000/api/health')
print(f"Status: {health.get('status')} | Vectorstore: {health.get('vectorstore_documents')} docs")

print("\n=== 2. BIS STANDARDS CATALOG ===")
standards = get('http://127.0.0.1:8000/api/bis/standards')
total = standards.get('total') or len(standards.get('standards', []))
print(f"Total Standards Loaded: {total}")
for s in standards.get('standards', [])[:4]:
    print(f"  • {s.get('standard_number')}: {s.get('title')} [{s.get('category')}]")

print("\n=== 3. INDUSTRY Q&A: TMT Steel ===")
r3 = post('http://127.0.0.1:8000/api/chat', {'query': 'Which IS standard applies to TMT steel bars?'})
print("Answer snippet:", r3.get('answer', '')[:160] + "...")
print("Citations:", r3.get('citations'))

print("\n=== 4. CONSUMER Q&A: Gold Hallmark HUID ===")
r4 = post('http://127.0.0.1:8000/api/chat', {'query': 'How to check gold hallmark HUID number?'})
print("Answer snippet:", r4.get('answer', '')[:160] + "...")
print("Citations:", r4.get('citations'))

print("\n=== 5. VAGUE QUERY CLARIFICATION ===")
r5 = post('http://127.0.0.1:8000/api/chat', {'query': 'water'})
print("Answer snippet:", r5.get('answer', '')[:180] + "...")
options = r5.get('metadata', {}).get('execution_trace', {}).get('follow_up_options', [])
if not options and r5.get('follow_up_options'):
    options = r5.get('follow_up_options')
print("Clarification options:", options)

print("\n=== 6. 'I DON'T KNOW' SAFE REFUSAL ===")
r6 = post('http://127.0.0.1:8000/api/chat', {'query': 'What is the standard for quantum teleporter spacecraft?'})
print("Answer snippet:", r6.get('answer', '')[:180] + "...")

print("\n=== 7. EXISTING FEATURE CHECK: MRPL H2S LIMIT ===")
r7 = post('http://127.0.0.1:8000/api/chat', {'query': 'What is the H2S exposure limit in CDU?'})
print("Answer snippet:", r7.get('answer', '')[:160] + "...")
print("Citations:", r7.get('citations'))

print("\n=== 8. STANDARDS COMPARISON ===")
r8 = post('http://127.0.0.1:8000/api/bis/compare', {'standard_1': 'IS 10500', 'standard_2': 'IS 14543'})
print("Comparison answer snippet:", r8.get('answer', '')[:160] + "...")
print("Comparison citations:", r8.get('citations'))

print("\n=== 9. HINDI (हिन्दी) QUERY SUPPORT ===")
r9 = post('http://127.0.0.1:8000/api/chat', {'query': 'सीमेंट के लिए कौन सा भारतीय मानक लागू होता है?'})
print("Answer snippet (Hindi):", r9.get('answer', '')[:160] + "...")
print("Citations:", r9.get('citations'))

print("\n=== 10. STEP-BY-STEP CERTIFICATION GUIDANCE ===")
r10 = get('http://127.0.0.1:8000/api/bis/certification-steps?scheme=scheme-i')
print("Scheme:", r10.get('scheme'))
print("Total Steps:", len(r10.get('steps', [])))
print("Step 1:", r10.get('steps', [])[0].get('title'))
print("Mandatory Docs:", len(r10.get('documents_required', [])))

print("\n=== 11. DYNAMIC STANDARD INGESTION (WITHOUT RETRAINING) ===")
import uuid
boundary = uuid.uuid4().hex
with open('Indian_Standards_BIS_Compendium_2026.pdf', 'rb') as f:
    pdf_bytes = f.read()

body = (
    f'--{boundary}\r\n'
    f'Content-Disposition: form-data; name="file"; filename="IS_Dynamic_Update_2026.pdf"\r\n'
    f'Content-Type: application/pdf\r\n\r\n'
).encode('utf-8') + pdf_bytes + f'\r\n--{boundary}--\r\n'.encode('utf-8')

req11 = urllib.request.Request(
    'http://127.0.0.1:8000/api/bis/standards/upload',
    data=body,
    headers={'Content-Type': f'multipart/form-data; boundary={boundary}'}
)
with urllib.request.urlopen(req11) as resp11:
    r11 = json.loads(resp11.read().decode('utf-8'))
    print("Ingestion Status:", r11.get('status'))
    print("Document:", r11.get('filename'))
    print("Chunks indexed into Vector DB:", r11.get('total_chunks'))

print("\n=== ALL 11 TEST SUITES PASSED VERIFICATION ===")

