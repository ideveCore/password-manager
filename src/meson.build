# ===== Generate Currency Convert bin ===== 
configure_file(
  input: 'password-manager.in',
  output: 'password-manager',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir'),
  install_mode: 'r-xr--r--'
)

## ===== Generate define module
configure_file(
  input: 'define.in',
  output: 'define.py',
  configuration: conf,
  install: true,
  install_dir: moduledir
)

# ===== Blueprint compiler =====
blueprints = custom_target('blueprints',
  input: files(
    'components/shortcuts/shortcuts.blp',
    'window.blp',
  ),
  output: '.',
  command: [find_program('blueprint-compiler'), 'batch-compile', '@OUTPUT@', '@CURRENT_SOURCE_DIR@', '@INPUT@'],
)

gnome.compile_resources('password-manager',
  'password-manager.gresource.xml',
  dependencies: blueprints,
  gresource_bundle: true,
  install: true,
  install_dir: pkgdatadir,
)

password_manager_sources = [
  '__init__.py',
  'components/shortcuts/shortcuts.py',
  'main.py',
  'window.py',
]

install_subdir('components', install_dir: moduledir)
install_data(password_manager_sources, install_dir: moduledir)

