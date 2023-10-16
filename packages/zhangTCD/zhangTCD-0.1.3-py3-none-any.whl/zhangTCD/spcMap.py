import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrow
import matplotlib.font_manager as fm
import matplotlib.patheffects as PathEffects
from mpl_toolkits.axes_grid1 import make_axes_locatable
from mpl_toolkits.axes_grid1.anchored_artists import AnchoredSizeBar
import seaborn as sns
import cv2 

import io
from contextlib import redirect_stdout
from spc import File
from copy import deepcopy
import pandas as pd

import numpy as np


from .hyperImg import hyperImg
from .figProc import point, scalebar

class spcMap(hyperImg):
    # Image parameters
       
    def __init__(self, rawdatafile):
        
        # Define a list of mapping modes: intensity, peak position, etc.
        self.title = 'Overview'
        self.source = rawdatafile
        self.experiment = 'specMap'
        self.datatype = 'spc_Img' # 'spc_Diff', 'sem_Img'
        
        # image resolution read from tif file
        self.load_data()
        self.x = self.spc.x
        
        # Filed of view, Image resolution, image dimension
        self.Points_per_Line = int(self.info['Points_per_Line']);
        self.Lines_per_Image = int(self.info['Lines_per_Image']);
        self.Scan_Width = float(self.info['Scan_Width']);
        self.Scan_Height = float(self.info['Scan_Height']);
        self.Scan_Origin_X = float(self.info['Scan_Origin_X']);
        self.Scan_Origin_Y = float(self.info['Scan_Origin_Y']);
        self.FOV = [self.Scan_Origin_X, self.Scan_Origin_X + self.Scan_Width, self.Scan_Origin_Y, self.Scan_Origin_Y + self.Scan_Height] # [left, right, bottom, top]
        self.imgRes = {'Points_per_Line':self.Points_per_Line, 'Lines_per_Image':self.Lines_per_Image} # lines_per_Image: row number - vertical/y; Points_per_Line:cols
        self.imgDim = {'Scan_Width':self.Scan_Width, 'Scan_Height':self.Scan_Height}
        
        # initiate scalebar
        self.points = self.initialise_points()
        self.scalebar = self.create_default_scalebar()
        
        # Convert the raw data to the data cube structure and create a copy for storing calibrated data cube
        raw_shape = (self.imgRes['Lines_per_Image'], self.imgRes['Points_per_Line'], len(self.spc.x))
        self.rawdata = np.empty(raw_shape)

        for col in range(self.imgRes['Points_per_Line']):
            for row in range(self.imgRes['Lines_per_Image']):
                index = col + row*self.imgRes['Points_per_Line']
                self.rawdata[row, col, :] = self.spc.sub[index].y

        # Spectrum calibration: intensity and peak position - cal_data
        self.cal_data = self.rawdata.copy()
        self.isPos_corrected = False
        self.isI_corrected = False
        
        # Setup spectra range/ background range
        self.spcRange = [self.x[0], self.x[-1]]
        self.bkRange = self.spcRange
        self.spcIndice = self.spcRange_to_spcIndex(self.spcRange)
        self.bkIndice = self.spcRange_to_spcIndex(self.bkRange)
        
        # Set up image modes
        self.setup_maps()
        self.default_img_mode = 'I'
        self.img_modes = ['I', 'rI', 'pos', 'pos_diff','rpk_I', 'pk_I', 'ref_pos', 'ref_offset', 'ref_I_avg']
        
        # set up line modes and calculate integrated 
        self.setup_lines()
        self.pk_cri = 100
        self.integrated = self.create_integrated()
        
        # create points - positions on map
        self.point_list = None
        self.points = self.initialise_points()
        
        # self.data stores the map information
        shape = (self.imgRes['Lines_per_Image'], self.imgRes['Points_per_Line'], len(self.img_modes))
        self.data = np.zeros(shape) # map datas
        
        # Threshold for the peak in the range
        self.I_th = 0
        self.max_I = np.average(self.cal_data[0,0,:]) # use (0,0) as the first attempt for the max_I
        #self.max_pk_I = 0
        self.process_map()
        self.filter_I_cri()
        
        # Create filename for save()
        self.filename = self.create_filename()
        
    
    ## ---------------------------------------------- load experimental data and information
    
    def load_data(self):
        # Import experimental info
        self.info= {}
        try:
            # Import info file
            with open(self.source + '.csv', 'r', encoding='utf-8-sig') as infile:
                lines = infile.readlines()
            for line in lines:
                line_info = line.split(":,")
                line_info[0] = line_info[0].split(" [")[0]
                line_info[0] = line_info[0].replace(' ', '_')
                line_info[1] = line_info[1].replace('\n', '')
                self.info[line_info[0]] = line_info[1]
        except:
            print('I cannot find the ' + self.source + '.csv file (or wrong format: it need to be utf-8-sig coded) ' )
            return None
        # Read data
        try:
            # Import spc file
            with redirect_stdout(io.StringIO()) as f:
                self.spc = File(self.source + '.spc');
        except:
            print('I cannot find the ' + self.source + '.spc file')
            return None
    
    # -------------------------------------------------- get/show information
    def get_spectra(self, point):
        row, col = self.xy_to_rc(point.x, point.y)
        spectrum = self.cal_data[row, col, :]
        return spectrum
    
    # -------------------- Convert the spec positions (xRange) into corresponding indice of the f.y[index] array
    def spcRange_to_spcIndex(self, spcRange):
        s = np.abs(self.x - spcRange[0]).argmin()
        e = np.abs(self.x - spcRange[1]).argmin()
        return [s, e]
    
    # ----------------------------------------- spectra operation
    # Calibrate peak intenstiy and position
    def cal_spec(self, mode = 'I', ref = None):        
        # Check reference peak provided
        if ref is None and mode == 'pos' :
            print ('you need to provide a peak ref for position calibration.')
            return None
        if ref is not None:
            if (ref[0] + ref[1]) > self.x[-1] or (ref[0]-ref[1]) < self.x[0]:
                print('The reference position (' + str(ref[0]) + ') is outside of the spectra range: [' + str(self.x[0]) + ', ' + str(self.x[-1]))
                return None
            
        # Generate offset holders
        self.offset_pk = np.empty([self.imgRes['Lines_per_Image'], self.imgRes['Points_per_Line']], np.float32)
        self.refI_pk = np.empty([self.imgRes['Lines_per_Image'], self.imgRes['Points_per_Line']], np.float32) # peak intensity
        self.refI_avg = np.empty([self.imgRes['Lines_per_Image'], self.imgRes['Points_per_Line']], np.float32) 
            
        # Convert peak range to indice sx, ex 
        pk_range = self.spcRange if ref is None else [ref[0]-ref[1], ref[0]+ref[1]]
        
        start = np.abs(self.x - pk_range[0]).argmin()
        end = np.abs(self.x - pk_range[1]).argmin()
        sx, ex = [start, end] # sx, ex: the indice for the reference peak range
        
        loc = {}
        for field in ['I', 'pos', 'pk_I', 'ref_I_avg', 'ref_offset', 'ref_pos']:
            mapInfo = self.get_map_info()[field]
            loc[field] = mapInfo['loc']
                                 
        # Generate intensity, peak maps
        for row in range(self.imgRes['Lines_per_Image']):
            for col in range(self.imgRes['Points_per_Line']):
                index = col + row*self.imgRes['Points_per_Line']
                y =  self.cal_data[row, col, :].astype('float')
                
                # the maximum position 
                self.data[row, col, loc['pk_I']] = float(np.max(y[sx:ex])) # ref_pk
                
                refI_avg = np.average(y[sx:ex])
                self.data[row, col, loc['ref_I_avg']] = refI_avg #I_avg
                
                if mode == 'I':
                    y = y/refI_avg # use the average peak to scale
                    self.cal_data[row, col, :] = y
                    self.isI_corrected = True
                    self.Ref_I = ref
                if mode == 'pos':
                    self.Ref_pos = ref
                    pk_pos = self.x[y[sx:ex].argmax()+sx]
                    self.data[row, col, loc['ref_pos']] = pk_pos
                    pk_shift = pk_pos - ref[0]
                    self.data[row, col, loc['ref_offset']] = pk_shift #offset
                    pk_shift_indice = y[sx:ex].argmax() - ref[1]
                    self.cal_data[row, col, :] = np.roll(y, - pk_shift_indice)
                    self.isPos_corrected = True
        self.process_map()
    
    # Apply filters to the data
    def filter_I_cri(self, I_th=None):
        '''
        Apply filters to the calculated maps(I, pos, pk_I)
        '''
        self.I_th = self.I_th if I_th is None else I_th
        self.process_map()
        loc = {}
        for field in ['I', 'pos', 'pk_I']:
            mapInfo = self.get_map_info()[field]
            loc[field] = mapInfo['loc']
            
        for col in range(self.imgRes['Points_per_Line']):
            for row in range(self.imgRes['Lines_per_Image']):
                index = col + row*self.imgRes['Points_per_Line']
                if self.data[row, col, loc['I']] < self.I_th:
                    self.data[row, col, loc['I']] = np.nan
                    self.data[row, col, loc['pos']] = np.nan
                    self.data[row, col, loc['pk_I']] =np.nan

        self.integrated = self.create_integrated()
        self.update_points()
        self.filename = self.create_filename()
        self.plot()
    
    # Apply filter and generate the data maps
    def process_map(self):
        '''
        Calculate I, pos, pk_I for individual points on the map
        '''
        loc = {}
        for field in ['I', 'pos', 'pk_I']:
            mapInfo = self.get_map_info()[field]
            loc[field] = mapInfo['loc']
        
        for col in range(self.imgRes['Points_per_Line']):
            for row in range(self.imgRes['Lines_per_Image']):
                index = col + row*self.imgRes['Points_per_Line']
                spec = self.cal_data[row, col, self.spcIndice[0]:self.spcIndice[1]].copy()
                
                # I is the average intensity over the spc range - normalised
                I = np.average(spec)
                self.data[row, col, loc['I']] = I # if I > self.I_th else np.nan # Integrated intensity
                # pos is the position of the peak - where the spc shows a maximum in the range
                self.data[row, col, loc['pos']] = self.x[spec.argmax() + self.spcIndice[0]] #if I > I_th else np.nan # Peak position, largest peak
                # pkI is the maximum value across the spc range
                self.data[row, col, loc['pk_I']] = np.max(spec) #if I > I_th else np.nan 
        
        self.max_I = np.max(self.data[:, :, loc['I']])
        #self.max_pk_I = np.max(self.data[:, :, loc['pk_I']])
        
        for col in range(self.imgRes['Points_per_Line']):
            for row in range(self.imgRes['Lines_per_Image']):
                self.data[row, col, loc['I']] = self.data[row, col, loc['I']]/self.max_I
                #self.data[row, col, loc['pk_I']] = self.data[row, col, loc['pk_I']]/self.max_pk_I
    
        # self.data = np.ma.masked_where(self.data == -1, self.data) - it can be masked, but this cause issues when put circles to data point in the plot
    
    # update selected points - I, etc; fomulate the dataframe for the points
    def update_points(self):
        fields = {}
        if self.datatype == 'spc_Img':
            modes = ['I', 'pos', 'pk_I', 'ref_pos', 'ref_offset', 'ref_I_avg']
            fields = {'label':np.empty(0), 'mode':np.empty(0), 'scale':np.empty(0),'color' :np.empty(0),
                      '(x,y)':np.empty(0),'(row,col)':np.empty(0), 'spc range': np.empty(0), 'I':np.empty(0), 'pk_Pos':np.empty(0), 'pk_Height':np.empty(0),
                      'Offset':np.empty(0), 'refI_max': np.empty(0), 'refI_avg':np.empty(0)}
        elif self.datatype == 'spc_Diff':
            modes = ['rI', 'pos_diff', 'I', 'pos', 'rpk_I', 'pk_I']
            fields = {'label':np.empty(0), 'mode':np.empty(0), 'scale':np.empty(0),'color' :np.empty(0),
                           '(x,y)':np.empty(0),'(row,col)':np.empty(0), 'spc range': np.empty(0), 
                      'I ratio':np.empty(0), 'pk diff':np.empty(0), 'IA_avg':np.empty(0), 'Pos A':np.empty(0), 'pk_I':np.empty(0),}
        for sp in self.points[1:]:
            row, col = self.xy_to_rc(sp.x, sp.y)
            values = [sp.label,
                      sp.mode,
                      sp.scale,
                      sp.color,
                      '('+"{:.2f}".format(sp.x) + ', ' + "{:.2f}".format(sp.y) + ')',
                      '('+"{:.0f}".format(row) + ', ' + "{:.0f}".format(col) + ')',
                      '('+"{:.2f}".format(self.spcRange[0]) + ', ' + "{:.2f}".format(self.spcRange[1]) + ')']
        
            for mode in modes:
                mapInfo = self.get_map_info()[mode]
                vars(sp)[mode] = self.data[row,col, mapInfo['loc']]
                values.append(vars(sp)[mode])
            
            for idx, item in enumerate(fields):
                fields[item] = np.append(fields[item], values[idx])
        
        self.point_list = pd.DataFrame(fields)
        self.point_list.index = self.point_list.index + 1
        
        return self.point_list

        
    # ------------- plot the data
    def plot(self, mode = 'Integrated'):
        if len(self.points) > 1:
            display(self.point_list)
        
        fig, ax = plt.subplots(1, 3, figsize = self.plotSize, gridspec_kw=self.plotRatio, constrained_layout=True)
        
        self.fig_label_num = 0
        self.imgData = self.create_image(mode)
        mapModes = ['rI', 'pos_diff'] if self.datatype == 'spc_Diff' else ['I', 'pos']
        for idx, imgMode in enumerate(mapModes): # Plot I and pos
            self.plot_image(ax[idx], imgMode)
            
        self.lineData = self.create_xydata(mode)
        self.plot_xydata(ax[2])
        self.fig = fig

    def browse_rawdata(self, spc, data = 'raw', fixMapRange = False):
        '''
        spc = [s1, s2, ...] - map using a given wn/wl (sn)
        data = 'raw' or 'cal'
        fixMapRange: True (all maps use the same colormap)
        '''
        N = len(spc)
        axs = np.ones(N)
        
        original_img_modes = self.img_modes
        self.img_modes = ['browse', 'pos', 'I']
        
        self.set_scalebar(isplot = False, length = int(self.imgDim['Scan_Width']/5), 
                          height = self.imgDim['Scan_Height']/30, 
                          unit = self.xy_unit, location = 'lower left', color = 'white')
        
        fig, axs = plt.subplots(1, N, figsize = self.plotSize, constrained_layout=True)
        title = 'Mapping: raw data' if data == 'raw' else 'Mapping: calibrated data'
        fig.suptitle(title, fontsize = 16)
        
        # Apply the same range for plotting
        if fixMapRange:
            spectra = self.rawdata[:,:,:] if data == 'raw' else self.cal_data[:,:,:]
            Vmin = np.min(spectra); Vmax = np.max(spectra)
        else:
            Vmin = None; Vmax = None
            
        self.fig_label_num = 0
        for idx, ax in enumerate(axs):
            self.fig_label_num = idx
            self.imgData = self.create_image(imgMode = data, spcPos = spc[idx], Vmin = Vmin, Vmax = Vmax)
            self.plot_image(ax, 'browse')
        
        self.points = self.initialise_points()
        self.img_modes = original_img_modes
        
    # ------------- Select spc_range/points/region
    def slect_spc_range(self, title = None, spcRange = None, bkRange = None, I_th = None):
        '''
        Generate individual peaks - specify the range of the peak
        '''
        self.I_th = self.I_th if I_th is None else I_th
        
        selected = deepcopy(self)
        
        # Update spcRange and spcIndice
        selected.spcRange = self.spcRange if spcRange is None else spcRange
        selected.bkRange = selected.bkRange if bkRange is None else bkRange
        selected.spcIndice = selected.spcRange_to_spcIndex(selected.spcRange)
        selected.bkIndice = selected.spcRange_to_spcIndex(selected.bkRange)
        
        # update title/filename
        selected.title = self.title if title is None else title
        selected.filename = selected.create_filename()
        selected.peaks = selected.find_peaks_spcRange()
        selected.process_map()
        selected.filter_I_cri()        
        return selected
    
    def select_points(self, mode = None):
        super().select_points(mode)
        
        self.update_points()
        self.plot('Points')
        
    
    def select_region(self, mode = None, sPoint = None, size = None):
        ext = super().select_region(mode = mode, sPoint = None, size = None)
        if ext is None:
            return

        raw_shape = (ext.imgRes['Lines_per_Image'], ext.imgRes['Points_per_Line'], len(ext.spc.x))
        ext.rawdata = np.empty(raw_shape)
        shape = (ext.imgRes['Lines_per_Image'], ext.imgRes['Points_per_Line'], len(ext.img_modes))
        ext.data = np.empty(shape)
        
        for col in range(self.cldwin[1], self.cldwin[3]):
            for row in range(self.cldwin[0], self.cldwin[2]):
                index = col + row*self.imgRes['Points_per_Line']
                ext.cal_data[row-self.cldwin[0], col-self.cldwin[1], :] = self.cal_data[row, col, :]
                ext.rawdata[row-self.cldwin[0], col-self.cldwin[1], :] = self.rawdata[row, col, :]
                ext.data[row-self.cldwin[0], col-self.cldwin[1], :] = self.data[row, col, :]
        
        ext.process_map()
        ext.filter_I_cri()
        ext.plot('Integrated')
        return ext
    
     # adding two objects
    def __sub__(self, pkB):
        diff = deepcopy(self)
        
        FOV_A = np.array(self.FOV); FOV_B = np.array(pkB.FOV)
        
        if np.array_equiv(FOV_A, FOV_B):
            print('The two maps have the same dimensions.')
        else:
            print('The two maps do not have the same dimensions.')
            return None
        
        loc= {}
        for field in ['rI', 'I', 'pos', 'pos_diff', 'pk_I', 'rpk_I']:
            mapInfo = self.get_map_info()[field]
            loc[field]= mapInfo['loc']
            
        # put peak with larger position first
        diff.spcRange[0] = min(self.spcRange[0], pkB.spcRange[0])
        diff.spcRange[1] = max(self.spcRange[1], pkB.spcRange[1])
        diff.spcIndice = diff.spcRange_to_spcIndex(diff.spcRange)
        diff.bkIndice = diff.spcRange_to_spcIndex(diff.bkRange)

        diff.title = self.title + ' vs. ' + pkB.title
        diff.filename = diff.create_filename()
        
        for col in range(self.imgRes['Points_per_Line']):
            for row in range(self.imgRes['Lines_per_Image']):
                if np.isnan(self.data[row, col, loc['I']]) or np.isnan(pkB.data[row, col, loc['I']]):
                    diff.data[row, col, loc['rI']] = np.nan
                    diff.data[row, col, loc['rpk_I']] = np.nan
                    diff.data[row, col, loc['pos_diff']] = np.nan
                    diff.data[row, col, loc['I']] = np.nan
                    diff.data[row, col, loc['pos']] = np.nan
                else:
                    diff.data[row, col, loc['rI']] = self.data[row, col, loc['I']]/pkB.data[row, col, loc['I']]
                    diff.data[row, col, loc['rpk_I']] = self.data[row, col, loc['pk_I']]/pkB.data[row, col, loc['pk_I']]
                    diff.data[row, col, loc['pos_diff']] = self.data[row, col, loc['pos']]- pkB.data[row, col, loc['pos']]
                    diff.data[row, col, loc['I']] = self.data[row, col, loc['I']]
                    diff.data[row, col, loc['pos']] = self.data[row, col, loc['pos']]
                    diff.data[row, col, loc['pk_I']] = self.data[row, col, loc['pk_I']]
                
        diff.title = self.title + '-' + pkB.title
        diff.datatype = 'spc_Diff'
        diff.peaks = diff.find_peaks_spcRange()
        diff.default_img_mode = 'rI'
        diff.img_modes = ['rI', 'pos_diff', 'I', 'pos', 'rpk_I', 'pk_I']
        diff.points = diff.initialise_points()
        diff.update_points()
        diff.default_line_mode = 'Points'
        
        diff.plot('Integrated')
        return diff