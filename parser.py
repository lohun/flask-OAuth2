import xml.etree.ElementTree as ET


def parse_ssml(ssml_string):
    try:
        root = ET.fromstring(ssml_string)
    except ET.ParseError as e:
        print(e)
        return None
    
    parsed_data = []
    for element in root.iter():
        tag = element.tag
        text = element.text.strip() if element.text else ""
        attributes = element.attrib

        if tag == "speak":
            pass
        elif tag == "p":
            parsed_data.append({"type": "paragraph", "text": text})
        elif tag == "s":
            parsed_data.append({"type": "sentence", "text": text})
        elif tag == "break":
            strength = attributes.get("strength")
            time = attributes.get("time")
            parsed_data.append({"type": "break", "strength": strength, "time": time})
        elif tag == "say-as":
            interpret_as = attributes.get("interpret-as")
            parsed_data.append({"type": "say-as", "text": text, "interpret_as": interpret_as})
        elif tag == "prosody":
            rate = attributes.get("rate")
            pitch = attributes.get("pitch")
            volume = attributes.get("volume")

            parsed_data.append({"type": "prosody", "rate": rate, "pitch": pitch, "volume": volume})
        else:
            parsed_data.append({"type": tag, "text": text, "attributes": attributes})
    return parsed_data



ssml_example = """
<speak>
  <p>This is a <prosody rate="fast">sample</prosody> paragraph.</p>
  <s>Hello, <say-as interpret-as="spell-out">SSML</say-as>!</s>
  <break time="500ms"/>
  <audio src="https://example.com/audio.mp3"/>
</speak>
"""

parsed_ssml = parse_ssml(ssml_example)
if parsed_ssml:
    for item in parsed_ssml:
        print(item)

