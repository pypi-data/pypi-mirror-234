import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrow
import matplotlib.font_manager as fm
import matplotlib.patheffects as PathEffects
from mpl_toolkits.axes_grid1 import make_axes_locatable
from mpl_toolkits.axes_grid1.anchored_artists import AnchoredSizeBar
import seaborn as sns
import cv2 

import numpy as np
from scipy.signal import find_peaks
from scipy.signal import savgol_filter

from copy import deepcopy
import pickle
import pandas as pd

from .figProc import point, scalebar, figProc

        
class hyperImg(figProc):
    default_img_mode = 'I'
    default_line_mode = 'Integrated'
    datatype = '' # ['spc_Img', 'spc_Diff', 'sem_Img']
    scalebar = None
    
    I_th = 0
    spcIndice = []
    
    x = [0,0]
    x_unit = ''

    nPoints = 0
    points = []
    Ref_I = [0,1]
    Ref_pos = [0,1]
    
    spcRange = None
    isPos_corrected = False
    isI_corrected = False
    
    def __init__(self):
        pass

    #---------------------------------------------- set up parameters/structures for maps and lines
    def setup_maps(self):
        '''
        Set up map modes
        '''
        self.img_modes = ['I', 'rI', 'pos', 'pos_diff', 'rpk_I', 'pk_I', 'ref_pos', 'ref_offset', 'ref_I_avg', 'browse', 'sem_I']
        #self.map_field = ['loc', 'cmap', 'cbar', 'title']
        map_info = { 'label': ['I', 'rI', 'pos', 'pos_diff', 'rpk_I', 'pk_I', 'ref_pos','ref_offset', 'ref_I_avg', 'browse', 'sem_I'],
                    'loc':[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0],
                    'cmap': [None, 'plasma','Blues', 'PuRd', 'plasma', None, 'crest', 'crest', 'crest', None, 'gray'],
                    'cbar': ['right', 'right', 'right', 'right','right', 'right', 'right', 'right', 'right', 'bottom',  None],
                    'title':['Integrated counts', 'Intensity ratio', 'Max peak', 'Peak difference', '$I_{max}$ ratio', 'Peak intensity', 'Ref Peak', 'Pos adjusted', 'I scaled', '', self.title]}
        self.map_info = pd.DataFrame(map_info, index = self.img_modes)
    
    def setup_lines(self):
        '''
        Set up line modes
        '''
        self.line_modes = ['Integrated', 'Points', 'linescan', 'histogram']
        #self.line_field = ['label','xlabel', 'ylabel', 'title']
        line_info = {'label': self.line_modes,
                    'xlabel':[self.x_label, self.x_label, 'Position (' + self.xy_unit + ')',self.x_label],
                    'ylabel':[self.y_label, self.y_label, [self.y_label, 'Peak position', 'Intensity ratio', 'Peak difference'], self.y_label],
                    'title': ['Integrated intensity: ' + self.title, self.title, ['Intensity and peak position profile','Intensity ratio and peak position difference'], 'Histogram']}
        self.line_info = pd.DataFrame(line_info, index = self.line_modes)
    

    # ---------------------- load data
    def load_data(self):
        pass
    
    # -------------------- save data
    def save(self, file = None):
        filename = self.create_filename() if file is None else file
        try:
            with open(filename, 'wb') as handle:
                    pickle.dump(vars(self), handle)
            print('Files saved (pkm, png): ' + filename)
            filename = filename.split('.')[0]
            self.fig.savefig(filename + '.png')
        except:
            print('Save failed.')
    
    # ------------------------            
    def create_filename(self):
        spcRange = '{:.{prec}f}'.format(self.spcRange[0], prec=self.spcRange_decimal) + '-' + '{:.{prec}f}'.format(self.spcRange[-1], prec=self.spcRange_decimal)
        title = self.title
        for char in ['$', '_', '{', '}']:
            title = title.replace(char, '')
        self.filename = title + '_' + spcRange + '_Ith-' + "{:.2f}".format(self.I_th)  + '.pkm'
        return self.filename
    
    # ---------------------- Get spectra for a selected point
    def get_map_info(self):
        '''
        Get spectra for a selected point
        '''
        modes = self.img_modes
        mapInfo = {}
        for mode in modes:
            Info = self.map_info[self.map_info.index==mode]
            mapInfo[mode] = {}
            for field in Info.keys():
                mapInfo[mode][field] = Info[field][mode]
                
        return mapInfo
    
    #-------------------- Create image data
    def create_default_scalebar(self):
        default_sb_length = np.array([1, 5, 10, 15, 20, 50, 100, 200, 500])
        intended_sb_length = self.imgDim['Scan_Width']/5
        sb_length = int(default_sb_length[np.abs(default_sb_length - intended_sb_length).argmin()])
        self.scalebar = scalebar(length = sb_length, height = self.imgDim['Scan_Height']/40, 
                          unit = self.xy_unit, location = 'lower left', color = 'white')
        return self.scalebar
    
    def create_image(self, imgMode = None, spcPos = None, Vmin = None, Vmax = None):
        '''
        imgMode/spcPos is to choose raw/cal data for browsing raw/cal data sets
        '''
        mapInfo = self.get_map_info()
        imgData = {}

        # Convert points to dict
        ptMarks = []
        for pt in self.points:
            ptMarks.append(vars(pt))
        
        sbar = vars(self.scalebar)
        
        for idx, img in enumerate(list(mapInfo.keys())):
            if imgMode == 'raw': # Use rawdata
                spcRange = 0 if spcPos is None else spcPos
                data = self.rawdata[:,:,np.abs(self.x - spcPos).argmin()]
                title = str(spcPos) + ' ' + self.x_unit
            elif imgMode == 'cal': # Use calibrated data
                spcRange = 0 if spcPos is None else spcPos
                data = self.cal_data[:,:,np.abs(self.x - spcRange).argmin()]
                title = str(spcPos) + ' ' + self.x_unit
            else: # Use processed data
                data = self.data[:,:, mapInfo[img]['loc']]
                title = self.title + ': ' + mapInfo[img]['title']
            
            if len(self.points) > 2 and imgMode == 'linescan':
                lnMarks = [{'x':[self.points[1].x, self.points[-1].x], 'y':[self.points[1].y, self.points[-1].y]}]
            else:
                lnMarks = None
           
                
            imgData[img] = {'image':data,
                            'aspect': np.shape(data)[1]/np.shape(data)[0],
                   'cmap': mapInfo[img]['cmap'],
                   'FOV': self.FOV,
                   'Vmin': Vmin,
                   'Vmax': Vmax,
                   'title': title,
                   'cbar':mapInfo[img]['cbar'],
                   'scalebar': sbar,
                   'xlabel':'$x$ (' + self.xy_unit + ')',
                   'ylabel':'$y$ (' + self.xy_unit + ')',
                   'Scan_Width': self.imgDim['Scan_Width'],
                   'Scan_Height': self.imgDim['Scan_Height'],
                   'ptMarks': ptMarks,
                   'lnMarks': lnMarks                       
                  }
        return imgData
    

    # ---------------------------------- Generate/plot curve figure
    def get_line_info(self, mode=None):
        '''
        Get spectra for a selected point
        mode = "Integrated", "Points", "linescan"
        '''
        mode = self.default_line_mode if mode is None else mode
        Info = self.line_info[self.line_info.index==mode]
        lineInfo = {}
        for field in Info.keys():
            lineInfo[field] = Info[field][mode]
        return lineInfo
    
    # --------------------------------
    def find_peaks_spcRange(self):
        '''
        Find peaks from integrated spectra
        '''
        x = self.x[self.spcIndice[0]:self.spcIndice[1]]; 
        y = self.integrated[self.spcIndice[0]:self.spcIndice[1]]
        try:
            positions, _ = find_peaks(y, prominence = np.max(y)/self.pk_cri)
        except:
            print('no peaks can be found in the range: (' + str(self.spcIndice[0]) + ',' + str(self.spcIndice[1]) + ')')
            return None
        
        peaks = np.empty((0, 2))
        
        for pos in positions:
            peaks = np.append(peaks, np.array([[x[pos], y[pos]]]), axis = 0)
        return peaks
        
    def create_integrated(self):
        integrated = np.empty(len(self.x))
        integrated = self.cal_data[0, 0, :]
        for col in range(1, self.imgRes['Points_per_Line']):
            for row in range(1, self.imgRes['Lines_per_Image']):
                index = col + row*self.imgRes['Points_per_Line']
                integrated  = integrated + self.cal_data[row, col, :]
        self.points[0].I = np.average(integrated)
        return integrated/np.average(integrated)
    
    def create_xydata(self, linemode = None):
        '''
        lineMode: 'Points', 'Integrated', 'histogram' (for SEM), 'linescan'
        '''
        linemode = self.default_line_mode if linemode is None else linemode
        lineInfo = self.get_line_info(linemode)
        ylabel = lineInfo['ylabel']
        y_twin_label = None # twin axis for linescans: I/rI and pos/pos_diff
        peaks = None
            
        # Convert points to dict, for plotting (so we can save and reload the data)
        ptMarks = []
        for pt in self.points:
            ptMarks.append(vars(pt))
            
        if linemode == 'Integrated':
            x = self.x; 
            y = np.empty((1, len(self.x))) # keep the same data type for y
            y[0, :] = self.integrated
            
            peaks = self.find_peaks_spcRange()
            line_label = [ptMarks[0]]
            spcRange = ' [' + '{:.{prec}f}'.format(self.spcRange[0], prec=self.spcRange_decimal) + ',' + '{:.{prec}f}'.format(self.spcRange[-1], prec=self.spcRange_decimal) + '] ' + self.x_unit
            title = self.title + ': Integrated intensity over' + spcRange
        
        if linemode == 'histogram':
            hist, bin_edges = np.histogram(self.cal_data[:,:,0].ravel(), bins=255, range=(1,254))
            x = range(len(hist)) ; 
            y = np.empty((1, len(x))) # keep the same data type for y
            y[0, :] = hist
            
            line_label = [ptMarks[0]]
            title = self.title + ': Pixel histogram'
        
        if linemode == 'Points':               
            x = self.x #if self.datatype == 'spc_Img' else self.x[self.spcIndice[0]:self.spcIndice[1]]
            y = np.empty((len(self.points), len(self.x))) # leave the first point alone 
            #y[0, :] = self.integrated
            for idx, sp in enumerate(self.points[1:]):
                y[idx+1,:] = self.get_spectra(sp)
            # y = y if self.datatype == 'spc_Img' else y[:, self.spcIndice[0]:self.spcIndice[1]]
            
            line_label = ptMarks 
            title = self.title + ': Spectra at selected points '
        
        if linemode == 'linescan':
            x, y = self.linescan()
            line_label = [ptMarks[0]]
            title = self.lineData['title'][0] if self.datatype == 'spcImg' else self.lineData['title'][1]
            title = 'Line scan profile: ' + title
            ypl = 0 if self.datatype == 'spc_Img' else 2
            ylabel = lineInfo['ylabel'][ypl]
            y_twin_label = lineInfo['ylabel'][ypl + 1]
        
        lineInfo = self.get_line_info(linemode)
        lineData = {}
        lineData = {'title': title,
                    'x': x,
                   'y':y,
                    'linemode': linemode,
                    'aspect': 1.618,
                   'peaks': peaks,
                   'label': lineInfo['label'],
                    'line_label': line_label,
                    'I_th':self.I_th,
                    'xlabel':lineInfo['xlabel'],
                    'ylabel':ylabel,
                    'y_twin_label':y_twin_label,
                    'spcRange':self.spcRange,
                    'spcIndice':self.spcIndice,
                    'x_unit':self.x_unit,
                    'full_spc_x': [self.x[0], self.x[-1]],
                    'isPos_corrected': self.isPos_corrected,
                    'pk_ref': self.Ref_pos[0],
                    'isI_corrected': self.isI_corrected,
                    'I_ref_range': [self.Ref_I[0], self.Ref_I[1]],
                    'datatype': self.datatype
                    
                   }
          
        return lineData
    
    # ------------------
    def plot(self):
        '''
        plot the class data - overload by child class
        '''
        pass
    
    # ------------------------------------ spectra access/information     
    def get_spectra(self, point):
        '''
        Overload by child class
        '''
        pass
    #-------------------
    def browse_rawdata(self, spc, data = 'raw'):
        '''
        Show spectrum image for a series of wn/wl: Overload by child class
        '''
        pass
    #-------------------
    
    # --------------------------- update/process spectra 
    def initialise_points(self):
        '''
        Add default points at the centre, which hosts the integrated intensity/pos over the full range of the spectra
        '''
        self.points = []
        self.points = [point(self.imgDim['Scan_Width']/2, self.imgDim['Scan_Height']/2, '')]
        self.nPoints = 1
        return self.points
    
    # --------------------------
    def set_point(self, ptIndex, isplot = True, **kwargs):
        '''
        Revise individual points on the map - overload figProc
        '''
        if ptIndex < 0 or ptIndex >= len(self.points) or len(kwargs)==0:
            print('No point find.')
            return None
        for field in list(kwargs.keys()):
            if field in list(vars(self.points[ptIndex]).keys()):
                vars(self.points[ptIndex])[field] = kwargs[field]
            else:
                print('The point does not have the field: ' + field)
        self.update_points()
        if isplot:
            self.plot()
            
    # ---------------------------
    def update_points(self):
        '''
        Update all points when data has been changed (cal/restore)
        '''
        pass
    
    # -------------------------
    def cal_spec(self, mode = 'pos', ref = None): 
        '''
        Calibrate spectra
        '''
        pass
    
    # -------------------------
    def restore_rawdata(self):
        '''
        restore the rawdata, i.e. discard the spectra calibration
        '''
        self.cal_data = self.rawdata.copy()
        self.isPos_corrected = False
        self.isI_corrected = False
        
    # ------------------------------------ Coordinate conversion: col/row vs. x, y 
    def rc_to_xy(self, row, col):
        """
        Convert (row, col) to physical coordinates
        """
        x = self.FOV[0]+float(col)*self.imgDim['Scan_Width']/self.imgRes['Points_per_Line'] #sp.y - col/x; sp.x - row/y
        y = self.imgDim['Scan_Height']+self.FOV[2]-float(row)*self.imgDim['Scan_Height']/self.imgRes['Lines_per_Image']
        return x, y
    # -------------------------
    def xy_to_rc(self, x, y):
        col = (x - self.FOV[0])*self.imgRes['Points_per_Line']/self.imgDim['Scan_Width']
        row = (self.imgDim['Scan_Height']+ self.FOV[2] - y)*self.imgRes['Lines_per_Image']/self.imgDim['Scan_Height']
        return int(row), int(col)
    
    # ------------------------------------- Image selection        
    def select_points(self, mode = None):
        '''
        Select points from the image
        mode = 'I', 'rI' ...
        '''
        # set default value
        mode = self.default_img_mode if mode is None else mode
        
        # Clear the existing points
        self.nPoints = 1
        tmpPoints = self.points
        self.points = [self.points[0]]
        
        # Read in the map data
        mapInfo = self.get_map_info()[mode]
        image = self.data[:,:, mapInfo['loc']]
        
        # Scale it in [0,1]
        imgRange = np.nanmax(image)-np.nanmin(image)
        img = (image-np.nanmin(image))/imgRange if imgRange != 0 else 0

        def draw_circle(event, x,y, flags, param):
            global mouseX, mouseY
            if event ==cv2.EVENT_LBUTTONDOWN:
                imgSize = len(self.data[:,:, mapInfo['loc']])
                r = int(imgSize/50)+1 if imgSize>50 else 2
                cv2.circle(img, (x,y), r, (255,255,255), 2)
                Mark = chr(ord('@')+ self.nPoints)
                self.nPoints += 1
                cv2.putText(img, Mark, (x+r+1, y-r-1), cv2.FONT_HERSHEY_SIMPLEX, r/8, (255,255,255),2)
                col, row = x, y # x-col; y-row
                sx, sy = self.rc_to_xy(row, col)
                self.points = np.append(self.points, point(sx, sy, Mark)) # the point is described as [row, col]
        
        window = self.title + '_' + mode
        cv2.namedWindow(window, cv2.WINDOW_NORMAL)
        cv2.setMouseCallback(window, draw_circle)

        while(1):
            cv2.imshow(window, img)
            k = cv2.waitKey(20) & 0xFF
            if k== 27:
                print('Action cancelled. No change made.')
                self.points = tmpPoints
                self.nPoints = len(self.points)
                cv2.destroyAllWindows()
                cv2.waitKey(1)
                return None
            elif k == ord('s'):
                cv2.destroyAllWindows()
                cv2.waitKey(1)
                break
            elif k == ord('d'):
                img = (image-np.nanmin(image))/imgRange if imgRange != 0 else 0
                self.points = []
                self.nPoints = 0
    
    # -----------------------------
    def select_region(self, mode = None, sPoint = None, size = None):
        '''
        extract_rectangular region
        '''
        # set default value
        mode = self.default_img_mode if mode is None else mode
                
        mapInfo = self.get_map_info()[mode]
        map_data = self.data[:,:, mapInfo['loc']]
        map_title = mapInfo['title']
        
        # scale image to [0, 1]
        imgRange = np.nanmax(map_data)-np.nanmin(map_data)
        img = (map_data-np.nanmin(map_data))/imgRange if imgRange != 0 else 0
        
        window = self.title + '_' + mode
        
        
        newImgDim = {'Scan_Width': self.imgDim['Scan_Width']/2, 'Scan_Height': self.imgDim['Scan_Height']/2} if size is None else {'Scan_Width': size[0], 'Scan_Height': size[1]}
        self.isSelected = False
        
        
        def calculate_selected(newImgDim, sx, sy): 
            # param[0] - marked; param[1] - parent
            sr, sc = self.xy_to_rc(sx, sy)
            ex, ey = sx + newImgDim['Scan_Width'], sy - newImgDim['Scan_Height']
            er, ec = self.xy_to_rc(ex, ey)
            if er > self.imgRes['Lines_per_Image']-1:
                sr = self.imgRes['Lines_per_Image'] -1 - (er-sr)
                er = self.imgRes['Lines_per_Image'] -1
            if ec > self.imgRes['Points_per_Line']-1: # ec - end-colume - x/horizontal
                sc = self.imgRes['Points_per_Line'] -1 - (ec-sc)
                ec = self.imgRes['Points_per_Line'] -1 
            return [sr, sc, er, ec]
        
        self.cldwin = calculate_selected(newImgDim, sPoint[0], sPoint[1]) if sPoint is not None else calculate_selected(newImgDim, 0, 0)
        
        def draw_rectangle(event, x,y, flags, param):
        
            if event ==cv2.EVENT_LBUTTONDOWN and self.isSelected is False:
                
                imgSize = len(map_data)
                r = int(imgSize/80)+1 if imgSize>80 else 2
        
                sr, sc = y, x # x - col; y - row
                sx, sy = self.rc_to_xy(sr, sc) # use original imgSlice to calculate the coordinates
                sr, sc, er, ec = calculate_selected(param[0], sx, sy)
                self.cldwin = [sr, sc, er, ec]
                cv2.rectangle(img, (sc, sr), (ec, er), (255,255,255), thickness=r)
                self.isSelected = True
        
        if sPoint is None:
            cv2.namedWindow(window, cv2.WINDOW_NORMAL)
            cv2.setMouseCallback(window, draw_rectangle, [newImgDim])

            while(1):
                cv2.imshow(window, img)
                k = cv2.waitKey(20) & 0xFF
                if k== 27:
                    cv2.destroyAllWindows()
                    cv2.waitKey(1)
                    print('Action cancelled - no region selected.')
                    return None
                elif k == ord('s'):
                    cv2.destroyAllWindows()
                    cv2.waitKey(1)
                    break
                elif k == ord('d'):
                    img  = (map_data-np.nanmin(map_data))/imgRange if imgRange != 0 else 0
                    self.isSelected =False
        
        sr, sc, er, ec = self.cldwin 
        
        ext = deepcopy(self)
        ext.imgDim = newImgDim
        ext.imgRes = {'Points_per_Line':ec-sc+1, 'Lines_per_Image':er-sr+1} # row - y
        ext.FOV = [0, ext.imgDim['Scan_Width'], 0, ext.imgDim['Scan_Height']]
        ext.points =  ext.initialise_points() # Add default points 
        return ext
    
    # ----------------------
    def linescan(self):     
        '''
        Generate linescan data
        '''
        # Check if there are two points on the map
        n_map_Points = len(self.points)
        if n_map_Points <2:
            print('We need at least two points. The points selected are:')
            display(self.point_list)
            return [], []
        
        # Get teh start/end points - they are in physical coordinates, convert them in pixels, row/col
        start = self.points[1]; end = self.points[-1]
        
        # The number of data points in x/y 
        s_row, s_col = self.xy_to_rc(start.x, start.y)
        e_row, e_col = self.xy_to_rc(end.x, end.y)
        
        # Calculate the total number of pixels along row(y/vertical) and col(x/horizontal) directions 
        n_row = abs(e_row - s_row);  
        n_col = abs(e_col - s_col);
        
        n_pts_in_line = max(n_col, n_row) +1
        # Moving directions: >0 (right/col-larger, down/row-larger); <0 (left, up)
        # Note the two coordinates y/row directions are opposite
        sign_row = 1 if e_row > s_row else -1
        sign_col = 1 if e_col > s_col else -1
        
        # The col, row sequences sampled from the original map - np.arange(3,7) = [3, 4, 5, 6]
        # The length of the arrays below should be n_row, n_col, i.e. including both terminals
        d_row = e_row-s_row; d_col = e_col-s_col
        col_sampled = np.arange(s_col, e_col + np.sign(d_col), step = np.sign(d_col)) if d_col != 0 else np.ones(n_pts_in_line)*s_col
        row_sampled = np.arange(s_row, e_row + np.sign(d_row), step = np.sign(d_row)) if d_row != 0 else np.ones(n_pts_in_line)*s_row
        step_row = float(e_row-s_row)/(n_pts_in_line - 1)
        step_col = float(e_col-s_col)/(n_pts_in_line - 1)
        row_extra = np.arange(s_row, e_row + step_row, step = step_row) if d_row != 0 else np.ones(n_pts_in_line)*s_row
        col_extra = np.arange(s_col, e_col + step_col, step = step_col) if d_col != 0 else np.ones(n_pts_in_line)*s_col

        n_pts_in_line = min(n_pts_in_line, len(row_extra), len(col_extra)) # ensure the same dimension
        dx = np.sqrt((end.x - start.x)**2 + (end.y - start.y)**2)/(n_pts_in_line -1)
        line_x = range(n_pts_in_line)*dx      
        
        weight_row = np.ones(n_pts_in_line) 
        weight_col = np.ones(n_pts_in_line)

        for idx, r in enumerate(row_extra[0:n_pts_in_line]):
            w = r - row_sampled[np.abs(row_sampled - r).argmin()]
            weight_row[idx] = (1 - w) if w<=0.5 and w >=0 else -w
        
        for idx, c in enumerate(col_extra[0:n_pts_in_line]):
            w =  c - col_sampled[np.abs(col_sampled - c).argmin()]
            weight_col[idx] = (1 - w) if w<=0.5 and w >=0 else -w
        
        if self.datatype == 'spc_Img':
            modes = ['I', 'pos']
        elif self.datatype == 'spc_Diff':
            modes = ['rI', 'pos_diff']
        elif self.datatype == 'sem_Img':
            modes = ['sem_I']
        
        line_profile = np.ones((len(modes), n_pts_in_line)) # the number of modes in profiles
        
        for idx, mode in enumerate(modes):
            pos_row = np.array([0, 1])
            pos_col = np.array([0, 1])
            mapInfo = self.get_map_info()[mode]
            for i in range(n_pts_in_line):
                row_pt1 = int(row_sampled[pos_row[0]]); row_pt2 = int(row_sampled[pos_row[1]])
                col_pt1 = int(col_sampled[pos_col[0]]); col_pt2 = int(col_sampled[pos_col[1]])
                w = weight_row[i] if n_col > n_row else weight_col[i]
                line_profile[idx, i] = w*self.data[row_pt1, col_pt1, mapInfo['loc']] + (1-w)*self.data[row_pt2, col_pt2, mapInfo['loc']]
                if weight_row[i] == 1 and i >0:
                    pos_row = pos_row + 1
                if weight_col[i] == 1 and i >0:
                    pos_col = pos_col + 1
            line_profile[idx, -1] = self.data[row_sampled[-1], col_sampled[-1], mapInfo['loc']]
        
        return line_x, line_profile