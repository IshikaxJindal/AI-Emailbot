# from models import Email, ProcessingLog
# from src.preprocessing.email_preprocessor import preprocess_email
# from src.intent.service import process_intent
#
#
# def process_email(email_data, db, event_id):
#     try:
#         print(f"[{event_id}] Processing started")
#
#         # 🔥 LOG PROCESSING
#         db.add(ProcessingLog(event_id=event_id, status="PROCESSING"))
#         db.commit()
#
#         # 🔥 RUN PREPROCESSING
#         result = preprocess_email(email_data["body"])
#
#         print(f"[{event_id}] Clean text:", result["clean_text"])
#         print(f"[{event_id}] Time entities:", result["time_entities"])
#
#         # 🔥 STORE RESULT
#         db.add(Email(
#             event_id=event_id,
#             clean_text=result["clean_text"],
#             entities=result["time_entities"]
#         ))
#
#         # 🔥 SUCCESS LOG
#         db.add(ProcessingLog(event_id=event_id, status="SUCCESS"))
#         db.commit()
#
#         print(f"[{event_id}] Pipeline success")
#
#     except Exception as e:
#         print(f"[{event_id}] Error:", str(e))
#
#         db.add(ProcessingLog(
#             event_id=event_id,
#             status="FAILED",
#             error_message=str(e)
#         ))
#         db.commit()


from models import Email, ProcessingLog
from src.preprocessing.email_preprocessor import preprocess_email
from src.intent.service import process_intent
from models import IntentResult


def process_email(email_data, db, event_id):
    try:
        print(f"[{event_id}] Processing started")

        # 🔥 LOG PROCESSING
        db.add(ProcessingLog(event_id=event_id, status="PROCESSING"))
        db.commit()

        # 🔥 STEP 1: PREPROCESSING
        result = preprocess_email(email_data["body"])

        clean_text = result["clean_text"]
        entities = result["time_entities"]

        print(f"[{event_id}] Clean text:", clean_text)
        print(f"[{event_id}] Time entities:", entities)

        # 🔥 STEP 2: INTENT CLASSIFICATION (NEW)
        intent_result = process_intent(
            event_id=event_id,
            clean_text=clean_text,
            entities=entities
        )
        db.add(IntentResult(
            event_id=event_id,
            intents=intent_result["intents"],
            entities=intent_result["entities"],
            actions=intent_result["actions"],
            source=intent_result["meta"]["source"]
        ))

        print(f"[{event_id}] Intent Result:", intent_result)

        # 🔥 STEP 3: STORE PREPROCESSED DATA (existing)
        db.add(Email(
            event_id=event_id,
            clean_text=clean_text,
            entities=entities
        ))

        # 🔥 (OPTIONAL BUT RECOMMENDED) STORE INTENT RESULT
        # For now just print — later we’ll create a new table

        # 🔥 SUCCESS LOG
        db.add(ProcessingLog(event_id=event_id, status="SUCCESS"))
        db.commit()

        print(f"[{event_id}] Pipeline success")

        # 🔥 RETURN RESPONSE (IMPORTANT FOR SWAGGER)
        return intent_result

    except Exception as e:
        print(f"[{event_id}] Error:", str(e))

        db.add(ProcessingLog(
            event_id=event_id,
            status="FAILED",
            error_message=str(e)
        ))
        db.commit()

        return {"error": str(e)}