try:
    from osgeo import gdal, ogr
except ImportError as error:
    raise Exception("""ERROR: Could not find the GDAL/OGR Python library bindings.""")
import os
import requests
import math
import copy
from xml.etree import ElementTree
from gdalwrap import Datasource, Transformation, makepoint

class Terraclip():
    def __init__(self, inputshape):
        self.inputshape = inputshape
        self._Initdata()
        self._Readinput()

    def _Initdata(self):
        if not os.path.isfile(self.inputshape):
            raise InvalidInputFile("Input file " + self.inputshape + " doesn't exist.")

        self.flightalt = 200
        self.tolerance = 5
        self.stepdistance = 500
        self.validOT =[
            'SRTMGL3',
            'SRTMGL1',
            'SRTMGL1_E',
            'AW3D30',
            'AW3D30_E',
            'SRTM15Plus',
            'NASADEM',
            'COP30',
            'COP30',
            'COP90',
            'EU_DTM',
            'GEDI_L3'
        ]

    def setdem(self, dempath, OTsource='skipOT', OTapi='yourOT_API_key'):
        if OTsource != 'skipOT':
            demdir = os.path.join(dempath)
            if not os.path.exists(demdir):
                os.mkdir(demdir)
            self.demdir = demdir
            self.OTsource = OTsource
            self._GetOTdem(OTapi)
        else:
            self._Readinput()
            self.dempath = os.path.join(dempath)

    def setparams(self, flightalt, tolerance, verticedistance, Takeoff=False, Land=False):
        self.flightalt = flightalt
        self.tolerance = tolerance
        self.stepdistance = verticedistance
        self.Takeoff = Takeoff
        self.Land = Land

    def rtlalt(self):
        return math.trunc(float(self.demdata.max()) + self.flightalt + 1)

    def maxterrain(self):
        return self.demdata.max()

    def minterrain(self):
        return self.demdata.min()

    def listOTsources(self):
        return self.validOT

    def maxinc(self):
        return self.maxinclination[3]

    def getarea(self):
        print(self.inputextent2)
        Xextent =  abs(self.inputextent2[0] - self.inputextent2[1])
        Yextent =  abs(self.inputextent2[2] - self.inputextent2[3])
        return [Xextent, Yextent, Xextent * Yextent]

    def execute(self):
        self._Compute()

    def _Getcoords(self, coord):
        wp = makepoint([coord[0], coord[1]])
        wppt = self.outrans.transform(wp).ExportToWkt()
        lat = str("{:.8f}".format(float(wppt.split(' ')[2].split(')')[0])))
        long = str("{:.8f}".format(float(wppt.split(' ')[1].split('(')[1])))
        alt = str("{:.6f}".format(float(coord[2])))
        return [lat, long, alt]

    def savemission(self, dest):
        self.outrans = Transformation('3395', '4326')
        filetype = dest.split('.')[-1].upper()
        if filetype == "TXT":
            vertices = open(dest, 'w')
            vertices.write('QGC WPL 110' + '\n')
            ###### home #####
            vertices.write('0\t1\t0\t16\t0\t0\t0\t0\t')
            home = self._Getcoords(self.tprofile[0])
            vertices.write(str(home[0])+' ')
            vertices.write(str(home[1]) + ' ')
            vertices.write(str(round(float(self.tprofile[0][2]),6)) + '\t1\n')
            ###### home #####
            wpcount = 1
            if self.Takeoff:
                vertices.write(str(wpcount) + '\t0\t3\t22\t0.00000000\t0.00000000\t0.00000000\t'
                                              '0.00000000\t0.00000000\t0.00000000\t')
                takeoffalt = self._Getdemalt([self.tprofile[0][0],self.tprofile[0][1]])
                takeoffalt = str("{:.6f}".format(float(self.tprofile[0][2] - takeoffalt)))
                vertices.write(takeoffalt + '\t1\n')
            pcount = len(self.tprofile) + 1
            for coord in self.tprofile:
                wpcount+=1
                wp = self._Getcoords(coord)
                if wpcount == pcount and self.Land is True:
                    vertices.write(str(wpcount) + '\t0\t0\t21\t0.00000000\t0.00000000\t0.00000000\t'
                                                  '0.00000000\t'+wp[0]+'\t'+wp[1]+'\t1.000000'+'\t1\n')
                else:
                    vertices.write(str(wpcount)+'\t0\t0\t16\t0.00000000\t0.00000000\t0.00000000\t'
                                                '0.00000000\t'+wp[0]+'\t'+wp[1]+'\t'+wp[2]+'\t1\n')
            vertices.close()
            sdest = dest.split('.')[0] + '_stats.txt'
            stats = open(sdest, 'w')
            stats.write('# Suggested RTL_ALT. DEM scene max value (above sea altitude + defined fligh altitude)\n')
            stats.write('RTL_ALT; ' + str(math.trunc(float(self.maxterrain())+self.flightalt+1))+'\n')
            stats.write('Max above ground altitude along path: ' + str(math.trunc(self.maxpoint[2] ) ) + 'm\n')
            stats.write('Min above ground altitude along path: ' + str(math.trunc(self.minpoint[2] ) ) + 'm\n')
            stats.write('Max segment inclination: ' + str(math.trunc(self.maxinclination[3])) + 'º\n')
            stats.close()
        else:
            out = Datasource('MemData', Action='Memory')
            out.Newlayer('WP', '4326', Type='Point')
            out.Newlayer('Paths', '4326', Type='Linestring')
            out.Newlayer('Stats', '4326', Type='Point')
            ly2 = out.getlayer('Paths')
            ly1 = out.getlayer('WP')
            ly3 = out.getlayer('Stats')
            ly1.createfield('Name', 'string')
            ly1.createfield('altmode', 'string')
            ly2.createfield('altmode', 'string')
            ly3.createfield('altmode', 'string')
            ly3.createfield('Name', 'string')
            ly1.createfield('Alt', 'integer')
            ly3.createfield('Alt', 'integer')
            gdal.SetConfigOption('LIBKML_ALTITUDEMODE_FIELD', 'altmode')

            WPname = 0
            tap = []
            for coord in self.tprofile:
                WPname = WPname + 1
                self._Insertkmlpoint(ly1, coord, coord[2], WPname)
                tap.append(str(coord[0]) + ' ' + str(coord[1]) + ' ' + str(coord[2]))

            mincoord = [self.minpoint[0][0],self.minpoint[0][1],self.minpoint[1]]
            maxcoord = [self.maxpoint[0][0],self.maxpoint[0][1],self.maxpoint[1]]
            maxinc = [self.maxinclination[0][0],self.maxinclination[0][1],self.maxinclination[1]]

            self._Insertkmlpoint(ly3, mincoord, mincoord[2], "MIN-"+
                                 str(math.trunc(self.minpoint[2] ) ) + "m" )
            self._Insertkmlpoint(ly3, maxcoord, maxcoord[2], "MAX-"+
                                 str(math.trunc(self.maxpoint[2] ) ) + "m" )
            self._Insertkmlpoint(ly3, maxinc, maxinc[2], "MAXINC-"+
                                 str(math.trunc(self.maxinclination[3] ) ) + "º" )

            st = 'LINESTRING Z (' + ','.join(tap) + ')'
            linez = ogr.CreateGeometryFromWkt(st)
            lineout = self.outrans.transform(linez)
            feat = ly2.Newfeature()
            feat.setgeom(lineout)
            feat.setfield('altmode', 'absolute')
            feat.insert()
            out.savefile(dest)

    def _Compute(self):
        self.minpoint = [[0,0],0,9000]
        self.maxpoint = [[0,0],0,0]
        self.maxinclination = [[0,0],0,0,0]
        # Step 1 -> Prepare data and transformations
        # Transforms everything to projected EPSG:3395 so we can use simple trigonometry for calculations
        # 3395 is not orthogonal but distortions are considered not relevant here for the case of small drones and small distances
        rasterdem = gdal.Open(self.dempath)
        warp = gdal.Warp('memoryRaster', rasterdem, dstSRS='EPSG:3395', resampleAlg='near', format='MEM')
        band = warp.GetRasterBand(1)
        self.demdata = band.ReadAsArray()
        self.demgeotransform = warp.GetGeoTransform()
        pp = self.demgeotransform[1]/2
        if pp < 1:
            pp = 1
        self.profileresolution = math.trunc(pp)
        if self.stepdistance < self.profileresolution * 2 and self.stepdistance != 0:
            self.stepdistance = self.profileresolution * 2

        # Step 2 -> Collect user vertices
        inputpoints = []
        ptcount = self.inputgeomt.GetPointCount()
        for pt in range(ptcount):
            coord = []
            tpt = self.inputgeomt.GetPoint(pt)
            alt = self._Getdemalt(tpt)
            coord.append(tpt[0])  # long
            coord.append(tpt[1])  # lat
            coord.append(alt + self.flightalt)  # desired flight altitude above ground
            coord.append("orig")  # Mark user created vertices
            inputpoints.append(coord)

        # Step 3 -> Adjust extra vertices accordingly self.stepdistance
        if self.stepdistance != 0:
            lock = True
            while lock:
                lock = False
                otprofile = []
                for c in range(0, len(inputpoints)-1):
                    otprofile.append(inputpoints[c])
                    coord1 = inputpoints[c]
                    coord2 = inputpoints[c + 1]
                    distp = self._Pointdistance(coord1, coord2)
                    if distp > self.stepdistance:
                        lock = True
                        newpointdist = distp/2
                        azimuth = self._Azimuth(coord1, coord2)
                        newcoord = self._Findcoords(coord1, azimuth, newpointdist)
                        alt = self._Getdemalt(newcoord) + self.flightalt
                        newcoord.append(alt)
                        newcoord.append('')
                        otprofile.append(newcoord)
                otprofile.append(inputpoints[len(inputpoints)-1])
                if lock:
                    inputpoints = copy.deepcopy(otprofile)

        # Step 4 -> Adjust vertices altitudes in respect to self.flightalt and tolerance. Anti-collision check along path
        lock = True
        while lock:
            lock = False
            for c in range(0, len(inputpoints) - 1):
                coord1 = inputpoints[c]
                coord2 = inputpoints[c + 1]
                scanpath = self._Scanpath(coord1, coord2)
                tolerance = float((self.tolerance / 100) * self.flightalt)
                if scanpath[0][2] < self.flightalt - tolerance:
                    lock = True
                    coord1[2] = coord1[2] + 2
                    coord2[2] = coord2[2] + 2

        # Step 5 -> Collect stats. TODO can be simplified
        for c in range(0, len(inputpoints) - 1):
            coord1 = inputpoints[c]
            coord2 = inputpoints[c + 1]
            scanpath = self._Scanpath(coord1, coord2)
            minft = scanpath[0][2]
            maxft = scanpath[1][2]
            maxinc = scanpath[2][3]
            if minft < self.minpoint[2]:
                self.minpoint[0][0] = scanpath[0][0][0]
                self.minpoint[0][1] = scanpath[0][0][1]
                self.minpoint[1] = scanpath[0][1]
                self.minpoint[2] = scanpath[0][2]
            if maxft > self.maxpoint[2]:
                self.maxpoint[0][0] = scanpath[1][0][0]
                self.maxpoint[0][1] = scanpath[1][0][1]
                self.maxpoint[1] = scanpath[1][1]
                self.maxpoint[2] = scanpath[1][2]
            if maxinc > self.maxinclination[3]:
                self.maxinclination[0][0] = scanpath[2][0][0]
                self.maxinclination[0][1] = scanpath[2][0][1]
                self.maxinclination[1] = scanpath[2][1]
                self.maxinclination[2] = scanpath[2][2]
                self.maxinclination[3] = scanpath[2][3]
        self.tprofile = inputpoints

    def _Scanpath(self, coord1, coord2):
        alts = []
        scanpath = []
        incl = []
        # Real (3D) total distance
        distanceZ = math.sqrt((coord1[0] - coord2[0]) ** 2 + (coord1[1] - coord2[1]) ** 2 + (coord1[2] - coord2[2]) ** 2)
        # Projected (2D) map distance
        distanceP = self._Pointdistance(coord1, coord2)
        inclination = math.degrees(math.asin((coord2[2] - coord1[2]) / distanceZ))
        incl.append(abs(inclination))
        azimuth = 180 + (math.degrees(math.atan2((coord1[0] - coord2[0]), (coord1[1] - coord2[1]))))
        # Real (3D) step distance
        rd = self.profileresolution / math.cos(math.radians(inclination))
        # Step altitude delta
        altdelta = math.sin(math.radians(inclination)) * rd
        # Map (2D) step distance
        diststep = math.trunc(distanceP / self.profileresolution)
        refalt = coord1[2]
        stepcoord = coord1
        for t in range(diststep):
            stepcoord = self._Findcoords(stepcoord, azimuth, self.profileresolution)
            demalt = self._Getdemalt(stepcoord)
            refalt = refalt + altdelta
            flightalt = refalt - demalt
            scanpath.append([stepcoord, refalt, flightalt])
            alts.append(flightalt)

        minalt = min(alts)
        maxalt = max(alts)
        maxinc = max(incl)
        minp = scanpath[alts.index(minalt)]
        maxp = scanpath[alts.index(maxalt)]
        maxincp = scanpath[incl.index(maxinc)] + [maxinc]
        return [minp, maxp, maxincp]

    def _Azimuth(self, coord1, coord2):
        azimuth = 180 + (math.degrees(math.atan2((coord1[0] - coord2[0]), (coord1[1] - coord2[1]))))
        return azimuth

    def _Findcoords(self, coordstart, azimuth, distance):
        stepX = (math.sin(math.radians(azimuth))) * distance
        stepY = (math.cos(math.radians(azimuth))) * distance
        coords = []
        coords.append(coordstart[0] + stepX)
        coords.append(coordstart[1] + stepY)
        return coords

    def _Pointdistance(self, coord1, coord2):
        #distance between points
        dist = math.sqrt((coord1[0] - coord2[0]) ** 2 + (coord1[1] - coord2[1]) ** 2)
        return dist

    def _Getdemalt(self, coords):
        pixelSizeX = self.demgeotransform[1]
        pixelSizeY = -self.demgeotransform[5]
        startX = self.demgeotransform[0]
        startY = self.demgeotransform[3]
        offsetX = coords[0] - startX
        pixelX = round(offsetX / pixelSizeX)
        offsetY = startY - coords[1]
        pixelY = round(offsetY / pixelSizeY)
        pixelvalue = self.demdata[pixelY][pixelX]
        return pixelvalue

    def _Insertkmlpoint(self, layer, coord, altitude, WPname):
        st = 'POINT(' + str(coord[0]) + ' ' + str(coord[1]) + ' ' + str(altitude) + ')'
        point = ogr.CreateGeometryFromWkt(st)
        feat = layer.Newfeature()
        pointout = self.outrans.transform(point)
        feat.setgeom(pointout)
        feat.setfield('Name', str(WPname))
        feat.setfield('altmode', 'absolute')
        feat.setfield('Alt', int(altitude))
        feat.insert()

    def _Readinput(self):
        self.inputset = Datasource(self.inputshape, Action='open r')
        self.inputlayer = self.inputset.getlayer(0)
        inputcrs = self.inputlayer.layer.GetSpatialRef()
        # Transforms everything to projected EPSG:3395 so we can use simple trigonometry for calculations
        # 3395 is not orthogonal but distortions are considered not relevant here for the case of small drones and small distances
        inputtrans = Transformation(inputcrs, '3395')
        inputtrans2 = Transformation(inputcrs, '4326') # CRS needed for OpenTopography
        iter = self.inputlayer.iterfeatures()
        for feature in iter:
            feat = feature
        inputgeom = feat.getgeom().geom
        inputgeomtemp = inputtrans2.transform(inputgeom)
        self.inputextent = inputgeomtemp.GetEnvelope()
        self.inputgeomt = inputtrans.transform(inputgeom)
        self.inputextent2 = self.inputgeomt.GetEnvelope()

    def _GetOTdem(self, OTapi):
        south = self.inputextent[2] - 0.00084 * 3
        north = self.inputextent[3] + 0.00084 * 3
        west = self.inputextent[0] - 0.00084 * 3
        east = self.inputextent[1] + 0.00084 * 3
        ext = []
        ext.append(str(south).replace('.', '_').replace('-', 'M') + '-')
        ext.append(str(north).replace('.', '_').replace('-', 'M') + '-')
        ext.append(str(west).replace('.', '_').replace('-', 'M') + '-')
        ext.append(str(east).replace('.', '_').replace('-', 'M') + '-' + self.OTsource)
        st = ''.join(ext) + ".tiff"
        filedir = os.path.join(self.demdir, st)
        otlink = 'https://portal.opentopography.org/API/globaldem?demtype=' + self.OTsource + '&south=' + str(
            south) + '&north=' + \
                 str(north) + '&west=' + str(west) + '&east=' + str(east) + '&outputFormat=GTiff&API_Key=' + OTapi
        if not os.path.exists(filedir):
            r = requests.get(otlink, allow_redirects=True)
            stcode = r.status_code
            if stcode == 401 or stcode == 400:
                root = ElementTree.fromstring(r.content)
                etxt = root.text
                if stcode == 400:
                    etxt = etxt + " List valid OTsource values with Terraclip.listOTsources()"
                raise InvalidOTException(etxt)
            elif stcode == 200:
                open(filedir, 'wb').write(r.content)

        self.dempath = filedir

class InvalidOTException(Exception):
    def __init__(self, message):
        message = message
        super().__init__(message)

class InvalidInputFile(Exception):
    def __init__(self, message):
        message = message
        super().__init__(message)

