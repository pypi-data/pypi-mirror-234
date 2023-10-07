from enum import Enum


class StudyType(Enum):
	BBROWSER=0
	H5_10X=1
	H5AD=2
	MTX_10X=3
	BCS=4
	RDS=5
	TSV=6
	DSP=7
	VISIUM=8
	VIZGEN=9
	COSMX=10
	XENIUM=11
	VISIUM_RDS=12
	VISIUM_ANN=13
	VIZGEN_V2=14
	TILE_DB=15
	PROTEOMICS_QPTIFF=16
	PROTEOMICS_OME_TIF=17
	PROTEOMICS_TIFF=18


class TechnologyType(Enum):
	SINGLE_CELL='SC'
	LENS_SC='LENS_SC'
	VISIUM='VISIUM'
	DSP='DSP'
	PROTEOMICS='PROTEOMICS'


class Species(Enum):
  HUMAN='human'
  MOUSE='mouse'
  NON_HUMAN_PRIMATE='primate'
  OTHERS='others'


class InputMatrixType(Enum):
  RAW='raw'
  NORMALIZED='normalized'


class StudyUnit(Enum):
	UNIT_RAW='raw'
	UNIT_LOGNORM='lognorm'


INPUT_LENS_SC = {
	StudyType.COSMX.value: {
		'folders': {
			'cell_boundaries': 'celllabels',
			'images': 'rawmorphologyimages'
		},
		'files': {
			'transcripts': 'tx_file.csv',
			'fov_positions': 'fov_positions_file.csv'
		}
	},
	StudyType.VIZGEN.value: {
		'folders': {
			'cell_boundaries': 'cell_boundaries',
			'images': 'images'
		},
		'files': {
			'transcripts': 'detected_transcripts.csv'
		}
	},
	StudyType.XENIUM.value: {
		'folders': {},
		'files': {
			'micron2pixel': 'experiment.xenium',
			'cell_boundaries': 'cell_boundaries.csv.gz',
			'transcripts': 'transcripts.csv.gz',
			'image': 'morphology_mip.ome.tif'
		}
	},
	StudyType.VIZGEN_V2.value: {
		'folders': {
			'images': 'images'
		},
		'files': {
			'transcripts': 'detected_transcripts.csv',
			'cell_boundaries': 'cell_boundaries.parquet'
		}
	},
	StudyType.PROTEOMICS_OME_TIF.value: {
		'folders': {},
		'files': {
			'image': 'image.ome.tif'
		}
	},
	StudyType.PROTEOMICS_QPTIFF.value: {
		'folders': {},
		'files': {
			'image': 'image.qptiff'
		}
	}
}


class ChunkSize(Enum):
  CHUNK_5_MB = 5 * 1024 * 1024
  CHUNK_100_MB = 100 * 1024 * 1024
  CHUNK_500_MB = 500 * 1024 * 1024
  CHUNK_1_GB = 1 * 1024 * 1024 * 1024