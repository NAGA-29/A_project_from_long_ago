import hashlib
import hmac

secretKey = '9yg5fc0iz3wytriy2qfm09ajx0e7eo'
Twitch_Eventsub_Message_Id = '0ba94a3f-3616-419b-899f-5f4dcaf32014'
Twitch_Eventsub_Message_Timestamp = '2021-08-20T15:44:12.445361478Z'
body = '{"subscription":{"id":"fda50b60-4184-4d67-8a6f-972f310054a6","status":"webhook_callback_verification_pending","type":"stream.online","version":"1","condition":{"broadcaster_user_id":"557359020"},"transport":{"method":"webhook","callback":"https://pvgllfml6j.execute-api.ap-northeast-1.amazonaws.com/Twitch-eventSub"},"created_at":"2021-08-20T15:44:12.440877915Z","cost":1},"challenge":"4n6zKvUu3cOwK8pAS-CmbrtUu3iGZmVmOW4uXg-Q268"}'

payload = Twitch_Eventsub_Message_Id + Twitch_Eventsub_Message_Timestamp + body
# payload = b'Hello World!'

signature = hmac.new(bytes(secretKey, 'UTF-8'), bytes(payload, 'UTF-8'), hashlib.sha256)
expected_signature_header = 'sha256=' + signature.hexdigest()

print(expected_signature_header)