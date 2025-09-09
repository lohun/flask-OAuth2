import xml.etree.ElementTree as ET

ssml_example = """
<speak>
  <p>This is a <prosody rate="fast">sample</prosody> paragraph.</p>
  <s>Hello, <say-as interpret-as="spell-out">SSML</say-as>!</s>
  <break time="500ms"/>
  <audio src="https://example.com/audio.mp3"/>
</speak>
"""

def parser(ssml_string):
    try:
        root = ET.fromstring(ssml_string)
    except ET.ParseError as e:
        print(e)
        return None
    
    parsedElements = []
    for element in root.iter():
        # text, tag & attributes
        tag = element.tag
        text = element.text.strip() if element.text else ""
        attributes = element.attrib

        if tag == "speak":
            pass
        elif tag == "p":
            parsedElements.append({"type": "paragraph", "text": text})
        elif tag == "s":
            parsedElements.append({"type": "sentence", "text": text})
        elif tag == "say-as":
            interpret_as = attributes.get("interpret_as")
            parsedElements.append({"type": "say-as", "interpret_as": interpret_as, "text": text})
        elif tag == "break":
            time = attributes.get("time")
            strength = attributes.get("strength")
            parsedElements.append({"type": "break", "time": time, "strength": strength})
        elif tag == "prosody":
            # rate, pitch, volume
            rate = attributes.get("rate")
            pitch = attributes.get("pitch")
            volume = attributes.get("volume")
            parsedElements.append({"type": "prosody", "rate": rate, "pitch": pitch, "volume": volume})
        else:
            parsedElements.append({"type": tag, "attributes": attributes, "text": text})
    return parsedElements

parsed_ssml = parser(ssml_example)
if parsed_ssml:
    for item in parsed_ssml:
        print(item)

            


