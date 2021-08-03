import redis

publisher = redis.Redis(host='localhost', port=6379)
message = ""
channel = "test"
while (message != "exit"):
    message = input("")
    send_message = "Python : " + message
    publisher.publish(channel, send_message)
