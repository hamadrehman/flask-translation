from bs4 import BeautifulSoup as BS
from urllib.parse import quote_plus

import httpx

import asyncio

from functools import lru_cache
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@lru_cache(maxsize=1000)
def cached_translation(text: str, language: str) -> str:
    """Cache translation results to avoid redundant API calls"""
    return text


async def makeRequests(google_translate_links):
    try:

        async with httpx.AsyncClient() as client:

            responses = await asyncio.gather(
                *[client.get(i) for i in google_translate_links],
                return_exceptions=True
            )
            rs = []
            for response in responses:
                if isinstance(response, Exception):
                    logger.error(f"Request failed: {str(response)}")
                    rs.append(None)
                    continue
                try:
                    rs.append(response.json()[0])
                except Exception as e:
                    logger.error(f"Failed to parse response: {str(e)}")
                    rs.append(None)

            return rs
    except Exception as e:
        logger.error(f"Batch request failed: {str(e)}")
        return [None] * len(google_translate_links)


def getTranslations(elementList, language):
    google_translate_links = []
    for element in elementList:
        if not element.text.strip():  # Skip empty elements
            continue
            
        cached = cached_translation(element.text, language)
        if cached != element.text:
            google_translate_links.append(None)
            continue

        baseUrl = (
            f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl={language}&dt=t&q="
            + quote_plus(element.text)
        )
        google_translate_links.append(baseUrl)

    try:
        results = asyncio.run(makeRequests(google_translate_links))
        return results
    except Exception as e:
        logger.error(f"Translation failed: {str(e)}")
        return [None] * len(google_translate_links)



def translate_page(pageName, language, text_elements):
    try:
        content = open(pageName, "rb").read()
        page = BS(content, features="lxml")

        for element_to_translate in text_elements:
            try:
                element_by_tag = page.findAll(element_to_translate)
                translated_elements = getTranslations(element_by_tag, language)
                translated_text = []
                
                for trans in translated_elements:
                    if trans is None:
                        translated_text.append(None)
                        continue
                    try:
                        trans = trans[0][0]
                        if isinstance(trans, list) == False:
                            translated_text.append(trans)
                            # Cache successful translation
                            cached_translation(trans, language)
                    except (IndexError, TypeError) as e:
                        logger.error(f"Failed to process translation: {str(e)}")
                        translated_text.append(None)

                for el, trans in zip(element_by_tag, translated_text):
                    if trans is not None:
                        el.string = trans
                    else:
                        logger.warning(f"Skipping translation for element: {el.text[:50]}...")
                        
            except Exception as e:
                logger.error(f"Failed to translate element {element_to_translate}: {str(e)}")
                continue

        return str(page)
    except Exception as e:
        logger.error(f"Failed to translate page {pageName}: {str(e)}")
        return content.decode() 