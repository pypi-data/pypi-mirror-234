import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrow
import matplotlib.font_manager as fm
import matplotlib.patheffects as PathEffects
from matplotlib import gridspec

from mpl_toolkits.axes_grid1 import make_axes_locatable
from mpl_toolkits.axes_grid1.anchored_artists import AnchoredSizeBar
import seaborn as sns
import cv2 

import numpy as np

from copy import deepcopy
import pickle
import pandas as pd

class point():
    x = 0;  y = 0 # x, y : physical coordinates
    scale = 0.02
    label =''
    mode = 'circle'
    coor = ''
    I = 0
    pos = 0
    rI = 0
    pos_diff = 0
    pk_I =0
    ref_pos=0
    ref_offset=0
    ref_I_avg=0

    def __init__(self, x, y, label, mode= 'circle', scale = 0.02, color = 'white'):
        self.x = x;
        self.y = y;
        self.coor = '(' + str(x) + ', ' + str(y) + ')'
        self.scale = scale
        self.mode = mode
        self.label = label;
        self.color = color

class scalebar():
    length = 0; height = 0; unit = ''; location = ''; color = '';
    def __init__(self, length = 0, height = 0, unit = '', location = 'lower left', color = 'white'):
        self.length = length
        self.height = height
        self.unit = unit
        self.location = location
        self.color = color   
        
