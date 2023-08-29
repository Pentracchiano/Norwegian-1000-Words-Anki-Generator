from google.cloud import translate
from google.oauth2.service_account import Credentials
import secrets_handler


project_id="able-veld-395215"
location = "global"

credentials = Credentials.from_service_account_file(secrets_handler.secrets["GOOGLE_API_KEY_FILE"],
                                                    scopes=["https://www.googleapis.com/auth/cloud-platform"])
client = translate.TranslationServiceClient(credentials=credentials)
parent = f"projects/{project_id}/locations/{location}"


def fetch_translation(text: str) -> str:
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",
            "source_language_code": "en-US",
            "target_language_code": "no",
        }
    )

    return response.translations[0].translated_text


if __name__ == "__main__":
    print(fetch_translation())
