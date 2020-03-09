from pushbullet import Pushbullet


def notify(title, body, _type="pb", **kws):
    if _type in ["pushbullet", "pb"]:
        token = kws.get("token")
        pb = Pushbullet(token)
        pb.push_note(title, body)
