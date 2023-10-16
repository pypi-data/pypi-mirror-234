def make_sub_unsub_messages(channel: str):
    return {
        "method": "SUBSCRIBE", 
        "params": [
            channel
        ],
    }, {
        "method": "UNSUBSCRIBE", 
        "params": [
            channel
        ]
    }
