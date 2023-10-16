# Academic Podcast Script Generator

## Usage
1. Create conda environment from YAML:
`conda env create --file environment.yml
`
## Development
### Export conda environment
`conda env export --name academicPodcaster --from-history | grep -v "^prefix: " > environment.yml`


## Building Package
`python setup.py bdist_wheel`

### Upload it to PyPI:
1. Must have an account with 2FA
2. Must have API key in ~/.pypirc
3. Run: `twine upload dist/*`