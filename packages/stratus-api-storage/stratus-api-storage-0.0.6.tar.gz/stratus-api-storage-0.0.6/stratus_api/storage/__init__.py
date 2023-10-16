from os.path import isdir

STORAGE_UPLOAD_FOLDER = '/apps/files' if isdir('/apps') else 'tests/mocks'
