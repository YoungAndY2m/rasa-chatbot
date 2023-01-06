def Detect_web(paths) -> list:
    """Detects web annotations given an image."""
    best_guesses = []

    from google.cloud import vision
    import io
    client = vision.ImageAnnotatorClient()

    for path in paths:
        with io.open(path, 'rb') as image_file:
            content = image_file.read()

        image = vision.Image(content=content)

        response = client.web_detection(image=image)
        annotations = response.web_detection

        if annotations.best_guess_labels:
            label = annotations.best_guess_labels[0]
            print('\n Best guess label: {}'.format(label.label))
            best_guesses.append([label.label])
            # for label in annotations.best_guess_labels:
            #     print('\nBest guess label: {}'.format(label.label))

        if annotations.visually_similar_images:
            print('\n{} visually similar images found:\n'.format(
                len(annotations.visually_similar_images)))
            for image in annotations.visually_similar_images:
                print('\tImage url    : {}'.format(image.url))
                best_guesses.append([image.url])

        if response.error.message:
            raise Exception(
                '{}\nFor more info on error messages, check: '
                'https://cloud.google.com/apis/design/errors'.format(
                    response.error.message))

    return best_guesses


# detect_web('/Users/young_y2m/Desktop/CSE/Tower.jpg')

def Find_location(address):
    import requests
    import os
    from dotenv import load_dotenv

    load_dotenv()

    GOOGLE_API_KEY = os.getenv('GOOGLE_MAP_TOKEN')

    lat, lng = None, None
    api_key = GOOGLE_API_KEY
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    endpoint = f"{base_url}?address={address}&key={api_key}"

    r = requests.get(endpoint)
    if r.status_code not in range(200, 299):
        return None, None
    try:
        results = r.json()['results'][0]
        print(results)
        lat = results['geometry']['location']['lat']
        lng = results['geometry']['location']['lng']
    except:
        pass

    return lat, lng