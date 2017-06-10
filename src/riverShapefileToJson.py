import json
import shapefile


class RiverShpToJson:
    '''
    convert river shapefile to node and stream json files
    '''

    def __init__(self, shpFilepath, jsonFilepath):
        self.shpFilepath = shpFilepath
        self.jsonFilepath = jsonFilepath

    def convertToJson(self):
        shpFile = shapefile.Reader(self.shpFilepath)
        # fields = shpFile.fields[1:]
        # field_names = [field[0] for field in fields]
        coordinates_list = []

        for sr in shpFile.shapeRecords():
            # attr = dict(zip(field_names, sr.record))
            geom = sr.shape.__geo_interface__
            # dict_buffer.append(dict(geometry=geom))
            coordinates_list.append(geom['coordinates'])

        with open(self.jsonFilepath, 'w') as f:
            json.dump(dict(coordinates=coordinates_list), f)


if __name__ == '__main__':
    shpFilepaths = ['../data/shapefile/river/kyoto/W05-09_26-g_RiverNode.shp',
                    '../data/shapefile/river/kyoto/W05-09_26-g_Stream.shp',
                    '../data/shapefile/river/gifu/W05-08_21-g_RiverNode.shp',
                    '../data/shapefile/river/gifu/W05-08_21-g_Stream.shp']
    jsonFilepaths = ['../data/jsonfile/river/kyoto_node.json',
                     '../data/jsonfile/river/kyoto_stream.json',
                     '../data/jsonfile/river/gifu_node.json',
                     '../data/jsonfile/river/gifu_stream.json']
    for shpFilepath, jsonFilepath in zip(shpFilepaths, jsonFilepaths):
        processor = RiverShpToJson(shpFilepath, jsonFilepath)
        processor.convertToJson()
