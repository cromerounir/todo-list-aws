import json
import decimalencoder
import todoList
import boto3

comprehend = boto3.client('comprehend')
translateapi = boto3.client('translate')

def translate(event, context):
    result = todoList.get_item(event['pathParameters']['id'])
    text = result['text']
    print('Calling DetectDominantLanguage')
    
    language_detected_obj = comprehend.detect_dominant_language(Text=text)
    language_detected = language_detected_obj ['Languages'][0]['LanguageCode']
    print("End of DetectDominantLanguage:"+language_detected)
    lang = event ['pathParameters']['language']
    result_translation = translateapi.translate_text(
        Text=text,
        SourceLanguageCode=language_detected,
        TargetLanguageCode=lang)
    result['text'] = result_translation['TranslagedText']
    
    response = {
        "statusCode": 200,
        "body": json.dumps(result,
                           cls=decimalencoder.DecimalEncoder)
    }
    
    return response