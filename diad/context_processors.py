from datetime import datetime

def copyright(request):
    actual = datetime.now()
    return {'actual': actual.year}