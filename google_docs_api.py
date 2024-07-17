import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Если изменить эти области, удалите файл token.json.
SCOPES = ["https://www.googleapis.com/auth/documents"]


def main():
    """Пример использования Google Docs API."""
    creds = None
    # Файл token.json хранит токены доступа и обновления пользователя
    # и создается автоматически после первого завершения потока авторизации.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # Если нет доступных (действительных) учетных данных, дайте пользователю войти в систему.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            # Укажите конкретный порт для локального сервера
            creds = flow.run_local_server(port=8000)
        # Сохраните учетные данные для следующего запуска
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("docs", "v1", credentials=creds)

        # Создание нового документа
        document = create_document(service, "Новый документ")
        print(f"Создан документ с ID: {document['documentId']}")

        # Получение информации о документе
        document_id = document['documentId']
        doc_info = get_document(service, document_id)
        print(f"Название документа: {doc_info.get('title')}")

        # Вставка текста
        insert_text(service, document_id, "Привет, мир!")
        print("Текст вставлен в документ.")

        # Обновление текста
        update_text(service, document_id, "Привет, мир!", "Привет, Google Docs API!")
        print("Текст обновлен в документе.")

        # Удаление текста
        delete_text(service, document_id, 1, 10)
        print("Текст удален из документа.")

    except HttpError as err:
        print(err)


def create_document(service, title):
    """Создание нового документа с указанным заголовком."""
    document = service.documents().create(body={"title": title}).execute()
    return document


def get_document(service, document_id):
    """Получение информации о документе."""
    document = service.documents().get(documentId=document_id).execute()
    return document


def insert_text(service, document_id, text, index=1):
    """Вставка текста в документ на указанную позицию."""
    requests = [
        {
            'insertText': {
                'location': {
                    'index': index,
                },
                'text': text
            }
        }
    ]
    result = service.documents().batchUpdate(
        documentId=document_id, body={'requests': requests}).execute()
    return result


def update_text(service, document_id, old_text, new_text):
    """Обновление текста в документе."""
    document = service.documents().get(documentId=document_id).execute()
    content = document.get('body').get('content')

    requests = []
    for element in content:
        if 'paragraph' in element:
            for text_run in element['paragraph']['elements']:
                if 'textRun' in text_run and old_text in text_run['textRun']['content']:
                    start_index = text_run['startIndex']
                    end_index = text_run['endIndex']
                    requests.append({
                        'replaceAllText': {
                            'containsText': {
                                'text': old_text,
                                'matchCase': True
                            },
                            'replaceText': new_text
                        }
                    })
    if requests:
        result = service.documents().batchUpdate(
            documentId=document_id, body={'requests': requests}).execute()
        return result


def delete_text(service, document_id, start_index, end_index):
    """Удаление текста из документа."""
    requests = [
        {
            'deleteContentRange': {
                'range': {
                    'startIndex': start_index,
                    'endIndex': end_index
                }
            }
        }
    ]
    result = service.documents().batchUpdate(
        documentId=document_id, body={'requests': requests}).execute()
    return result


if __name__ == "__main__":
    main()


