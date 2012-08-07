import xmlToJson

xmlString = '<alice xmlns="http://some-namespace" xmlns:charlie="http://some-other-namespace"><bob>david</bob> <charlie:edgar>frank</charlie:edgar></alice>'

print(xmlToJson.to_json(xmlString))
