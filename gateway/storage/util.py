import pika, json


def upload(f, fs, channel, access):
    try:
        fid = fs.put(f)
    except:
        return "Internal Server Error", 500

    msg = {"video_fid": str(fid), "mp3_fid": None, "username": access["username"]}

    try:
        channel.basic_publish(
            exchange="",
            routing_key="video",
            body=json.dumps(msg),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE  # pika.DeliveryMode.Persistent
            ),
        )
    except:
        fs.delete(fid)
        return "Internal Server Error", 500
