import pdfplumber

from logger import logger


def extract_resume_text(pdf_path):

    logger.info(f"Extracting text from resume: '{pdf_path}'")

    text = ""

    try:

        with pdfplumber.open(pdf_path) as pdf:

            for i, page in enumerate(pdf.pages):

                page_text = page.extract_text()

                if page_text:
                    text += page_text + "\n"
                else:
                    logger.warning(f"Page {i + 1} of '{pdf_path}' returned no text.")

        if not text.strip():
            logger.warning(f"Resume '{pdf_path}' appears to be empty or unreadable.")
        else:
            logger.info(
                f"Resume text extracted: {len(text)} characters, "
                f"{len(pdf.pages)} page(s)."
            )

    except FileNotFoundError:

        logger.error(f"Resume file not found: '{pdf_path}'")
        raise

    except Exception as e:

        logger.error(f"Failed to extract resume text from '{pdf_path}': {e}")
        raise

    return text