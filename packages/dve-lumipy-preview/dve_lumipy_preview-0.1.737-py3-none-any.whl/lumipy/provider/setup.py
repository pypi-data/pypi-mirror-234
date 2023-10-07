import os
from pathlib import Path
from zipfile import ZipFile
from shutil import rmtree, which

import lusid_drive
from lusid_drive import ApiException
from lumipy import get_client
from time import sleep

from lumipy.provider.common import binary_path, target_sdk_version


# noinspection SqlResolve,SqlNoDataSourceInspection
def download_files(lm_client, files, path, pattern):
    sql = f"SELECT [Id], [Name] FROM [Drive.File] WHERE [RootPath] = '{path}' and [Name] like '{pattern}'"

    wait = 30
    df = lm_client.run(sql, quiet=True)
    locations = []
    for _, r in df.iterrows():
        _print(f'Downloading {path}/{r["Name"]}.', 4)

        count = 0
        while True:
            try:
                locations.append(Path(files.download_file(r['Id'])))
                break
            except ApiException as ae:
                if count > 3:
                    raise ae
                count += 1
                _print(f'Couldn\'t get file (reason: {ae.reason}). Waiting {wait}s before retry.')
                sleep(wait)

    return locations


def _print(s, n=0):
    indent = ' ' * n
    print(indent + s)


def setup(**kwargs):
    """Run the lumipy python providers setup given your user credentials for a domain.

    Keyword Args:
        token (str): Bearer token used to authenticate.
        api_secrets_filename (str): Name of secrets file (including full path)
        api_url (str): luminesce API url
        app_name (str): Application name (optional)
        certificate_filename (str): Name of the certificate file (.pem, .cer or .crt)
        proxy_url (str): The url of the proxy to use including the port e.g. http://myproxy.com:8888
        proxy_username (str): The username for the proxy to use
        proxy_password (str): The password for the proxy to use
        correlation_id (str): Correlation id for all calls made from the returned finbournesdkclient API instances

    """

    if which('dotnet') is None:
        print('Dotnet runtime not found: please install dotnet 6.')
        return

    sdk_version = kwargs.pop('sdk_version', target_sdk_version)
    bin_path = binary_path(sdk_version)

    if bin_path.exists():
        rmtree(bin_path)
    else:
        bin_path.mkdir(parents=True)

    _print('Setting up python providers. 🛠')
    lm_client = get_client(**kwargs)

    lumi_url = lm_client._factory.api_client.configuration._base_path
    cfg = lusid_drive.Configuration(host=lumi_url.split('.com')[0] + '.com/drive')
    cfg.access_token = lm_client.get_token()
    api_client = lusid_drive.ApiClient(cfg)
    files = lusid_drive.FilesApi(api_client)

    drive_path = '/LUSID-support-document-share/Luminesce/'
    zip_name = f'finbourne.luminesce.pythonproviders.{sdk_version}.zip'

    _print('Getting the provider factory dlls zip.', 2)
    zip_path = download_files(lm_client, files, drive_path + 'Providers', zip_name)
    if len(zip_path) != 1:
        raise ValueError(f"Couldn't get {drive_path}/{zip_name}. Please contact support as the binaries may not have been added to your domain.")

    _print('Unzipping the provider factory dlls.', 2)
    with ZipFile(zip_path[0], 'r') as zf:
        zf.extractall(bin_path)

    _print('Cleaning up zip file.', 2)
    os.remove(zip_path[0])

    _print('Getting pem files.', 2)
    pem_paths = download_files(lm_client, files, drive_path + 'Certificates', '%.pem')
    if len(pem_paths) != 2:
        raise ValueError(f"Couldn't get {drive_path}/Certificates/*.pem. Please contact support as the certs may not have been added to your domain.")

    dll_path = bin_path / 'tools' / 'net6.0' / 'any'
    for pem_path in pem_paths:
        pem_name = pem_path.parts[-1].strip(';')
        _print(f'Copying {pem_name}.', 2)
        target = dll_path / pem_name
        with open(pem_path, 'rb') as pfr:
            with open(target, 'wb') as pfw:
                pfw.write(pfr.read())

    _print('Checking pem files.', 2)
    pems = list(dll_path.glob('*.pem'))
    if len(pems) != 2:
        raise ValueError(f"Couldn't find pem files at {dll_path}.")

    _print("\nAll set! You can now build and run python Luminesce providers.")

    _print(f"\nTry running the following command in a terminal:")
    cmd = 'python -m lumipy.provider run --set=demo '
    _print(cmd + '\n', 2)
    _print('This will open a browser window for you to log in. '
           'Once startup has finished only you will be able to query it.\n')
    _print('To run these demo providers so others in your domain can use them:')
    cmd = 'python -m lumipy.provider run --set=demo --user=global --whitelist-me'
    _print(cmd + '\n', 2)
    _print('In this case it will not open a browser window.')
