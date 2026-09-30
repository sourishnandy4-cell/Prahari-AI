import os
import shutil
import uuid
from typing import Dict, Any, List, Optional
from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Query
from pydantic import BaseModel

from backend.app.config import settings
from backend.app.services.bis_service import bis_service, STANDARDS_CATALOG, SCHEME_I_STEPS, SCHEME_II_STEPS
from backend.app.services.ingest_service import ingest_pdf_manual
from backend.app.services.document_manager import register_document
from backend.app.services.hybrid_search import invalidate_bm25_cache

bis_router = APIRouter(prefix="/bis", tags=["Bureau of Indian Standards (BIS)"])


class CompareRequest(BaseModel):
    standard_a: Optional[str] = None
    standard_b: Optional[str] = None
    standard_1: Optional[str] = None
    standard_2: Optional[str] = None
    language: Optional[str] = "en"


class HUIDVerifyRequest(BaseModel):
    huid: str


class CMLVerifyRequest(BaseModel):
    cml: str


@bis_router.get("/standards")
async def list_standards(category: Optional[str] = None):
    """Returns all indexed Indian Standards (IS Codes) and their metadata."""
    results = []
    for k, v in STANDARDS_CATALOG.items():
        if category and category.lower() not in v.get("category", "").lower():
            continue
        results.append({
            "code": k,
            "standard_number": v.get("standard_number"),
            "title": v.get("title"),
            "category": v.get("category"),
            "scope": v.get("scope"),
            "mandatory_qco": v.get("mandatory_qco"),
            "certification_scheme": v.get("certification_scheme"),
            "key_clauses_count": len(v.get("key_clauses", {})),
            "mandatory_tests": v.get("mandatory_tests", [])
        })
    return {"total": len(results), "standards": results}


@bis_router.get("/categories")
async def list_categories():
    """Returns all industry and consumer product categories available."""
    categories = sorted(list(set(v.get("category") for v in STANDARDS_CATALOG.values())))
    return {
        "categories": categories,
        "entry_points": {
            "industry": [
                "Steel & Construction Infrastructure",
                "Electrical Accessories",
                "Electrical Cables & Wires",
                "Building Materials",
                "Electronics & IT Goods",
                "Electronics & Energy Storage",
                "Lighting & Electronics"
            ],
            "consumer": [
                "Food & Public Health",
                "Packaged Food & Beverages",
                "Gold Hallmarking",
                "Silver Hallmarking",
                "Automotive & Personal Protection",
                "Consumer Kitchen Appliances",
                "Consumer & Child Safety",
                "Consumer Electrical Appliances"
            ]
        }
    }


@bis_router.post("/compare")
async def compare_standards(req: CompareRequest):
    """Compares two Indian Standards side-by-side with clauses and differences."""
    std_a = req.standard_a or req.standard_1 or "IS 10500"
    std_b = req.standard_b or req.standard_2 or "IS 14543"
    query = f"compare {std_a} and {std_b}"
    is_hi = req.language == "hi"
    res = bis_service._check_standards_comparison(query, is_hi=is_hi)
    if not res:
        # Fallback generic comparison
        res = bis_service._generate_generic_comparison(std_a, std_b, is_hi=is_hi)
    return res


@bis_router.post("/verify-huid")
async def verify_huid(req: HUIDVerifyRequest):
    """
    Validates the structure of a 6-digit alphanumeric Hallmark Unique Identification (HUID)
    and explains the official verification process via BIS Care App.
    """
    code = req.huid.strip().upper()
    is_valid_format = len(code) == 6 and code.isalnum()

    if not is_valid_format:
        return {
            "valid_format": False,
            "huid": code,
            "message": "Invalid HUID format. A genuine BIS HUID must be exactly 6 alphanumeric characters (e.g. AX49Z2).",
            "guide": "Please check the laser engraving on your gold jewellery using a 10x magnifying loupe."
        }

    return {
        "valid_format": True,
        "huid": code,
        "message": f"HUID '{code}' follows the authentic BIS 6-digit alphanumeric standard.",
        "verification_steps": [
            "1. Open the official 'BIS Care App' (or visit www.manakonline.in).",
            "2. Select the 'Verify HUID' service tile.",
            f"3. Enter '{code}' to pull the official assay record from the central Hallmarking database.",
            "4. Verify that the displayed Jeweller Name, Hallmarking Center (AHC), Date, and Karat Purity (e.g., 22K916) match your purchase bill."
        ],
        "compensation_right": "Under BIS Act 2016, if purity tested at a BIS lab is lower than declared, you are entitled to the purity difference plus 2x the testing fee."
    }


