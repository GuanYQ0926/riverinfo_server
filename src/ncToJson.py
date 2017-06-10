from netCDF4 import Dataset
import json


def convertToJson(ncFilelist, jsonFilepath):
    # kyoto range
    # (135.55916666666667, 34.875)
    # (135.8786111111111, 35.32111111111111)
    # wanted area
    # (135.4, 34.8), (135.4, 35.0), (135.4, 35.2), (135.4, 35.4)
    # (135.6, 34.8), (135.6, 35.0), (135.6, 35.2), (135.6, 35.4)
    # (135.8, 34.8), (135.8, 35.0), (135.8, 35.2), (135.8, 35.4)
    # (136.0, 34.8), (136.0, 35.0), (136.0, 35.2), (136.0, 35.4)
    # {'factor1': {'lat_lon':[], 'lat_lon': []}}
    lat_list = [34.8, 35.0, 35.2, 35.4]
    lon_list = [135.4, 135.6, 135.8, 136.0]
    lat_index_list = [int(round((v - 15.0) / 0.2)) for v in lat_list]
    lon_index_list = [int(round((v - 105.0) / 0.2)) for v in lon_list]
    tempDict = {}
    for ncfile in ncFilelist:
        dataset = Dataset(ncfile, 'r')
        properties = [str(v) for v in dataset.variables]
        lons = dataset.variables[properties[0]][:]
        lats = dataset.variables[properties[1]][:]
        times = dataset.variables[properties[2]][:]
        values = dataset.variables[properties[3]][:]
        subtempDict = {}
        for lt in lat_index_list:
            for ln in lon_index_list:
                tempArr = []
                for t in xrange(len(times)):
                    tempArr.append(float(values[t, lt, ln]))
                subtempDict[str(lats[lt]) + '_' + str(lons[ln])] = tempArr
        tempDict[properties[3]] = subtempDict
    # reform data into the form as {lat_lon: {'factor1':[], 'factor2': []}}
    with open(jsonFilepath, 'w') as f:
        json.dump(tempDict, f)


if __name__ == '__main__':
    ncFilelist = ['../data/ncfile/precipitation.nc',
                  '../data/ncfile/surface_pressure.nc',
                  '../data/ncfile/temperature.nc',
                  '../data/ncfile/total_cloud_cover.nc']
    jsonFilepath = '../data/jsonfile/weatherdata.json'
    convertToJson(ncFilelist, jsonFilepath)
