NAME = "Name"
KVP = "kVp"

### Constants file
SHOW_LEGEND = 'Show legend'

CRITICAL_POINT_DOSE_CORRECTED = 'Dose corrected for occupancy [mSv]'
CRITICAL_POINT_DOSE = 'Dose [mSv]'

RULERS = 'Rulers'
                             
WALLS_AND_SHIELDING = "Walls && Shieldings"
SOURCES_NM_CT_XRAY = "Sources NM, CT, XRAY"
PROJECT = 'Project'


PYSHIELD = 'PyShield'
RADTRACER = 'Radtracer'


LOAD_SAVE = "Load/Save"
PREFERENCES = "Preferences"
CRITICAL_POINT_REPORT_VIEW = "Critical Point Report"
CANVAS = "Canvas"

ENABLED = 'Enabled'


# Materials
BASE_MATERIALS = 'Base Materials'
BUILDUP_MATERIALS = 'Buildup Materials'
MATERIALS = "Materials"
MATERIAL = 'Material'
DENSITY = "Density"
THICKNESS = "Thickness [cm]"
BUILDUP_TABLE = 'Buildup Table'
ATTENUATION_TABLE = 'Attenuation Table'
RADTRACER_MATERIAL = 'Radtracer Material'
EMPTY_MATERIAL = 'None'
EMPTY_SHIELDING = 'None'
EMPTY_TABLE = 'None'

# Isotopes
ISOTOPES = "Isotopes"
HALF_LIFE = "Half life [h]"
SELF_SHIELDING_OPTIONS = "Self shielding options"
SELF_SHIELDING_NONE = 'None'
SELF_SHIELDING_BODY = 'Body'
SELF_SHIELDING_FACTOR = 'Factor'
DECAY_CHAINS = "Decay chains"
ISOTOPE_SPECTRA = "Isotope spectra"
SPECTRUM = "Spectrum"
SUPPORTED_ISOTOPES = 'Supported isotopes'


# Archer parameters
CT_BODY_PART_OPTIONS = "CT Body part options"
CT_PARAMETERS = "CT parameters"
XRAY_PARAMETERS = "Xray parameters"
ARCHER = "Archer"
CT_SCATTER_FRACTION_BODY = "Scatter fraction body"
CT_SCATTER_FRACTION_HEAD = "Scatter fraction head"
XRAY_SCATTER_FRACTION = "Scatter fraction"
# 


### Model file
ENGINE = "Engine"
RADTRACER = "Radtracer"
PYSHIELD = "pyShield"

# Floor plan
FLOORPLAN = "Floor plan"
IMAGE = 'image'
FILENAME = "Filename"
PIXEL_SIZE_CM = "Pixel size [cm]"
ORIGIN_CM = "Origin [cm]"
ORIGIN = 'Origin'
TOP_LEFT = "top_left"
BOTTOM_LEFT = "bottom_left"
PIXEL_SIZE_METHOD = 'Pixel size method'
FIXED = 'fixed' # pixel size set by hand
MEASURED = 'measured' # measured form floor plan
REAL_WORLD_DISTANCE_CM = 'Real world distance [cm]' # distance set in gui
VERTICES_PIXELS = 'vertices [pixels]'

# Plot style
DOSEMAP_STYLE = "Dose map style"
CMAP_NAME = "Colormap name"
CMAP_MIN = "Colormap min"
CMAP_MAX = "Colormap max"
CMAP_ALPHA = "Transparency"
CMAP_ALPHA_GRADIENT = "Transparency gradient"
CONTOUR_LINES = "Contour lines"

# Dose map
RESULT = 'Result'
DOSEMAP = "Dose map"
GEOMETRY = "Geometry"
GRID_MATRIX_SIZE = "Grid matrix size"
EXTENT = "Extent [cm]"
INTERPOLATE = 'Interpolate'
MULTI_CPU = 'Multi CPU'

# Model
CRITICAL_POINTS = "Critical points"
SHIELDINGS = "Shieldings"
WALLS = "Walls"
SOURCES_CT = 'Sources CT'
SOURCES_NM = 'Sources NM'
SOURCES_XRAY = 'Sources Xray'


### General
POSITION = "Position"

SELECTED_ENGINE = 'Selected Engine'
    
### Shielding
COLOR = "Color"
LINEWIDTH = "Linewidth [pt]"
MATERIAL_NAME = "Material name"
MATERIAL_THICKNESS = "Thickness [cm]"

### Wall
SHIELDING = "Shielding"
VERTICES = "Vertices"
CLOSED = "Closed"

### Critical point
OCCUPANCY_FACTOR = "Occupancy factor"

### Sources    
NUMBER_OF_EXAMS = "Number of exams"

# Nuclear
ISOTOPE = "Isotope"
ACTIVITY = "Activity [MBq]"
DURATION = "Duration [h]"
SELF_SHIELDING = "Self shielding"    

# Legacy
APPLY_DECAY_CORRECTION = "Apply decay correction"
BIOLOGICAL_HALFLIFE = "Biological half-life [h]"
APPLY_BIOLOGICAL_DECAY = "Apply biological decay"
SELF_SHIELDING_PYSHIELD = 'Self shielding pyshield'

# display nuclear
PARENT = 'Parent'
ENERGY_KEV = 'Energy [keV]'
ABUNDANCE = 'Abundance [%]'


# New decay model
CLEARANCE = 'Clearance'
EMPTY_CLEARANCE = 'No Clearance'
APPLY_FRACTION1 = 'Apply Fraction 1'
APPLY_FRACTION2 = 'Apply Fraction 2'
DECAY_FRACTION1 = 'Fraction 1'
DECAY_FRACTION2 = 'Fraction 2'
HALFLIFE1 = 'Half Life 1 [h]'
HALFLIFE2 = 'Half Life 2 [h]'
SPLIT_FRACTION_TIME = 'Split Time [h]'
ENABLE_SPLIT_FRACTIONS = 'Split fractions by time'

# XRAY / CT
DAP = "DAP [Gycm2]"
DLP = "DLP [mGycm]"
CT_BODY_PART = "Body part"


NEW_PROJECT = 'New Project'

# Matplotlib
WALL_MARKER = 'WallMarker'
PIXEL_SIZE_MARKER = 'PixelSizeMarker'

MODEL_ITEMS = [SOURCES_CT, SOURCES_NM, SOURCES_XRAY, WALLS, SHIELDINGS,
               CRITICAL_POINTS]

SOURCES = [SOURCES_CT, SOURCES_NM, SOURCES_XRAY]

# GUI Toolbar
LABEL = 'Label'
ICON = 'Icon'
TOOILTIP = 'Tooltip'
CHECKABLE = 'Checkable'