class figProc():
    filename = None
    imgData = None
    lineData = None
    
    #data = {}
    # figure layout
    fig_height = 20
    fig_width = 20
    
    plotSize = (14, 3.5)
    plotRatio ={'width_ratios': [1, 1, 1.5]} 
    
    title_fontsize = 10
    isSubFigTitle = True
    label_pos = {'ha':'center', 'va': 'bottom'}
    spcRange_decimal = 0 # decimal places to show the range
    
    # -------------- xy-plot 
    palette = "crest" # line colors
    # line labels e.g. spectra from individual points on map
    line_label_fontsize = 12
    line_label_pos = {'ha':'center', 'va': 'bottom'}
    # Mark peaks in integrated view
    peak_label_fontsize = 12
    peak_label_yshift = 1.05
    peak_label_pos = {'ha':'center', 'va': 'bottom'}
    peak_label_fontsize = 12
    peak_label_yshift = 0.05
    peak_label_alpha = 0.8
    # x, y axis labels
    x_label = 'x'
    y_label = 'y'
    xylabel_fontsize = 12
    # spcRange shaded
    isRangeMarked = True
    ref_alpha = 0.1
    
    
    # labeling subplots, a, b etc.
    isSubFigLabel = True # Turn this off if there is only one figure
    fig_label_x_offset = -0.05 # the relative position of a, b, c for subplot
    fig_label_y_offset = 1.05
    fig_label_size = 12
    fig_label_weight = 'bold'
    fig_label_num = 0
    
    # image formate
    scalebar_fontsize = 16
    
    
    def __init__(self, file = None):
        if file is not None:
            try:
                with open(file, 'rb') as handle:
                    source = pickle.loads(handle.read())
            except:
                print('I cannot find the file')
                return None

            self.imgData = source['imgData']
            self.lineData = source['lineData']
            
        parameters = ['filename', 'fig_width']
        category = ['data storage', 'fig layout']
        values = [self.filename, self.fig_width]
        comments = ['The file name that will store the data/figure when you save the data, fig.save()',
                'The number of rows of the figure grids - subfigures are put on rowxcol meshes']
        notes = {'parameter': parameters,
                'category': category,
                 'value': values,
                'comment':comments}
        self.notes = pd.DataFrame(notes)
        pd.options.display.max_colwidth = 100
            
    # -------------- create figures
    def setup(self, **kwargs):
        for field in list(kwargs.keys()):
            if field in list(vars(figProc).keys()):
                vars(self)[field] = kwargs[field]
            else:
                print('I cannot find the parameter: ' + field)
                print('The parameters you can change:')
                display(self.notes)
            fig = plt.figure()
            
            fig.set_figheight(self.fig_height)
            fig.set_figwidth(self.fig_width)
    
                
    # ----------------------- data operations
    
    def __add__(self, b):
        '''
        a + b: merge line curves 
        '''
        # if self.lineData['label'] != b.lineData['label']:
        #     print("The two sets need have the same type, but the first is " + self.lineData['label'] + " while the second " + b.lineData['label'])
        #     print("I did not merge these, but the result is set to the first set.")
        #     return self
        
        result = deepcopy(self)
        
        nData_sets = np.shape(self.lineData['y'])[0] + np.shape(b.lineData['y'])[0]
        y = np.empty((nData_sets, len(self.lineData['x'])))
        
        for idx, data in enumerate(self.lineData['y']):
            y[idx, :] = data
        
        for idx, data in enumerate(b.lineData['y']):
            y[idx+np.shape(self.lineData['y'])[0], :] = data
        
        result.lineData['label'] = 'merged'
        
        result.lineData['y'] = y
        
        # line label
        self.lineData['line_label'][0]['label'] = 'A'
        b.lineData['line_label'][0]['label'] = 'B'
        result.lineData['line_label'] = self.lineData['line_label'] + b.lineData['line_label']
        
        # line - x range
        result.lineData['spcRange'] = [min(result.lineData['spcRange'][0],b.lineData['spcRange'][0] ), max( result.lineData['spcRange'][1],b.lineData['spcRange'][1])]
        result.lineData['spcIndice'] = [min(result.lineData['spcIndice'][0],b.lineData['spcIndice'][0] ), max( result.lineData['spcIndice'][1],b.lineData['spcIndice'][1])]

        #result.lineData['peaks'] =  np.concatenate((self.lineData['peaks'], b.lineData['peaks']), axis=0)
        return result
    #---------------------------
    
    def __lt__(self, b):
        '''
        a<b: copy b data into a
        '''
        self.imgData = b.imgData
        self.lineData = b.lineData
    
    # -------------------------------- Image operation 
    def set_scalebar(self, isplot = True, **kwargs): #length, height, unit, position, color, isplot = True):
        '''
        Set scalebar
        '''
        for field in list(kwargs.keys()):
            if field in list(vars(self.scalebar).keys()):
                vars(self.scalebar)[field]  = kwargs[field]
            else:
                print('The point does not have the field: ' + field)
        if isplot:
            self.plot()
    
    #  ------------------------------ 
    def set_point(self, ptIndex, isplot = True, **kwargs):
        '''
        Revise individual points on the map ------------------------------ to reset the self.plot() to the map structure
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
    
    

    # ----------------------- plot maps: (1) format_colorbar (2) Create_image data (3) Plot image
    def format_colorbar(self, ax, location = 'right'):
        """
        add an ax besides the image map, i.e. resize the colorbar to fit the image
        """
        divider = make_axes_locatable(ax)
        return divider.append_axes(location, size="5%", pad=0.05)
    
    def plot_image(self, ax, imgMode):
        '''
        imgMode is one of the modes defined in self.img_modes
        '''
        imgData = self.imgData[imgMode]
        img = ax.imshow(imgData['image'], cmap =imgData['cmap'], extent=imgData['FOV'], 
                        vmin=imgData['Vmin'], vmax=imgData['Vmax'])
                
        # Add label
        if self.isSubFigLabel:
            fig_label_text = chr(ord('a')+ self.fig_label_num)
            ax.text(self.fig_label_x_offset, self.fig_label_y_offset, 
                    fig_label_text, transform=ax.transAxes, 
                    size=self.fig_label_size, weight=self.fig_label_weight)
            self.fig_label_num = self.fig_label_num + 1
        
        # Add title
        if self.isSubFigTitle:
            ax.set_title(imgData['title'], fontsize = self.title_fontsize)
        
        # Add colorbar
        if imgData['cbar'] is not None:
            plt.colorbar(img, location =  imgData['cbar'], ax=ax, 
                         cax = self.format_colorbar(ax, location = imgData['cbar']))

        # Add scale bar if choosed
        if imgData['scalebar'] is None:
            
            ax.set_xlabel(imgData['xlabel'], fontsize = self.xylabel_fontsize)
            ax.set_ylabel(imgData['ylabel'], fontsize = self.xylabel_fontsize)
        elif imgData['scalebar']['length'] <= 0:
            ax.set_xlabel(imgData['xlabel'], fontsize = self.xylabel_fontsize)
            ax.set_ylabel(imgData['ylabel'], fontsize = self.xylabel_fontsize)
        else:
            ax.tick_params(axis='both',          # changes apply to the x-axis
                           which='both',      # both major and minor ticks are affected
                           left = False,
                           bottom=False,      # ticks along the bottom edge are off
                           top=False,         # ticks along the top edge are off
                           labelbottom=False,
                           labelleft = False) # labels along the bottom edge are off
            length = imgData['scalebar']['length']
            fontprops = fm.FontProperties(size=self.scalebar_fontsize)
            label =  str(length) + ' ' + imgData['scalebar']['unit'] if len(imgData['scalebar']['unit'])>0 else ''
            scalebar = AnchoredSizeBar(ax.transData,
                           length,label, imgData['scalebar']['location'], 
                           pad = 0.1,
                           color = imgData['scalebar']['color'],
                           frameon = False,
                           size_vertical = imgData['scalebar']['height'],
                           fontproperties = fontprops)
            ax.add_artist(scalebar)

        # add point marks to the maps: x-sp['x'], y-sp['y'], label-sp['label']
        if imgData['ptMarks'] is not None: 
            imgSize = min(imgData['Scan_Width'], imgData['Scan_Height'])
            for idx, sp in enumerate(imgData['ptMarks']):
                if len(sp['label']) > 0:
                    if sp['mode'] == 'circle':
                        mark = Circle([sp['x'], sp['y']], imgSize*sp['scale'], fill=False, 
                                      linestyle='--', edgecolor=sp['color'])
                        txt_shift = 2*imgSize*sp['scale']
                    elif sp['mode'] == 'arrow':
                        mark = FancyArrow(sp['x'], sp['y'], dx=imgSize*sp['scale'], dy=imgSize*sp['scale'],
                                width=.02, length_includes_head=True, color=sp['color'])
                        txt_shift = 0
                    ax.add_patch(mark)
                    txt = ax.text(sp['x'], sp['y']-txt_shift, sp['label'], color = sp['color'], 
                                  ha='center', va='top', weight='normal',fontsize=16)
                    txt.set_path_effects([PathEffects.withStroke(linewidth=1, foreground='k')])
        if imgData['lnMarks'] is not None:
            for line in imgData['lnMarks']:
                ax.plot(line['x'], line['y'], marker = 'o', linestyle='dotted', color="white")
    
    #----------------------------
    def plot_xydata(self, ax): 
        colors = sns.color_palette(self.palette, len(self.lineData['line_label'])+1)
        
        # Add label (a, b, c, d, etc.)
        if self.isSubFigLabel is not None:
            fig_label_text = chr(ord('a')+ self.fig_label_num)
            ax.text(self.fig_label_x_offset, self.fig_label_y_offset, 
                    fig_label_text, transform=ax.transAxes, 
                    size=self.fig_label_size, weight=self.fig_label_weight)
            self.fig_label_num = self.fig_label_num + 1
        
        if self.lineData['label'] == 'histogram':
            ax.bar(self.lineData['x'],self.lineData['y'][0,:], width=1, color = colors[-1])
        
        if self.lineData['label'] == 'Integrated':
            y = self.lineData['y'][0, self.lineData['spcIndice'][0]:self.lineData['spcIndice'][1]]
            text_shift = self.peak_label_yshift*(np.max(y) - np.min(y)) # text shift relative to the peak y
            
            ax.plot(self.lineData['x'][self.lineData['spcIndice'][0]:self.lineData['spcIndice'][1]],y, 
                    color = colors[-1])
            # Add peaks 
            if self.lineData['peaks'] is not None:
                for pk in self.lineData['peaks']:
                    ax.scatter(pk[0], pk[1], s=15, facecolors='none', edgecolors='black', alpha=0.8)
                    ax.text(pk[0], pk[1] + text_shift, "{:.0f}".format(pk[0]) + ' ' + self.lineData['x_unit'], 
                            ha= self.peak_label_pos['ha'], va=self.peak_label_pos['va'], color = colors[-1],
                            weight='normal', fontsize=self.peak_label_fontsize, alpha = self.peak_label_alpha)
                ymin, ymax = ax.get_ylim()
                ax.set_ylim([ymin, ymax + text_shift + (ymax-ymin)/16])
        
        if self.lineData['label'] == 'linescan' and len(self.lineData['x'])>0:
            ydata = self.lineData['y']
            ax.scatter(self.lineData['x'], ydata[0, :], s=60, facecolors=colors[0],  color = colors[-1])
            ax.plot(self.lineData['x'], ydata[0, :], '--', color = colors[-1], alpha = 0.3, linewidth=2)
            ax.tick_params(axis='y', labelcolor=colors[-1])
            ax.yaxis.label.set_color(colors[-1])
            ax_right=ax.twinx()
            colors = sns.color_palette("Blues", len(self.lineData['line_label'])+1)
            ax_right.scatter(self.lineData['x'], ydata[1, :], s=60, facecolors=colors[0], color = colors[-1])
            ax_right.plot(self.lineData['x'], ydata[1, :], '--', color = colors[-1], alpha = 0.3, linewidth=2)
            ax_right.tick_params(axis='y', labelcolor=colors[-1])
            ax_right.yaxis.label.set_color(colors[-1])
        
        if self.lineData['label'] == 'Points' and len(self.lineData['y'][1:])>0:
            shift = 0
            text_shift = self.peak_label_yshift*(np.max(self.lineData['y'][1, :]) - np.min(self.lineData['y'][1, :])) 
            
            # line_label: the labels marking individual lines 
            for idx, y in enumerate(self.lineData['y'][1:]):#y[0] is the integrated, idx starts from 0
                sp = self.lineData['line_label'][idx+1]
                ax.plot(self.lineData['x'], y-shift, color = colors[idx], label = sp['label'])
                
                # Add marks/labels to indicate the peak
                ax.scatter(sp['pos'], sp['pk_I'] - shift, s=15, facecolors='none', edgecolors='black', alpha=0.8)
                if not np.isnan(sp['I']):
                    ax.text(sp['pos'], sp['pk_I'] - shift + text_shift, "{:.0f}".format(sp['pos']) + ' ' + self.lineData['x_unit'], ha= self.peak_label_pos['ha'], 
                            va=self.peak_label_pos['va'],weight='normal', color = colors[idx], 
                            fontsize=self.peak_label_fontsize, alpha = self.peak_label_alpha)
                # add 2nd peak if the plot is A-B
                if self.lineData['datatype']== 'spc_Diff':
                    ax.scatter(sp['pos']-sp['pos_diff'], sp['pk_I']/sp['rpk_I'] - shift, s=15, facecolors='none', edgecolors='black', alpha=0.8)
                    if not np.isnan(sp['I']):
                        ax.text(sp['pos']-sp['pos_diff'], sp['pk_I']/sp['rpk_I'] - shift + text_shift, "{:.0f}".format(sp['pos']-sp['pos_diff']) + ' ' + self.lineData['x_unit'], 
                                ha= self.peak_label_pos['ha'], va=self.peak_label_pos['va'],weight='normal', color = colors[idx], 
                                fontsize=self.peak_label_fontsize, alpha = self.peak_label_alpha)
                    ext = (self.lineData['spcRange'][1]- self.lineData['spcRange'][0])/8
                    ax.set_xlim([self.lineData['spcRange'][0]-ext, self.lineData['spcRange'][1]+ext])

                # Label the curve - point from the map
                line_label_y = np.average(y-shift) #self.lineData['I_th'] - shift if np.isnan(sp['I']) else sp['I'] - shift
                lx = self.lineData['spcIndice'][0] if self.lineData['datatype']== 'spc_Diff' else 0
                ax.text(self.lineData['x'][lx], line_label_y, sp['label'], ha= self.line_label_pos['ha'], 
                        va=self.line_label_pos['va'],weight='normal', fontsize=self.line_label_fontsize)
                # Add vertical shift
                shift = shift + (np.max(y) - np.min(y))
            if len(self.lineData['line_label'])>0:
                ymin, ymax = ax.get_ylim()
                ax.set_ylim([ymin, ymax + text_shift])
        
        if self.lineData['label'] == 'merged':
            shift = 0
            for idx, y in enumerate(self.lineData['y']): 
                y = y[self.lineData['spcIndice'][0]:self.lineData['spcIndice'][1]]
                ax.plot(self.lineData['x'][self.lineData['spcIndice'][0]:self.lineData['spcIndice'][1]], y-shift, color = colors[idx])
                
                 # Label the curve - point from the map
                sp = self.lineData['line_label'][idx]
                line_label_y = np.average(y-shift) #self.lineData['I_th'] - shift if np.isnan(sp['I']) else sp['I'] - shift
                ax.text(self.lineData['x'][self.lineData['spcIndice'][0]], line_label_y, sp['label'], ha= self.line_label_pos['ha'], 
                        va=self.line_label_pos['va'],weight='normal', fontsize=self.line_label_fontsize)
                # Add vertical shift
                shift = shift + (np.max(y) - np.min(y))
        
        # Set titles, axis labels
        if self.isSubFigTitle:
            ax.set_title(self.lineData['title'], fontsize = self.title_fontsize)
        ax.set_xlabel(self.lineData['xlabel'], fontsize =  self.xylabel_fontsize)
        ax.set_ylabel(self.lineData['ylabel'], fontsize = self.xylabel_fontsize)
        if self.lineData['label'] == 'linescan' and len(self.lineData['x'])>0:
            ax_right.set_ylabel(self.lineData['y_twin_label'], fontsize = self.xylabel_fontsize)
            
         # Mark spcRange
        if self.isRangeMarked:
            xmin, xmax = ax.get_xlim()
            if xmin <= self.lineData['full_spc_x'][0] and xmax >= self.lineData['full_spc_x'][1]:
                # Mark Calibration 
                if self.lineData['isPos_corrected']:
                    ax.axvline(x = self.lineData['pk_ref'], color = 'black', linestyle = '--')
                if self.lineData['isI_corrected']:
                    ax.axvspan(self.lineData['I_ref_range'][0]- self.lineData['I_ref_range'][1], 
                               self.lineData['I_ref_range'][0]+ self.lineData['I_ref_range'][1], alpha=self.ref_alpha, color='gray')
            if self.lineData['label'] == 'Points' and len(self.lineData['y'][1:])>0:
                ax.axvspan(self.lineData['spcRange'][0], self.lineData['spcRange'][1], alpha=self.ref_alpha, color='lavender')
     
    
    
    