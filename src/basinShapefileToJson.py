import json
import shapefile
import sys
sys.path.append('/usr/local/lib/python2.7/site-packages')
import cv2
import numpy as np


class BasinShpToJson:

    def __init__(self, shpFilepath, jsonFilepath, basinImagePath):
        self.shpFilepath = shpFilepath
        self.jsonFilepath = jsonFilepath
        self.basinImagePath = basinImagePath
        self.mesh_list = []
        self.basinCode = []
        # iamge info
        self.imgWidth = 0
        self.imgHeight = 0
        self.imgWidthLons = []
        self.imgHeightLats = []
        self.basinImg = None
        # contours
        self.bcode_contours = {}

    def unpackMeshData(self):
        # convert basin shapefile to jsonfile
        shpFile = shapefile.Reader(self.shpFilepath)

        for sr in shpFile.shapeRecords():
            info = sr.record  # info[1]: basin code, # info[2] river code
            geom = sr.shape.__geo_interface__
            # geom['coordinates'].shape = (1,5,2)
            self.mesh_list.append(dict(bcode=info[1], rcode=info[2],
                                       coords=geom['coordinates'][0]))

    def genBasinCodeList(self):
        for mesh in self.mesh_list:
            temp_bcode = mesh['bcode']
            if temp_bcode not in self.basinCode:
                self.basinCode.append(temp_bcode)
        print(self.basinCode)
        print(len(self.basinCode))

    def saveMeshDataToImg(self):
        '''
        generate image info in this function
        convert file to the image or matrx
        '''
        # count longitutde and treat as width of image
        # count lattitude and treat as height of image
        img_info = {}
        for mesh in self.mesh_list:
            temp_coords = mesh['coords']
            temp_bcode = mesh['bcode']
            for xy in temp_coords:
                # check weather x,y  are alreay in width_heihgt_pixl
                # xy[0]: longitutde, xy[1]: lattitude
                if xy[0] not in self.imgWidthLons:
                    self.imgWidthLons.append(xy[0])
                if xy[1] not in self.imgHeightLats:
                    self.imgHeightLats.append(xy[1])
                img_info[(xy[0], xy[1])] = float(
                    self.basinCode.index(temp_bcode)) * 4
        # generate image
        self.imgWidth = len(self.imgWidthLons)
        self.imgHeight = len(self.imgHeightLats)
        mesh_image = np.zeros((self.imgHeight, self.imgWidth, 1))
        for i in xrange(self.imgHeight):
            for j in xrange(self.imgWidth):
                try:
                    mesh_image[i, j] = img_info[
                        (self.imgWidthLons[j],
                         self.imgHeightLats[self.imgHeight - i - 1])]
                except:
                    mesh_image[i, j] = 255
        self.basinImg = mesh_image
        # save the image
        cv2.imwrite(self.basinImagePath, self.basinImg)

    def findCountours(self):
        # image value range [0, len(self.basinCode)]*4
        # undefined where values 255
        for index, bcode in enumerate(self.basinCode):
            # search for all image
            value = index * 4
            self.bcode_contours[bcode] = self.detectAdjacentPoint(value)

    def detectAdjacentPoint(self, value):
        coord_list = []
        for row in xrange(self.imgHeight):
            for col in xrange(self.imgWidth):
                if self.basinImg[row][col] == value:
                    isRectContours = False
                    top = right = bot = left = value
                    # top
                    try:
                        top = self.basinImg[row - 1][col]
                    except:
                        isRectContours = True
                    # right
                    try:
                        right = self.basinImg[row][col + 1]
                    except:
                        isRectContours = True
                    # bot
                    try:
                        bot = self.basinImg[row + 1][col]
                    except:
                        isRectContours = True
                    # left
                    try:
                        left = self.basinImg[row][col - 1]
                    except:
                        isRectContours = True
                    if top != value or right != value or bot != value or \
                            left != value or isRectContours:
                        coord_list.append(
                            [self.imgHeightLats[self.imgHeight - 1 - row],
                             self.imgWidthLons[col]])
        return coord_list

    def saveToJson(self):
        with open(self.jsonFilepath, 'w') as f:
            dumpout = dict(basin_code=self.basinCode,
                           bcode_contours=self.bcode_contours)
            json.dump(dumpout, f)


if __name__ == '__main__':
    shpFilepaths = [
        '../data/shapefile/basin/gifu_e/W07-09_5237-jgd_ValleyMesh.shp']
    jsonFilepaths = ['../data/jsonfile/basin/gifu_e.json']
    basinImagePath = '../data/img/gifu_e.png'
    for shpFilepath, jsonFilepath in zip(shpFilepaths, jsonFilepaths):
        processor = BasinShpToJson(shpFilepath, jsonFilepath, basinImagePath)
        processor.unpackMeshData()  # convert data into python format
        processor.genBasinCodeList()  # create list that decide matrix value
        processor.saveMeshDataToImg()  # create matrx(img) and get basic info
        processor.findCountours()  # check the point on contours
        processor.saveToJson()
