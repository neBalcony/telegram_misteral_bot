from mistralai import Mistral
from config import settings

class MistralClient():
    mistral = None

    def get_mistral()-> Mistral:
        if MistralClient.mistral is None:
            MistralClient._init()
        return MistralClient.mistral
    def _init():
        MISTRAL_API_KEY = settings.MISTRAL_API_KEY
        MistralClient.mistral = Mistral(api_key=MISTRAL_API_KEY)
    