@bis_router.post("/verify-cml")
async def verify_cml(req: CMLVerifyRequest):
    """
    Validates the structure of a 7 or 8 digit CM/L (Certificate of Manufacture License) number
    and explains verification on the BIS portal / BIS Care App.
    """
    digits = "".join(filter(str.isdigit, req.cml))
    is_valid_length = len(digits) in (7, 8)

    if not is_valid_length:
        return {
            "valid_format": False,
            "cml": req.cml,
            "message": "Invalid CM/L format. A genuine BIS License Number consists of 7 or 8 digits (e.g., CM/L-1234567 or 1234567).",
            "guide": "Look directly beneath the rectangular ISI monogram on the product packaging."
        }

    return {
        "valid_format": True,
        "cml": digits,
        "formatted": f"CM/L-{digits}",
        "message": f"CM/L number '{digits}' format is valid.",
        "verification_steps": [
            "1. Open 'BIS Care App' and tap 'Verify Licence Details'.",
            f"2. Enter CM/L Number: {digits}.",
            "3. Confirm that the Manufacturer Name, Factory Location, Brand, and Validity Status are active."
        ]
    }


@bis_router.get("/certification-steps")
async def get_certification_steps(scheme: Optional[str] = "scheme-1"):
    """Returns step-by-step licensing workflow and document checklist."""
    if "2" in scheme or "crs" in scheme.lower():
        return SCHEME_II_STEPS
    return SCHEME_I_STEPS


@bis_router.get("/helpline")
async def get_helpline():
    """Returns official BIS helplines, addresses, and portals."""
    return {
        "toll_free_helpline": "1800-11-1255",
        "consumer_helpline": "1915",
        "official_portals": {
            "main_website": "https://www.bis.gov.in",
            "manak_online": "https://www.manakonline.in",
            "crs_portal": "https://www.bis.gov.in/index.php/crs-portal/",
            "consumer_portal": "https://www.services.bis.gov.in/php/BIS_2.0/bisconnect/"
        },
        "emails": {
            "general_info": "info@bis.gov.in",
            "complaints": "complaints@bis.gov.in",
            "hallmarking": "hallmarking@bis.gov.in"
        },
        "headquarters": {
            "name": "Bureau of Indian Standards",
            "address": "Manak Bhavan, 9 Bahadur Shah Zafar Marg, New Delhi 110002",
            "phone": "+91-11-23230131"
        },
        "mobile_app": {
            "name": "BIS Care App",
            "android": "Google Play Store",
            "ios": "Apple App Store",
            "features": ["Verify ISI Mark (CML)", "Verify Gold HUID", "Verify CRS Registration", "Lodge Complaints"]
        }
    }


@bis_router.post("/standards/upload")
async def upload_standard_document(
    file: UploadFile = File(...),
    standard_name: Optional[str] = Form(None)
):
    """
    Ingestion & update mechanism: Upload and index any new Indian Standard (IS code)
    or BIS Scheme document (PDF) dynamically into the searchable knowledge base without retraining!
    """
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF standards documents are supported.")

    os.makedirs(settings.STANDARDS_DIR, exist_ok=True)
    dest_path = os.path.join(settings.STANDARDS_DIR, file.filename)

    with open(dest_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Ingest into ChromaDB and update BM25 cache
    try:
        result = ingest_pdf_manual(dest_path)
        invalidate_bm25_cache()

        # Register in catalog
        doc_id = str(uuid.uuid4())
        register_document(
            doc_id=doc_id,
            filename=file.filename,
            filepath=dest_path,
            total_pages=result["total_pages"],
            total_chunks=result["total_chunks_indexed"],
            file_size_kb=result["file_size_kb"],
        )

        return {
            "status": "success",
            "message": f"Standard '{file.filename}' ingested and indexed successfully without retraining!",
            "doc_id": doc_id,
            "filename": file.filename,
            "total_chunks_indexed": result["total_chunks_indexed"],
            "total_pages": result["total_pages"],
            "searchable": True
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to ingest standard PDF: {e}")
