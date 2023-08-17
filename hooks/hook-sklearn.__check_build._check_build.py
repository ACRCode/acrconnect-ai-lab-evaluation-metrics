from PyInstaller.utils.hooks import collect_submodules
from PyInstaller.utils.hooks import collect_data_files

print('hidden stuff wowowowowowowowowo')
hiddenimports = collect_submodules('sklearn')
datas = collect_data_files('sklearn')